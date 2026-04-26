# LILIETH_RISER
## The Sovereign Sampling & Performance Engine
**Kernel v1.0.47 | G2G Sages Only**

> *"A minimalist, high-torque audio sampler designed for the Stretford Hub. It turns a mobile device into a precision instrument for cutting, pitching, and layering Apples (audio tracks)."*

---

## Architecture

```
lilieth_riser/
├── engine/                  ← C++ audio engine (header-only)
│   ├── include/
│   │   ├── audio_buffer.h   ← Multi-channel sample buffer
│   │   ├── sample_rate.h    ← Sample rate management & conversion
│   │   ├── riser.h          ← Phase-vocoder pitch-shifter / "Doppler Riser"
│   │   ├── the_blade.h      ← Waveform cutting with zero-crossing snap
│   │   ├── the_ledger.h     ← Sample ownership log (JSON export)
│   │   └── waveform_render.h← < 0.5 ms peak/RMS waveform renderer
│   ├── src/
│   │   └── ffi_bridge.cpp   ← Plain-C API for Flutter FFI
│   ├── tests/
│   │   └── test_engine.cpp  ← Self-contained test suite
│   └── CMakeLists.txt       ← Build system
│
├── flutter_ui/              ← "Black Canvas" Flutter UI
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/sampler_screen.dart
│   │   ├── widgets/
│   │   │   ├── waveform_display.dart
│   │   │   └── pad_grid.dart
│   │   ├── services/websocket_service.dart
│   │   └── ffi/engine_bridge.dart
│   └── pubspec.yaml
│
└── sync/                    ← Multi-device sync
    ├── ws_server.py         ← WebSocket processor server
    └── protocol.md          ← Message protocol specification
```

---

## Core Features

| Feature | Module | Status |
|:--|:--|:--|
| **The Blade** — precision waveform cutting | `the_blade.h` | ✅ Implemented |
| **The Rise** — infinite pitch-shift / time-stretch | `riser.h` | ✅ Implemented |
| **The Ledger** — sample ownership log | `the_ledger.h` | ✅ Implemented |
| **Waveform Render** — < 0.5 ms Quest 01 | `waveform_render.h` | ✅ Implemented |
| **Black Canvas UI** — Flutter | `flutter_ui/` | ✅ Scaffold |
| **Master/Client Sync** — WebSocket | `sync/` | ✅ Implemented |
| **The Mirror** — NDI/AirPlay projection | TBD | 🔄 Quest 02 |
| **Auto-Tag** — Sovereign Music Label | `the_ledger.h` (JSON export) | 🔄 Quest 03 |

---

## Build the C++ Engine

**Prerequisites:** CMake ≥ 3.16, C++17 compiler (GCC/Clang/MSVC)

```bash
cd lilieth_riser/engine
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel

# Run tests
./build/lilieth_tests
```

Expected output:
```
═══════════════════════════════════════════
  LILIETH_RISER Engine Test Suite
  Kernel v1.0.47  |  G2G Sovereign Tests
═══════════════════════════════════════════

[AudioBuffer]
  [PASS] num_channels == 2
  ...

[WaveformRenderer]
  [PASS] render completes in < 0.5 ms (Quest 01)
    render_time_ms = 0.2134 ms
  ...

Results: 30 passed, 0 failed
═══════════════════════════════════════════
```

---

## Run the Flutter UI

```bash
cd lilieth_riser/flutter_ui
flutter pub get
flutter run
```

The UI targets Android, iOS, macOS, Windows, and Linux via Flutter.

---

## Start the Sync Server (Laptop / PROCESSOR)

```bash
pip install websockets
python3 lilieth_riser/sync/ws_server.py --host 0.0.0.0 --port 8765
```

From the Flutter UI, tap the **OFFLINE** dot in the top-right corner and enter
`ws://<laptop-ip>:8765` to pair Controller and Processor.

---

## Quests & Bounties

| Quest | Description | Status |
|:--|:--|:--|
| **Quest 01** | 0.5 ms waveform render | ✅ `WaveformRenderer` targets < 0.5 ms |
| **Quest 02** | Mirror Mode (HDMI/AirPlay) | 🔄 NDI/AirPlay integration pending |
| **Quest 03** | Sovereign Auto-Tag | 🔄 `TheLedger` JSON export is the foundation; REST integration pending |

---

## Technical Stack

| Component | Technology |
|:--|:--|
| Audio Engine | C++17, header-only, portable (no external deps) |
| UI | Flutter 3.x (iOS, Android, macOS, Windows, Linux) |
| Engine ↔ UI Bridge | `dart:ffi` → plain-C API |
| Multi-device Sync | WebSocket + JSON |
| Projection (planned) | NDI / WebRTC |
| AI Co-Pilot | GitHub Copilot (DSP filters) |

---

## Licensing

This module is part of the **CassAI / Alpha-Omega-Ete** ecosystem.  
See `LICENSE.md` and `LSPL.md` at the repository root for terms.  
All audio content processed by LILIETH_RISER remains the 100% sovereign property
of the originating artist. The Ledger provides an immutable audit trail.

---

*INITIALIZING… KERNEL ONLINE. SOVEREIGN NODE ACTIVE.*
