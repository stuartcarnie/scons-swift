// cpp_library.cpp
// Implementation of C++ library

#include "cpp_library.h"
#include <cmath>
#include <algorithm>
#include <sstream>
#include <chrono>
#include <numeric>
#include <iomanip>

// MARK: - Math utilities implementation

namespace MathUtils {
    double add(double a, double b) {
        return a + b;
    }
    
    double multiply(double a, double b) {
        std::cout << "C++: Multiplying " << a << " * " << b << std::endl;
        return a * b;
    }
    
    double power(double base, double exponent) {
        double result = std::pow(base, exponent);
        std::cout << "C++: " << base << "^" << exponent << " = " << result << std::endl;
        return result;
    }
    
    double factorial(int n) {
        if (n < 0) return -1; // Error case
        if (n <= 1) return 1;
        
        double result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        
        std::cout << "C++: " << n << "! = " << result << std::endl;
        return result;
    }
    
    bool isPrime(int n) {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        
        for (int i = 3; i * i <= n; i += 2) {
            if (n % i == 0) return false;
        }
        
        std::cout << "C++: " << n << " is " << (true ? "prime" : "not prime") << std::endl;
        return true;
    }
}

// MARK: - Vector3D implementation

Vector3D::Vector3D() : x_(0), y_(0), z_(0) {
    std::cout << "C++: Vector3D created: (0, 0, 0)" << std::endl;
}

Vector3D::Vector3D(double x, double y, double z) : x_(x), y_(y), z_(z) {
    std::cout << "C++: Vector3D created: (" << x << ", " << y << ", " << z << ")" << std::endl;
}

Vector3D Vector3D::add(const Vector3D& other) const {
    return Vector3D(x_ + other.x_, y_ + other.y_, z_ + other.z_);
}

Vector3D Vector3D::subtract(const Vector3D& other) const {
    return Vector3D(x_ - other.x_, y_ - other.y_, z_ - other.z_);
}

Vector3D Vector3D::multiply(double scalar) const {
    return Vector3D(x_ * scalar, y_ * scalar, z_ * scalar);
}

double Vector3D::dot(const Vector3D& other) const {
    double result = x_ * other.x_ + y_ * other.y_ + z_ * other.z_;
    std::cout << "C++: Dot product = " << result << std::endl;
    return result;
}

Vector3D Vector3D::cross(const Vector3D& other) const {
    return Vector3D(
        y_ * other.z_ - z_ * other.y_,
        z_ * other.x_ - x_ * other.z_,
        x_ * other.y_ - y_ * other.x_
    );
}

double Vector3D::magnitude() const {
    double mag = std::sqrt(x_ * x_ + y_ * y_ + z_ * z_);
    std::cout << "C++: Vector magnitude = " << mag << std::endl;
    return mag;
}

Vector3D Vector3D::normalize() const {
    double mag = magnitude();
    if (mag == 0) return Vector3D();
    return Vector3D(x_ / mag, y_ / mag, z_ / mag);
}

void Vector3D::print() const {
    std::cout << "C++: Vector3D(" << x_ << ", " << y_ << ", " << z_ << ")" << std::endl;
}

std::string Vector3D::toString() const {
    std::ostringstream oss;
    oss << "(" << x_ << ", " << y_ << ", " << z_ << ")";
    return oss.str();
}

// MARK: - String utilities implementation

namespace StringUtils {
    std::string reverse(const std::string& str) {
        std::string result = str;
        std::reverse(result.begin(), result.end());
        std::cout << "C++: Reversed '" << str << "' to '" << result << "'" << std::endl;
        return result;
    }
    
    std::string toUpperCase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::toupper);
        return result;
    }
    
    std::string toLowerCase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }
    
    bool isPalindrome(const std::string& str) {
        std::string lower = toLowerCase(str);
        std::string reversed = lower;
        std::reverse(reversed.begin(), reversed.end());
        bool result = (lower == reversed);
        std::cout << "C++: '" << str << "' is " << (result ? "a palindrome" : "not a palindrome") << std::endl;
        return result;
    }
    
    int splitString(const std::string& str, char delimiter, char* result[], int maxResults) {
        std::vector<std::string> parts;
        std::stringstream ss(str);
        std::string item;
        
        while (std::getline(ss, item, delimiter) && parts.size() < maxResults) {
            parts.push_back(item);
        }
        
        for (size_t i = 0; i < parts.size(); ++i) {
            result[i] = new char[parts[i].length() + 1];
            strcpy(result[i], parts[i].c_str());
        }
        
        std::cout << "C++: Split '" << str << "' into " << parts.size() << " parts" << std::endl;
        return static_cast<int>(parts.size());
    }
    
    std::string simpleJoin(const std::string& str1, const std::string& str2, const std::string& separator) {
        std::string result = str1 + separator + str2;
        std::cout << "C++: Joined 2 strings with '" << separator << "'" << std::endl;
        return result;
    }
}

