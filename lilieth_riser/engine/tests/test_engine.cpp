/**
 * LILIETH_RISER — Engine Test Suite
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * Compile & run:
 *   cd lilieth_riser/engine && cmake -B build && cmake --build build
 *   ./build/lilieth_tests
 */

#include "../include/audio_buffer.h"
#include "../include/sample_rate.h"
#include "../include/riser.h"
#include "../include/the_blade.h"
#include "../include/the_ledger.h"
#include "../include/waveform_render.h"

#include <cassert>
#include <cmath>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <chrono>

// ---------------------------------------------------------------------------
// Minimal test framework
// ---------------------------------------------------------------------------

static int  g_passed = 0;
static int  g_failed = 0;

#define PASS(msg)  do { ++g_passed; std::printf("  [PASS] %s\n", msg); } while(0)
#define FAIL(msg)  do { ++g_failed; std::printf("  [FAIL] %s\n", msg); } while(0)

#define EXPECT_TRUE(expr, msg) \
    do { if (expr) PASS(msg); else FAIL(msg); } while(0)
#define EXPECT_EQ(a, b, msg) \
    EXPECT_TRUE((a) == (b), msg)
#define EXPECT_NEAR(a, b, tol, msg) \
    EXPECT_TRUE(std::abs((a) - (b)) <= (tol), msg)
#define EXPECT_THROWS(stmt, msg) \
    do { bool caught = false; \
         try { stmt; } catch (...) { caught = true; } \
         if (caught) PASS(msg); else FAIL(msg); } while(0)

// ---------------------------------------------------------------------------
// AudioBuffer tests
// ---------------------------------------------------------------------------

void test_audio_buffer() {
    std::printf("\n[AudioBuffer]\n");

    // Construction
    lilieth::AudioBufferF buf(2, 512);
    EXPECT_EQ(buf.num_channels(), 2u, "num_channels == 2");
    EXPECT_EQ(buf.num_samples(),  512u, "num_samples == 512");

    // Zero on construction
    EXPECT_EQ(buf(0, 0), 0.0f, "samples initialised to 0");

    // Write and read back
    buf(0, 10) = 0.5f;
    EXPECT_NEAR(buf(0, 10), 0.5f, 1e-6f, "write / read single sample");

    // clear()
    buf.clear();
    EXPECT_EQ(buf(0, 10), 0.0f, "clear() zeros all samples");

    // apply_gain()
    buf(0, 0) = 1.0f;
    buf.apply_gain(0.5f);
    EXPECT_NEAR(buf(0, 0), 0.5f, 1e-6f, "apply_gain(0.5) halves amplitude");

    // slice()
    lilieth::AudioBufferF src(1, 100);
    for (std::size_t i = 0; i < 100; ++i)
        src(0, i) = static_cast<float>(i);
    auto sl = src.slice(10, 20);
    EXPECT_EQ(sl.num_samples(), 10u, "slice length == 10");
    EXPECT_NEAR(sl(0, 0), 10.0f, 1e-6f, "slice first sample");
    EXPECT_NEAR(sl(0, 9), 19.0f, 1e-6f, "slice last sample");

    // slice out-of-range
    EXPECT_THROWS(src.slice(50, 40), "slice start>end throws");
    EXPECT_THROWS(src.slice(90, 200), "slice end>size throws");

    // add_from()
    lilieth::AudioBufferF a(1, 4), b(1, 4);
    a(0,0) = 1.0f; a(0,1) = 2.0f;
    b(0,0) = 0.5f; b(0,1) = 0.5f;
    a.add_from(b, 2.0f);
    EXPECT_NEAR(a(0, 0), 2.0f, 1e-6f, "add_from: channel 0 sample 0");
    EXPECT_NEAR(a(0, 1), 3.0f, 1e-6f, "add_from: channel 0 sample 1");

    // peak()
    lilieth::AudioBufferF p(1, 4);
    p(0,0) = 0.3f; p(0,1) = -0.7f; p(0,2) = 0.1f; p(0,3) = 0.5f;
    EXPECT_NEAR(p.peak(), 0.7f, 1e-6f, "peak() returns max |sample|");

    // rms()
    lilieth::AudioBufferF r(1, 2);
    r(0,0) = 1.0f; r(0,1) = -1.0f;
    EXPECT_NEAR(r.rms(0), 1.0f, 1e-4f, "rms of ±1 square wave == 1.0");
}

// ---------------------------------------------------------------------------
// SampleRate tests
// ---------------------------------------------------------------------------

