// LILIETH_RISER — Main Sampler Screen ("The Black Canvas")
// Sovereign Sampling Engine | Kernel v1.0.47

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../widgets/waveform_display.dart';
import '../widgets/pad_grid.dart';
import '../services/websocket_service.dart';
import '../ffi/engine_bridge.dart';

// ─────────────────────────────────────────────────────────────────────────────
// SamplerState — shared app state
// ─────────────────────────────────────────────────────────────────────────────

enum DeviceRole { controller, processor }

class Apple {
  final String  label;
  final int     startFrame;
  final int     endFrame;
  final double  durationMs;
  bool          isPlaying;

  Apple({
    required this.label,
    required this.startFrame,
    required this.endFrame,
    required this.durationMs,
    this.isPlaying = false,
  });
}

class SamplerState extends ChangeNotifier {
  // Engine state
  List<Apple>  apples      = [];
  int          activeApple = -1;
  double       playPosition = 0.0;   // 0.0–1.0
  double       riserProgress = 0.0;  // 0.0–1.0
  bool         riserArmed  = false;

  // Riser parameters
  double riserStartSt  = -24.0;
  double riserEndSt    =  12.0;
  double riserDurationMs = 2000.0;

  // Device role
  DeviceRole role = DeviceRole.controller;

  // Waveform data (populated by EngineBridge after loading an Apple)
  List<double> waveformPeaksPos = [];
  List<double> waveformPeaksNeg = [];
  List<double> waveformRms      = [];

  // ── Actions ──────────────────────────────────────────────────────────────

  void setActiveApple(int index) {
    activeApple = index;
    notifyListeners();
  }

  void armRiser() {
    riserArmed = true;
    EngineBridge.riserArm(riserStartSt, riserEndSt, riserDurationMs);
    notifyListeners();
  }

  void stopRiser() {
    riserArmed = false;
    EngineBridge.riserStop();
    notifyListeners();
  }

  void updateRiserProgress(double v) {
    riserProgress = v;
    notifyListeners();
  }

  void setRole(DeviceRole r) {
    role = r;
    notifyListeners();
  }

  void addApple(Apple a) {
    apples.add(a);
    notifyListeners();
  }

  void removeApple(int index) {
    if (index >= 0 && index < apples.length) {
      apples.removeAt(index);
      notifyListeners();
    }
  }

  void updateWaveform(List<double> pos, List<double> neg, List<double> rms) {
    waveformPeaksPos = pos;
    waveformPeaksNeg = neg;
    waveformRms      = rms;
    notifyListeners();
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// SamplerScreen
// ─────────────────────────────────────────────────────────────────────────────

class SamplerScreen extends StatelessWidget {
  const SamplerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Column(
          children: [
            // ── Top bar ──────────────────────────────────────────────────
            _TopBar(),

            // ── Waveform display ("The Blade" canvas) ───────────────────
            Expanded(
              flex: 5,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
                child: WaveformDisplay(),
              ),
            ),

            // ── Riser controls ──────────────────────────────────────────
            _RiserControls(),

            // ── Pad grid ────────────────────────────────────────────────
            Expanded(
              flex: 3,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: PadGrid(),
              ),
            ),

            // ── Status bar ──────────────────────────────────────────────
            _StatusBar(),
          ],
        ),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// _TopBar
// ─────────────────────────────────────────────────────────────────────────────

class _TopBar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final state = context.watch<SamplerState>();
    final ws    = context.watch<WebSocketService>();

    return Container(
      height: 44,
      color: const Color(0xFF0A0A0A),
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        children: [
          // Logo / kernel ID
          const Text(
            'LILIETH_RISER',
            style: TextStyle(
              color:      Color(0xFFE8C44A),
              fontSize:   14,
              fontWeight: FontWeight.bold,
              letterSpacing: 2.0,
            ),
          ),

          const Spacer(),

          // Device role toggle
          _RoleToggle(state: state),

          const SizedBox(width: 16),

          // WebSocket connection indicator
          _ConnectionDot(connected: ws.isConnected),
        ],
      ),
    );
  }
}

class _RoleToggle extends StatelessWidget {
  final SamplerState state;
  const _RoleToggle({required this.state});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => state.setRole(
          state.role == DeviceRole.controller
              ? DeviceRole.processor
              : DeviceRole.controller),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
        decoration: BoxDecoration(
          border: Border.all(color: const Color(0xFFE8C44A), width: 1),
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(
          state.role == DeviceRole.controller ? 'CONTROLLER' : 'PROCESSOR',
          style: const TextStyle(
            color: Color(0xFFE8C44A), fontSize: 10, letterSpacing: 1.5,
          ),
        ),
      ),
    );
  }
}

