// benchmark.swift
// Dedicated benchmark for Swift calling C++

import Foundation
import CxxStdlib
import CppLibrary

class BenchmarkTimer {
    private var startTime: DispatchTime?
    
    func start() {
        startTime = DispatchTime.now()
    }
    
    func getMicroseconds() -> Double {
        guard let start = startTime else { return 0 }
        let end = DispatchTime.now()
        let nanos = end.uptimeNanoseconds - start.uptimeNanoseconds
        return Double(nanos) / 1000.0 // Convert to microseconds
    }
}

func benchmarkFunctionCalls(iterations: Int) {
    print("\n=== Function Call Benchmark (\(iterations) iterations) ===")
    
    let timer = BenchmarkTimer()
    
    // Warm up
    for i in 0..<100 {
        let _ = MathUtils.add(Double(i), Double(i + 1))
    }
    
    // Benchmark function calls
    timer.start()
    for i in 0..<iterations {
        let _ = MathUtils.add(Double(i), Double(i + 1))
    }
    let elapsed = timer.getMicroseconds()
    
    print("Function calls: \(iterations) calls in \(elapsed) μs (\(elapsed / Double(iterations)) μs per call)")
}

func benchmarkObjectCreation(iterations: Int) {
    print("\n=== Object Creation Benchmark (\(iterations) iterations) ===")
    
    let timer = BenchmarkTimer()
    var vectors: [Vector3D] = []
    vectors.reserveCapacity(iterations)
    
    timer.start()
    for i in 0..<iterations {
        let vector = Vector3D(Double(i), Double(i + 1), Double(i + 2))
        vectors.append(vector)
    }
    let elapsed = timer.getMicroseconds()
    
    print("Object creation: \(iterations) objects in \(elapsed) μs (\(elapsed / Double(iterations)) μs per object)")
}

func benchmarkStringOperations(iterations: Int) {
    print("\n=== String Operations Benchmark (\(iterations) iterations) ===")
    
    let timer = BenchmarkTimer()
    
    timer.start()
    for i in 0..<iterations {
        let input = std.string("Benchmark\(i)")
        let reversed = StringUtils.reverse(input)
        let _ = String(reversed) // Convert back to Swift string
    }
    let elapsed = timer.getMicroseconds()
    
    print("String operations: \(iterations) operations in \(elapsed) μs (\(elapsed / Double(iterations)) μs per operation)")
}

func benchmarkDataProcessing(iterations: Int) {
    print("\n=== Data Processing Benchmark (\(iterations) iterations) ===")
    
    // Create test data
    let testData: [Double] = (0..<100).map { Double($0) * 1.5 }
    
    let timer = BenchmarkTimer()
    
    timer.start()
    for _ in 0..<iterations {
        var processor = DataProcessor(std.string("BenchmarkTest"))
        testData.withUnsafeBufferPointer { buffer in
            processor.addMultipleData(buffer.baseAddress!, buffer.count)
        }
        let _ = processor.getAverage()
    }
    let elapsed = timer.getMicroseconds()
    
    print("Data processing: \(iterations) datasets (100 elements each) in \(elapsed) μs (\(elapsed / Double(iterations)) μs per dataset)")
}

func runMultipleIterations(testName: String, testFunc: () -> Void, runs: Int) {
    var times: [Double] = []
    
    for _ in 0..<runs {
        let timer = BenchmarkTimer()
        timer.start()
        testFunc()
        times.append(timer.getMicroseconds())
    }
    
    let avg = times.reduce(0, +) / Double(times.count)
    let minTime = times.min() ?? 0
    let maxTime = times.max() ?? 0
    
    print("\(testName) - \(runs) runs:")
    print("  Average: \(avg) μs")
    print("  Min: \(minTime) μs")
    print("  Max: \(maxTime) μs")
}

@main
struct SwiftCppBenchmark {
    static func main() {
        print("=== Swift C++ Interop Performance Benchmark (Optimized Build) ===")
        
        // Initialize C++ library
        initializeCppLibrary()
        
        // Run individual benchmarks
        benchmarkFunctionCalls(iterations: 10000)
        benchmarkObjectCreation(iterations: 5000)
        benchmarkStringOperations(iterations: 1000)
        benchmarkDataProcessing(iterations: 1000)
        
        print("\n=== Consistency Tests (Multiple Runs) ===")
        
        // Test consistency of function calls
        runMultipleIterations(testName: "Function calls (1000 each)", testFunc: {
            for i in 0..<1000 {
                let _ = MathUtils.add(Double(i), Double(i + 1))
            }
        }, runs: 10)
        
        print("\n=== Benchmark Complete ===")
    }
}