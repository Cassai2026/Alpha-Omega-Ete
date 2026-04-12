// LILIETH_RISER — C++ Engine FFI Bridge (Dart side)
// Sovereign Sampling Engine | Kernel v1.0.47
//
// Loads the native shared library produced by CMakeLists.txt and exposes
// a type-safe Dart API for the sampler UI.
//
// dart:ffi docs: https://dart.dev/guides/libraries/c-interop

import 'dart:ffi' as ffi;
import 'dart:io' show Platform;
import 'package:ffi/ffi.dart';

// ─────────────────────────────────────────────────────────────────────────────
// Native type definitions  (must match ffi_bridge.cpp exactly)
// ─────────────────────────────────────────────────────────────────────────────

// Opaque handle structs
final class _LRRiser  extends ffi.Opaque {}
final class _LRBuffer extends ffi.Opaque {}
final class _LRLedger extends ffi.Opaque {}

// --- AudioBuffer ---
typedef _lr_buffer_create_native = ffi.Pointer<_LRBuffer> Function(
    ffi.Uint32, ffi.Uint32);
typedef _lr_buffer_create_dart = ffi.Pointer<_LRBuffer> Function(int, int);

typedef _lr_buffer_destroy_native = ffi.Void Function(ffi.Pointer<_LRBuffer>);
typedef _lr_buffer_destroy_dart   = void Function(ffi.Pointer<_LRBuffer>);

typedef _lr_buffer_clear_native = ffi.Void Function(ffi.Pointer<_LRBuffer>);
typedef _lr_buffer_clear_dart   = void Function(ffi.Pointer<_LRBuffer>);

typedef _lr_buffer_write_channel_native = ffi.Void Function(
    ffi.Pointer<_LRBuffer>, ffi.Uint32, ffi.Pointer<ffi.Float>, ffi.Uint32);
typedef _lr_buffer_write_channel_dart = void Function(
    ffi.Pointer<_LRBuffer>, int, ffi.Pointer<ffi.Float>, int);

typedef _lr_buffer_read_channel_native = ffi.Void Function(
    ffi.Pointer<_LRBuffer>, ffi.Uint32, ffi.Pointer<ffi.Float>, ffi.Uint32);
typedef _lr_buffer_read_channel_dart = void Function(
    ffi.Pointer<_LRBuffer>, int, ffi.Pointer<ffi.Float>, int);

// --- Riser ---
typedef _lr_riser_create_native = ffi.Pointer<_LRRiser> Function(
    ffi.Uint32, ffi.Uint32, ffi.Uint32);
typedef _lr_riser_create_dart = ffi.Pointer<_LRRiser> Function(int, int, int);

typedef _lr_riser_destroy_native = ffi.Void Function(ffi.Pointer<_LRRiser>);
typedef _lr_riser_destroy_dart   = void Function(ffi.Pointer<_LRRiser>);

typedef _lr_riser_arm_native = ffi.Void Function(
    ffi.Pointer<_LRRiser>, ffi.Float, ffi.Float, ffi.Float);
typedef _lr_riser_arm_dart = void Function(
    ffi.Pointer<_LRRiser>, double, double, double);

typedef _lr_riser_stop_native = ffi.Void Function(ffi.Pointer<_LRRiser>);
typedef _lr_riser_stop_dart   = void Function(ffi.Pointer<_LRRiser>);

typedef _lr_riser_is_running_native = ffi.Int32 Function(ffi.Pointer<_LRRiser>);
typedef _lr_riser_is_running_dart   = int Function(ffi.Pointer<_LRRiser>);

typedef _lr_riser_progress_native = ffi.Float Function(ffi.Pointer<_LRRiser>);
typedef _lr_riser_progress_dart   = double Function(ffi.Pointer<_LRRiser>);

typedef _lr_riser_process_block_native = ffi.Uint32 Function(
    ffi.Pointer<_LRRiser>,
    ffi.Pointer<ffi.Float>, ffi.Uint32,
    ffi.Pointer<ffi.Float>);
typedef _lr_riser_process_block_dart = int Function(
    ffi.Pointer<_LRRiser>,
    ffi.Pointer<ffi.Float>, int,
    ffi.Pointer<ffi.Float>);

// --- WaveformRenderer ---
typedef _lr_render_waveform_native = ffi.Double Function(
    ffi.Pointer<_LRBuffer>, ffi.Uint32, ffi.Uint32, ffi.Uint32, ffi.Uint32,
    ffi.Pointer<ffi.Float>, ffi.Pointer<ffi.Float>, ffi.Pointer<ffi.Float>);
typedef _lr_render_waveform_dart = double Function(
    ffi.Pointer<_LRBuffer>, int, int, int, int,
    ffi.Pointer<ffi.Float>, ffi.Pointer<ffi.Float>, ffi.Pointer<ffi.Float>);

