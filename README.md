# SCons Swift Tool

A comprehensive SCons tool for building Swift projects with support for modern Swift features, cross-platform builds, and dependency management.

## Installation

Copy the `sconscontrib` directory to your project or SCons tool path.

## Usage

In your SConstruct file:

```python
env = Environment(
    toolpath=['path/to/sconscontrib/SCons/Tool/swift'],
    tools=['swift']
)

# Build object files
env.Object('file.swift')

# Build a program
env.SwiftProgram('myapp', ['main.swift', 'utils.swift'])

# Build a library
env.SwiftLibrary('mylib', ['lib.swift'])

# Build a module
env.SwiftModule('MyModule', ['module.swift'], SWIFTMODULENAME='MyModule')
```

## Features

### Core Features
- Swift object file compilation (static and shared)
- Swift executable building
- Swift library building
- Swift module building
- Automatic dependency scanning for Swift imports
- C++ interoperability support
- Whole Module Optimization support

### Platform Support
- macOS/iOS (Darwin)
- Linux
- Windows (with Swift for Windows)

### Build Configuration
- Debug/Release build modes
- Module search path configuration
- Custom import handling
- Version-specific feature detection

### Advanced Features
- Swift Package Manager integration
- Async/await support detection
- Regex support detection (Swift 5.7+)
- Proper error handling with timeouts

## Configuration Variables

### Basic Variables
- `SWIFT` - Swift compiler command (default: auto-detected)
- `SWIFTFLAGS` - General Swift compiler flags
- `SWIFTPATH` - Include paths for Swift compilation

### Module Support
- `SWIFTMODULEPATH` - Module search paths
- `SWIFTMODULENAME` - Name for module generation
- `SWIFTIMPORTS` - Objective-C headers to import

### Debug/Release
- `DEBUG` - Set to True for debug builds
- `SWIFTDEBUGFLAGS` - Debug-specific flags (default: `-g -Onone`)
- `SWIFTRELEASEFLAGS` - Release-specific flags (default: `-O`)
- `SWIFTWMO` - Enable Whole Module Optimization

### C++ Interop
- `SWIFT_CXX_INTEROP` - Enable C++ interoperability
- `SWIFT_EMIT_CXX_HEADER` - Generate C++ header
- `SWIFT_CXX_HEADER_NAME` - Name for generated C++ header

### Platform-Specific
- `SDKROOT` - SDK path (auto-detected on macOS)
- `SWIFTSHLIBSUFFIX` - Shared library suffix (platform-specific)

## Example: Debug/Release Builds

```python
# Configure based on command-line argument
debug = ARGUMENTS.get('debug', 0)
if int(debug):
    env['DEBUG'] = True
else:
    env['DEBUG'] = False
    env['SWIFTWMO'] = True  # Enable WMO for release builds

# Build program
env.SwiftProgram('myapp', ['main.swift'])
```

Build commands:
```bash
scons          # Release build
scons debug=1  # Debug build
```

## Example: Module Dependencies

```python
# Add module search paths
env.AppendUnique(SWIFTMODULEPATH=['modules', 'third_party/modules'])

# Build a module
mymodule = env.SwiftModule('MyModule', ['MyModule.swift'], 
                          SWIFTMODULENAME='MyModule')

# Build a program that imports the module
# (dependency will be automatically detected)
program = env.SwiftProgram('app', ['main.swift'])
```

## Swift Package Manager Integration

If Swift Package Manager is available:

```python
if env.get('SWIFTPM'):
    spm_build = env.Command('spm_build', [], '$SWIFTPMBUILDCOM')
    spm_test = env.Command('spm_test', [], '$SWIFTPMTESTCOM')
    env.Alias('spm', spm_build)
    env.Alias('test', spm_test)
```

## Requirements

- Swift compiler (swiftc) 5.0 or later
- SCons 4.0 or later
- Platform-specific requirements:
  - macOS: Xcode Command Line Tools
  - Linux: Swift toolchain and dependencies
  - Windows: Swift for Windows

## License

MIT License
