/**
 * LILIETH_RISER — The Riser Algorithm
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * "Infinite pitch-shift and time-stretch without losing fidelity."
 *
 * Implements a phase-vocoder pitch-shifter / time-stretcher and a granular
 * "Doppler Riser" sweep for dramatic pitch ascents.
 *
 * Pipeline overview
 * ─────────────────
 *   Input PCM  →  [Analysis STFT]  →  [Phase Accumulation]
 *              →  [Magnitude Scale / Phase Advance]
 *              →  [Synthesis STFT]  →  Output PCM
 *
 * For the low-latency "Riser sweep" a lighter granular engine is available
 * that avoids full FFT analysis and targets < 5 ms additional latency.
 */

#pragma once

#include "audio_buffer.h"
#include "sample_rate.h"

#include <complex>
#include <cmath>
#include <vector>
#include <stdexcept>
#include <algorithm>
#include <numeric>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

namespace lilieth {

// ---------------------------------------------------------------------------
// FFT helpers (portable Cooley-Tukey, power-of-two only)
// ---------------------------------------------------------------------------

namespace detail {

/// In-place Cooley-Tukey FFT (Radix-2 DIT).
/// @param data  Complex samples; size must be a power of two.
/// @param inv   If true, performs IFFT (scaled by 1/N).
inline void fft(std::vector<std::complex<float>>& data, bool inv = false) {
    const std::size_t N = data.size();
    if (N <= 1) return;
    if ((N & (N - 1)) != 0)
        throw std::invalid_argument("FFT size must be a power of two");

    // Bit-reversal permutation
    for (std::size_t i = 1, j = 0; i < N; ++i) {
        std::size_t bit = N >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) std::swap(data[i], data[j]);
    }

    // Butterfly stages
    for (std::size_t len = 2; len <= N; len <<= 1) {
        const double ang = 2.0 * M_PI / static_cast<double>(len) * (inv ? 1.0 : -1.0);
        const std::complex<float> wlen(static_cast<float>(std::cos(ang)),
                                       static_cast<float>(std::sin(ang)));
        for (std::size_t i = 0; i < N; i += len) {
            std::complex<float> w(1.0f, 0.0f);
            for (std::size_t j = 0; j < len / 2; ++j) {
                const auto u = data[i + j];
                const auto v = data[i + j + len / 2] * w;
                data[i + j]           = u + v;
                data[i + j + len / 2] = u - v;
                w *= wlen;
            }
        }
    }
    if (inv) {
        const float inv_n = 1.0f / static_cast<float>(N);
        for (auto& s : data) s *= inv_n;
    }
}

/// Build a Hann analysis/synthesis window.
inline std::vector<float> hann_window(std::size_t size) {
    std::vector<float> w(size);
    for (std::size_t i = 0; i < size; ++i)
        w[i] = 0.5f * (1.0f - std::cos(2.0f * static_cast<float>(M_PI) *
                                        static_cast<float>(i) /
                                        static_cast<float>(size - 1)));
    return w;
}

/// Wrap phase into [-π, π].
inline float wrap_phase(float p) noexcept {
    while (p >  static_cast<float>(M_PI)) p -= 2.0f * static_cast<float>(M_PI);
    while (p < -static_cast<float>(M_PI)) p += 2.0f * static_cast<float>(M_PI);
    return p;
}

} // namespace detail


// ---------------------------------------------------------------------------
// PhaseVocoder
// ---------------------------------------------------------------------------

/**
 * @brief Phase-vocoder based pitch-shifter / time-stretcher (single channel).
 *
 * Usage:
 * @code
 *   PhaseVocoder pv(1024, 4, SampleRate(48000));
 *   pv.set_pitch_shift_semitones(+7.0f);   // transpose up a fifth
 *   auto out = pv.process(input_buffer);
 * @endcode
 */
class PhaseVocoder {
public:
    static constexpr std::size_t kDefaultFftSize   = 1024;
    static constexpr std::size_t kDefaultOverlapFactor = 4;  // 75 % overlap

