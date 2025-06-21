// swift_library.swift
// Swift library that will be called from C++

import Foundation

// MARK: - Calculator class exposed to C++

public class Calculator {
    private var history: [Double] = []
    
    public init() {
    }
    
    public func add(_ a: Double, _ b: Double) -> Double {
        let result = a + b
        history.append(result)
        return result
    }

    public func addOnly(_ a: Double, _ b: Double) -> Double {
        a + b
    }

    public func multiply(_ a: Double, _ b: Double) -> Double {
        let result = a * b
        history.append(result)
        return result
    }
    
    public func getHistoryCount() -> Int32 {
        return Int32(history.count)
    }
    
    public func getLastResult() -> Double {
        return history.last ?? 0.0
    }
    
    public func clearHistory() {
        history.removeAll()
    }
}

// MARK: - CalculatorStruct struct exposed to C++

public struct CalculatorStruct {
    private var history: [Double] = []
    
    public init() {
    }
    
    public mutating func add(_ a: Double, _ b: Double) -> Double {
        let result = a + b
        history.append(result)
        return result
    }

    public func addOnly(_ a: Double, _ b: Double) -> Double {
        a + b
    }
    
    public mutating func multiply(_ a: Double, _ b: Double) -> Double {
        let result = a * b
        history.append(result)
        return result
    }
    
    public func getHistoryCount() -> Int32 {
        return Int32(history.count)
    }
    
    public func getLastResult() -> Double {
        return history.last ?? 0.0
    }
    
    public mutating func clearHistory() {
        history.removeAll()
    }
}

// MARK: - Point struct exposed to C++

public struct Point {
    public var x: Double
    public var y: Double
    
    public init() {
        self.x = 0.0
        self.y = 0.0
    }
    
    public init(x: Double, y: Double) {
        self.x = x
        self.y = y
    }
    
    public func distance(to other: Point) -> Double {
        let dx = x - other.x
        let dy = y - other.y
        let result = sqrt(dx * dx + dy * dy)
        return result
    }
    
    public func midpoint(to other: Point) -> Point {
        let midX = (x + other.x) / 2.0
        let midY = (y + other.y) / 2.0
        return Point(x: midX, y: midY)
    }
}

// MARK: - Free functions exposed to C++

public func greet(_ name: String) -> String {
    let greeting = "Hello from Swift, \(name)!"
    return greeting
}

public func fibonacci(_ n: Int32) -> Int32 {
    if n <= 1 {
        return n
    }
    
    var a: Int32 = 0
    var b: Int32 = 1
    
    for _ in 2...n {
        let temp = a + b
        a = b
        b = temp
    }
    
    return b
}

public func processArray(_ numbers: [Double]) -> Double {
    let sum = numbers.reduce(0, +)
    let average = sum / Double(numbers.count)
    print("Swift: Processed \(numbers.count) numbers, average = \(average)")
    return average
}

// MARK: - Error handling example

public func safeDivide(_ a: Double, _ b: Double) -> Double {
    guard b != 0 else {
        print("Swift: Error - Division by zero!")
        return Double.nan
    }
    
    let result = a / b
    return result
}

// MARK: - Module initialization

public func initializeSwiftLibrary() {
    print("Swift library initialized successfully!")
    print("Available functions: Calculator, Point, greet, fibonacci, processArray, safeDivide")
}
