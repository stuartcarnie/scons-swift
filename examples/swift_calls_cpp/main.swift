// main.swift
// Swift program that calls C++ code

import Foundation
import CxxStdlib
import CppLibrary  // Import the C++ module

@main
struct SwiftCallsCppApp {
    static func main() {
        print("=== Swift Program Calling C++ Code ===")
        
        // Initialize C++ library
        initializeCppLibrary()
        printSystemInfo()
        
        print("\n1. Testing Math Utilities:")
        testMathUtils()
        
        print("\n2. Testing Vector3D class:")
        testVector3D()
        
        print("\n3. Testing String utilities:")
        testStringUtils()
        
        print("\n4. Testing DataProcessor:")
        testDataProcessor()
        
        print("\n5. Testing Timer:")
        testTimer()
        
        print("\n6. Performance test:")
        performanceTest()
        
        print("\n=== Test Complete ===")
    }
    
    static func testMathUtils() {
        // Test basic math operations
        let sum = MathUtils.add(15.5, 24.3)
        let product = MathUtils.multiply(7.2, 8.5)
        let power = MathUtils.power(2.0, 10.0)
        
        print("Swift: Received results - sum: \(sum), product: \(product), power: \(power)")
        
        // Test factorial
        for i in 0...10 {
            let fact = MathUtils.factorial(Int32(i))
            print("Swift: \(i)! = \(fact)")
        }
        
        // Test prime checking
        let testNumbers = [2, 3, 4, 5, 17, 25, 29, 100]
        for num in testNumbers {
            let isPrime = MathUtils.isPrime(Int32(num))
            print("Swift: \(num) is \(isPrime ? "prime" : "not prime")")
        }
    }
    
    static func testVector3D() {
        // Create vectors
        let v1 = Vector3D(1.0, 2.0, 3.0)
        let v2 = Vector3D(4.0, 5.0, 6.0)
        
        v1.print()
        v2.print()
        
        // Vector operations
        let sum = v1.add(v2)
        let diff = v1.subtract(v2)
        let scaled = v1.multiply(2.5)
        
        print("Swift: Vector operations completed")
        sum.print()
        diff.print()
        scaled.print()
        
        // Dot and cross products
        let dotProduct = v1.dot(v2)
        let crossProduct = v1.cross(v2)
        
        print("Swift: Dot product: \(dotProduct)")
        crossProduct.print()
        
        // Magnitude and normalization
        let magnitude = v1.magnitude()
        let normalized = v1.normalize()
        
        print("Swift: Original magnitude: \(magnitude)")
        normalized.print()
        
        // Test string representation
        let str = v1.toString()
        print("Swift: Vector as string: \(str)")
    }
    
    static func testStringUtils() {
        let testString = "Hello World"
        
        // String operations
        let reversed = StringUtils.reverse(std.string(testString))
        let upper = StringUtils.toUpperCase(std.string(testString))
        let lower = StringUtils.toLowerCase(std.string(testString))
        
        print("Swift: Original: '\(testString)'")
        print("Swift: Reversed: '\(String(reversed))'")
        print("Swift: Upper: '\(String(upper))'")
        print("Swift: Lower: '\(String(lower))'")
        
        // Palindrome test
        let palindromes = ["racecar", "hello", "madam", "swift"]
        for word in palindromes {
            let isPalin = StringUtils.isPalindrome(std.string(word))
            print("Swift: '\(word)' palindrome check: \(isPalin)")
        }
        
        // String joining (simplified)
        let str1 = "Swift"
        let str2 = "C++"
        let joined = StringUtils.simpleJoin(std.string(str1), std.string(str2), std.string(" and "))
        print("Swift: Joined: '\(String(joined))'")
    }
    
    static func testDataProcessor() {
        // Create data processor
        var processor = DataProcessor(std.string("SwiftTest"))
        
        // Add individual data points
        processor.addData(10.5)
        processor.addData(15.2)
        processor.addData(8.7)
        processor.addData(22.1)
        processor.addData(12.8)
        
        // Add array of data (using pointer-based interface)
        let moreData: [Double] = [5.5, 18.3, 11.9, 25.4, 9.1, 16.7, 13.2]
        moreData.withUnsafeBufferPointer { buffer in
            processor.addMultipleData(buffer.baseAddress!, buffer.count)
        }
        
        print("Swift: Added \(moreData.count) more data points")
        print("Swift: Total data count: \(processor.getDataCount())")
        
        // Get statistics
        let sum = processor.getSum()
        let avg = processor.getAverage()
        let min = processor.getMin()
        let max = processor.getMax()
        let stdDev = processor.getStandardDeviation()
        
        print("Swift: Statistics from C++:")
        print("  Sum: \(sum)")
        print("  Average: \(avg)")
        print("  Min: \(min)")
        print("  Max: \(max)")
        print("  Std Dev: \(stdDev)")
        
        // Print detailed statistics
        processor.printStatistics()
        
        // Get some data back
        let dataCount = processor.getDataCount()
        print("Swift: Data count: \(dataCount)")
        if dataCount > 0 {
            let firstValue = processor.getDataAtIndex(0)
            let lastValue = processor.getDataAtIndex(dataCount - 1)
            print("Swift: First value: \(firstValue), Last value: \(lastValue)")
        }
        
        processor.clearData()
        print("Swift: Data cleared, new count: \(processor.getDataCount())")
    }
    
    static func testTimer() {
        var timer = Timer()
        
        timer.start()
        
        // Simulate some work
        var sum = 0.0
        for i in 0..<100000 {
            sum += sin(Double(i)) * cos(Double(i))
        }
        
        timer.stop()
        
        let elapsedMs = timer.getElapsedMilliseconds()
        let elapsedSec = timer.getElapsedSeconds()
        
        print("Swift: Computation result: \(sum)")
        print("Swift: Time from C++ timer: \(elapsedMs) ms (\(elapsedSec) seconds)")
        
        timer.printElapsed()
        
        timer.reset()
        print("Swift: Timer reset, running: \(timer.isRunning())")
    }
    
    static func performanceTest() {
        print("Swift: Starting performance test...")
        
        var timer = Timer()
        timer.start()
        
        // Test calling C++ functions in a loop
        for i in 0..<1000 {
            let _ = MathUtils.add(Double(i), Double(i + 1))
        }
        
        timer.stop()
        let elapsedMs = timer.getElapsedMilliseconds()
        
        print("Swift: 1000 C++ function calls took \(elapsedMs) ms")
        
        // Run C++ benchmark
        performBenchmark()
        
        // Get timestamp
        let timestamp = getCurrentTimestamp()
        print("Swift: Current timestamp from C++: \(String(timestamp))")
    }
}