
add_library(stuff STATIC)
target_sources(stuff PUBLIC
        calculator.swift
        point.swift
)
set(CMAKE_Swift_FLAGS "-cxx-interoperability-mode=default -emit-clang-header-path ${CMAKE_CURRENT_SOURCE_DIR}/SwiftLibrary-Swift.h")

add_executable(cpp_calls_swift)
target_sources(cpp_calls_swift PUBLIC main.cpp)
target_link_libraries(cpp_calls_swift stuff)
