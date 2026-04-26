cmake_minimum_required(VERSION 3.16)
project(lilieth_riser_engine VERSION 1.0.47 LANGUAGES CXX)

# ──────────────────────────────────────────────────────────────────────────────
# Standard
# ──────────────────────────────────────────────────────────────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ──────────────────────────────────────────────────────────────────────────────
# Compiler flags
# ──────────────────────────────────────────────────────────────────────────────
if(MSVC)
    add_compile_options(/W4 /WX /O2)
else()
    add_compile_options(
        -Wall -Wextra -Wpedantic
        -O3                    # Full optimisation (latency-critical engine)
        -ffast-math            # Allow re-ordering for SIMD-friendly code
        -march=native          # Enable all CPU extensions on the build host
    )
endif()

# ──────────────────────────────────────────────────────────────────────────────
# Header-only engine library
#
# All engine modules are header-only (template + inline implementations).
# The "lilieth_engine" target simply exposes the include directory so that
# the test executable and the FFI shared library can both link against it.
# ──────────────────────────────────────────────────────────────────────────────
add_library(lilieth_engine INTERFACE)
target_include_directories(lilieth_engine INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# ──────────────────────────────────────────────────────────────────────────────
# Shared library (FFI surface for Flutter)
#
# Exposes a plain-C API so that Flutter/Dart can call the engine via dart:ffi
# without name mangling.  The implementation is in src/ffi_bridge.cpp.
# ──────────────────────────────────────────────────────────────────────────────
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/ffi_bridge.cpp")
    add_library(lilieth_ffi SHARED
        src/ffi_bridge.cpp
    )
    target_link_libraries(lilieth_ffi PRIVATE lilieth_engine)

    # On macOS / iOS the Flutter engine expects the dylib to be named
    # "liblilieth_ffi.dylib" (the default for SHARED on Apple platforms).
    set_target_properties(lilieth_ffi PROPERTIES
        OUTPUT_NAME "lilieth_ffi"
    )
endif()

# ──────────────────────────────────────────────────────────────────────────────
# Test executable
# ──────────────────────────────────────────────────────────────────────────────
add_executable(lilieth_tests
    tests/test_engine.cpp
)
target_link_libraries(lilieth_tests PRIVATE lilieth_engine)

# CTest integration
enable_testing()
add_test(NAME LiliethEngineTests COMMAND lilieth_tests)

# ──────────────────────────────────────────────────────────────────────────────
# Optional: install targets
# ──────────────────────────────────────────────────────────────────────────────
install(DIRECTORY include/ DESTINATION include/lilieth_riser)
if(TARGET lilieth_ffi)
    install(TARGETS lilieth_ffi LIBRARY DESTINATION lib)
endif()