// --- Ledger ---
typedef _lr_ledger_create_native = ffi.Pointer<_LRLedger> Function(
    ffi.Pointer<Utf8>, ffi.Pointer<Utf8>);
typedef _lr_ledger_create_dart = ffi.Pointer<_LRLedger> Function(
    ffi.Pointer<Utf8>, ffi.Pointer<Utf8>);

typedef _lr_ledger_destroy_native = ffi.Void Function(ffi.Pointer<_LRLedger>);
typedef _lr_ledger_destroy_dart   = void Function(ffi.Pointer<_LRLedger>);

typedef _lr_ledger_log_use_native = ffi.Void Function(
    ffi.Pointer<_LRLedger>, ffi.Pointer<_LRBuffer>,
    ffi.Uint32, ffi.Pointer<Utf8>, ffi.Float, ffi.Float);
typedef _lr_ledger_log_use_dart = void Function(
    ffi.Pointer<_LRLedger>, ffi.Pointer<_LRBuffer>,
    int, ffi.Pointer<Utf8>, double, double);

typedef _lr_ledger_entry_count_native = ffi.Uint32 Function(ffi.Pointer<_LRLedger>);
typedef _lr_ledger_entry_count_dart   = int Function(ffi.Pointer<_LRLedger>);

typedef _lr_ledger_export_json_native = ffi.Uint32 Function(
    ffi.Pointer<_LRLedger>, ffi.Pointer<Utf8>, ffi.Uint32);
typedef _lr_ledger_export_json_dart = int Function(
    ffi.Pointer<_LRLedger>, ffi.Pointer<Utf8>, int);

// ─────────────────────────────────────────────────────────────────────────────
// EngineBridge — singleton
// ─────────────────────────────────────────────────────────────────────────────

class EngineBridge {
  static late ffi.DynamicLibrary _lib;

  // Function pointers
  static late _lr_buffer_create_dart          _bufCreate;
  static late _lr_buffer_destroy_dart         _bufDestroy;
  static late _lr_buffer_clear_dart           _bufClear;
  static late _lr_buffer_write_channel_dart   _bufWrite;
  static late _lr_buffer_read_channel_dart    _bufRead;
  static late _lr_riser_create_dart           _riserCreate;
  static late _lr_riser_destroy_dart          _riserDestroy;
  static late _lr_riser_arm_dart              _riserArm;
  static late _lr_riser_stop_dart             _riserStop;
  static late _lr_riser_is_running_dart       _riserIsRunning;
  static late _lr_riser_progress_dart         _riserProgress;
  static late _lr_riser_process_block_dart    _riserProcessBlock;
  static late _lr_render_waveform_dart        _renderWaveform;
  static late _lr_ledger_create_dart          _ledgerCreate;
  static late _lr_ledger_destroy_dart         _ledgerDestroy;
  static late _lr_ledger_log_use_dart         _ledgerLogUse;
  static late _lr_ledger_entry_count_dart     _ledgerEntryCount;
  static late _lr_ledger_export_json_dart     _ledgerExportJson;

  // Native handles
  static ffi.Pointer<_LRRiser>?  _riser;
  static ffi.Pointer<_LRLedger>? _ledger;

  // ── Initialisation ────────────────────────────────────────────────────

