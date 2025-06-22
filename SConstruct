#!/usr/bin/env python3
from utils.scons_hints import *

import os

# Create base environment with Swift tool
env = Environment(
    tools=['default', 'swift'],
    toolpath=['sconscontrib/SCons/Tool']
)

# Set up common Swift configuration
env['SWIFT_CXX_INTEROP'] = True

# Export the environment for subdirectories
Export('env')

SConscript("examples/cpp_calls_swift/SCsub", variant_dir="build/cpp_calls_swift", duplicate=0)
SConscript("examples/swift_calls_cpp/SCsub", variant_dir="build/swift_calls_cpp", duplicate=0)
