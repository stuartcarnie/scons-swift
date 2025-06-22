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
import re
import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Scanner
import SCons.Tool
import SCons.Util
import SCons.Warnings

# Swift source file suffixes
SwiftSuffixes = [".swift"]

# Swift compiler to use
compilers = ["swiftc"]

def _detect_swift_version(env, swift):
    """Detect Swift compiler version"""
    import subprocess
    
    try:
        result = subprocess.run([swift, "--version"], 
                              capture_output=True, 
                              text=True,
                              timeout=5)  # Add timeout
        if result.returncode == 0:
            # More robust version parsing
            match = re.search(r'Swift version (\d+\.\d+(?:\.\d+)?)', result.stdout)
            if match:
                return match.group(1)
            # Fallback to full version line
            if "Swift version" in result.stdout:
                version_line = result.stdout.split("\n")[0]
                return version_line
    except subprocess.TimeoutExpired:
        SCons.Warnings.warn(SCons.Warnings.ToolWarning,
                           "Swift version detection timed out")
    except FileNotFoundError:
        SCons.Warnings.warn(SCons.Warnings.ToolWarning,
                           f"Swift compiler '{swift}' not found")
    except Exception as e:
        SCons.Warnings.warn(SCons.Warnings.ToolWarning,
                           f"Failed to detect Swift version: {e}")
    return None

def cpp_header_generator(target, source, env):
    cmd = SCons.Util.CLVar(['$SHLINK', '$SHLINKFLAGS'])

    return ["$SWIFTMODULECOM", "$SWIFTMODULECOMSTR"]


