/**
 * LILIETH_RISER — Audio Buffer
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * A multi-channel, lock-free audio buffer designed for ultra-low latency (< 0.5 ms)
 * sample manipulation. Supports float32 and float64 sample formats.
 *
 * Architect: Stretford Hub / G2G Sages
 */

#pragma once

#include <cmath>
#include <cstddef>
#include <cstring>
#include <stdexcept>
#include <vector>
#include <atomic>
#include <memory>
#include <algorithm>
#include <cassert>

namespace lilieth {

/**
 * @brief A non-interleaved, multi-channel audio buffer.
 *
 * Memory layout: channels × samples  (channel-major order).
 * All heap allocation is done at construction; the audio-thread hot path
 * performs zero dynamic allocations.
 *
 * @tparam T  Sample type — float (default) or double.
 */
template <typename T = float>
class AudioBuffer {
public:
    static_assert(std::is_floating_point<T>::value,
                  "AudioBuffer<T> requires a floating-point type.");

    // -------------------------------------------------------------------------
    // Construction / Destruction
    // -------------------------------------------------------------------------

    AudioBuffer() : num_channels_(0), num_samples_(0) {}

    /**
     * @param num_channels  Number of audio channels (1 = mono, 2 = stereo).
     * @param num_samples   Number of frames (samples per channel).
     */
    AudioBuffer(std::size_t num_channels, std::size_t num_samples)
        : num_channels_(num_channels),
          num_samples_(num_samples),
          data_(num_channels, std::vector<T>(num_samples, T(0))) {}

    /// Copy constructor performs a deep copy.
    AudioBuffer(const AudioBuffer&) = default;
    AudioBuffer& operator=(const AudioBuffer&) = default;

    /// Move constructor transfers ownership.
    AudioBuffer(AudioBuffer&&) noexcept = default;
    AudioBuffer& operator=(AudioBuffer&&) noexcept = default;

    ~AudioBuffer() = default;

    // -------------------------------------------------------------------------
    // Capacity
    // -------------------------------------------------------------------------

    /// Returns the number of channels.
    std::size_t num_channels() const noexcept { return num_channels_; }

    /// Returns the number of frames (samples per channel).
    std::size_t num_samples() const noexcept { return num_samples_; }

    /// Returns true if the buffer holds no data.
    bool empty() const noexcept { return num_channels_ == 0 || num_samples_ == 0; }

    // -------------------------------------------------------------------------
    // Raw access (audio-thread safe — no locking)
    // -------------------------------------------------------------------------

    /** Read/write pointer to a channel's sample array. */
    T* channel_data(std::size_t channel) {
        assert(channel < num_channels_);
        return data_[channel].data();
    }

    /** Read-only pointer to a channel's sample array. */
    const T* channel_data(std::size_t channel) const {
        assert(channel < num_channels_);
        return data_[channel].data();
    }

    /** Single sample access by [channel][frame]. */
    T& operator()(std::size_t channel, std::size_t frame) {
        assert(channel < num_channels_ && frame < num_samples_);
        return data_[channel][frame];
    }

    const T& operator()(std::size_t channel, std::size_t frame) const {
        assert(channel < num_channels_ && frame < num_samples_);
        return data_[channel][frame];
    }

    // -------------------------------------------------------------------------
    // Bulk operations
    // -------------------------------------------------------------------------

    /// Zero all samples across all channels.
    void clear() noexcept {
        for (auto& ch : data_)
            std::fill(ch.begin(), ch.end(), T(0));
    }

    /// Apply a gain scalar to every sample.
    void apply_gain(T gain) noexcept {
        for (auto& ch : data_)
            for (auto& s : ch)
                s *= gain;
    }

