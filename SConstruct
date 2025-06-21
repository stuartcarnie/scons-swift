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

# Process example subdirectories
examples = ['cpp_calls_swift', 'swift_calls_cpp']

for example in examples:
    example_dir = os.path.join('examples', example)
    if os.path.exists(os.path.join(example_dir, 'SCsub')):
        SConscript(os.path.join(example_dir, 'SCsub'), variant_dir=os.path.join('build', example), duplicate=0)