def generate(env) -> None:
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

    # Detect Swift compiler
    if "SWIFT" not in env:
        env["SWIFT"] = env.Detect(compilers) or compilers[0]

    # Basic Swift variables
    env["SWIFTFLAGS"] = SCons.Util.CLVar("")
    env["SWIFTPATH"] = SCons.Util.CLVar("")
    
    # Module search path support
    env["SWIFTMODULEPATH"] = SCons.Util.CLVar("")
    env["SWIFTMODULEPREFIX"] = "-I "
    env["SWIFTMODULESUFFIX"] = ""
    env["_SWIFTMODULEFLAGS"] = "$( ${_concat(SWIFTMODULEPREFIX, SWIFTMODULEPATH, SWIFTMODULESUFFIX, __env__, RDirs, TARGET, SOURCE)} $)"

    # Swift-specific import resolution
    env["SWIFTIMPORTS"] = SCons.Util.CLVar("")
    env["SWIFTIMPORTPREFIX"] = "-import-objc-header "
    env["SWIFTIMPORTSUFFIX"] = ""
    env["_SWIFTIMPORTFLAGS"] = "${_concat(SWIFTIMPORTPREFIX, SWIFTIMPORTS, SWIFTIMPORTSUFFIX, __env__)}"

    # C++ interoperability support
    env["SWIFT_CXX_INTEROP"] = False
    env["_SWIFT_CXX_INTEROP_FLAG"] = (
        '${SWIFT_CXX_INTEROP and "-cxx-interoperability-mode=default" or ""}'
    )

    # Include paths (-I flag)
    env["INCPREFIX"] = "-I "
    env["INCSUFFIX"] = ""
    env["_SWIFTINCFLAGS"] = (
        "$( ${_concat(INCPREFIX, SWIFTPATH, INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)"
    )

    # Framework paths (-F flag)
    env["FRAMEWORKPREFIX"] = "-F "
    env["FRAMEWORKSUFFIX"] = ""
    env["_SWIFTFRAMEWORKPATH"] = (
        "$( ${_concat(FRAMEWORKPREFIX, FRAMEWORKPATH, FRAMEWORKSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)"
    )

    # Library paths (-L flag)
    env["SWIFTLIBDIRPREFIX"] = "-L "
    env["SWIFTLIBDIRSUFFIX"] = ""
    env["_SWIFTLIBFLAGS"] = (
        "$( ${_concat(SWIFTLIBDIRPREFIX, LIBPATH, SWIFTLIBDIRSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)"
    )

    # Common flags for both static and shared compilation
    env["_SWIFTCOMCOM"] = (
        "$_SWIFTINCFLAGS $_SWIFTMODULEFLAGS $_SWIFTFRAMEWORKPATH $_SWIFTLIBFLAGS $_SWIFT_CXX_INTEROP_FLAG $_SWIFT_EMIT_CXX_HEADER_FLAG $_SWIFTIMPORTFLAGS $_SWIFTOPTFLAG $_SWIFTWMOFLAG"
    )

    # Static object compilation
    env["SWIFTCOM"] = (
        "cd ${TARGET.dir} && $SWIFT -c -parse-as-library ${SOURCES.abspath} -o ${TARGET.file} $SWIFTFLAGS $_SWIFTCOMCOM"
    )

    # Shared object compilation (with -emit-object)
    env["SWIFTSH"] = "$SWIFT"
    env["SWIFTSHFLAGS"] = SCons.Util.CLVar("$SWIFTFLAGS")
    env["SWIFTSHCOM"] = (
        "cd ${TARGET.dir} && $SWIFTSH -c -parse-as-library ${SOURCES.abspath} -o ${TARGET.file} -emit-object $SWIFTSHFLAGS $_SWIFTCOMCOM"
    )

    # Object file suffixes
    env["SWIFTOBJSUFFIX"] = ".o"
    env["SWIFTSHOBSUFFIX"] = ".os"

    # Whole module optimization support
    env["SWIFTWMO"] = False
    env["_SWIFTWMOFLAG"] = '${SWIFTWMO and "-whole-module-optimization" or ""}'

    # Library builder for Swift
    env["SWIFTLIBCOM"] = (
        "$SWIFT -emit-library -o $TARGET $SOURCES $SWIFTLIBFLAGS $_SWIFTCOMCOM"
    )
    env["SWIFTLIBFLAGS"] = SCons.Util.CLVar("")

    # Executable builder for Swift
    env["SWIFTEXECOM"] = "$SWIFT -o $TARGET $SOURCES $SWIFTEXEFLAGS $_SWIFTCOMCOM"
    env["SWIFTEXEFLAGS"] = SCons.Util.CLVar("")

    # Set up platform-specific flags
    if env["PLATFORM"] == "darwin":
        # macOS/iOS specific flags
        env["SWIFTSHLIBSUFFIX"] = ".dylib"
        env.AppendUnique(SWIFTFLAGS=["-sdk", "$SDKROOT"])
        if not env.get("SDKROOT"):
            import subprocess

            try:
                result = subprocess.run(
                    ["xcrun", "--show-sdk-path"], 
                    capture_output=True, 
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    env["SDKROOT"] = result.stdout.strip()
            except:
                pass

        # Add Swift runtime libraries for C++ interop
        if env.get("SWIFT_CXX_INTEROP"):
            # Find Swift toolchain
            try:
                result = subprocess.run(
                    ["xcrun", "--find", "swift"], 
                    capture_output=True, 
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    swift_path = result.stdout.strip()
                    swift_lib_dir = swift_path.replace(
                        "/bin/swift", "/lib/swift/macosx"
                    )
                    env.AppendUnique(LIBPATH=[swift_lib_dir])
                    env.AppendUnique(LIBS=["swiftCore"])
            except:
                pass
    
    elif env["PLATFORM"] == "win32":
        # Windows specific configuration
        env["SWIFTSHLIBSUFFIX"] = ".dll"
        env["SWIFTOBJSUFFIX"] = ".obj"
        env["SWIFTSHOBSUFFIX"] = ".obj"
        # Windows Swift uses different flags
        env.AppendUnique(SWIFTFLAGS=["-sdk", env.get("SDKROOT", "Windows.sdk")])
    
    else:  # Linux and other Unix-like systems
        env["SWIFTSHLIBSUFFIX"] = ".so"
        # Linux Swift configuration
        env.AppendUnique(SWIFTFLAGS=["-sdk", env.get("SDKROOT", "/")])
        # On Linux, we might need to link against dispatch and Foundation
        if env.get("SWIFT_CXX_INTEROP"):
            env.AppendUnique(LIBS=["swiftCore", "dispatch", "Foundation"])


def exists(env):
    """Check if Swift compiler exists"""
    return env.Detect(compilers)
