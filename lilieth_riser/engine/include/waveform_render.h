/**
 * LILIETH_RISER — Waveform Renderer
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * "Quest 01: Implement a 0.5 ms latency waveform render in C++."
 *
 * WaveformRenderer converts an AudioBuffer into a compact peak+RMS dataset
 * ready for the Flutter waveform display.  The hot-loop uses only integer
 * arithmetic and sequential memory access, targeting < 0.5 ms for typical
 * display widths on modern hardware.
 *
 * Downstream Flutter code reads the RenderResult and maps peaks/rms values
 * to canvas heights via a CustomPainter.
 */

#pragma once

#include "audio_buffer.h"

#include <vector>
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <chrono>

namespace lilieth {

// ---------------------------------------------------------------------------
// RenderResult
// ---------------------------------------------------------------------------

/**
 * @brief The per-pixel waveform data produced by WaveformRenderer.
 *
 * Each element corresponds to one horizontal pixel column in the display.
 */
struct WaveformPixel {
    float peak_positive;   ///< Maximum positive amplitude in the column's frame range
    float peak_negative;   ///< Maximum negative amplitude (stored as positive magnitude)
    float rms;             ///< RMS amplitude for the column
};

struct RenderResult {
    std::vector<WaveformPixel> pixels;    ///< One entry per display column
    double render_time_ms;                ///< Wall-clock time for the render pass
    std::size_t frames_rendered;          ///< Number of source frames covered
    std::size_t channel_rendered;         ///< Which channel was rendered
};

// ---------------------------------------------------------------------------
// WaveformRenderer
// ---------------------------------------------------------------------------

/**
 * @brief Converts a region of an AudioBuffer into a per-pixel waveform summary.
 *
 * The render algorithm uses two passes over the data per pixel column:
 *  1. Peak scan (max |sample|) — O(samples_per_pixel)
 *  2. RMS accumulation (Σ s²) — combined with pass 1
 *
 * Both passes share the same inner loop to maximise cache efficiency.
 *
 * Usage:
 * @code
 *   WaveformRenderer renderer;
 *   auto result = renderer.render(buffer, 0, 1280,
 *                                 0, buffer.num_samples());
 *   // Pass result.pixels to Flutter via FFI
 * @endcode
 */
class WaveformRenderer {
public:
    WaveformRenderer() = default;

    // ------------------------------------------------------------------
    // Main render entry point
    // ------------------------------------------------------------------

    /**
     * @brief Render a waveform summary for a channel region.
     *
     * @param buf          Source AudioBuffer (must have at least `channel+1` channels).
     * @param channel      Channel index to render.
     * @param width_px     Number of output pixel columns.
     * @param start_frame  First source frame (default: start of buffer).
     * @param end_frame    One-past-last source frame (0 = end of buffer).
     * @return             RenderResult with per-pixel peak & RMS data.
     */
    template <typename T>
    RenderResult render(const AudioBuffer<T>& buf,
                        std::size_t channel    = 0,
                        std::size_t width_px   = 1280,
                        std::size_t start_frame = 0,
                        std::size_t end_frame   = 0) const {
        // Validate inputs
        if (channel >= buf.num_channels())
            throw std::out_of_range("WaveformRenderer::render — channel out of range");
        if (end_frame == 0 || end_frame > buf.num_samples())
            end_frame = buf.num_samples();
        if (start_frame >= end_frame)
            throw std::invalid_argument(
                "WaveformRenderer::render — start_frame must be < end_frame");
        if (width_px == 0)
            throw std::invalid_argument(
                "WaveformRenderer::render — width_px must be > 0");

        // Start timing
        const auto t0 = std::chrono::high_resolution_clock::now();

        const T*          data = buf.channel_data(channel);
        const std::size_t span = end_frame - start_frame;

        RenderResult result;
        result.pixels.resize(width_px);
        result.frames_rendered  = span;
        result.channel_rendered = channel;

        // ------------------------------------------------------------------
        // Hot loop — compute peak_positive, peak_negative, rms per column
        // ------------------------------------------------------------------
        for (std::size_t px = 0; px < width_px; ++px) {
            // Map pixel column to source frame range
            const std::size_t f0 = start_frame + (px * span) / width_px;
            const std::size_t f1 = start_frame + ((px + 1) * span) / width_px;

            float pos  = 0.0f;
            float neg  = 0.0f;
            float sum2 = 0.0f;
            const std::size_t count = f1 - f0;

            // Branch-free inner loop — compiler can auto-vectorise with SIMD
            for (std::size_t f = f0; f < f1; ++f) {
                const float s = static_cast<float>(data[f]);
                pos  = s > pos  ?  s : pos;
                neg  = s < -neg ? -s : neg;
                sum2 += s * s;
            }

            WaveformPixel& pix = result.pixels[px];
            pix.peak_positive = pos;
            pix.peak_negative = neg;
            pix.rms = (count > 0)
                      ? std::sqrt(sum2 / static_cast<float>(count))
                      : 0.0f;
        }

        // Record timing
        const auto t1 = std::chrono::high_resolution_clock::now();
        result.render_time_ms =
            std::chrono::duration<double, std::milli>(t1 - t0).count();

        return result;
    }

    // ------------------------------------------------------------------
    // Downsampled overview (for the full-file thumbnail)
    // ------------------------------------------------------------------

    /**
     * @brief Render a multi-channel overview waveform (all channels averaged).
     *
     * Returns only peak values (no RMS) for maximum speed.
     *
     * @param buf       Source buffer.
     * @param width_px  Number of output pixel columns.
     * @return          Vector of peak amplitudes in [0, 1], length = width_px.
     */
    template <typename T>
    std::vector<float> render_overview(const AudioBuffer<T>& buf,
                                       std::size_t width_px = 512) const {
        if (buf.empty() || width_px == 0) return std::vector<float>(width_px, 0.0f);

        const std::size_t N  = buf.num_samples();
        const std::size_t CH = buf.num_channels();
        std::vector<float> out(width_px, 0.0f);

        for (std::size_t ch = 0; ch < CH; ++ch) {
            const T* data = buf.channel_data(ch);
            for (std::size_t px = 0; px < width_px; ++px) {
                const std::size_t f0 = (px * N) / width_px;
                const std::size_t f1 = ((px + 1) * N) / width_px;
                float peak = 0.0f;
                for (std::size_t f = f0; f < f1; ++f) {
                    const float s = std::abs(static_cast<float>(data[f]));
                    if (s > peak) peak = s;
                }
                out[px] = std::max(out[px], peak);
            }
        }
        return out;
    }

    // ------------------------------------------------------------------
    // Normalisation helper
    // ------------------------------------------------------------------

    /**
     * @brief Normalise a pixel vector so the highest peak = 1.0.
     *
     * Call after render() if you want a display that always fills the canvas
     * height regardless of input level.
     *
     * @param pixels  In-place modified.
     */
    static void normalise(std::vector<WaveformPixel>& pixels) noexcept {
        float max_peak = 0.0f;
        for (const auto& p : pixels)
            max_peak = std::max(max_peak,
                                std::max(p.peak_positive, p.peak_negative));
        if (max_peak <= 0.0f) return;
        for (auto& p : pixels) {
            p.peak_positive /= max_peak;
            p.peak_negative /= max_peak;
            p.rms           /= max_peak;
        }
    }

    static void normalise(std::vector<float>& peaks) noexcept {
        const float mx = *std::max_element(peaks.begin(), peaks.end());
        if (mx <= 0.0f) return;
        for (auto& v : peaks) v /= mx;
    }
};

} // namespace lilieth
