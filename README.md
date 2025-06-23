# SCons Swift Tool

A comprehensive SCons tool for building Swift projects with support for modern Swift features, cross-platform builds, and dependency management.

## Installation

Copy the `sconscontrib` directory to your project or SCons tool path.

## Usage

Look at the SConstruct file in the root.

## Features

### Core Features
- Swift module
- C++ interoperability support

### Platform Support
- macOS/iOS (Darwin)

## Configuration Variables

### Basic Variables
- `SWIFT` - Swift compiler command (default: auto-detected)
- `SWIFTFLAGS` - General Swift compiler flags
- `SWIFTPATH` - Include paths for Swift compilation

### C++ Interop
- `SWIFT_CXX_INTEROP` - Enable C++ interoperability
- `SWIFT_EMIT_CXX_HEADER` - Generate C++ header
- `SWIFT_CXX_HEADER_NAME` - Name for generated C++ header

### Platform-Specific
- `SDKROOT` - SDK path (auto-detected on macOS)

## Requirements

- Swift compiler (swiftc) 5.0 or later
- SCons 4.0 or later
- Platform-specific requirements:
  - macOS: Xcode Command Line Tools

## License

MIT License
