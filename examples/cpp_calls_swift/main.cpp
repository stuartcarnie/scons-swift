// main.cpp
// C++ program that calls Swift code

#include <iostream>
#include <vector>
#include <iomanip>
#include <chrono>
#include <cmath>
#include "examples/SwiftLibrary/SwiftLibrary-Swift.h"  // Generated header from Swift

int main() {
    std::cout << "=== C++ Program Calling Swift Code ===" << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    
    // Initialize Swift library
    SwiftLibrary::initializeSwiftLibrary();
    
    std::cout << "\n1. Testing Calculator class:" << std::endl;
    
    // Create and use Swift CalculatorStruct
    auto calculator_struct = SwiftLibrary::CalculatorStruct::init();
    
    auto sum_struct = calculator_struct.add(15.5, 24.3);
    auto product_struct = calculator_struct.multiply(7.0, 8.5);
    
    std::cout << "C++: CalculatorStruct history count: " << calculator_struct.getHistoryCount() << std::endl;
    std::cout << "C++: CalculatorStruct last result: " << calculator_struct.getLastResult() << std::endl;
    
    calculator_struct.clearHistory();
    
    std::cout << "\n2. Testing Point struct:" << std::endl;
    
    // Create Swift Points
    auto point1 = SwiftLibrary::Point::init(3.0, 4.0);
    auto point2 = SwiftLibrary::Point::init(6.0, 8.0);
    
    auto distance = point1.distance(point2);
    auto midpoint = point1.midpoint(point2);
    
    std::cout << "C++: Distance between points: " << distance << std::endl;
    std::cout << "C++: Midpoint coordinates: (" << midpoint.getX() << ", " << midpoint.getY() << ")" << std::endl;
    
    std::cout << "\n3. Testing free functions:" << std::endl;
    
    // Test greeting function
    auto greeting = SwiftLibrary::greet(swift::String("C++ Developer"));
    std::cout << "C++: Received greeting: " << greeting.operator std::string() << std::endl;

    return 0;
}
