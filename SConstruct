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

SConscript("examples/cpp_calls_swift/SCsub")
SConscript("examples/swift_calls_cpp/SCsub")
