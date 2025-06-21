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

def swift_scan_func(node, env, path):
    """Scanner function to find Swift import dependencies"""
    # This is a simple scanner that looks for import statements
    # In a real implementation, this would parse Swift's dependency files
    imports = []
    contents = node.get_text_contents()
    
    # Look for import statements
    import_re = re.compile(r'^\s*import\s+(\w+)', re.MULTILINE)
    for match in import_re.finditer(contents):
        module_name = match.group(1)
        # Skip system modules
        if module_name not in ['Foundation', 'UIKit', 'SwiftUI', 'Darwin', 'Glibc']:
            imports.append(module_name)
    
    # Convert module names to potential file dependencies
    # This is simplified - real implementation would use Swift's module map
    deps = []
    for imp in imports:
        # Look for .swiftmodule files in the module path
        for dir in path:
            module_file = env.File(os.path.join(str(dir), imp + '.swiftmodule'))
            if module_file.exists():
                deps.append(module_file)
                break
    
    return deps

# Create Swift scanner
SwiftScanner = SCons.Scanner.Scanner(
    function = swift_scan_func,
    name = 'SwiftScanner',
    skeys = ['.swift'],
    path_function = SCons.Scanner.FindPathDirs('SWIFTMODULEPATH')
)


def _swift_emitter(target, source, env):
    """Add swiftmodule, swiftdoc, and swiftsourceinfo files to targets when building object files"""
    # Swift generates additional files alongside object files
    base = SCons.Util.splitext(str(target[0]))[0]

    # When C++ interop is enabled, Swift generates additional files
    if env.get("SWIFT_CXX_INTEROP"):
        # Add .swiftsourceinfo file for dependency tracking (as side effect)
        swiftsourceinfo = env.File(base + ".swiftsourceinfo")
        env.SideEffect(swiftsourceinfo, target)

        # Add generated C++ header if requested (as side effect)
        if env.get("SWIFT_EMIT_CXX_HEADER"):
            header_name = env.get("SWIFT_CXX_HEADER_NAME", base + "-Swift.h")
            # Generate the header in the same directory as the target
            header_dir = os.path.dirname(str(target[0]))
            if header_dir:
                cxx_header = env.File(os.path.join(header_dir, header_name))
            else:
                cxx_header = env.File(header_name)
            env.SideEffect(cxx_header, target)
            env.Clean(target, cxx_header)

    # Add module files if we're building a module (as side effects)
    if env.get("SWIFTMODULENAME"):
        module_name = env["SWIFTMODULENAME"]
        swiftmodule = env.File(base + ".swiftmodule")
        swiftdoc = env.File(base + ".swiftdoc")
        env.SideEffect([swiftmodule, swiftdoc], target)

    return target, source


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
    
    # Add Swift scanner
    env.Append(SCANNERS = SwiftScanner)

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
    env["SWIFT_EMIT_CXX_HEADER"] = False
    env["SWIFT_CXX_HEADER_NAME"] = ""
    env["_SWIFT_CXX_INTEROP_FLAG"] = (
        '${SWIFT_CXX_INTEROP and "-cxx-interoperability-mode=default" or ""}'
    )
    env["_SWIFT_EMIT_CXX_HEADER_FLAG"] = (
        '${SWIFT_EMIT_CXX_HEADER and "-emit-clang-header-path $SWIFT_CXX_HEADER_NAME" or ""}'
    )

    # Module support
    env["SWIFTMODULENAME"] = ""
    env["SWIFTMODULESUFFIX"] = ".swiftmodule"
    env["SWIFTDOCSUFFIX"] = ".swiftdoc"
    env["SWIFTSOURCEINFOSUFFIX"] = ".swiftsourceinfo"

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

    # Module builder for Swift
    env["SWIFTMODULECOM"] = (
        "$SWIFT -emit-module -module-name $SWIFTMODULENAME -o $TARGET $SOURCES $SWIFTMODULEFLAGS $_SWIFTCOMCOM"
    )
    env["SWIFTMODULEFLAGS"] = SCons.Util.CLVar("")

    # Executable builder for Swift
    env["SWIFTEXECOM"] = "$SWIFT -o $TARGET $SOURCES $SWIFTEXEFLAGS $_SWIFTCOMCOM"
    env["SWIFTEXEFLAGS"] = SCons.Util.CLVar("")
    
    # Swift Package Manager support
    env["SWIFTPM"] = env.Detect(["swift-build", "swift"]) or None
    env["SWIFTPMFLAGS"] = SCons.Util.CLVar("")
    env["SWIFTPMBUILDCOM"] = "$SWIFTPM build $SWIFTPMFLAGS"
    env["SWIFTPMTESTCOM"] = "$SWIFTPM test $SWIFTPMFLAGS"

    # Create Swift-specific builders

    # Swift Module Builder
    swift_module_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$SWIFTMODULECOM", "$SWIFTMODULECOMSTR"),
        suffix="$SWIFTMODULESUFFIX",
        src_suffix=SwiftSuffixes,
        single_source=0,
    )
    env["BUILDERS"]["SwiftModule"] = swift_module_builder

    # Swift Library Builder
    swift_lib_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$SWIFTLIBCOM", "$SWIFTLIBCOMSTR"),
        suffix="$SHLIBSUFFIX",
        src_suffix=SwiftSuffixes,
        single_source=0,
    )
    env["BUILDERS"]["SwiftLibrary"] = swift_lib_builder

    # Swift Program Builder
    swift_exe_builder = SCons.Builder.Builder(
        action=SCons.Action.Action("$SWIFTEXECOM", "$SWIFTEXECOMSTR"),
        suffix="$PROGSUFFIX",
        src_suffix=SwiftSuffixes,
        single_source=0,
    )
    env["BUILDERS"]["SwiftProgram"] = swift_exe_builder

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

    # Detect Swift version and set version-specific flags
    version = _detect_swift_version(env, env["SWIFT"])
    if version:
        env["SWIFTVERSION"] = version
        
        # Extract numeric version for feature detection
        version_match = re.match(r'(\d+)\.(\d+)(?:\.(\d+))?', str(version))
        if version_match:
            major = int(version_match.group(1))
            minor = int(version_match.group(2))
            
            # Enable version-specific features
            if major >= 5:
                # Swift 5.0+ features
                env["SWIFT_ASYNC_SUPPORT"] = True
                env["_SWIFT_ASYNC_FLAG"] = '${SWIFT_ASYNC_SUPPORT and "-enable-experimental-concurrency" or ""}'
                
                if minor >= 5:
                    # Swift 5.5+ has native async/await
                    env["_SWIFT_ASYNC_FLAG"] = ""  # No flag needed
                    
                if minor >= 7:
                    # Swift 5.7+ features
                    env["SWIFT_REGEX_SUPPORT"] = True
            
            if major >= 6:
                # Swift 6.0+ features (future)
                env["SWIFT_STRICT_CONCURRENCY"] = True
                env["_SWIFT_CONCURRENCY_FLAG"] = '${SWIFT_STRICT_CONCURRENCY and "-strict-concurrency=complete" or ""}'


def exists(env):
    """Check if Swift compiler exists"""
    return env.Detect(compilers)
