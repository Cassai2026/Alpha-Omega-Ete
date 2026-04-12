/**
 * LILIETH_RISER — The Blade
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * "Precision touch-gesture waveform cutting."
 *
 * TheBlade provides non-destructive, zero-crossing-aware waveform cutting.
 * It tracks a list of CutPoints on an AudioBuffer and can extract regions
 * between cuts as independent AudioBuffers ("Apples").
 */

#pragma once

#include "audio_buffer.h"

#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <chrono>

namespace lilieth {

// ---------------------------------------------------------------------------
// CutPoint
// ---------------------------------------------------------------------------

/**
 * @brief A single edit point on a waveform timeline.
 *
 * The frame index is snapped to the nearest zero-crossing on construction
 * so that cuts never introduce clicks.
 */
struct CutPoint {
    std::size_t frame;      ///< Frame index (already zero-crossing snapped)
    std::string label;      ///< Optional user label (e.g. "VERSE_START")
    bool        enabled;    ///< Disabled cuts are ignored during extraction

    CutPoint(std::size_t f, std::string lbl = "", bool en = true)
        : frame(f), label(std::move(lbl)), enabled(en) {}

    bool operator<(const CutPoint& o) const noexcept { return frame < o.frame; }
};

// ---------------------------------------------------------------------------
// TheBlade
// ---------------------------------------------------------------------------

/**
 * @brief Non-destructive waveform editor for an AudioBuffer.
 *
 * CutPoints are stored in sorted order.  Regions are extracted as new
 * AudioBuffer instances ("Apples") without modifying the source buffer.
 *
 * Thread-safety: NOT thread-safe.  All operations must occur on a single
 * thread (typically the UI thread); pass results to the audio thread via
 * a lock-free queue.
 *
 * @tparam T  Sample type of the underlying AudioBuffer.
 */
template <typename T = float>
class TheBlade {
public:
    // ------------------------------------------------------------------
    // Construction
    // ------------------------------------------------------------------

    /**
     * @param source           Buffer to edit. The blade holds a non-owning reference.
     * @param snap_window      Zero-crossing search radius (frames) around each cut.
     */
    explicit TheBlade(AudioBuffer<T>& source, std::size_t snap_window = 256)
        : source_(source), snap_window_(snap_window) {}

    // ------------------------------------------------------------------
    // Cut management
    // ------------------------------------------------------------------

    /**
     * @brief Add a cut at the given frame position.
     *
     * The frame is snapped to the nearest zero-crossing of channel 0.
     * Duplicate cuts (within ±1 frame after snapping) are silently ignored.
     *
     * @param frame  Desired cut position (0…source.num_samples()-1).
     * @param label  Optional label for this cut.
     * @return       Actual frame index after zero-crossing snap.
     */
    std::size_t cut(std::size_t frame, const std::string& label = "") {
        if (frame >= source_.num_samples())
            throw std::out_of_range("TheBlade::cut — frame out of range");

        const std::size_t snapped =
            source_.nearest_zero_crossing(0, frame, snap_window_);

        // Check for near-duplicate
        for (const auto& cp : cuts_)
            if (cp.enabled &&
                (cp.frame == snapped ||
                 (cp.frame > 0 && cp.frame - 1 == snapped) ||
                 cp.frame + 1 == snapped))
                return cp.frame; // already cut here

        cuts_.emplace_back(snapped, label);
        std::sort(cuts_.begin(), cuts_.end());
        return snapped;
    }

    /**
     * @brief Remove all cuts within `tolerance` frames of `frame`.
     *
     * @param frame      Target frame.
     * @param tolerance  Search radius in frames.
     * @return           Number of cuts removed.
     */
    std::size_t remove_near(std::size_t frame, std::size_t tolerance = 64) {
        const std::size_t before = cuts_.size();
        cuts_.erase(std::remove_if(cuts_.begin(), cuts_.end(),
                        [&](const CutPoint& cp) {
                            const std::size_t d = (cp.frame > frame)
                                ? cp.frame - frame : frame - cp.frame;
                            return d <= tolerance;
                        }),
                    cuts_.end());
        return before - cuts_.size();
    }

    /// Remove all cuts.
    void clear_cuts() noexcept { cuts_.clear(); }