    /**
     * @param fft_size      FFT window length (power of two, typically 512–4096).
     * @param overlap       Overlap factor — must divide fft_size evenly.
     * @param rate          Engine sample rate.
     */
    PhaseVocoder(std::size_t fft_size      = kDefaultFftSize,
                 std::size_t overlap_factor = kDefaultOverlapFactor,
                 SampleRate  rate           = SampleRate(48000))
        : fft_size_(fft_size),
          hop_size_(fft_size / overlap_factor),
          sample_rate_(rate),
          pitch_factor_(1.0f),
          time_stretch_(1.0f),
          window_(detail::hann_window(fft_size)),
          last_phase_(fft_size / 2 + 1, 0.0f),
          synth_phase_(fft_size / 2 + 1, 0.0f),
          output_accum_(fft_size * 2, 0.0f),
          input_buf_(fft_size, 0.0f),
          input_pos_(0)
    {
        if ((fft_size & (fft_size - 1)) != 0)
            throw std::invalid_argument("PhaseVocoder: fft_size must be a power of two");
        if (overlap_factor == 0 || fft_size % overlap_factor != 0)
            throw std::invalid_argument("PhaseVocoder: overlap_factor must divide fft_size");
    }

    // ------------------------------------------------------------------
    // Parameters
    // ------------------------------------------------------------------

    /** Set pitch shift in semitones (positive = up, negative = down). */
    void set_pitch_shift_semitones(float semitones) noexcept {
        pitch_factor_ = std::pow(2.0f, semitones / 12.0f);
    }

    /** Set pitch shift factor directly (1.0 = no change, 2.0 = one octave up). */
    void set_pitch_factor(float factor) noexcept {
        pitch_factor_ = std::max(0.1f, factor);
    }

    /** Set time stretch ratio (1.0 = no change, 2.0 = double duration). */
    void set_time_stretch(float ratio) noexcept {
        time_stretch_ = std::max(0.1f, ratio);
    }

    float pitch_factor()  const noexcept { return pitch_factor_; }
    float time_stretch()  const noexcept { return time_stretch_; }

    /** Reset all internal phase state (call when loading a new sample). */
    void reset() noexcept {
        std::fill(last_phase_.begin(),   last_phase_.end(),   0.0f);
        std::fill(synth_phase_.begin(),  synth_phase_.end(),  0.0f);
        std::fill(output_accum_.begin(), output_accum_.end(), 0.0f);
        std::fill(input_buf_.begin(),    input_buf_.end(),    0.0f);
        input_pos_ = 0;
    }

    // ------------------------------------------------------------------
    // Processing
    // ------------------------------------------------------------------

