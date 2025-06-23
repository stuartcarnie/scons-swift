# SCons Swift Tool

A comprehensive SCons tool for building Swift projects with support for modern Swift features, cross-platform builds, and dependency management.

## Installation

Copy the `sconscontrib` directory to your project or SCons tool path.

## Usage

Look at the SConstruct file in the root.

## Examples

The `examples/` directory contains five demonstrations of Swift and C++ interoperability:

### 1. **SwiftLibrary** - Building a Swift static library
Creates a Swift library with multiple source files that can be called from C++. Demonstrates:
- Building Swift modules with C++ interoperability enabled
- Generating C++ headers from Swift code
- Creating static libraries from Swift object files

### 2. **cpp_calls_swift** - C++ application using Swift code
Shows how to write a C++ program that calls Swift functions and uses Swift types:
- Linking against Swift libraries
- Using generated Swift-to-C++ headers
- Calling Swift structs and functions from C++

### 3. **cpp_library** - C++ library for Swift consumption
Demonstrates creating a C++ library designed to be called from Swift:
- Comprehensive C++ API with classes, namespaces, and templates
- Module map creation for Swift import
- Proper header design for Swift interoperability

### 4. **swift_calls_cpp** - Swift application using C++ code
Shows how to write a Swift program that uses C++ libraries:
- Importing C++ modules in Swift
- Using C++ classes and functions from Swift
- Handling data type conversions between languages

### 5. **swift_calls_swift** - Swift application using Swift library
The simplest case of Swift-to-Swift linking:
- Linking Swift programs against Swift static libraries
- Module imports between Swift components

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
