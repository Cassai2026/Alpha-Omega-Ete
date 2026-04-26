# LILIETH_RISER — Sync Protocol Specification
**Kernel v1.0.47 | Sovereign Sampling Engine**

---

## Overview

The LILIETH_RISER sync layer uses a **WebSocket + newline-delimited JSON** protocol.

| Role | Device | Responsibility |
|:--|:--|:--|
| **CONTROLLER** | Phone | Touch input, pad triggers, Riser control |
| **PROCESSOR** | Laptop | Audio rendering, Ledger storage, waveform computation |
| **MIRROR** | Projector/TV | Receives waveform / live-build stream (read-only) |

---

## Transport

| Property | Value |
|:--|:--|
| Transport | WebSocket (RFC 6455) |
| Encoding | UTF-8 JSON, one object per message |
| Port (default) | **8765** |
| Keep-alive | Server sends WebSocket `ping` every 20 s |

---

## Message Format

Every message is a JSON object with a required `"type"` string field:

```json
{ "type": "<MsgType>", ...payload fields... }
```

---

## Message Types

### Controller → Processor

#### `padTrigger`
Fired when the user touches a pad.

```json
{
  "type": "padTrigger",
  "pad_index": 3,
  "velocity": 0.85
}
```

| Field | Type | Description |
|:--|:--|:--|
| `pad_index` | int | 0-based pad index (0–15 for a 4×4 grid) |
| `velocity` | float | Touch pressure / velocity 0.0–1.0 |

---

#### `riserArm`
Arms the Riser sweep.  Processor begins real-time pitch processing.

```json
{
  "type": "riserArm",
  "start_st": -24.0,
  "end_st": 12.0,
  "duration_ms": 2000.0
}
```

---

#### `riserStop`
Stops an in-progress Riser sweep.

```json
{ "type": "riserStop" }
```

---

#### `cut`
Places a cut point ("The Blade") at a normalised position.

```json
{
  "type": "cut",
  "position": 0.4375
}
```

| Field | Type | Description |
|:--|:--|:--|
| `position` | float | Normalised time position 0.0–1.0 |

---

#### `loadApple`
Requests a sample region to be loaded onto a pad.

```json
{
  "type": "loadApple",
  "label": "Breakbeat_A",
  "start_frame": 0,
  "end_frame": 48000,
  "sr": 48000
}
```

---

### Processor → Controller

#### `waveformData`
Delivers rendered waveform data (after loading an Apple or cutting).

```json
{
  "type": "waveformData",
  "peaks_pos": [0.1, 0.5, 0.9, ...],
  "peaks_neg": [0.1, 0.4, 0.8, ...],
  "rms":       [0.05, 0.25, 0.45, ...],
  "render_ms": 0.312
}
```

Array length equals the display width in pixels (default 1280).

---

#### `riserProgress`
Streams sweep progress 0.0–1.0 at ~60 fps while the Riser is active.

```json
{ "type": "riserProgress", "progress": 0.4 }
```

---

#### `ledgerEntry`
Notifies the Controller that a new Ledger entry has been created.

```json
{
  "type": "ledgerEntry",
  "entry": {
    "id": "LR_1_deadbeef",
    "ts": "2026-04-12T13:28:02Z",
    "source": "Breakbeat_A",
    "dur_ms": 1000.0,
    "artist": "G2G Sages",
    "project": "Track_001",
    "pitch_st": -12.0,
    "stretch": 1.0
  }
}
```

---

### Bidirectional

#### `ping` / `pong`

```json
{ "type": "ping" }
{ "type": "pong", "ts": 1712926082.0 }
```

---

## Sequence: Loading an Apple

```
Controller                           Processor
    │                                    │
    │──── loadApple ────────────────────►│
    │                                    │  (renders waveform via C++ engine)
    │◄─── waveformData ──────────────────│
    │                                    │  (logs to Ledger)
    │◄─── ledgerEntry ───────────────────│
```

---

## Sequence: Riser Sweep

```
Controller                           Processor
    │                                    │
    │──── riserArm ─────────────────────►│
    │                                    │  (starts pitch sweep in audio thread)
    │◄─── riserProgress (0.0) ───────────│
    │◄─── riserProgress (0.1) ───────────│
    │◄─── ...          (0.99) ───────────│
    │──── riserStop ─────────────────────►│ (optional early stop)
```

---

## Security Notes

- The sync server is designed for **local network (LAN)** use only.
- No authentication is included in the base protocol; add TLS + token auth
  before deploying over the internet.
- All audio content remains on the originating device; only metadata (labels,
  frame indices, Ledger entries) crosses the WebSocket.
