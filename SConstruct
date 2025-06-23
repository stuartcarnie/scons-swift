#!/usr/bin/env python3
from utils.scons_hints import *

import os

# Create base environment with Swift tool
env = Environment(
    tools=['default', 'swift'],
    toolpath=['sconscontrib/SCons/Tool']
)

# Export the environment for subdirectories
Export('env')

env.Prepend(CPPPATH=["#"])

SConscript("examples/SwiftLibrary/SCsub")
SConscript("examples/cpp_library/SCsub")
SConscript("examples/cpp_calls_swift/SCsub")
SConscript("examples/swift_calls_cpp/SCsub")
SConscript("examples/swift_calls_swift/SCsub")