  static void init({
    String  artist  = 'Sovereign',
    String  project = 'Untitled',
    int     sampleRate = 48000,
    int     fftSize    = 1024,
    int     overlap    = 4,
  }) {
    _lib = _loadLibrary();

    _bufCreate      = _lib.lookupFunction<_lr_buffer_create_native,    _lr_buffer_create_dart>   ('lr_buffer_create');
    _bufDestroy     = _lib.lookupFunction<_lr_buffer_destroy_native,   _lr_buffer_destroy_dart>  ('lr_buffer_destroy');
    _bufClear       = _lib.lookupFunction<_lr_buffer_clear_native,     _lr_buffer_clear_dart>    ('lr_buffer_clear');
    _bufWrite       = _lib.lookupFunction<_lr_buffer_write_channel_native, _lr_buffer_write_channel_dart>('lr_buffer_write_channel');
    _bufRead        = _lib.lookupFunction<_lr_buffer_read_channel_native,  _lr_buffer_read_channel_dart> ('lr_buffer_read_channel');
    _riserCreate    = _lib.lookupFunction<_lr_riser_create_native,     _lr_riser_create_dart>    ('lr_riser_create');
    _riserDestroy   = _lib.lookupFunction<_lr_riser_destroy_native,    _lr_riser_destroy_dart>   ('lr_riser_destroy');
    _riserArm       = _lib.lookupFunction<_lr_riser_arm_native,        _lr_riser_arm_dart>       ('lr_riser_arm');
    _riserStop      = _lib.lookupFunction<_lr_riser_stop_native,       _lr_riser_stop_dart>      ('lr_riser_stop');
    _riserIsRunning = _lib.lookupFunction<_lr_riser_is_running_native, _lr_riser_is_running_dart>('lr_riser_is_running');
    _riserProgress  = _lib.lookupFunction<_lr_riser_progress_native,   _lr_riser_progress_dart>  ('lr_riser_progress');
    _riserProcessBlock = _lib.lookupFunction<_lr_riser_process_block_native, _lr_riser_process_block_dart>('lr_riser_process_block');
    _renderWaveform = _lib.lookupFunction<_lr_render_waveform_native,  _lr_render_waveform_dart> ('lr_render_waveform');
    _ledgerCreate   = _lib.lookupFunction<_lr_ledger_create_native,    _lr_ledger_create_dart>   ('lr_ledger_create');
    _ledgerDestroy  = _lib.lookupFunction<_lr_ledger_destroy_native,   _lr_ledger_destroy_dart>  ('lr_ledger_destroy');
    _ledgerLogUse   = _lib.lookupFunction<_lr_ledger_log_use_native,   _lr_ledger_log_use_dart>  ('lr_ledger_log_use');
    _ledgerEntryCount = _lib.lookupFunction<_lr_ledger_entry_count_native, _lr_ledger_entry_count_dart>('lr_ledger_entry_count');
    _ledgerExportJson = _lib.lookupFunction<_lr_ledger_export_json_native, _lr_ledger_export_json_dart>('lr_ledger_export_json');

    // Create engine instances
    _riser = _riserCreate(sampleRate, fftSize, overlap);

    final artistPtr  = artist.toNativeUtf8();
    final projectPtr = project.toNativeUtf8();
    _ledger = _ledgerCreate(artistPtr, projectPtr);
    calloc.free(artistPtr);
    calloc.free(projectPtr);
  }

  // ── Riser API ─────────────────────────────────────────────────────────

  static void riserArm(double startSt, double endSt, double durationMs) {
    if (_riser == null) return;
    _riserArm(_riser!, startSt, endSt, durationMs);
  }

  static void riserStop() {
    if (_riser == null) return;
    _riserStop(_riser!);
  }

  static bool riserIsRunning() =>
      _riser != null && _riserIsRunning(_riser!) != 0;

  static double riserProgress() =>
      _riser != null ? _riserProgress(_riser!) : 0.0;

  // ── Waveform API ──────────────────────────────────────────────────────

  /// Render the waveform of a buffer and return [peaksPos, peaksNeg, rms].
  static ({
    List<double> peaksPos,
    List<double> peaksNeg,
    List<double> rms,
    double renderMs,
  }) renderWaveform(
    ffi.Pointer<_LRBuffer> bufHandle, {
    int channel    = 0,
    int widthPx    = 1280,
    int startFrame = 0,
    int endFrame   = 0,
  }) {
    final pp  = calloc<ffi.Float>(widthPx);
    final pn  = calloc<ffi.Float>(widthPx);
    final rms = calloc<ffi.Float>(widthPx);

    final ms = _renderWaveform(
        bufHandle, channel, widthPx, startFrame, endFrame, pp, pn, rms);

    final posL  = List<double>.generate(widthPx, (i) => pp[i].toDouble());
    final negL  = List<double>.generate(widthPx, (i) => pn[i].toDouble());
    final rmsL  = List<double>.generate(widthPx, (i) => rms[i].toDouble());

    calloc.free(pp);
    calloc.free(pn);
    calloc.free(rms);

    return (peaksPos: posL, peaksNeg: negL, rms: rmsL, renderMs: ms);
  }

  // ── Ledger API ────────────────────────────────────────────────────────

  static int ledgerEntryCount() =>
      _ledger != null ? _ledgerEntryCount(_ledger!) : 0;

  static String ledgerExportJson() {
    if (_ledger == null) return '{}';
    final needed = _ledgerExportJson(_ledger!, nullptr.cast<Utf8>(), 0);
    final buf    = calloc<Utf8>(needed + 1);
    _ledgerExportJson(_ledger!, buf, needed + 1);
    final result = buf.toDartString();
    calloc.free(buf);
    return result;
  }

  // ── Private ───────────────────────────────────────────────────────────

  static ffi.DynamicLibrary _loadLibrary() {
    if (Platform.isAndroid)       return ffi.DynamicLibrary.open('liblilieth_ffi.so');
    if (Platform.isIOS)           return ffi.DynamicLibrary.process();
    if (Platform.isMacOS)         return ffi.DynamicLibrary.open('liblilieth_ffi.dylib');
    if (Platform.isWindows)       return ffi.DynamicLibrary.open('lilieth_ffi.dll');
    if (Platform.isLinux)         return ffi.DynamicLibrary.open('liblilieth_ffi.so');
    throw UnsupportedError('Unsupported platform: ${Platform.operatingSystem}');
  }
}
