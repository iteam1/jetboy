# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build

# Include any dependencies generated for this target.
include CMakeFiles/make_this_build_fail.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/make_this_build_fail.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/make_this_build_fail.dir/flags.make

CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o: CMakeFiles/make_this_build_fail.dir/flags.make
CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o: /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx/this_file_doesnt_compile.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o -c /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx/this_file_doesnt_compile.cpp

CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.i: cmake_force
	@echo "Preprocessing CXX source to CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx/this_file_doesnt_compile.cpp > CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.i

CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.s: cmake_force
	@echo "Compiling CXX source to assembly CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx/this_file_doesnt_compile.cpp -o CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.s

CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.requires:

.PHONY : CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.requires

CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.provides: CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.requires
	$(MAKE) -f CMakeFiles/make_this_build_fail.dir/build.make CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.provides.build
.PHONY : CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.provides

CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.provides.build: CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o


# Object files for target make_this_build_fail
make_this_build_fail_OBJECTS = \
"CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o"

# External object files for target make_this_build_fail
make_this_build_fail_EXTERNAL_OBJECTS =

libmake_this_build_fail.a: CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o
libmake_this_build_fail.a: CMakeFiles/make_this_build_fail.dir/build.make
libmake_this_build_fail.a: CMakeFiles/make_this_build_fail.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libmake_this_build_fail.a"
	$(CMAKE_COMMAND) -P CMakeFiles/make_this_build_fail.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/make_this_build_fail.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/make_this_build_fail.dir/build: libmake_this_build_fail.a

.PHONY : CMakeFiles/make_this_build_fail.dir/build

CMakeFiles/make_this_build_fail.dir/requires: CMakeFiles/make_this_build_fail.dir/this_file_doesnt_compile.cpp.o.requires

.PHONY : CMakeFiles/make_this_build_fail.dir/requires

CMakeFiles/make_this_build_fail.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/make_this_build_fail.dir/cmake_clean.cmake
.PHONY : CMakeFiles/make_this_build_fail.dir/clean

CMakeFiles/make_this_build_fail.dir/depend:
	cd /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/dlib/cmake_utils/test_for_avx /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build /home/jetboy/Workspace/robot-jetboy/init/dlib-19.23/build/temp.linux-aarch64-3.6/dlib_build/avx_test_build/CMakeFiles/make_this_build_fail.dir/DependInfo.cmake
.PHONY : CMakeFiles/make_this_build_fail.dir/depend