class _ConnectionDot extends StatelessWidget {
  final bool connected;
  const _ConnectionDot({required this.connected});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 8, height: 8,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: connected ? const Color(0xFF44FF88) : const Color(0xFF444444),
          ),
        ),
        const SizedBox(width: 6),
        Text(
          connected ? 'SYNCED' : 'OFFLINE',
          style: TextStyle(
            color: connected ? const Color(0xFF44FF88) : const Color(0xFF666666),
            fontSize: 10,
            letterSpacing: 1.2,
          ),
        ),
      ],
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// _RiserControls
// ─────────────────────────────────────────────────────────────────────────────

class _RiserControls extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final state = context.watch<SamplerState>();

    return Container(
      height: 56,
      color: const Color(0xFF080808),
      padding: const EdgeInsets.symmetric(horizontal: 12),
      child: Row(
        children: [
          // Label
          const Text(
            'THE RISE',
            style: TextStyle(
              color: Color(0xFF3D9BFF), fontSize: 10, letterSpacing: 2.5,
            ),
          ),
          const SizedBox(width: 16),

          // Start semitone
          _ParamKnob(
            label: 'START',
            value: state.riserStartSt,
            min: -48.0, max: 0.0,
            onChanged: (v) {
              state.riserStartSt = v;
              state.notifyListeners();
            },
          ),
          const SizedBox(width: 12),

          // End semitone
          _ParamKnob(
            label: 'END',
            value: state.riserEndSt,
            min: 0.0, max: 48.0,
            onChanged: (v) {
              state.riserEndSt = v;
              state.notifyListeners();
            },
          ),
          const SizedBox(width: 12),

          // Duration
          _ParamKnob(
            label: 'DUR ms',
            value: state.riserDurationMs,
            min: 250.0, max: 8000.0,
            onChanged: (v) {
              state.riserDurationMs = v;
              state.notifyListeners();
            },
          ),

          const Spacer(),

          // Progress bar
          if (state.riserArmed)
            SizedBox(
              width: 120,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('RISER',
                      style: TextStyle(color: Color(0xFF3D9BFF),
                          fontSize: 8, letterSpacing: 1.5)),
                  const SizedBox(height: 4),
                  LinearProgressIndicator(
                    value: state.riserProgress,
                    backgroundColor: const Color(0xFF1A1A2E),
                    color: const Color(0xFF3D9BFF),
                    minHeight: 3,
                  ),
                ],
              ),
            ),

          const SizedBox(width: 12),

          // ARM button
          GestureDetector(
            onTapDown: (_) => state.armRiser(),
            onTapUp:   (_) => state.stopRiser(),
            onTapCancel: ()  => state.stopRiser(),
            child: Container(
              width: 60, height: 36,
              decoration: BoxDecoration(
                color: state.riserArmed
                    ? const Color(0xFF3D9BFF)
                    : const Color(0xFF1A1A2E),
                borderRadius: BorderRadius.circular(4),
                border: Border.all(color: const Color(0xFF3D9BFF)),
              ),
              alignment: Alignment.center,
              child: Text(
                state.riserArmed ? 'RISING' : 'ARM',
                style: const TextStyle(
                  color: Colors.white, fontSize: 10, letterSpacing: 1.5,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ParamKnob extends StatelessWidget {
  final String  label;
  final double  value;
  final double  min;
  final double  max;
  final ValueChanged<double> onChanged;

  const _ParamKnob({
    required this.label,
    required this.value,
    required this.min,
    required this.max,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(label,
            style: const TextStyle(color: Color(0xFF666666),
                fontSize: 8, letterSpacing: 1.2)),
        const SizedBox(height: 2),
        SizedBox(
          width: 80,
          child: SliderTheme(
            data: SliderThemeData(
              trackHeight: 2,
              thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 5),
              overlayShape: SliderComponentShape.noOverlay,
              activeTrackColor: const Color(0xFFE8C44A),
              inactiveTrackColor: const Color(0xFF333333),
              thumbColor: const Color(0xFFE8C44A),
            ),
            child: Slider(
              value: value.clamp(min, max),
              min: min, max: max,
              onChanged: onChanged,
            ),
          ),
        ),
        Text('${value.toStringAsFixed(1)}',
            style: const TextStyle(color: Color(0xFFE8C44A),
                fontSize: 9, letterSpacing: 0.5)),
      ],
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// _StatusBar
// ─────────────────────────────────────────────────────────────────────────────

class _StatusBar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final state = context.watch<SamplerState>();
    return Container(
      height: 24,
      color: const Color(0xFF050505),
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        children: [
          Text(
            'APPLES: ${state.apples.length}',
            style: const TextStyle(color: Color(0xFF444444),
                fontSize: 9, letterSpacing: 1.5),
          ),
          const Spacer(),
          const Text(
            'KERNEL v1.0.47 · SOVEREIGN',
            style: TextStyle(color: Color(0xFF333333),
                fontSize: 9, letterSpacing: 1.5),
          ),
        ],
      ),
    );
  }
}