void test_sample_rate() {
    std::printf("\n[SampleRate]\n");

    lilieth::SampleRate sr48(48000);
    EXPECT_EQ(sr48.hz(), 48000u, "hz() == 48000");

    // ms → samples
    EXPECT_EQ(sr48.ms_to_samples(1.0), 48u, "1 ms == 48 samples @48kHz");

    // block size for 0.5 ms → 24 samples
    EXPECT_EQ(sr48.block_size_for_latency_ms(0.5), 24u,
              "0.5ms block == 24 samples @48kHz");

    // conversion ratio
    lilieth::SampleRate sr44(44100);
    const double ratio = sr48.conversion_ratio(sr44);
    EXPECT_NEAR(ratio, 48000.0 / 44100.0, 1e-9, "conversion ratio 44100→48000");

    // resample (upsampled output should be longer)
    std::vector<float> in44(4410, 0.5f);  // 0.1 s of audio at 44.1 kHz
    auto out48 = sr48.resample_linear(in44, sr44);
    EXPECT_EQ(out48.size(), 4800u, "resampled length == 4800 at 48 kHz");

    // standard rates
    EXPECT_TRUE(sr48.is_standard(), "48000 is standard");
    lilieth::SampleRate sr_odd(12345);
    EXPECT_TRUE(!sr_odd.is_standard(), "12345 is not standard");

    // Zero Hz throws
    EXPECT_THROWS(lilieth::SampleRate(0), "SampleRate(0) throws");
}

// ---------------------------------------------------------------------------
// Riser / PhaseVocoder tests
// ---------------------------------------------------------------------------

void test_riser() {
    std::printf("\n[Riser / PhaseVocoder]\n");

    // Phase-vocoder unity (pitch=1, stretch=1) should preserve approximate length
    lilieth::PhaseVocoder pv(512, 4);
    pv.set_pitch_factor(1.0f);

    std::vector<float> tone(2048);
    for (std::size_t i = 0; i < tone.size(); ++i)
        tone[i] = std::sin(2.0f * 3.14159f * 440.0f * static_cast<float>(i) / 48000.0f);

    auto out = pv.process(tone);
    EXPECT_TRUE(!out.empty(), "PhaseVocoder produces output");

    // Riser arm + process
    lilieth::Riser riser(lilieth::SampleRate(48000), 512, 4);
    riser.arm(-12.0f, +12.0f, 1000.0f);  // 1 second sweep -12 to +12 st
    EXPECT_TRUE(riser.is_running(), "Riser is running after arm()");
    EXPECT_NEAR(riser.progress(), 0.0f, 1e-4f, "progress starts at 0");

    std::vector<float> block(256, 0.5f);
    const auto res = riser.process_block(block);
    EXPECT_TRUE(!res.empty(), "Riser process_block returns data");

    // Stop
    riser.stop();
    EXPECT_TRUE(!riser.is_running(), "Riser stops");
}

// ---------------------------------------------------------------------------
// TheBlade tests
// ---------------------------------------------------------------------------

void test_the_blade() {
    std::printf("\n[TheBlade]\n");

    // Build a simple sine wave buffer
    lilieth::AudioBufferF buf(1, 4800);
    for (std::size_t i = 0; i < 4800; ++i)
        buf(0, i) = std::sin(2.0f * 3.14159f * 100.0f *
                             static_cast<float>(i) / 4800.0f);

    lilieth::TheBladeF blade(buf, 128);

    // Add a cut at frame 2400
    const std::size_t cut_pos = blade.cut(2400, "midpoint");
    EXPECT_EQ(blade.num_cuts(), 1u, "one cut added");

    // Extract regions — should have 2 regions
    const auto regions = blade.extract_all();
    EXPECT_EQ(regions.size(), 2u, "two regions after one cut");

    // Region 0 ends at cut, region 1 starts at cut
    EXPECT_EQ(regions[0].num_samples() + regions[1].num_samples(),
              buf.num_samples(),
              "total samples preserved across cut");

    // Duplicate cut ignored
    blade.cut(cut_pos, "dup");
    EXPECT_EQ(blade.num_cuts(), 1u, "duplicate cut ignored");

    // remove_near
    const auto removed = blade.remove_near(2400, 100);
    EXPECT_EQ(removed, 1u, "remove_near removes one cut");
    EXPECT_EQ(blade.num_cuts(), 0u, "no cuts remain");

    // Waveform peak extraction
    const auto peaks = blade.compute_peak_waveform(0, 100);
    EXPECT_EQ(peaks.size(), 100u, "peak waveform has 100 columns");
    bool all_valid = true;
    for (float p : peaks) if (p < 0.0f || p > 1.0f + 1e-4f) all_valid = false;
    EXPECT_TRUE(all_valid, "all peak values are in [0, 1]");
}

// ---------------------------------------------------------------------------
// TheLedger tests
// ---------------------------------------------------------------------------

