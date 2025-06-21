"""SCons.Tool.swift

Tool-specific initialization for Swift language.

This tool configures SCons to compile Swift source files using swiftc.
It supports both static and shared object compilation, as well as
program and library linking.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

#
# Copyright (c) 2024 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Tool
import SCons.Util

# Swift source file suffixes
SwiftSuffixes = ['.swift']

# Swift compiler to use
compilers = ['swiftc']

def _swift_emitter(target, source, env):
    """Add swiftmodule, swiftdoc, and swiftsourceinfo files to targets when building object files"""
    # Swift generates additional files alongside object files
    base = SCons.Util.splitext(str(target[0]))[0]
    
    # When C++ interop is enabled, Swift generates additional files
    if env.get('SWIFT_CXX_INTEROP'):
        # Add .swiftsourceinfo file for dependency tracking (as side effect)
        swiftsourceinfo = env.File(base + '.swiftsourceinfo')
        env.SideEffect(swiftsourceinfo, target)
        
        # Add generated C++ header if requested (as side effect)
        if env.get('SWIFT_EMIT_CXX_HEADER'):
            header_name = env.get('SWIFT_CXX_HEADER_NAME', base + '-Swift.h')
            # Generate the header in the same directory as the target
            header_dir = os.path.dirname(str(target[0]))
            if header_dir:
                cxx_header = env.File(os.path.join(header_dir, header_name))
            else:
                cxx_header = env.File(header_name)
            env.SideEffect(cxx_header, target)
            env.Clean(target, cxx_header)
    
    # Add module files if we're building a module (as side effects)
    if env.get('SWIFTMODULENAME'):
        module_name = env['SWIFTMODULENAME']
        swiftmodule = env.File(base + '.swiftmodule')
        swiftdoc = env.File(base + '.swiftdoc')
        env.SideEffect([swiftmodule, swiftdoc], target)
    
    return target, source

def _detect_swift_version(env, swift):
    """Detect Swift compiler version"""
    import subprocess
    try:
        result = subprocess.run([swift, '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            # Parse version from output
            output = result.stdout
            if 'Swift version' in output:
                version_line = output.split('\n')[0]
                return version_line
    except:
        pass
    return None

def generate(env):
    """Add Builders and construction variables for Swift to an Environment."""
    
    # Create object builders
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)

    # Swift Actions
    SwiftAction = SCons.Action.Action("$SWIFTCOM", "$SWIFTCOMSTR")
    SwiftShAction = SCons.Action.Action("$SWIFTSHCOM", "$SWIFTSHCOMSTR")
    
    # Add actions and emitters for Swift suffixes
    for suffix in SwiftSuffixes:
        static_obj.add_action(suffix, SwiftAction)
        shared_obj.add_action(suffix, SwiftShAction)
        static_obj.add_emitter(suffix, _swift_emitter)
        shared_obj.add_emitter(suffix, _swift_emitter)

    # Detect Swift compiler
    if 'SWIFT' not in env:
        env['SWIFT'] = env.Detect(compilers) or compilers[0]
    
    # Basic Swift variables
    env['SWIFTFLAGS'] = SCons.Util.CLVar('')
    env['SWIFTPATH'] = SCons.Util.CLVar('')
    
    # C++ interoperability support
    env['SWIFT_CXX_INTEROP'] = False
    env['SWIFT_EMIT_CXX_HEADER'] = False
    env['SWIFT_CXX_HEADER_NAME'] = ''
    env['_SWIFT_CXX_INTEROP_FLAG'] = '${SWIFT_CXX_INTEROP and "-cxx-interoperability-mode=default" or ""}'
    env['_SWIFT_EMIT_CXX_HEADER_FLAG'] = '${SWIFT_EMIT_CXX_HEADER and "-emit-clang-header-path $SWIFT_CXX_HEADER_NAME" or ""}'
    
    # Module support
    env['SWIFTMODULENAME'] = ''
    env['SWIFTMODULESUFFIX'] = '.swiftmodule'
    env['SWIFTDOCSUFFIX'] = '.swiftdoc'
    env['SWIFTSOURCEINFOSUFFIX'] = '.swiftsourceinfo'
    
    # Include paths (-I flag)
    env['INCPREFIX'] = '-I '
    env['INCSUFFIX'] = ''
    env['_SWIFTINCFLAGS'] = '$( ${_concat(INCPREFIX, SWIFTPATH, INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
    
    # Framework paths (-F flag)
    env['FRAMEWORKPREFIX'] = '-F '
    env['FRAMEWORKSUFFIX'] = ''
    env['_SWIFTFRAMEWORKPATH'] = '$( ${_concat(FRAMEWORKPREFIX, FRAMEWORKPATH, FRAMEWORKSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
    
    # Library paths (-L flag)
    env['SWIFTLIBDIRPREFIX'] = '-L '
    env['SWIFTLIBDIRSUFFIX'] = ''
    env['_SWIFTLIBFLAGS'] = '$( ${_concat(SWIFTLIBDIRPREFIX, LIBPATH, SWIFTLIBDIRSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
    
    # Common flags for both static and shared compilation
    env['_SWIFTCOMCOM'] = '$_SWIFTINCFLAGS $_SWIFTFRAMEWORKPATH $_SWIFTLIBFLAGS $_SWIFT_CXX_INTEROP_FLAG $_SWIFT_EMIT_CXX_HEADER_FLAG'
    
    # Static object compilation
    env['SWIFTCOM'] = 'cd ${TARGET.dir} && $SWIFT -c -parse-as-library ${SOURCES.abspath} -o ${TARGET.file} $SWIFTFLAGS $_SWIFTCOMCOM'
    env['SWIFTCOMSTR'] = env.get('SWIFTCOMSTR', 
                                 SCons.Action.Action("$SWIFTCOM", "$SWIFTCOMSTR"))
    
    # Shared object compilation (with -emit-object)
    env['SWIFTSH'] = '$SWIFT'
    env['SWIFTSHFLAGS'] = SCons.Util.CLVar('$SWIFTFLAGS')
    env['SWIFTSHCOM'] = 'cd ${TARGET.dir} && $SWIFTSH -c -parse-as-library ${SOURCES.abspath} -o ${TARGET.file} -emit-object $SWIFTSHFLAGS $_SWIFTCOMCOM'
    env['SWIFTSHCOMSTR'] = env.get('SWIFTSHCOMSTR',
                                   SCons.Action.Action("$SWIFTSHCOM", "$SWIFTSHCOMSTR"))
    
    # Object file suffixes
    env['SWIFTOBJSUFFIX'] = '.o'
    env['SWIFTSHOBSUFFIX'] = '.os'
    
    # Whole module optimization support
    env['SWIFTWMO'] = False
    env['_SWIFTWMOFLAG'] = '${SWIFTWMO and "-whole-module-optimization" or ""}'
    
    # Library builder for Swift
    env['SWIFTLIBCOM'] = '$SWIFT -emit-library -o $TARGET $SOURCES $SWIFTLIBFLAGS $_SWIFTCOMCOM'
    env['SWIFTLIBCOMSTR'] = env.get('SWIFTLIBCOMSTR',
                                    SCons.Action.Action("$SWIFTLIBCOM", "$SWIFTLIBCOMSTR"))
    env['SWIFTLIBFLAGS'] = SCons.Util.CLVar('')
    
    # Module builder for Swift  
    env['SWIFTMODULECOM'] = '$SWIFT -emit-module -module-name $SWIFTMODULENAME -o $TARGET $SOURCES $SWIFTMODULEFLAGS $_SWIFTCOMCOM'
    env['SWIFTMODULECOMSTR'] = env.get('SWIFTMODULECOMSTR',
                                       SCons.Action.Action("$SWIFTMODULECOM", "$SWIFTMODULECOMSTR"))
    env['SWIFTMODULEFLAGS'] = SCons.Util.CLVar('')
    
    # Executable builder for Swift
    env['SWIFTEXECOM'] = '$SWIFT -o $TARGET $SOURCES $SWIFTEXEFLAGS $_SWIFTCOMCOM'
    env['SWIFTEXECOMSTR'] = env.get('SWIFTEXECOMSTR',
                                    SCons.Action.Action("$SWIFTEXECOM", "$SWIFTEXECOMSTR"))
    env['SWIFTEXEFLAGS'] = SCons.Util.CLVar('')
    
    # Create Swift-specific builders
    
    # Swift Module Builder
    swift_module_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$SWIFTMODULECOM", "$SWIFTMODULECOMSTR"),
        suffix='$SWIFTMODULESUFFIX',
        src_suffix=SwiftSuffixes,
        single_source=0
    )
    env['BUILDERS']['SwiftModule'] = swift_module_builder
    
    # Swift Library Builder
    swift_lib_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$SWIFTLIBCOM", "$SWIFTLIBCOMSTR"),
        suffix='$SHLIBSUFFIX',
        src_suffix=SwiftSuffixes,
        single_source=0
    )
    env['BUILDERS']['SwiftLibrary'] = swift_lib_builder
    
    # Swift Program Builder
    swift_exe_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$SWIFTEXECOM", "$SWIFTEXECOMSTR"),
        suffix='$PROGSUFFIX',
        src_suffix=SwiftSuffixes,
        single_source=0
    )
    env['BUILDERS']['SwiftProgram'] = swift_exe_builder
    
    # Set up platform-specific flags
    if env['PLATFORM'] == 'darwin':
        # macOS/iOS specific flags
        env.AppendUnique(SWIFTFLAGS=['-sdk', '$SDKROOT'])
        if not env.get('SDKROOT'):
            import subprocess
            try:
                result = subprocess.run(['xcrun', '--show-sdk-path'], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode == 0:
                    env['SDKROOT'] = result.stdout.strip()
            except:
                pass
        
        # Add Swift runtime libraries for C++ interop
        if env.get('SWIFT_CXX_INTEROP'):
            # Find Swift toolchain
            try:
                result = subprocess.run(['xcrun', '--find', 'swift'], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode == 0:
                    swift_path = result.stdout.strip()
                    swift_lib_dir = swift_path.replace('/bin/swift', '/lib/swift/macosx')
                    env.AppendUnique(LIBPATH=[swift_lib_dir])
                    env.AppendUnique(LIBS=['swiftCore'])
            except:
                pass
    
    # Detect Swift version and set version-specific flags
    version = _detect_swift_version(env, env['SWIFT'])
    if version:
        env['SWIFTVERSION'] = version
        # Could add version-specific flags here

def exists(env):
    """Check if Swift compiler exists"""
    return env.Detect(compilers)