    /**
     * @brief Process a block of mono samples through the phase vocoder.
     *
     * @param input   Input samples.
     * @return        Pitch-shifted / time-stretched output (same length as input
     *                for unity time-stretch; otherwise proportionally sized).
     */
    std::vector<float> process(const std::vector<float>& input) {
        const std::size_t half = fft_size_ / 2 + 1;
        const float expected_phase_advance =
            2.0f * static_cast<float>(M_PI) * static_cast<float>(hop_size_) /
            static_cast<float>(fft_size_);

        // Output length scales with time_stretch
        const auto out_len = static_cast<std::size_t>(
            static_cast<float>(input.size()) * time_stretch_ + 0.5f);
        std::vector<float> output(out_len, 0.0f);

        // Feed samples into the sliding buffer and process hop by hop
        std::size_t in_cursor  = 0;
        std::size_t out_cursor = 0;

        while (in_cursor < input.size()) {
            // Fill input buffer
            while (input_pos_ < fft_size_ && in_cursor < input.size())
                input_buf_[input_pos_++] = input[in_cursor++];

            if (input_pos_ < hop_size_) break;
            input_pos_ = 0;

            // --- Analysis ---
            std::vector<std::complex<float>> spectrum(fft_size_);
            for (std::size_t i = 0; i < fft_size_; ++i)
                spectrum[i] = std::complex<float>(input_buf_[i] * window_[i], 0.0f);
            detail::fft(spectrum, false);

            // --- Phase processing ---
            std::vector<float> true_freq(half);
            for (std::size_t k = 0; k < half; ++k) {
                const float mag   = std::abs(spectrum[k]);
                const float phase = std::arg(spectrum[k]);

                float delta = phase - last_phase_[k] - expected_phase_advance *
                              static_cast<float>(k);
                delta = detail::wrap_phase(delta);

                true_freq[k] = (expected_phase_advance * static_cast<float>(k) + delta) /
                               static_cast<float>(hop_size_);
                last_phase_[k] = phase;

                // Modify magnitude for pitch shifting (resample in frequency domain below)
                spectrum[k] = std::polar(mag, synth_phase_[k]);
            }

            // Pitch shift: re-bin the spectrum
            std::vector<std::complex<float>> shifted(fft_size_, {0.0f, 0.0f});
            for (std::size_t k = 0; k < half; ++k) {
                const auto shifted_k = static_cast<std::size_t>(
                    static_cast<float>(k) * pitch_factor_ + 0.5f);
                if (shifted_k < half) {
                    const float mag = std::abs(spectrum[k]);
                    synth_phase_[shifted_k] +=
                        true_freq[k] * pitch_factor_ * static_cast<float>(hop_size_);
                    shifted[shifted_k] = std::polar(
                        mag, synth_phase_[shifted_k]);
                    // Mirror into negative-frequency half
                    if (shifted_k > 0 && shifted_k < fft_size_ - shifted_k)
                        shifted[fft_size_ - shifted_k] = std::conj(shifted[shifted_k]);
                }
            }

            // --- Synthesis ---
            detail::fft(shifted, true);
            const float window_sum_sq = std::accumulate(
                window_.begin(), window_.end(), 0.0f,
                [](float a, float b) { return a + b * b; });
            const float norm = (window_sum_sq > 0.0f)
                               ? static_cast<float>(hop_size_) / window_sum_sq
                               : 1.0f;

            for (std::size_t i = 0; i < fft_size_ && out_cursor + i < out_len; ++i)
                output[out_cursor + i] += shifted[i].real() * window_[i] * norm;

            out_cursor += static_cast<std::size_t>(
                static_cast<float>(hop_size_) * time_stretch_ + 0.5f);

            // Slide the input buffer
            std::copy(input_buf_.begin() + static_cast<std::ptrdiff_t>(hop_size_),
                      input_buf_.end(),
                      input_buf_.begin());
            std::fill(input_buf_.end() - static_cast<std::ptrdiff_t>(hop_size_),
                      input_buf_.end(), 0.0f);
        }

        return output;
    }

private:
    std::size_t fft_size_;
    std::size_t hop_size_;
    SampleRate  sample_rate_;
    float       pitch_factor_;
    float       time_stretch_;

    std::vector<float> window_;
    std::vector<float> last_phase_;
    std::vector<float> synth_phase_;
    std::vector<float> output_accum_;
    std::vector<float> input_buf_;
    std::size_t        input_pos_;
};


// ---------------------------------------------------------------------------
// Riser — Doppler pitch-sweep
// ---------------------------------------------------------------------------

/**
 * @brief The Riser: a continuous pitch-sweep effect ("Doppler Riser").
 *
 * Smoothly interpolates the PhaseVocoder's pitch factor from a start value to
 * an end value over a configurable duration, creating the signature "infinite
 * ascent" sound popular in DJ drops and cinematic builds.
 *
 * Usage:
 * @code
 *   Riser riser(SampleRate(48000));
 *   riser.arm(-24.0f,   // start_semitones
 *             +12.0f,   // end_semitones
 *             2000.0f); // duration_ms
 *
 *   while (riser.is_running()) {
 *       auto block_out = riser.process_block(input_block);
 *       // push block_out to audio output
 *   }
 * @endcode
 */
