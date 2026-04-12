// LILIETH_RISER — Main Entry Point
// "The Black Canvas"
// Sovereign Sampling Engine | Kernel v1.0.47

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import 'screens/sampler_screen.dart';
import 'services/websocket_service.dart';
import 'ffi/engine_bridge.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Lock to landscape for the sampler layout
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);

  // Full-screen immersive mode — "zero clutter"
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);

  // Initialise the native engine
  EngineBridge.init();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SamplerState()),
        ChangeNotifierProvider(create: (_) => WebSocketService()),
      ],
      child: const LiliethRiserApp(),
    ),
  );
}

class LiliethRiserApp extends StatelessWidget {
  const LiliethRiserApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LILIETH_RISER',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: const Color(0xFF000000), // Pure black canvas
        colorScheme: const ColorScheme.dark(
          primary:   Color(0xFFE8C44A),  // Sovereign gold
          secondary: Color(0xFF3D9BFF),  // Signal blue
          surface:   Color(0xFF0A0A0A),
          error:     Color(0xFFFF4444),
        ),
        fontFamily: 'Monospace',
        useMaterial3: false,
      ),
      home: const SamplerScreen(),
    );
  }
}
