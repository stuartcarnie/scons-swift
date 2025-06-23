// cpp_library.h
// C++ library that will be called from Swift

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <iostream>
#include <chrono>

// MARK: - Math utilities

namespace MathUtils {
    double add(double a, double b);
    double multiply(double a, double b);
    double power(double base, double exponent);
    double factorial(int n);
    bool isPrime(int n);
}

// MARK: - Vector operations

class Vector3D {
private:
    double x_, y_, z_;
    
public:
    Vector3D();
    Vector3D(double x, double y, double z);
    
    // Getters
    double getX() const { return x_; }
    double getY() const { return y_; }
    double getZ() const { return z_; }
    
    // Setters
    void setX(double x) { x_ = x; }
    void setY(double y) { y_ = y; }
    void setZ(double z) { z_ = z; }
    
    // Operations
    Vector3D add(const Vector3D& other) const;
    Vector3D subtract(const Vector3D& other) const;
    Vector3D multiply(double scalar) const;
    double dot(const Vector3D& other) const;
    Vector3D cross(const Vector3D& other) const;
    double magnitude() const;
    Vector3D normalize() const;
    
    // Utility
    void print() const;
    std::string toString() const;
};

// MARK: - String utilities

namespace StringUtils {
    std::string reverse(const std::string& str);
    std::string toUpperCase(const std::string& str);
    std::string toLowerCase(const std::string& str);
    bool isPalindrome(const std::string& str);
    int splitString(const std::string& str, char delimiter, char* result[], int maxResults);
    std::string simpleJoin(const std::string& str1, const std::string& str2, const std::string& separator);
}

// MARK: - Data processor

class DataProcessor {
private:
    std::vector<double> data_;
    std::string name_;
    
public:
    DataProcessor(const std::string& name);
    
    void addData(double value);
    void addMultipleData(const double* values, size_t count);
    void clearData();
    
    size_t getDataCount() const;
    double getSum() const;
    double getAverage() const;
    double getMin() const;
    double getMax() const;
    double getStandardDeviation() const;
    
    double getDataAtIndex(size_t index) const;
    void printStatistics() const;
    
    const std::string& getName() const { return name_; }
};

// MARK: - Timer class

class Timer {
private:
    std::chrono::high_resolution_clock::time_point start_time_;
    bool is_running_;
    
public:
    Timer();
    
    void start();
    void stop();
    void reset();
    
    double getElapsedMilliseconds() const;
    double getElapsedSeconds() const;
    bool isRunning() const { return is_running_; }
    
    void printElapsed() const;
};

// MARK: - Global utility functions

void initializeCppLibrary();
void printSystemInfo();
std::string getCurrentTimestamp();
void performBenchmark();