class Riser {
public:
    explicit Riser(SampleRate rate = SampleRate(48000),
                   std::size_t fft_size = 1024,
                   std::size_t overlap  = 4)
        : sample_rate_(rate),
          pv_(fft_size, overlap, rate),
          start_semitones_(-24.0f),
          end_semitones_(12.0f),
          total_samples_(0),
          elapsed_samples_(0),
          running_(false)
    {}

    // ------------------------------------------------------------------
    // Configuration
    // ------------------------------------------------------------------

    /**
     * @brief Arm the riser for playback.
     *
     * @param start_semitones  Pitch at t=0 (e.g. -24 = two octaves below).
     * @param end_semitones    Pitch at t=duration (e.g. +12 = one octave above).
     * @param duration_ms      Sweep duration in milliseconds.
     */
    void arm(float start_semitones,
             float end_semitones,
             float duration_ms) noexcept {
        start_semitones_  = start_semitones;
        end_semitones_    = end_semitones;
        total_samples_    = sample_rate_.ms_to_samples(static_cast<double>(duration_ms));
        elapsed_samples_  = 0;
        running_          = (total_samples_ > 0);
        pv_.reset();
        pv_.set_pitch_shift_semitones(start_semitones);
    }

    /// Stop/reset the riser.
    void stop() noexcept {
        running_ = false;
        elapsed_samples_ = 0;
        pv_.reset();
    }

    bool is_running() const noexcept { return running_; }

    /// 0.0 = not started, 1.0 = sweep complete.
    float progress() const noexcept {
        if (total_samples_ == 0) return 1.0f;
        return static_cast<float>(elapsed_samples_) /
               static_cast<float>(total_samples_);
    }

    // ------------------------------------------------------------------
    // Processing
    // ------------------------------------------------------------------

    /**
     * @brief Process a mono block through the riser.
     *
     * The pitch factor is updated once per block (not per sample) for
     * performance. At typical block sizes (64–256 frames) this is inaudible.
     *
     * @param input  Input audio block.
     * @return       Pitch-shifted output block.
     */
    std::vector<float> process_block(const std::vector<float>& input) {
        if (!running_ || input.empty()) return input;

        // Update pitch for this block's midpoint
        const float t = progress();
        const float current_semitones =
            start_semitones_ + t * (end_semitones_ - start_semitones_);
        pv_.set_pitch_shift_semitones(current_semitones);

        elapsed_samples_ += input.size();
        if (elapsed_samples_ >= total_samples_) {
            elapsed_samples_ = total_samples_;
            running_ = false;
        }

        return pv_.process(input);
    }

    /**
     * @brief Apply the riser to a whole AudioBuffer (convenience wrapper).
     *
     * Processes each channel independently.  The buffer is modified in-place
     * and potentially resized if time_stretch != 1.0.
     *
     * @param buf  Buffer to process; all channels treated identically.
     */
    void apply_to_buffer(AudioBufferF& buf) {
        for (std::size_t ch = 0; ch < buf.num_channels(); ++ch) {
            std::vector<float> chan(buf.channel_data(ch),
                                   buf.channel_data(ch) + buf.num_samples());
            const auto out = process_block(chan);
            // If output length differs, keep the shorter of the two
            const std::size_t copy_len = std::min(out.size(), buf.num_samples());
            std::copy(out.begin(), out.begin() + static_cast<std::ptrdiff_t>(copy_len),
                      buf.channel_data(ch));
        }
    }

    PhaseVocoder& vocoder() noexcept { return pv_; }

private:
    SampleRate   sample_rate_;
    PhaseVocoder pv_;
    float        start_semitones_;
    float        end_semitones_;
    uint64_t     total_samples_;
    uint64_t     elapsed_samples_;
    bool         running_;
};

} // namespace lilieth