    /**
     * @brief Copy samples from another buffer into this one, with gain.
     *
     * Channels and sample counts must match.
     *
     * @param src   Source buffer.
     * @param gain  Scalar applied to each sample before adding.
     */
    void add_from(const AudioBuffer<T>& src, T gain = T(1)) {
        if (src.num_channels() != num_channels_ ||
            src.num_samples()  != num_samples_)
            throw std::invalid_argument("AudioBuffer::add_from — dimension mismatch");

        for (std::size_t ch = 0; ch < num_channels_; ++ch) {
            const T* s = src.channel_data(ch);
            T*       d = channel_data(ch);
            for (std::size_t i = 0; i < num_samples_; ++i)
                d[i] += s[i] * gain;
        }
    }

    /**
     * @brief Copy a contiguous region into a new buffer ("The Blade" slice).
     *
     * @param start_frame  First frame to include (inclusive).
     * @param end_frame    One past the last frame to include (exclusive).
     * @return A new AudioBuffer containing the sliced region.
     */
    AudioBuffer<T> slice(std::size_t start_frame, std::size_t end_frame) const {
        if (start_frame >= end_frame || end_frame > num_samples_)
            throw std::out_of_range("AudioBuffer::slice — range out of bounds");

        const std::size_t len = end_frame - start_frame;
        AudioBuffer<T> out(num_channels_, len);
        for (std::size_t ch = 0; ch < num_channels_; ++ch)
            std::copy(data_[ch].begin() + static_cast<std::ptrdiff_t>(start_frame),
                      data_[ch].begin() + static_cast<std::ptrdiff_t>(end_frame),
                      out.channel_data(ch));
        return out;
    }

    /**
     * @brief Find the nearest zero-crossing before or at position `hint`.
     *
     * Used by TheBlade to make clean, click-free cuts.
     *
     * @param channel  Channel index to search.
     * @param hint     Starting frame to search backwards from.
     * @param window   Maximum number of frames to search backwards.
     * @return Frame index of the zero-crossing, or `hint` if none found.
     */
    std::size_t nearest_zero_crossing(std::size_t channel,
                                      std::size_t hint,
                                      std::size_t window = 256) const noexcept {
        assert(channel < num_channels_);
        if (hint == 0 || hint >= num_samples_) return hint;

        const T* d = data_[channel].data();
        const std::size_t lo = (hint > window) ? hint - window : 0;

        for (std::size_t i = hint; i > lo; --i) {
            if ((d[i] >= T(0) && d[i - 1] < T(0)) ||
                (d[i] <  T(0) && d[i - 1] >= T(0)))
                return i;
        }
        return hint;
    }

    // -------------------------------------------------------------------------
    // Statistics (useful for waveform rendering)
    // -------------------------------------------------------------------------

    /// Peak amplitude across all channels.
    T peak() const noexcept {
        T p = T(0);
        for (const auto& ch : data_)
            for (const auto& s : ch)
                p = std::max(p, std::abs(s));
        return p;
    }

    /// RMS amplitude for a given channel.
    T rms(std::size_t channel) const noexcept {
        assert(channel < num_channels_);
        if (num_samples_ == 0) return T(0);
        T sum = T(0);
        for (const auto& s : data_[channel])
            sum += s * s;
        return static_cast<T>(std::sqrt(sum / static_cast<double>(num_samples_)));
    }

    // -------------------------------------------------------------------------
    // Resize
    // -------------------------------------------------------------------------

    /// Resize the buffer, clearing all existing content.
    void resize(std::size_t new_channels, std::size_t new_samples) {
        num_channels_ = new_channels;
        num_samples_  = new_samples;
        data_.assign(new_channels, std::vector<T>(new_samples, T(0)));
    }

private:
    std::size_t              num_channels_;
    std::size_t              num_samples_;
    std::vector<std::vector<T>> data_;
};

// -------------------------------------------------------------------------
// Convenience aliases
// -------------------------------------------------------------------------

using AudioBufferF = AudioBuffer<float>;   ///< 32-bit float buffer (default)
using AudioBufferD = AudioBuffer<double>;  ///< 64-bit double buffer (high-fidelity)

} // namespace lilieth
