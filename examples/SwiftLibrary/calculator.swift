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

func distance(p1: Point, p2: Point) -> Double {
    p1.distance(to: p2)
}
