// LILIETH_RISER — WebSocket Sync Service
// Sovereign Sampling Engine | Kernel v1.0.47
//
// Master/Client architecture:
//   Phone  (CONTROLLER) — sends touch events, pad triggers, Riser commands
//   Laptop (PROCESSOR)  — receives commands, renders heavy audio, stores Ledger
//
// Protocol: newline-delimited JSON messages over ws://

import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

// ─────────────────────────────────────────────────────────────────────────────
// Message types
// ─────────────────────────────────────────────────────────────────────────────

enum MsgType {
  // Controller → Processor
  padTrigger,    // { type, pad_index, velocity }
  riserArm,      // { type, start_st, end_st, duration_ms }
  riserStop,     // { type }
  cut,           // { type, position }     (normalised 0.0–1.0)
  loadApple,     // { type, label, start_frame, end_frame, sr }

  // Processor → Controller
  waveformData,  // { type, peaks_pos: [], peaks_neg: [], rms: [] }
  riserProgress, // { type, progress }     (0.0–1.0)
  ledgerEntry,   // { type, entry: {...} }

  // Bidirectional
  ping,
  pong,
  error,
}

class LiliethMessage {
  final MsgType         type;
  final Map<String, dynamic> payload;

  const LiliethMessage(this.type, [this.payload = const {}]);

  Map<String, dynamic> toJson() => {'type': type.name, ...payload};

  static LiliethMessage fromJson(Map<String, dynamic> json) {
    final t = MsgType.values.firstWhere(
        (e) => e.name == json['type'],
        orElse: () => MsgType.error);
    return LiliethMessage(t, Map.from(json)..remove('type'));
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// WebSocketService
// ─────────────────────────────────────────────────────────────────────────────

class WebSocketService extends ChangeNotifier {
  WebSocketChannel? _channel;
  StreamSubscription? _sub;

  bool    _connected   = false;
  String? _peerAddress;

  bool    get isConnected  => _connected;
  String? get peerAddress  => _peerAddress;

  /// Message stream for widgets / state to listen to
  final _controller = StreamController<LiliethMessage>.broadcast();
  Stream<LiliethMessage> get messages => _controller.stream;

  // ── Connect ────────────────────────────────────────────────────────────

  Future<void> connect(String wsUrl) async {
    await disconnect();
    try {
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
      await _channel!.ready;
      _connected   = true;
      _peerAddress = wsUrl;
      notifyListeners();

      _sub = _channel!.stream.listen(
        _onData,
        onError:   _onError,
        onDone:    _onDone,
        cancelOnError: false,
      );

      send(const LiliethMessage(MsgType.ping));
    } catch (e) {
      _connected = false;
      notifyListeners();
      debugPrint('[WS] connect error: $e');
    }
  }

  Future<void> disconnect() async {
    await _sub?.cancel();
    await _channel?.sink.close();
    _channel   = null;
    _sub       = null;
    _connected = false;
    notifyListeners();
  }

  // ── Send ───────────────────────────────────────────────────────────────

  void send(LiliethMessage msg) {
    if (!_connected || _channel == null) return;
    try {
      _channel!.sink.add(jsonEncode(msg.toJson()));
    } catch (e) {
      debugPrint('[WS] send error: $e');
    }
  }

  void sendPadTrigger(int padIndex, double velocity) =>
      send(LiliethMessage(MsgType.padTrigger,
          {'pad_index': padIndex, 'velocity': velocity}));

  void sendRiserArm(double startSt, double endSt, double durationMs) =>
      send(LiliethMessage(MsgType.riserArm,
          {'start_st': startSt, 'end_st': endSt, 'duration_ms': durationMs}));

  void sendRiserStop() => send(const LiliethMessage(MsgType.riserStop));

  void sendCut(double position) =>
      send(LiliethMessage(MsgType.cut, {'position': position}));

  // ── Internals ──────────────────────────────────────────────────────────

  void _onData(dynamic raw) {
    try {
      final json = jsonDecode(raw as String) as Map<String, dynamic>;
      final msg  = LiliethMessage.fromJson(json);

      if (msg.type == MsgType.ping) {
        send(const LiliethMessage(MsgType.pong));
        return;
      }
      _controller.add(msg);
    } catch (e) {
      debugPrint('[WS] parse error: $e');
    }
  }

  void _onError(Object error) {
    debugPrint('[WS] error: $error');
    _connected = false;
    notifyListeners();
  }

  void _onDone() {
    _connected = false;
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    _controller.close();
    super.dispose();
  }
}
