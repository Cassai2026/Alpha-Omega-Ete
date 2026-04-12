// LILIETH_RISER — Waveform Display Widget ("The Blade" Canvas)
// Sovereign Sampling Engine | Kernel v1.0.47
//
// Renders peak + RMS data received from the C++ WaveformRenderer via FFI.
// Supports touch gestures for placing cut points (CutPoints → TheBlade).

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../screens/sampler_screen.dart';

// ─────────────────────────────────────────────────────────────────────────────
// WaveformDisplay
// ─────────────────────────────────────────────────────────────────────────────

class WaveformDisplay extends StatefulWidget {
  const WaveformDisplay({super.key});

  @override
  State<WaveformDisplay> createState() => _WaveformDisplayState();
}

class _WaveformDisplayState extends State<WaveformDisplay> {
  final List<double> _cutPositions = []; // Normalised 0.0–1.0
  double?            _playhead;          // Normalised 0.0–1.0

  // Touch: drag to set playhead; tap to add a cut
  void _onTap(TapUpDetails details, BoxConstraints constraints) {
    final norm = details.localPosition.dx / constraints.maxWidth;
    setState(() => _cutPositions.add(norm.clamp(0.0, 1.0)));
  }

  void _onDrag(DragUpdateDetails details, BoxConstraints constraints) {
    setState(() =>
        _playhead = (details.localPosition.dx / constraints.maxWidth)
            .clamp(0.0, 1.0));
  }

  @override
  Widget build(BuildContext context) {
    final state = context.watch<SamplerState>();

    return LayoutBuilder(
      builder: (context, constraints) {
        return GestureDetector(
          onTapUp: (d) => _onTap(d, constraints),
          onHorizontalDragUpdate: (d) => _onDrag(d, constraints),
          child: ClipRect(
            child: CustomPaint(
              size: Size(constraints.maxWidth, constraints.maxHeight),
              painter: _WaveformPainter(
                peaksPos:     state.waveformPeaksPos,
                peaksNeg:     state.waveformPeaksNeg,
                rms:          state.waveformRms,
                cutPositions: _cutPositions,
                playhead:     _playhead ?? state.playPosition,
              ),
            ),
          ),
        );
      },
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// _WaveformPainter
// ─────────────────────────────────────────────────────────────────────────────

class _WaveformPainter extends CustomPainter {
  final List<double> peaksPos;
  final List<double> peaksNeg;
  final List<double> rms;
  final List<double> cutPositions;
  final double       playhead;

  _WaveformPainter({
    required this.peaksPos,
    required this.peaksNeg,
    required this.rms,
    required this.cutPositions,
    required this.playhead,
  });

  static final Paint _rmsPaint = Paint()
    ..color = const Color(0xFF1A3A5E)
    ..strokeWidth = 1;

  static final Paint _peakPosPaint = Paint()
    ..color = const Color(0xFF3D9BFF)
    ..strokeWidth = 1;

  static final Paint _peakNegPaint = Paint()
    ..color = const Color(0xFF2D7ACC)
    ..strokeWidth = 1;

  static final Paint _cutPaint = Paint()
    ..color = const Color(0xFFE8C44A)
    ..strokeWidth = 1.5
    ..style = PaintingStyle.stroke;

  static final Paint _playheadPaint = Paint()
    ..color = const Color(0xFFFF4444)
    ..strokeWidth = 1.5;

  static final Paint _bgPaint = Paint()
    ..color = const Color(0xFF050810);

  @override
  void paint(Canvas canvas, Size size) {
    // Background
    canvas.drawRect(Offset.zero & size, _bgPaint);

    // Subtle centre line
    canvas.drawLine(
      Offset(0, size.height / 2),
      Offset(size.width, size.height / 2),
      Paint()..color = const Color(0xFF1A1A1A)..strokeWidth = 0.5,
    );

    if (peaksPos.isEmpty) {
      // Empty state: draw placeholder text
      const tp = TextPainter(
        text: TextSpan(
          text: 'LOAD AN APPLE',
          style: TextStyle(
            color: Color(0xFF333333), fontSize: 12, letterSpacing: 3.0,
          ),
        ),
        textDirection: TextDirection.ltr,
      );
      // ignore: cascade_invocations
      (tp..layout()).paint(canvas, Offset(
        (size.width  - tp.width)  / 2,
        (size.height - tp.height) / 2,
      ));
      return;
    }

    final int n    = peaksPos.length;
    final double w = size.width / n;
    final double cy = size.height / 2;

    for (int i = 0; i < n; ++i) {
      final double x = i * w;

      // RMS fill
      if (i < rms.length) {
        final double rh = rms[i] * cy;
        canvas.drawLine(Offset(x, cy - rh), Offset(x, cy + rh), _rmsPaint);
      }

      // Peak positive
      final double ph = peaksPos[i] * cy;
      canvas.drawLine(Offset(x, cy - ph), Offset(x, cy), _peakPosPaint);

      // Peak negative
      if (i < peaksNeg.length) {
        final double nh = peaksNeg[i] * cy;
        canvas.drawLine(Offset(x, cy), Offset(x, cy + nh), _peakNegPaint);
      }
    }

    // Cut points ("The Blade" marks)
    for (final pos in cutPositions) {
      final double x = pos * size.width;
      canvas.drawLine(
        Offset(x, 0), Offset(x, size.height), _cutPaint);
      // Diamond marker at top
      final Path diamond = Path()
        ..moveTo(x, 0)
        ..lineTo(x + 5, 8)
        ..lineTo(x, 16)
        ..lineTo(x - 5, 8)
        ..close();
      canvas.drawPath(
          diamond,
          Paint()
            ..color = const Color(0xFFE8C44A)
            ..style = PaintingStyle.fill);
    }

    // Playhead
    final double px = playhead * size.width;
    canvas.drawLine(Offset(px, 0), Offset(px, size.height), _playheadPaint);
  }

  @override
  bool shouldRepaint(_WaveformPainter old) =>
      old.peaksPos     != peaksPos     ||
      old.cutPositions != cutPositions ||
      old.playhead     != playhead;
}
