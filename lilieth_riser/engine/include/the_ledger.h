/**
 * LILIETH_RISER — The Ledger
 * Sovereign Sampling Engine | Kernel v1.0.47
 *
 * "Every sample used is logged to ensure the artist maintains 100% ownership
 *  of the resulting track." — LILIETH_RISER Spec §02
 *
 * TheLedger records every sample-use event to a JSON-compatible log.
 * Each entry captures:
 *   - A deterministic fingerprint of the audio content (FNV-1a hash)
 *   - The originating file path / label
 *   - Start / end frame and duration
 *   - Timestamp (ISO-8601)
 *   - Artist / project context
 *   - Any applied processing (pitch shift, time stretch, etc.)
 *
 * The log can be exported to JSON for submission to a Sovereign Music Label
 * "Auto-Tag" service (Quest 03 integration point).
 */

#pragma once

#include "audio_buffer.h"

#include <cstdint>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <stdexcept>

namespace lilieth {

// ---------------------------------------------------------------------------
// Fingerprinting
// ---------------------------------------------------------------------------

namespace detail {

/**
 * @brief Compute an FNV-1a 64-bit hash over a block of audio samples.
 *
 * Deterministic: identical audio content always yields the same hash.
 * Not cryptographic — used only for ownership correlation, not security.
 */
inline uint64_t fnv1a_audio_hash(const float* samples, std::size_t count) noexcept {
    constexpr uint64_t FNV_OFFSET = 14695981039346656037ULL;
    constexpr uint64_t FNV_PRIME  =        1099511628211ULL;

    uint64_t hash = FNV_OFFSET;
    const auto* bytes = reinterpret_cast<const uint8_t*>(samples);
    const std::size_t byte_count = count * sizeof(float);

    for (std::size_t i = 0; i < byte_count; ++i) {
        hash ^= static_cast<uint64_t>(bytes[i]);
        hash *= FNV_PRIME;
    }
    return hash;
}

/// Format a UTC time as an ISO-8601 string ("2026-04-12T13:28:02Z").
inline std::string iso8601_now() {
    std::time_t t = std::time(nullptr);
    std::tm* tm_p = std::gmtime(&t);
    std::ostringstream oss;
    oss << std::put_time(tm_p, "%Y-%m-%dT%H:%M:%SZ");
    return oss.str();
}

} // namespace detail


// ---------------------------------------------------------------------------
// LedgerEntry
// ---------------------------------------------------------------------------

/**
 * @brief A single record of a sample-use event.
 */
struct LedgerEntry {
    // Identity
    std::string  entry_id;          ///< Unique identifier (timestamp + hash prefix)
    std::string  timestamp;         ///< ISO-8601 UTC timestamp of the use event
    uint64_t     content_hash;      ///< FNV-1a hash of the audio content

    // Source
    std::string  source_label;      ///< Name / path of the source audio file or Apple
    std::size_t  start_frame;       ///< First frame used
    std::size_t  end_frame;         ///< One-past-last frame used
    uint32_t     sample_rate_hz;    ///< Sample rate at which frames are measured
    double       duration_ms;       ///< Duration of the used region in milliseconds

    // Ownership context
    std::string  artist;            ///< Artist / creator name
    std::string  project;           ///< Project / track name

    // Processing applied
    float        pitch_shift_semitones; ///< 0.0 = none
    float        time_stretch_ratio;    ///< 1.0 = none
    std::string  extra_tags;            ///< Free-form JSON fragment for future extension

    // -----------------------------------------------------------------------
    // Serialisation helpers
    // -----------------------------------------------------------------------

    /**
     * @brief Serialise this entry to a single-line JSON object.
     *
     * Produces a compact, standards-compliant JSON string that can be appended
     * to a newline-delimited JSON log file.
     */
    std::string to_json() const {
        std::ostringstream j;
        j << "{"
          << "\"id\":\"" << entry_id << "\","
          << "\"ts\":\"" << timestamp << "\","
          << "\"hash\":\"" << std::hex << content_hash << std::dec << "\","
          << "\"source\":\"" << escape_json(source_label) << "\","
          << "\"start\":" << start_frame << ","
          << "\"end\":"   << end_frame   << ","
          << "\"sr\":"    << sample_rate_hz << ","
          << "\"dur_ms\":" << duration_ms  << ","
          << "\"artist\":\"" << escape_json(artist) << "\","
          << "\"project\":\"" << escape_json(project) << "\","
          << "\"pitch_st\":" << pitch_shift_semitones << ","
          << "\"stretch\":"  << time_stretch_ratio << ","
          << "\"tags\":"     << (extra_tags.empty() ? "null" : extra_tags)
          << "}";
        return j.str();
    }

private:
    static std::string escape_json(const std::string& s) {
        std::ostringstream out;
        for (char c : s) {
            switch (c) {
                case '"':  out << "\\\""; break;
                case '\\': out << "\\\\"; break;
                case '\n': out << "\\n";  break;
                case '\r': out << "\\r";  break;
                case '\t': out << "\\t";  break;
                default:   out << c;
            }
        }
        return out.str();
    }
};


// ---------------------------------------------------------------------------
// TheLedger
// ---------------------------------------------------------------------------

/**
 * @brief Append-only ownership ledger for all sample-use events.
 *
 * Usage:
 * @code
 *   TheLedger ledger("Stretford Hub", "Track_001");
 *   ledger.log_use(apple_buffer, 48000, "Breakbeat_A", 0.0f, 1.0f);
 *   std::cout << ledger.export_json() << std::endl;
 * @endcode
 */
class TheLedger {
public:
    /**
     * @param artist   Artist / creator name stamped on every entry.
     * @param project  Track / project name stamped on every entry.
     */
    explicit TheLedger(std::string artist  = "Unknown",
                       std::string project = "Untitled")
        : artist_(std::move(artist)),
          project_(std::move(project)),
          entry_counter_(0) {}

