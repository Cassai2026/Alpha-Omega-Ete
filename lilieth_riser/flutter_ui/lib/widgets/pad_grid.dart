// LILIETH_RISER — Touch-Sensitive Pad Grid
// Sovereign Sampling Engine | Kernel v1.0.47
//
// 4×4 grid of "Apple pads" — each pad maps to a loaded sample slice.
// Touch velocity is captured and passed to the engine for dynamic gain.

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../screens/sampler_screen.dart';

// ─────────────────────────────────────────────────────────────────────────────
// PadGrid
// ─────────────────────────────────────────────────────────────────────────────

class PadGrid extends StatelessWidget {
  static const int kRows = 4;
  static const int kCols = 4;

  const PadGrid({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<SamplerState>();

    return GridView.builder(
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: kCols,
        crossAxisSpacing: 6,
        mainAxisSpacing: 6,
      ),
      itemCount: kRows * kCols,
      itemBuilder: (context, index) {
        final hasApple = index < state.apples.length;
        final apple    = hasApple ? state.apples[index] : null;
        final isActive = state.activeApple == index;

        return _Pad(
          index:    index,
          apple:    apple,
          isActive: isActive,
          onTap: () {
            state.setActiveApple(index);
            if (hasApple) {
              // TODO: trigger sample playback via EngineBridge.play(index)
            }
          },
          onLongPress: () {
            if (hasApple) {
              state.removeApple(index);
            }
          },
        );
      },
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// _Pad
// ─────────────────────────────────────────────────────────────────────────────

class _Pad extends StatefulWidget {
  final int    index;
  final Apple? apple;
  final bool   isActive;
  final VoidCallback onTap;
  final VoidCallback onLongPress;

  const _Pad({
    required this.index,
    required this.apple,
    required this.isActive,
    required this.onTap,
    required this.onLongPress,
  });

  @override
  State<_Pad> createState() => _PadState();
}

class _PadState extends State<_Pad> with SingleTickerProviderStateMixin {
  late AnimationController _anim;
  late Animation<double>   _glow;

  @override
  void initState() {
    super.initState();
    _anim = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 120),
    );
    _glow = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _anim, curve: Curves.easeOut));
  }

  @override
  void dispose() {
    _anim.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails _) => _anim.forward();
  void _onTapUp(TapUpDetails _) {
    _anim.reverse();
    widget.onTap();
  }
  void _onTapCancel() => _anim.reverse();

  // Pad colours cycle through a sovereign palette
  static const List<Color> _baseColors = [
    Color(0xFF0D1B2A), Color(0xFF1A0D2A), Color(0xFF0D2A1A),
    Color(0xFF2A1A0D), Color(0xFF0D1B2A), Color(0xFF1A2A0D),
    Color(0xFF2A0D1A), Color(0xFF0D2A2A), Color(0xFF1A1A2A),
    Color(0xFF2A2A0D), Color(0xFF0D2A0D), Color(0xFF2A0D2A),
    Color(0xFF0D1B2A), Color(0xFF1A0D2A), Color(0xFF0D2A1A),
    Color(0xFF2A1A0D),
  ];

  static const List<Color> _activeColors = [
    Color(0xFF3D9BFF), Color(0xFF9B3DFF), Color(0xFF3DFF9B),
    Color(0xFFFF9B3D), Color(0xFF3D9BFF), Color(0xFF9BFF3D),
    Color(0xFFFF3D9B), Color(0xFF3DFFFF), Color(0xFF9B9BFF),
    Color(0xFFFFFF3D), Color(0xFF3DFF3D), Color(0xFFFF3DFF),
    Color(0xFF3D9BFF), Color(0xFF9B3DFF), Color(0xFF3DFF9B),
    Color(0xFFFF9B3D),
  ];

  @override
  Widget build(BuildContext context) {
    final hasApple = widget.apple != null;
    final base     = _baseColors[widget.index % _baseColors.length];
    final accent   = _activeColors[widget.index % _activeColors.length];

    return GestureDetector(
      onTapDown:   _onTapDown,
      onTapUp:     _onTapUp,
      onTapCancel: _onTapCancel,
      onLongPress: widget.onLongPress,
      child: AnimatedBuilder(
        animation: _glow,
        builder: (context, child) {
          return Container(
            decoration: BoxDecoration(
              color: widget.isActive
                  ? accent.withValues(alpha: 0.35)
                  : base,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(
                color: hasApple
                    ? accent.withValues(alpha: 0.6 + _glow.value * 0.4)
                    : const Color(0xFF222222),
                width: widget.isActive ? 1.5 : 1.0,
              ),
              boxShadow: (hasApple && (_glow.value > 0.1 || widget.isActive))
                  ? [
                      BoxShadow(
                        color: accent.withValues(alpha: _glow.value * 0.6),
                        blurRadius: 12,
                        spreadRadius: 2,
                      )
                    ]
                  : null,
            ),
            child: child,
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(6.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Pad index
              Text(
                '${widget.index + 1 < 10 ? '0' : ''}${widget.index + 1}',
                style: const TextStyle(
                    color: Color(0xFF555555), fontSize: 8, letterSpacing: 1),
              ),
              const Spacer(),
              if (hasApple) ...[
                Text(
                  widget.apple!.label,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                      color: Colors.white, fontSize: 9, letterSpacing: 0.5),
                ),
                Text(
                  '${widget.apple!.durationMs.toStringAsFixed(0)} ms',
                  style: const TextStyle(
                      color: Color(0xFF888888), fontSize: 8),
                ),
              ] else ...[
                const Text(
                  'EMPTY',
                  style: TextStyle(
                      color: Color(0xFF2A2A2A),
                      fontSize: 8,
                      letterSpacing: 1.5),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