void test_the_ledger() {
    std::printf("\n[TheLedger]\n");

    lilieth::TheLedger ledger("G2G Sages", "Track_001");

    lilieth::AudioBufferF buf(2, 4800);
    buf(0, 100) = 0.9f; // make it non-trivially hashed

    const auto& entry = ledger.log_use(buf, 48000, "Apple_01", -12.0f, 1.0f);
    EXPECT_EQ(ledger.entry_count(), 1u, "one entry after log_use");
    EXPECT_EQ(entry.artist, std::string("G2G Sages"), "artist matches");
    EXPECT_EQ(entry.project, std::string("Track_001"), "project matches");
    EXPECT_TRUE(entry.content_hash != 0, "non-zero content hash");
    EXPECT_NEAR(entry.pitch_shift_semitones, -12.0f, 1e-4f, "pitch_shift recorded");
    EXPECT_NEAR(entry.duration_ms, 4800.0 / 48000.0 * 1000.0, 0.01, "duration_ms correct");

    // Log another entry
    ledger.log_use(buf, 48000, "Apple_02");
    EXPECT_EQ(ledger.entry_count(), 2u, "two entries");

    // find_by_source
    const auto found = ledger.find_by_source("Apple_01");
    EXPECT_EQ(found.size(), 1u, "find_by_source finds one entry");

    // Export JSON
    const auto json = ledger.export_json();
    EXPECT_TRUE(json.find("\"artist\":\"G2G Sages\"") != std::string::npos,
                "JSON contains artist");
    EXPECT_TRUE(json.find("\"entry_count\":2") != std::string::npos,
                "JSON contains entry_count");

    // Empty buffer throws
    lilieth::AudioBufferF empty_buf;
    EXPECT_THROWS(ledger.log_use(empty_buf, 48000, "bad"), "empty buffer throws");
}

// ---------------------------------------------------------------------------
// WaveformRenderer tests
// ---------------------------------------------------------------------------

void test_waveform_renderer() {
    std::printf("\n[WaveformRenderer]\n");

    // Build a 2-second stereo buffer at 48 kHz (96 000 samples per channel)
    // — Quest 01 targets the real-time display window, not a full-archive render
    constexpr std::size_t N  = 96000;
    constexpr std::size_t W  = 1280;
    lilieth::AudioBufferF big(2, N);
    for (std::size_t i = 0; i < N; ++i) {
        const float s = std::sin(2.0f * 3.14159f * 440.0f *
                                 static_cast<float>(i) / 48000.0f);
        big(0, i) = s;
        big(1, i) = s * 0.5f;
    }

    lilieth::WaveformRenderer renderer;

    // Render channel 0, 1280 pixels wide
    const auto result = renderer.render(big, 0, W);
    EXPECT_EQ(result.pixels.size(), W, "output pixel count matches width");

    // Sub-millisecond render time check (Quest 01)
    EXPECT_TRUE(result.render_time_ms < 0.5,
                "render completes in < 0.5 ms (Quest 01)");
    std::printf("    render_time_ms = %.4f ms\n", result.render_time_ms);

    // All peak values should be > 0 for a sine wave
    bool any_nonzero = false;
    for (const auto& p : result.pixels)
        if (p.peak_positive > 0.0f) { any_nonzero = true; break; }
    EXPECT_TRUE(any_nonzero, "at least one non-zero pixel");

    // Overview render
    const auto overview = renderer.render_overview(big, 512);
    EXPECT_EQ(overview.size(), 512u, "overview has 512 pixels");

    // Normalisation
    auto pixels_copy = result.pixels;
    lilieth::WaveformRenderer::normalise(pixels_copy);
    float max_after = 0.0f;
    for (const auto& p : pixels_copy)
        max_after = std::max(max_after, p.peak_positive);
    EXPECT_NEAR(max_after, 1.0f, 1e-4f, "normalised peak == 1.0");

    // Error on invalid channel
    EXPECT_THROWS(renderer.render(big, 5, W),
                  "invalid channel throws");
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

int main() {
    std::printf("═══════════════════════════════════════════\n");
    std::printf("  LILIETH_RISER Engine Test Suite\n");
    std::printf("  Kernel v1.0.47  |  G2G Sovereign Tests\n");
    std::printf("═══════════════════════════════════════════\n");

    test_audio_buffer();
    test_sample_rate();
    test_riser();
    test_the_blade();
    test_the_ledger();
    test_waveform_renderer();

    std::printf("\n═══════════════════════════════════════════\n");
    std::printf("  Results: %d passed, %d failed\n", g_passed, g_failed);
    std::printf("═══════════════════════════════════════════\n");

    return g_failed > 0 ? 1 : 0;
}