    /// Read-only access to all cut points.
    const std::vector<CutPoint>& cuts() const noexcept { return cuts_; }

    /// Number of cuts.
    std::size_t num_cuts() const noexcept { return cuts_.size(); }

    // ------------------------------------------------------------------
    // Region extraction
    // ------------------------------------------------------------------

    /**
     * @brief Extract the audio between two consecutive cuts (or buffer edges)
     *        as a new AudioBuffer — an "Apple".
     *
     * Regions are indexed 0…N where N = num_cuts().
     *  - Region 0:    start of buffer → first cut
     *  - Region k:    cut[k-1]        → cut[k]    (for k = 1…N-1)
     *  - Region N:    last cut         → end of buffer
     *
     * @param region_index  Index of the region to extract.
     * @return              New AudioBuffer containing the region's samples.
     */
    AudioBuffer<T> extract_region(std::size_t region_index) const {
        const auto enabled = enabled_cuts();
        const std::size_t num_regions = enabled.size() + 1;

        if (region_index >= num_regions)
            throw std::out_of_range("TheBlade::extract_region — index out of range");

        const std::size_t start = (region_index == 0)
                                  ? 0
                                  : enabled[region_index - 1];
        const std::size_t end   = (region_index == enabled.size())
                                  ? source_.num_samples()
                                  : enabled[region_index];

        return source_.slice(start, end);
    }

    /**
     * @brief Extract all regions as a vector of AudioBuffers.
     *
     * @return  One AudioBuffer per region (num_cuts() + 1 total).
     */
    std::vector<AudioBuffer<T>> extract_all() const {
        const auto enabled = enabled_cuts();
        std::vector<AudioBuffer<T>> result;
        result.reserve(enabled.size() + 1);

        std::size_t prev = 0;
        for (const std::size_t cut_frame : enabled) {
            result.push_back(source_.slice(prev, cut_frame));
            prev = cut_frame;
        }
        result.push_back(source_.slice(prev, source_.num_samples()));
        return result;
    }

    // ------------------------------------------------------------------
    // Waveform overview helpers (used by Flutter waveform display)
    // ------------------------------------------------------------------

    /**
     * @brief Compute peak values for each pixel column in a waveform view.
     *
     * This is the inner loop targeted for < 0.5 ms rendering at typical
     * display widths.  Operates on channel `ch` of the source buffer.
     *
     * @param ch          Channel index to render.
     * @param width_px    Number of output columns (pixels).
     * @param start_frame First frame in the visible range.
     * @param end_frame   One-past-last frame in the visible range.
     * @return            Vector of `width_px` peak magnitudes in [0, 1].
     */
    std::vector<float> compute_peak_waveform(std::size_t ch,
                                             std::size_t width_px,
                                             std::size_t start_frame = 0,
                                             std::size_t end_frame   = 0) const {
        if (end_frame == 0 || end_frame > source_.num_samples())
            end_frame = source_.num_samples();
        if (start_frame >= end_frame || width_px == 0)
            return std::vector<float>(width_px, 0.0f);

        const T* data          = source_.channel_data(ch);
        const std::size_t span = end_frame - start_frame;
        std::vector<float> peaks(width_px, 0.0f);

        for (std::size_t px = 0; px < width_px; ++px) {
            // Map pixel → frame range
            const std::size_t f0 = start_frame + (px * span) / width_px;
            const std::size_t f1 = start_frame + ((px + 1) * span) / width_px;

            float peak = 0.0f;
            for (std::size_t f = f0; f < f1 && f < end_frame; ++f) {
                const float s = std::abs(static_cast<float>(data[f]));
                if (s > peak) peak = s;
            }
            peaks[px] = peak;
        }
        return peaks;
    }

private:
    AudioBuffer<T>&     source_;
    std::size_t         snap_window_;
    std::vector<CutPoint> cuts_;

    /// Returns a sorted list of frame indices for enabled cuts only.
    std::vector<std::size_t> enabled_cuts() const {
        std::vector<std::size_t> out;
        out.reserve(cuts_.size());
        for (const auto& cp : cuts_)
            if (cp.enabled) out.push_back(cp.frame);
        return out;
    }
};

using TheBladeF = TheBlade<float>;
using TheBladeD = TheBlade<double>;

} // namespace lilieth
