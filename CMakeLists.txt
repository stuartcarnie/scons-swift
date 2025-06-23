cmake_minimum_required(VERSION 3.30 FATAL_ERROR)

project(mixed_lang
        LANGUAGES C CXX OBJC OBJCXX Swift
)

add_subdirectory(examples/cpp_calls_swift)

