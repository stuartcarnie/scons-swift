# C++ Calls Swift Example

This example demonstrates a C++ program that calls Swift code using Swift's C++ interoperability features.

## Files

- **`SConstruct`**: Build configuration that enables C++ interop and generates headers
- **`swift_library.swift`**: Swift library with classes, functions, and structs exposed to C++
- **`main.cpp`**: C++ main program that uses the Swift library

## How It Works

### 1. Swift Code Preparation

The Swift code uses `@_expose(Cxx)` annotations to expose APIs to C++:

```swift
@_expose(Cxx)
public class Calculator {
    @_expose(Cxx)
    public func add(_ a: Double, _ b: Double) -> Double {
        return a + b
    }
}
```

### 2. Header Generation

SCons automatically generates `SwiftLibrary-Swift.h` from the Swift code:

```python
env['SWIFT_EMIT_CXX_HEADER'] = True
env['SWIFT_CXX_HEADER_NAME'] = 'SwiftLibrary-Swift.h'
```

### 3. C++ Usage

The C++ code includes the generated header and uses Swift types:

```cpp
#include "SwiftLibrary-Swift.h"

int main() {
    swift::initializeSwiftRuntime();
    auto calc = SwiftLibrary::Calculator::init();
    auto result = calc.add(5.0, 3.0);
}
```

## Building

```bash
scons
```

This will:
1. Compile Swift code and generate the C++ header
2. Compile C++ code that includes the generated header
3. Link everything into an executable

## Running

```bash
./cpp_calls_swift
```

## Expected Output

The program demonstrates:
- Creating and using Swift classes from C++
- Calling Swift methods with parameters and return values
- Using Swift structs and their methods
- Calling Swift free functions
- Processing arrays between languages
- Error handling with Swift optionals/NaN
- Performance testing across language boundaries

## Key Features Demonstrated

### Swift Classes in C++
- Creating Swift objects: `SwiftLibrary::Calculator::init()`
- Calling methods: `calc.add(5.0, 3.0)`
- Memory management handled automatically by Swift ARC

### Swift Structs in C++
- Value semantics preserved
- Method calls work as expected
- Efficient copying between languages

### Array Processing
- Converting C++ `std::vector` to Swift `Array`
- Processing in Swift and returning results to C++

### Error Handling
- Swift can return special values (like NaN) for errors
- C++ can check for error conditions

### Performance
- Demonstrates overhead of language boundary crossings
- Shows that frequent calls are feasible for many use cases

## Technical Notes

### Memory Management
- Swift objects are managed by Swift's ARC
- C++ holds Swift objects by value in the generated wrapper types
- No manual memory management required

### Type Mapping
- `Double` ↔ `double`
- `Int32` ↔ `int32_t`
- `String` ↔ `swift::String`
- `Array<T>` ↔ `swift::Array<T>`

### Limitations
- Not all Swift types can be exposed to C++
- Generics have limited support
- Protocols don't map to C++
- Closures can't be exposed

### Debugging
- Use LLDB which understands both Swift and C++
- Enable debug symbols with `-g`
- Generated headers are readable for understanding type mappings