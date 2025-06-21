# Swift Calls C++ Example

This example demonstrates a Swift program that calls C++ code using Swift's C++ interoperability features.

## Files

- **`SConstruct`**: Build configuration that creates module maps and enables C++ interop
- **`cpp_library.h`**: C++ header with classes, namespaces, and functions
- **`cpp_library.cpp`**: Implementation of the C++ library
- **`main.swift`**: Swift main program that uses the C++ library

## How It Works

### 1. Swift Import

Swift imports the C++ module directly:

```swift
import CppLibrary
```

### 2. C++ Usage from Swift

Swift can use C++ classes, namespaces, and functions directly:

```swift
// Use C++ namespace functions
let sum = MathUtils.add(15.5, 24.3)

// Create and use C++ objects
let vector = Vector3D(1.0, 2.0, 3.0)
let magnitude = vector.magnitude()

// Use STL containers
var cppVector = std.vector<Double>()
cppVector.push_back(5.5)
```

## Building

```bash
scons
```

This will:
1. Compile C++ source files
2. Compile Swift code with C++ interop enabled
3. Link everything into an executable

## Running

```bash
./swift_calls_cpp
```

## Expected Output

The program demonstrates:
- Using C++ namespace functions from Swift
- Creating and manipulating C++ objects
- Working with STL containers (`std::vector`, `std::string`)
- Complex data processing with C++ classes
- Performance timing using C++ Timer class
- String manipulation across language boundaries

## Key Features Demonstrated

### C++ Namespaces in Swift
- `MathUtils.add()`, `MathUtils.multiply()`
- `StringUtils.reverse()`, `StringUtils.split()`
- Direct access to namespace functions

### C++ Classes in Swift
- Creating objects: `Vector3D(1.0, 2.0, 3.0)`
- Method calls: `vector.magnitude()`
- Property access: `vector.getX()`

### STL Container Integration
- `std.vector<Double>()` creation and manipulation
- `std.string()` for string processing
- Automatic memory management

### Complex Data Processing
- `DataProcessor` class for statistical analysis
- Adding data, computing statistics
- Retrieving processed results

### Performance Measurement
- `Timer` class for accurate timing
- Microsecond precision measurements
- Cross-language performance testing

## Technical Notes

### Module Maps
- Required to expose C++ headers to Swift
- Must specify `requires cplusplus`
- Include path must contain the module map

### Type Compatibility
- Basic types work seamlessly: `double`, `int`, `bool`
- STL containers are accessible: `std::vector`, `std::string`
- C++ objects can be created and used directly

### Memory Management
- C++ objects follow RAII principles
- Swift doesn't need to manage C++ object lifetimes
- STL containers handle their own memory

### String Handling
- Use `std.string()` to create C++ strings from Swift
- Convert back with `String(cppString)` 
- Automatic conversion for many operations

### Namespace Access
- C++ namespaces are accessible directly
- Nested namespaces work as expected
- Static member functions accessible

## Building Tips

### Include Paths
- Module map must be in Swift's include path (`-I .`)
- C++ headers must be findable by Clang
- Use `-Xcc` to pass flags to the C++ compiler

### Compilation Flags
- `-cxx-interoperability-mode=default` enables C++ interop
- `-std=c++17` or later required
- Debug symbols: `-g` for both languages

### Dependencies
- Swift compilation depends on module map existence
- SCons handles dependency tracking automatically

## Limitations

### Unsupported C++ Features
- Templates with complex specializations
- Multiple inheritance
- Some STL algorithms (use member functions instead)
- C++ exceptions (handle in C++, return error codes)

### Performance Considerations
- STL container access has some overhead
- Frequent boundary crossings should be minimized
- String conversions can be expensive

### Platform Differences
- Best support on macOS/iOS
- Linux requires Swift toolchain installation
- Windows support is experimental

## Advanced Usage

### Error Handling
```cpp
// C++ returns error codes or special values
double result = safeDivide(10.0, 0.0);
if (std::isnan(result)) {
    // Handle error in Swift
}
```

### Complex Objects
```swift
// C++ objects can have complex state
let processor = DataProcessor(std.string("MyData"))
processor.addData(42.0)
processor.printStatistics()
```

### STL Integration
```swift
// Work with STL containers naturally
var numbers = std.vector<Double>()
for i in 1...10 {
    numbers.push_back(Double(i))
}
let joined = StringUtils.join(parts, std.string(", "))
```
