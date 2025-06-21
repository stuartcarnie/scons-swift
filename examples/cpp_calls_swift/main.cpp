// main.cpp
// C++ program that calls Swift code

#include <iostream>
#include <vector>
#include <iomanip>
#include <chrono>
#include <cmath>
#include "SwiftLibrary-Swift.h"  // Generated header from Swift

int main() {
    std::cout << "=== C++ Program Calling Swift Code ===" << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    
    // Initialize Swift library
    swift_library::initializeSwiftLibrary();
    
    std::cout << "\n1. Testing Calculator class:" << std::endl;
    
    // Create and use Swift Calculator
    auto calculator = swift_library::Calculator::init();
    
    auto sum = calculator.add(15.5, 24.3);
    auto product = calculator.multiply(7.0, 8.5);
    
    std::cout << "C++: Calculator history count: " << calculator.getHistoryCount() << std::endl;
    std::cout << "C++: Last result: " << calculator.getLastResult() << std::endl;
    
    calculator.clearHistory();
    
    std::cout << "\n1b. Testing CalculatorStruct struct:" << std::endl;
    
    // Create and use Swift CalculatorStruct
    auto calculator_struct = swift_library::CalculatorStruct::init();
    
    auto sum_struct = calculator_struct.add(15.5, 24.3);
    auto product_struct = calculator_struct.multiply(7.0, 8.5);
    
    std::cout << "C++: CalculatorStruct history count: " << calculator_struct.getHistoryCount() << std::endl;
    std::cout << "C++: CalculatorStruct last result: " << calculator_struct.getLastResult() << std::endl;
    
    calculator_struct.clearHistory();
    
    std::cout << "\n2. Testing Point struct:" << std::endl;
    
    // Create Swift Points
    auto point1 = swift_library::Point::init(3.0, 4.0);
    auto point2 = swift_library::Point::init(6.0, 8.0);
    
    auto distance = point1.distance(point2);
    auto midpoint = point1.midpoint(point2);
    
    std::cout << "C++: Distance between points: " << distance << std::endl;
    std::cout << "C++: Midpoint coordinates: (" << midpoint.getX() << ", " << midpoint.getY() << ")" << std::endl;
    
    std::cout << "\n3. Testing free functions:" << std::endl;
    
    // Test greeting function
    auto greeting = swift_library::greet(swift::String("C++ Developer"));
    std::cout << "C++: Received greeting: " << greeting.operator std::string() << std::endl;
    
    // Test Fibonacci
    for (int i = 0; i <= 10; i++) {
        auto fib = swift_library::fibonacci(i);
        std::cout << "C++: fib(" << i << ") = " << fib << std::endl;
    }
    
    std::cout << "\n4. Testing array processing:" << std::endl;
    
    // Create array of numbers
    std::vector<double> numbers = {1.5, 2.7, 3.9, 4.1, 5.3, 6.8, 7.2, 8.4, 9.6, 10.0};
    
    // Convert to Swift array
    auto swiftArray = swift::Array<double>::init();
    for (const auto& num : numbers) {
        swiftArray.append(num);
    }
    
    auto average = swift_library::processArray(swiftArray);
    std::cout << "C++: Calculated average: " << average << std::endl;
    
    std::cout << "\n5. Testing error handling:" << std::endl;
    
    // Test normal division
    auto result1 = swift_library::safeDivide(10.0, 3.0);
    std::cout << "C++: 10.0 / 3.0 = " << result1 << std::endl;
    
    // Test division by zero
    auto result2 = swift_library::safeDivide(10.0, 0.0);
    if (std::isnan(result2)) {
        std::cout << "C++: Division by zero properly handled (returned NaN)" << std::endl;
    }
    
    std::cout << "\n6. Performance test:" << std::endl;
    
    // Performance test - calling Swift class from a loop
    auto calc2 = swift_library::Calculator::init();
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < 1000; i++) {
        calc2.add(i, i + 1);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "C++: 1000 Swift class function calls took " << duration.count() << " microseconds" << std::endl;
    std::cout << "C++: Final class history count: " << calc2.getHistoryCount() << std::endl;
    
    // Performance test - calling Swift struct from a loop
    auto calc_struct = swift_library::CalculatorStruct::init();
    start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < 1000; i++) {
        calc_struct.add(i, i + 1);
    }
    
    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "C++: 1000 Swift struct function calls took " << duration.count() << " microseconds" << std::endl;
    std::cout << "C++: Final struct history count: " << calc_struct.getHistoryCount() << std::endl;
    
    std::cout << "\n=== Test Complete ===" << std::endl;
    
    return 0;
}