    // ------------------------------------------------------------------
    // Logging
    // ------------------------------------------------------------------

    /**
     * @brief Log a sample-use event from an AudioBuffer region.
     *
     * @param buf                  The audio being used (channel 0 is hashed).
     * @param sample_rate_hz       Sample rate at which the buffer was captured.
     * @param source_label         Name of the source Apple / file.
     * @param pitch_shift_st       Pitch shift applied in semitones (0 = none).
     * @param time_stretch_ratio   Time stretch applied (1.0 = none).
     * @param extra_tags           Optional extra JSON fragment.
     * @return                     Reference to the newly created entry.
     */
    const LedgerEntry& log_use(const AudioBufferF& buf,
                                uint32_t            sample_rate_hz,
                                const std::string&  source_label,
                                float               pitch_shift_st    = 0.0f,
                                float               time_stretch_ratio = 1.0f,
                                const std::string&  extra_tags        = "") {
        if (buf.empty())
            throw std::invalid_argument("TheLedger::log_use — cannot log empty buffer");
        if (buf.num_channels() == 0)
            throw std::invalid_argument("TheLedger::log_use — buffer has no channels");

        const uint64_t hash = detail::fnv1a_audio_hash(buf.channel_data(0),
                                                        buf.num_samples());
        const std::string ts = detail::iso8601_now();

        LedgerEntry e;
        e.content_hash            = hash;
        e.timestamp               = ts;
        e.source_label            = source_label;
        e.start_frame             = 0;
        e.end_frame               = buf.num_samples();
        e.sample_rate_hz          = sample_rate_hz;
        e.duration_ms             = static_cast<double>(buf.num_samples()) /
                                    static_cast<double>(sample_rate_hz) * 1000.0;
        e.artist                  = artist_;
        e.project                 = project_;
        e.pitch_shift_semitones   = pitch_shift_st;
        e.time_stretch_ratio      = time_stretch_ratio;
        e.extra_tags              = extra_tags;
        e.entry_id                = make_id(ts, hash);

        entries_.push_back(std::move(e));
        return entries_.back();
    }

    /**
     * @brief Log a use event by frame range (without owning the buffer data).
     *
     * Useful when the engine has already applied the use but you only have
     * the original buffer to hash against.
     */
    const LedgerEntry& log_region(const AudioBufferF& source_buf,
                                   std::size_t        start_frame,
                                   std::size_t        end_frame,
                                   uint32_t           sample_rate_hz,
                                   const std::string& source_label,
                                   float              pitch_shift_st    = 0.0f,
                                   float              time_stretch_ratio = 1.0f) {
        const auto region = source_buf.slice(start_frame, end_frame);
        auto& e = const_cast<LedgerEntry&>(
            log_use(region, sample_rate_hz, source_label,
                    pitch_shift_st, time_stretch_ratio));
        e.start_frame = start_frame;
        e.end_frame   = end_frame;
        return e;
    }

    // ------------------------------------------------------------------
    // Query
    // ------------------------------------------------------------------

    std::size_t entry_count() const noexcept { return entries_.size(); }
    const std::vector<LedgerEntry>& entries() const noexcept { return entries_; }

    /// Find all entries with a matching source label.
    std::vector<const LedgerEntry*> find_by_source(const std::string& label) const {
        std::vector<const LedgerEntry*> out;
        for (const auto& e : entries_)
            if (e.source_label == label) out.push_back(&e);
        return out;
    }

    // ------------------------------------------------------------------
    // Export
    // ------------------------------------------------------------------

    /**
     * @brief Export the full ledger as a JSON array string.
     *
     * The output is suitable for writing to a `.json` file or POSTing to the
     * Sovereign Music Label Auto-Tag API endpoint.
     */
    std::string export_json() const {
        std::ostringstream j;
        j << "{\n"
          << "  \"artist\":\"" << artist_  << "\",\n"
          << "  \"project\":\"" << project_ << "\",\n"
          << "  \"entry_count\":" << entries_.size() << ",\n"
          << "  \"entries\":[\n";

        for (std::size_t i = 0; i < entries_.size(); ++i) {
            j << "    " << entries_[i].to_json();
            if (i + 1 < entries_.size()) j << ",";
            j << "\n";
        }
        j << "  ]\n}";
        return j.str();
    }

    /**
     * @brief Export as newline-delimited JSON (NDJSON) — one object per line.
     *
     * NDJSON is streaming-friendly and can be appended to without re-parsing
     * the full file.
     */
    std::string export_ndjson() const {
        std::ostringstream s;
        for (const auto& e : entries_)
            s << e.to_json() << "\n";
        return s.str();
    }

    /// Clear all entries (non-reversible).
    void clear() noexcept { entries_.clear(); }

    // ------------------------------------------------------------------
    // Context
    // ------------------------------------------------------------------

    void set_artist(std::string name)  { artist_  = std::move(name); }
    void set_project(std::string name) { project_ = std::move(name); }
    const std::string& artist()  const noexcept { return artist_; }
    const std::string& project() const noexcept { return project_; }

private:
    std::string              artist_;
    std::string              project_;
    std::vector<LedgerEntry> entries_;
    uint64_t                 entry_counter_;

    std::string make_id(const std::string& /*ts*/, uint64_t hash) {
        std::ostringstream id;
        id << "LR_" << ++entry_counter_ << "_"
           << std::hex << (hash & 0xFFFFFFFF);
        return id.str();
    }
};

} // namespace lilieth
