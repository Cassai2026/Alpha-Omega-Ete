/**
 * LILIETH_RISER — C FFI Bridge
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * Plain-C API surface exported as a shared library (.so / .dylib / .dll).
 * Flutter/Dart loads this via dart:ffi on Android, iOS, macOS, Windows, Linux.
 *
 * Naming convention: lr_<module>_<action>
 */

#include "../include/audio_buffer.h"
#include "../include/sample_rate.h"
#include "../include/riser.h"
#include "../include/the_blade.h"
#include "../include/the_ledger.h"
#include "../include/waveform_render.h"

#include <cstring>
#include <cstdlib>

// Export as plain C to avoid C++ name mangling
extern "C" {

// ============================================================================
// Opaque handle types (forward-declared in engine_bridge.dart)
// ============================================================================

struct LR_Riser   { lilieth::Riser*       impl; };
struct LR_Buffer  { lilieth::AudioBufferF* impl; };
struct LR_Blade   { lilieth::TheBladeF*   impl; };
struct LR_Ledger  { lilieth::TheLedger*   impl; };

// ============================================================================
// AudioBuffer
// ============================================================================

LR_Buffer* lr_buffer_create(uint32_t channels, uint32_t samples) {
    auto* h  = new LR_Buffer;
    h->impl  = new lilieth::AudioBufferF(channels, samples);
    return h;
}

void lr_buffer_destroy(LR_Buffer* h) {
    if (!h) return;
    delete h->impl;
    delete h;
}

void lr_buffer_clear(LR_Buffer* h) {
    if (h && h->impl) h->impl->clear();
}

/** Copy raw float samples into channel `ch`. `count` must equal num_samples. */
void lr_buffer_write_channel(LR_Buffer* h, uint32_t ch,
                              const float* data, uint32_t count) {
    if (!h || !h->impl || ch >= h->impl->num_channels()) return;
    const uint32_t n = static_cast<uint32_t>(h->impl->num_samples());
    std::memcpy(h->impl->channel_data(ch), data,
                static_cast<std::size_t>(count < n ? count : n) * sizeof(float));
}

/** Read raw float samples from channel `ch` into caller-supplied buffer. */
void lr_buffer_read_channel(LR_Buffer* h, uint32_t ch,
                             float* out, uint32_t count) {
    if (!h || !h->impl || ch >= h->impl->num_channels()) return;
    const uint32_t n = static_cast<uint32_t>(h->impl->num_samples());
    std::memcpy(out, h->impl->channel_data(ch),
                static_cast<std::size_t>(count < n ? count : n) * sizeof(float));
}

uint32_t lr_buffer_num_channels(LR_Buffer* h) {
    return h && h->impl ? static_cast<uint32_t>(h->impl->num_channels()) : 0;
}

uint32_t lr_buffer_num_samples(LR_Buffer* h) {
    return h && h->impl ? static_cast<uint32_t>(h->impl->num_samples()) : 0;
}

// ============================================================================
// Riser
// ============================================================================

LR_Riser* lr_riser_create(uint32_t sample_rate_hz,
                           uint32_t fft_size,
                           uint32_t overlap_factor) {
    auto* h = new LR_Riser;
    h->impl = new lilieth::Riser(
        lilieth::SampleRate(sample_rate_hz),
        fft_size  > 0 ? fft_size  : 1024,
        overlap_factor > 0 ? overlap_factor : 4);
    return h;
}

void lr_riser_destroy(LR_Riser* h) {
    if (!h) return;
    delete h->impl;
    delete h;
}

void lr_riser_arm(LR_Riser* h,
                  float start_semitones,
                  float end_semitones,
                  float duration_ms) {
    if (h && h->impl)
        h->impl->arm(start_semitones, end_semitones, duration_ms);
}

void lr_riser_stop(LR_Riser* h) {
    if (h && h->impl) h->impl->stop();
}

int lr_riser_is_running(LR_Riser* h) {
    return (h && h->impl && h->impl->is_running()) ? 1 : 0;
}

float lr_riser_progress(LR_Riser* h) {
    return (h && h->impl) ? h->impl->progress() : 0.0f;
}

/**
 * Process `count` input samples through the Riser.
 * Output is written to `out` (caller must allocate at least `count` floats).
 * Returns the number of output samples written.
 */
uint32_t lr_riser_process_block(LR_Riser* h,
                                 const float* in, uint32_t count,
                                 float* out) {
    if (!h || !h->impl || count == 0) return 0;
    const std::vector<float> input(in, in + count);
    const auto output = h->impl->process_block(input);
    const uint32_t written = static_cast<uint32_t>(output.size());
    std::memcpy(out, output.data(), written * sizeof(float));
    return written;
}

// ============================================================================
// WaveformRenderer
// ============================================================================

/**
 * Render the waveform of buffer channel `ch` into `out_peaks` and `out_rms`.
 * Both arrays must be pre-allocated by the caller with `width_px` floats.
 *
 * @return Render time in milliseconds.
 */
double lr_render_waveform(LR_Buffer* h,
                           uint32_t   channel,
                           uint32_t   width_px,
                           uint32_t   start_frame,
                           uint32_t   end_frame,
                           float*     out_peaks_pos,
                           float*     out_peaks_neg,
                           float*     out_rms) {
    if (!h || !h->impl || width_px == 0) return -1.0;

    lilieth::WaveformRenderer renderer;
    const auto result = renderer.render(
        *h->impl, channel, width_px, start_frame, end_frame);

    for (std::size_t i = 0; i < result.pixels.size(); ++i) {
        out_peaks_pos[i] = result.pixels[i].peak_positive;
        out_peaks_neg[i] = result.pixels[i].peak_negative;
        out_rms[i]       = result.pixels[i].rms;
    }
    return result.render_time_ms;
}

// ============================================================================
// TheLedger
// ============================================================================

LR_Ledger* lr_ledger_create(const char* artist, const char* project) {
    auto* h = new LR_Ledger;
    h->impl = new lilieth::TheLedger(
        artist  ? artist  : "",
        project ? project : "");
    return h;
}

void lr_ledger_destroy(LR_Ledger* h) {
    if (!h) return;
    delete h->impl;
    delete h;
}

void lr_ledger_log_use(LR_Ledger* h,
                        LR_Buffer* buf,
                        uint32_t   sample_rate_hz,
                        const char* source_label,
                        float       pitch_shift_st,
                        float       time_stretch) {
    if (!h || !h->impl || !buf || !buf->impl) return;
    h->impl->log_use(*buf->impl, sample_rate_hz,
                     source_label ? source_label : "",
                     pitch_shift_st, time_stretch);
}

uint32_t lr_ledger_entry_count(LR_Ledger* h) {
    return h && h->impl
        ? static_cast<uint32_t>(h->impl->entry_count())
        : 0;
}

/**
 * Write the ledger JSON export into `out_buf` (caller-allocated).
 * Returns the number of bytes written (excluding null terminator).
 * If `out_buf` is NULL, returns the required buffer size.
 */
uint32_t lr_ledger_export_json(LR_Ledger* h, char* out_buf, uint32_t buf_size) {
    if (!h || !h->impl) return 0;
    const std::string json = h->impl->export_json();
    if (out_buf == nullptr) return static_cast<uint32_t>(json.size() + 1);
    const uint32_t to_copy = std::min(static_cast<uint32_t>(json.size()),
                                      buf_size - 1);
    std::memcpy(out_buf, json.c_str(), to_copy);
    out_buf[to_copy] = '\0';
    return to_copy;
}

} // extern "C"
