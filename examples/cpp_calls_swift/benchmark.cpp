// benchmark.cpp
// Dedicated benchmark for C++ calling Swift

#include <iostream>
#include <chrono>
#include <vector>
#include <numeric>
#include <functional>
#include "SwiftLibrary-Swift.h"

class BenchmarkTimer {
private:
    std::chrono::high_resolution_clock::time_point start_time;
    
public:
    void start() {
        start_time = std::chrono::high_resolution_clock::now();
    }
    
    double get_microseconds() const {
        auto now = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(now - start_time);
        return duration.count() / 1000.0; // Convert to microseconds
    }
};

void benchmark_function_calls(int iterations) {
    std::cout << "\n=== Function Call Benchmark (" << iterations << " iterations) ===" << std::endl;
    
    auto calculator = swift_library::Calculator::init();
    BenchmarkTimer timer;
    
    // Warm up
    for (int i = 0; i < 100; ++i) {
        calculator.addOnly(i, i + 1);
    }
    
    // Benchmark class function calls
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        calculator.addOnly(i, i + 1);
    }
    double elapsed_class = timer.get_microseconds();
    
    std::cout << "Class function calls: " << iterations << " calls in " 
              << elapsed_class << " μs (" << (elapsed_class / iterations) << " μs per call)" << std::endl;
}

void benchmark_struct_function_calls(int iterations) {
    std::cout << "\n=== Struct Function Call Benchmark (" << iterations << " iterations) ===" << std::endl;
    
    auto calculator_struct = swift_library::CalculatorStruct::init();
    BenchmarkTimer timer;
    
    // Warm up
    for (int i = 0; i < 100; ++i) {
        calculator_struct.addOnly(i, i + 1);
    }
    
    // Benchmark struct function calls
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        calculator_struct.addOnly(i, i + 1);
    }
    double elapsed_struct = timer.get_microseconds();
    
    std::cout << "Struct function calls: " << iterations << " calls in " 
              << elapsed_struct << " μs (" << (elapsed_struct / iterations) << " μs per call)" << std::endl;
}

void benchmark_object_creation(int iterations) {
    std::cout << "\n=== Object Creation Benchmark (" << iterations << " iterations) ===" << std::endl;
    
    BenchmarkTimer timer;
    
    // Benchmark class creation
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        auto calculator = swift_library::Calculator::init();
        (void)calculator; // Avoid unused variable warning
    }
    double elapsed_class = timer.get_microseconds();
    
    std::cout << "Class creation: " << iterations << " objects in " 
              << elapsed_class << " μs (" << (elapsed_class / iterations) << " μs per object)" << std::endl;
    
    // Benchmark struct creation
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        auto calculator_struct = swift_library::CalculatorStruct::init();
        (void)calculator_struct; // Avoid unused variable warning
    }
    double elapsed_struct = timer.get_microseconds();
    
    std::cout << "Struct creation: " << iterations << " objects in " 
              << elapsed_struct << " μs (" << (elapsed_struct / iterations) << " μs per object)" << std::endl;
    
    // Benchmark Point struct creation for comparison
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        auto point = swift_library::Point::init(i, i + 1);
        double x = point.getX(); // Use the point to prevent optimization
        (void)x; // Avoid unused variable warning
    }
    double elapsed_point = timer.get_microseconds();
    
    std::cout << "Point struct creation: " << iterations << " objects in " 
              << elapsed_point << " μs (" << (elapsed_point / iterations) << " μs per object)" << std::endl;
}

void benchmark_string_operations(int iterations) {
    std::cout << "\n=== String Operations Benchmark (" << iterations << " iterations) ===" << std::endl;
    
    BenchmarkTimer timer;
    
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        auto greeting = swift_library::greet(swift::String("Bench"));
        // Convert back to std::string to ensure full round-trip
        std::string result = greeting.operator std::string();
    }
    double elapsed = timer.get_microseconds();
    
    std::cout << "String operations: " << iterations << " operations in " 
              << elapsed << " μs (" << (elapsed / iterations) << " μs per operation)" << std::endl;
}

void benchmark_math_operations(int iterations) {
    std::cout << "\n=== Math Operations Benchmark (" << iterations << " iterations) ===" << std::endl;
    
    BenchmarkTimer timer;
    
    timer.start();
    for (int i = 0; i < iterations; ++i) {
        double result = swift_library::fibonacci(i % 20 + 1);
        (void)result; // Avoid unused variable warning
    }
    double elapsed = timer.get_microseconds();
    
    std::cout << "Math operations: " << iterations << " fibonacci calls in " 
              << elapsed << " μs (" << (elapsed / iterations) << " μs per operation)" << std::endl;
}

void run_multiple_iterations(const std::string& test_name, std::function<void()> test_func, int runs) {
    std::vector<double> times;
    
    for (int i = 0; i < runs; ++i) {
        BenchmarkTimer timer;
        timer.start();
        test_func();
        times.push_back(timer.get_microseconds());
    }
    
    double avg = std::accumulate(times.begin(), times.end(), 0.0) / times.size();
    double min_time = *std::min_element(times.begin(), times.end());
    double max_time = *std::max_element(times.begin(), times.end());
    
    std::cout << test_name << " - " << runs << " runs:" << std::endl;
    std::cout << "  Average: " << avg << " μs" << std::endl;
    std::cout << "  Min: " << min_time << " μs" << std::endl;
    std::cout << "  Max: " << max_time << " μs" << std::endl;
}

int main() {
    std::cout << "=== Swift C++ Interop Performance Benchmark (Optimized Build) ===" << std::endl;
    
    // Initialize Swift library
    swift_library::initializeSwiftLibrary();
    
    // Run individual benchmarks
    benchmark_function_calls(10000);
    benchmark_struct_function_calls(10000);
    benchmark_object_creation(5000);
    benchmark_string_operations(1000);
    benchmark_math_operations(1000);
    
    std::cout << "\n=== Consistency Tests (Multiple Runs) ===" << std::endl;
    
    auto calculator = swift_library::Calculator::init();
    auto calculator_struct = swift_library::CalculatorStruct::init();
    
    // Test consistency of class function calls
    run_multiple_iterations("Class function calls (1000 each)", [&]() {
        for (int i = 0; i < 1000; ++i) {
            calculator.add(i, i + 1);
        }
    }, 10);
    
    // Test consistency of struct function calls
    run_multiple_iterations("Struct function calls (1000 each)", [&]() {
        for (int i = 0; i < 1000; ++i) {
            calculator_struct.add(i, i + 1);
        }
    }, 10);
    
    std::cout << "\n=== Benchmark Complete ===" << std::endl;
    
    return 0;
}