// MARK: - DataProcessor implementation

DataProcessor::DataProcessor(const std::string& name) : name_(name) {
    std::cout << "C++: DataProcessor '" << name << "' created" << std::endl;
}

void DataProcessor::addData(double value) {
    data_.push_back(value);
}

void DataProcessor::addMultipleData(const double* values, size_t count) {
    for (size_t i = 0; i < count; ++i) {
        data_.push_back(values[i]);
    }
    std::cout << "C++: Added " << count << " values to DataProcessor" << std::endl;
}

void DataProcessor::clearData() {
    data_.clear();
    std::cout << "C++: DataProcessor data cleared" << std::endl;
}

size_t DataProcessor::getDataCount() const {
    return data_.size();
}

double DataProcessor::getSum() const {
    return std::accumulate(data_.begin(), data_.end(), 0.0);
}

double DataProcessor::getAverage() const {
    if (data_.empty()) return 0.0;
    return getSum() / data_.size();
}

double DataProcessor::getMin() const {
    if (data_.empty()) return 0.0;
    return *std::min_element(data_.begin(), data_.end());
}

double DataProcessor::getMax() const {
    if (data_.empty()) return 0.0;
    return *std::max_element(data_.begin(), data_.end());
}

double DataProcessor::getStandardDeviation() const {
    if (data_.size() < 2) return 0.0;
    
    double mean = getAverage();
    double sum_squared_diff = 0.0;
    
    for (double value : data_) {
        double diff = value - mean;
        sum_squared_diff += diff * diff;
    }
    
    return std::sqrt(sum_squared_diff / (data_.size() - 1));
}

double DataProcessor::getDataAtIndex(size_t index) const {
    if (index < data_.size()) {
        return data_[index];
    }
    return 0.0;
}

void DataProcessor::printStatistics() const {
    std::cout << "C++: DataProcessor '" << name_ << "' Statistics:" << std::endl;
    std::cout << "  Count: " << getDataCount() << std::endl;
    std::cout << "  Sum: " << getSum() << std::endl;
    std::cout << "  Average: " << getAverage() << std::endl;
    std::cout << "  Min: " << getMin() << std::endl;
    std::cout << "  Max: " << getMax() << std::endl;
    std::cout << "  Std Dev: " << getStandardDeviation() << std::endl;
}

// MARK: - Timer implementation

Timer::Timer() : is_running_(false) {}

void Timer::start() {
    start_time_ = std::chrono::high_resolution_clock::now();
    is_running_ = true;
    std::cout << "C++: Timer started" << std::endl;
}

void Timer::stop() {
    is_running_ = false;
    std::cout << "C++: Timer stopped" << std::endl;
}

void Timer::reset() {
    start_time_ = std::chrono::high_resolution_clock::now();
    is_running_ = false;
    std::cout << "C++: Timer reset" << std::endl;
}

double Timer::getElapsedMilliseconds() const {
    auto now = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(now - start_time_);
    return duration.count() / 1000.0;
}

double Timer::getElapsedSeconds() const {
    return getElapsedMilliseconds() / 1000.0;
}

void Timer::printElapsed() const {
    std::cout << "C++: Elapsed time: " << getElapsedMilliseconds() << " ms" << std::endl;
}

// MARK: - Global utility functions

void initializeCppLibrary() {
    std::cout << "C++: Library initialized successfully!" << std::endl;
    std::cout << "C++: Available modules: MathUtils, Vector3D, StringUtils, DataProcessor, Timer" << std::endl;
}

void printSystemInfo() {
    std::cout << "C++: System Information:" << std::endl;
    std::cout << "  C++ Standard: " << __cplusplus << std::endl;
    std::cout << "  Compiler: " << 
#ifdef __clang__
    "Clang"
#elif defined(__GNUC__)
    "GCC"
#elif defined(_MSC_VER)
    "MSVC"
#else
    "Unknown"
#endif
    << std::endl;
}

std::string getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    
    std::ostringstream oss;
    oss << std::put_time(std::localtime(&time_t), "%Y-%m-%d %H:%M:%S");
    return oss.str();
}

void performBenchmark() {
    std::cout << "C++: Performing benchmark..." << std::endl;
    
    Timer timer;
    timer.start();
    
    // Perform some computations
    double sum = 0;
    for (int i = 0; i < 1000000; i++) {
        sum += std::sin(i) * std::cos(i);
    }
    
    timer.stop();
    
    std::cout << "C++: Benchmark completed. Sum = " << sum << std::endl;
    timer.printElapsed();
}