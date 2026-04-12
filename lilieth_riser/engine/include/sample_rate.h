/**
 * LILIETH_RISER — Sample Rate Manager
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * Defines standard sample rates, provides conversion helpers, and maintains
 * the engine's active sample rate configuration.
 */

#pragma once

#include <cstdint>
#include <stdexcept>
#include <vector>
#include <cmath>

namespace lilieth {

// ---------------------------------------------------------------------------
// Standard sample rates
// ---------------------------------------------------------------------------

enum class SampleRateHz : uint32_t {
    SR_8000   =   8000,
    SR_22050  =  22050,
    SR_44100  =  44100,   ///< CD quality
    SR_48000  =  48000,   ///< Studio / broadcast standard
    SR_88200  =  88200,
    SR_96000  =  96000,   ///< High-resolution audio
    SR_192000 = 192000,   ///< Ultra-high-resolution
};

// ---------------------------------------------------------------------------
// SampleRate
// ---------------------------------------------------------------------------

/**
 * @brief Immutable value-object representing the current engine sample rate.
 *
 * Convert between sample counts and time (milliseconds / seconds) with no
 * heap allocation.
 */
class SampleRate {
public:
    /// Construct with an explicit Hz value (use SampleRateHz enum for safety).
    explicit SampleRate(uint32_t hz = 48000) : hz_(hz) {
        if (hz == 0)
            throw std::invalid_argument("SampleRate: Hz must be > 0");
    }

    explicit SampleRate(SampleRateHz preset)
        : SampleRate(static_cast<uint32_t>(preset)) {}

    // ------------------------------------------------------------------
    // Accessors
    // ------------------------------------------------------------------

    /// Returns the sample rate in Hz.
    uint32_t hz() const noexcept { return hz_; }

    /// Returns the sample rate as a double for arithmetic.
    double hz_d() const noexcept { return static_cast<double>(hz_); }

    // ------------------------------------------------------------------
    // Time ↔ sample conversions
    // ------------------------------------------------------------------

    /// Convert time in seconds to the nearest integer sample count.
    uint64_t seconds_to_samples(double seconds) const noexcept {
        return static_cast<uint64_t>(seconds * hz_d() + 0.5);
    }

    /// Convert time in milliseconds to sample count.
    uint64_t ms_to_samples(double ms) const noexcept {
        return seconds_to_samples(ms / 1000.0);
    }

    /// Convert a sample count to seconds.
    double samples_to_seconds(uint64_t samples) const noexcept {
        return static_cast<double>(samples) / hz_d();
    }

    /// Convert a sample count to milliseconds.
    double samples_to_ms(uint64_t samples) const noexcept {
        return samples_to_seconds(samples) * 1000.0;
    }

    /**
     * @brief Number of samples in one "block" at the given latency target.
     *
     * Example: block_size_for_latency_ms(0.5) at 48 kHz → 24 samples.
     *
     * @param target_ms  Target round-trip latency in milliseconds.
     * @return           Buffer block size (number of frames) — always ≥ 1.
     */
    uint32_t block_size_for_latency_ms(double target_ms) const noexcept {
        const auto n = static_cast<uint32_t>(target_ms * hz_d() / 1000.0 + 0.5);
        return n > 0 ? n : 1u;
    }

    // ------------------------------------------------------------------
    // Sample-rate conversion ratio
    // ------------------------------------------------------------------

    /**
     * @brief Ratio to resample audio from `source` to this rate.
     *
     * Multiply each output sample index by this ratio to get the
     * corresponding fractional input index.
     *
     * @param source  The rate of the incoming audio.
     * @return        Conversion ratio  (>1 upsamples, <1 downsamples).
     */
    double conversion_ratio(const SampleRate& source) const noexcept {
        return hz_d() / source.hz_d();
    }

    /**
     * @brief Simple linear-interpolation sample rate converter.
     *
     * Converts `input` recorded at `source_rate` to the current sample rate.
     * Suitable for offline conversion and preview; for production use a
     * polyphase FIR resampler.
     *
     * @param input        Source audio channel (mono).
     * @param source_rate  Sample rate of `input`.
     * @return             Resampled channel at this->hz().
     */
    std::vector<float> resample_linear(const std::vector<float>& input,
                                       const SampleRate& source_rate) const {
        if (input.empty()) return {};
        const double ratio    = conversion_ratio(source_rate);
        const auto   out_len  = static_cast<std::size_t>(
                                    static_cast<double>(input.size()) * ratio + 0.5);
        std::vector<float> output(out_len);

        for (std::size_t i = 0; i < out_len; ++i) {
            const double src_pos = static_cast<double>(i) / ratio;
            const auto   lo      = static_cast<std::size_t>(src_pos);
            const auto   hi      = lo + 1 < input.size() ? lo + 1 : lo;
            const float  frac    = static_cast<float>(src_pos - static_cast<double>(lo));
            output[i] = input[lo] + frac * (input[hi] - input[lo]);
        }
        return output;
    }

    // ------------------------------------------------------------------
    // Utilities
    // ------------------------------------------------------------------

    bool operator==(const SampleRate& o) const noexcept { return hz_ == o.hz_; }
    bool operator!=(const SampleRate& o) const noexcept { return hz_ != o.hz_; }

    /// Returns true if this is a "standard" rate known to hardware drivers.
    bool is_standard() const noexcept {
        for (auto r : {8000u, 22050u, 44100u, 48000u, 88200u, 96000u, 192000u})
            if (hz_ == r) return true;
        return false;
    }

private:
    uint32_t hz_;
};

} // namespace lilieth
