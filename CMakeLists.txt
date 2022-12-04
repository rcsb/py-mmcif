cmake_minimum_required(VERSION 2.8.12)
project(mmciflib)
#
# File: CMakeLists.txt -
# Date: 1-Aug-2017
#
# Updates:
#   8-Aug-2018 jdw fix Ubuntu loading problems
#
# C++ wrappers using  https://github.com/RosettaCommons/pybind11.git
#
if (POLICY CMP0048)
  # cmake warns if loaded from a min-3.0-required parent dir, so silence the warning:
  cmake_policy(SET CMP0048 NEW)
endif()
#
#
find_package(PythonInterp)
find_package(PythonLibs)
include_directories(${PYTHON_INCLUDE_DIRS})
message(STATUS "Python include path set to " ${PYTHON_INCLUDE_DIRS})
#
#  -- Build a wrapper library  --
#
if(${PYTHON_VERSION_STRING} VERSION_LESS "3.6")
  add_subdirectory("modules/pybind11_2_6_3_dev1")
else()
  add_subdirectory("modules/pybind11")  
endif()
#
#
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

#IF(NOT DEFINED ENV{RUN_FROM_DISUTILS})
#    set(CMAKE_VERBOSE_MAKEFILE ON)
#ENDIF()
#
#
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    # require at least gcc 4.8
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 4.8)
        message(FATAL_ERROR "GCC version must be at least 4.8!")
    endif()
    set(warnings " -Wall -Wno-unused-variable -Wno-unused-value -Wno-unused-but-set-variable -Wno-deprecated-declarations")
    # set(WRAPPER_DIR_EXT "Linux")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
     if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 8.1)
        message(FATAL_ERROR "Clang version must be at least 8.1!")
    endif()
    #set(warnings "-Wall -Wextra -Werror")
    set(warnings " -Wall -Wno-unused-variable -Wno-deprecated-declarations -Wno-register")
    #set(WRAPPER_DIR_EXT "Darwin")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    message(FATAL_ERROR "No current support for MSVC!")
    set(warnings "/W4 /WX /EHsc")
endif()
#
set(mydefines " -DBIG_ENDIAN_PLATFORM  -DHAVE_STRCASECMP -DINCL_TEMPLATE_SRC -DHAVE_PLACEMENT_NEW  ")
if (NOT CONFIGURED_ONCE)
    #set(CMAKE_CXX_FLAGS "${warnings} ${mydefines}  -fno-common -fvisibility=hidden -fvisibility-inlines-hidden -std=c++14  -flto "
    #    CACHE STRING "Flags used by the compiler during all build types." FORCE)
    #
    set(CMAKE_CXX_FLAGS "${warnings} ${mydefines}  -fno-common -fvisibility=hidden -fvisibility-inlines-hidden -std=c++11  -flto "
        CACHE STRING "Flags used by the compiler during all build types." FORCE)
    #
    set(CMAKE_C_FLAGS   "${warnings} ${mydefines}  -fPIC"
        CACHE STRING "Flags used by the compiler during all build types." FORCE)
    #
    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
        SET(CMAKE_AR  "gcc-ar")
        SET(CMAKE_CXX_ARCHIVE_CREATE "<CMAKE_AR> qcs <TARGET> <LINK_FLAGS> <OBJECTS>")
        SET(CMAKE_CXX_ARCHIVE_FINISH   true)
    endif()

endif()

message(STATUS "Compiler flags " ${CMAKE_CXX_FLAGS})

#
# ---------------------------------------------------------------
#   WHERE AM I RUNNING
#
message(STATUS "---CMAKE MODULE PATH - " ${CMAKE_MODULE_PATH})
message(STATUS "---CMAKE SOURCE DIR  - " ${CMAKE_SOURCE_DIR})
message(STATUS "---CMAKE PROJECT DIR - " ${PROJECT_SOURCE_DIR})
# ---------------------------------------------------------------
#
set(BUILD_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/src")
set(BUILD_INCLUDE_DIR "${CMAKE_CURRENT_BINARY_DIR}/include")
set(BUILD_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/bin")
set(BUILD_LIBRARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/lib")
#
#  Set the source module paths ---
#
#set(WRAP_DIR_1      "modules/cpp-core-mmciflib-wrapper-gen/src-${WRAPPER_DIR_EXT}")
set(WRAP_DIR_1      "modules/cpp-core-mmciflib-wrapper-gen/src")
#set(WRAP_INCL_DIR_1 "modules/cpp-core-mmciflib-wrapper-gen/include-binder")
#set(WRAP_INCL_BINDER_DIR_1 "modules/cpp-core-mmciflib-wrapper-gen/binder-mappers")

set(SOURCE_DIR_1 "modules/cpp-common/src")
set(INCLUDE_DIR_1 "modules/cpp-common/include")
#
set(SOURCE_DIR_2 "modules/cpp-tables/src")
set(INCLUDE_DIR_2 "modules/cpp-tables/include")

set(SOURCE_DIR_3 "modules/cc-regex/src")
set(INCLUDE_DIR_3 "modules/cc-regex/include")

set(SOURCE_DIR_4  "modules/cpp-cif-file/src")
set(INCLUDE_DIR_4 "modules/cpp-cif-file/include")

set(SOURCE_DIR_5  "modules/cpp-cif-file-util/src")
set(INCLUDE_DIR_5 "modules/cpp-cif-file-util/include")

set(SOURCE_DIR_6  "modules/cpp-dict-obj-file/src")
set(INCLUDE_DIR_6 "modules/cpp-dict-obj-file/include")

set(SOURCE_DIR_7  "modules/cpp-cif-parser/src")
set(INCLUDE_DIR_7 "modules/cpp-cif-parser/include")
#
set(SOURCE_TEST_DIR  "modules/cpp-mmciflib-test/src")
#
# ---------------------------------------------------------------
#
file(GLOB INC_1 "${INCLUDE_DIR_1}/*.h")
file(COPY ${INC_1} DESTINATION include)
file(COPY  "${SOURCE_DIR_1}/mapped_vector.C"     DESTINATION include)
file(COPY  "${SOURCE_DIR_1}/mapped_ptr_vector.C" DESTINATION include)
#
file(GLOB INC_2 "${INCLUDE_DIR_2}/*.h")
file(COPY ${INC_2} DESTINATION include)
#
file(GLOB INC_3 "${INCLUDE_DIR_3}/*.h" "${INCLUDE_DIR_3}/*.ih")
file(COPY ${INC_3} DESTINATION include)
#
file(GLOB INC_4 "${INCLUDE_DIR_4}/*.h")
file(COPY ${INC_4} DESTINATION include)

file(GLOB INC_5 "${INCLUDE_DIR_5}/*.h")
file(COPY ${INC_5} DESTINATION include)

file(GLOB INC_6 "${INCLUDE_DIR_6}/*.h")
file(COPY ${INC_6} DESTINATION include)

file(GLOB INC_7 "${INCLUDE_DIR_7}/*.h")
file(COPY ${INC_7} DESTINATION include)
#
#file(GLOB INC_8 "${WRAP_INCL_BINDER_DIR_1}/*.hpp")
#file(COPY ${INC_8} DESTINATION include)
#
file(MAKE_DIRECTORY ${BUILD_SOURCE_DIR})
file(MAKE_DIRECTORY ${BUILD_INCLUDE_DIR})
file(MAKE_DIRECTORY ${BUILD_BINARY_DIR})
file(MAKE_DIRECTORY ${BUILD_LIBRARY_DIR})
#
IF(NOT DEFINED ENV{RUN_FROM_DISUTILS})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY  ${BUILD_LIBRARY_DIR})
ENDIF()
#
#set(LIBRARY_OUTPUT_DIRECTORY        ${BUILD_LIBRARY_DIR})
#set(ARCHIVE_OUTPUT_DIRECTORY        ${BUILD_LIBRARY_DIR})
#
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY  ${BUILD_LIBRARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY  ${BUILD_BINARY_DIR})
#
# ---------------------------------------------------------------
install(DIRECTORY ${INCLUDE_DIR_1} DESTINATION include FILES_MATCHING PATTERN "*.h")
install(DIRECTORY ${INCLUDE_DIR_2} DESTINATION include FILES_MATCHING PATTERN "*.h")
install(DIRECTORY ${INCLUDE_DIR_3} DESTINATION include FILES_MATCHING PATTERN "*.h")
install(DIRECTORY ${INCLUDE_DIR_4} DESTINATION include FILES_MATCHING PATTERN "*.h")
#
install(FILES  "${SOURCE_DIR_1}/mapped_vector.C"     DESTINATION include)
install(FILES  "${SOURCE_DIR_1}/mapped_ptr_vector.C" DESTINATION include)
#
#
#  Build 'common' library
set(SOURCES_1
         "${SOURCE_DIR_1}/RcsbPlatform.C"
         "${SOURCE_DIR_1}/RcsbFile.C"
         "${SOURCE_DIR_1}/BlockIO.C"
         "${SOURCE_DIR_1}/CifString.C"
         "${SOURCE_DIR_1}/Serializer.C"
         "${SOURCE_DIR_1}/GenString.C"
         "${SOURCE_DIR_1}/GenCont.C"
         "${SOURCE_DIR_1}/Exceptions.C"
         "${SOURCE_DIR_1}/DataInfo.C"
         "${SOURCE_DIR_1}/mapped_vector.C"
         "${SOURCE_DIR_1}/mapped_ptr_vector.C")


add_library("common" OBJECT ${SOURCES_1})
target_include_directories("common" PUBLIC ${BUILD_INCLUDE_DIR})

#
#  Build 'tables' library
#

set(SOURCES_2
             "${SOURCE_DIR_2}/ISTable.C"
             "${SOURCE_DIR_2}/ITTable.C"
             "${SOURCE_DIR_2}/TTable.C"
             "${SOURCE_DIR_2}/TableFile.C")
#

add_library("tables" OBJECT ${SOURCES_2})
target_include_directories("tables" PUBLIC ${BUILD_INCLUDE_DIR})
#
#
#  Build 'regex' library
#

set(SOURCES_3
            "${SOURCE_DIR_3}/regcomp.c"
            "${SOURCE_DIR_3}/regexec.c"
            "${SOURCE_DIR_3}/regerror.c"
            "${SOURCE_DIR_3}/regfree.c")
#

add_library("regex" OBJECT ${SOURCES_3})
target_include_directories("regex" PUBLIC ${BUILD_INCLUDE_DIR})
#
#  Build 'cif-file' library
#

set(SOURCES_4
            "${SOURCE_DIR_4}/CifFile.C"
            "${SOURCE_DIR_4}/DicFile.C"
            "${SOURCE_DIR_4}/ParentChild.C"
            "${SOURCE_DIR_4}/CifParentChild.C"
            "${SOURCE_DIR_4}/CifDataInfo.C"
            "${SOURCE_DIR_4}/CifExcept.C")


add_library("cif-file" OBJECT ${SOURCES_4})
target_include_directories("cif-file" PUBLIC ${BUILD_INCLUDE_DIR})
#
#  Build 'cif-file-util' library
#

set(SOURCES_5
         "${SOURCE_DIR_5}/CifFileUtil.C"
         "${SOURCE_DIR_5}/CifCorrector.C"
           )


add_library("cif-file-util" OBJECT ${SOURCES_5})
target_include_directories("cif-file-util" PUBLIC ${BUILD_INCLUDE_DIR})

#
#  Build 'dict-obj-file' library
#

set(SOURCES_6
        "${SOURCE_DIR_6}/DictObjFileCreator.C"
        "${SOURCE_DIR_6}/DictObjFileReader.C"
        "${SOURCE_DIR_6}/DictObjContInfo.C"
        "${SOURCE_DIR_6}/DictObjCont.C"
        "${SOURCE_DIR_6}/DictObjFile.C"
        "${SOURCE_DIR_6}/DictDataInfo.C"
        "${SOURCE_DIR_6}/DictParentChild.C"
           )


add_library("dict-obj-file"  OBJECT ${SOURCES_6})
target_include_directories("dict-obj-file" PUBLIC ${BUILD_INCLUDE_DIR})
#
#  Build 'cif-parser' library
#


find_package(FLEX)
find_package(BISON)
#
flex_target(flextarget1 "${SOURCE_DIR_7}/CifScanner.l"  "${BUILD_SOURCE_DIR}/CifScanner.c" COMPILE_FLAGS "-Cfr -L -Pcifparser_")
flex_target(flextarget2 "${SOURCE_DIR_7}/DICScanner.l"  "${BUILD_SOURCE_DIR}/DICScanner.c" COMPILE_FLAGS "-Cfr -L -Pdicparser_")

bison_target(bisontarget1 "${SOURCE_DIR_7}/CifParser.y"  "${BUILD_SOURCE_DIR}/CifParser.c" COMPILE_FLAGS "-d -v -l -p cifparser_")
bison_target(bisontarget2 "${SOURCE_DIR_7}/DICParser.y"  "${BUILD_SOURCE_DIR}/DICParser.c" COMPILE_FLAGS "-d -v -l -p dicparser_")

add_flex_bison_dependency(flextarget1 bisontarget1)
add_flex_bison_dependency(flextarget2 bisontarget2)


set(SOURCES_7
             "${SOURCE_DIR_7}/CifFileReadDef.C"
             "${BUILD_SOURCE_DIR}/CifParser.c"
             "${BUILD_SOURCE_DIR}/CifScanner.c"
             "${SOURCE_DIR_7}/CifScannerBase.C"
             "${SOURCE_DIR_7}/CifParserBase.C"
             "${BUILD_SOURCE_DIR}/DICScanner.c"
             "${SOURCE_DIR_7}/DICScannerBase.C"
             "${BUILD_SOURCE_DIR}/DICParser.c"
             "${SOURCE_DIR_7}/DICParserBase.C"
           )

add_library("cif-parser" OBJECT ${SOURCES_7})
target_include_directories("cif-parser" PUBLIC ${BUILD_INCLUDE_DIR} ${BUILD_SOURCE_DIR})
#
# Combine the all object into consolidated library  'mmciflib-all'
#
add_library("mmciflib-all" STATIC
            "$<TARGET_OBJECTS:common>"
            "$<TARGET_OBJECTS:tables>"
            "$<TARGET_OBJECTS:regex>"
            "$<TARGET_OBJECTS:cif-parser>"
            "$<TARGET_OBJECTS:dict-obj-file>"
            "$<TARGET_OBJECTS:cif-file>"
            "$<TARGET_OBJECTS:cif-file-util>"
            )
#
#  -- Build a test application binary to verify the completeness of the library--
#
add_executable("mmcif_reader_test_1" "${SOURCE_TEST_DIR}/CifReader.C")
target_link_libraries("mmcif_reader_test_1" "mmciflib-all")
target_include_directories("mmcif_reader_test_1" PUBLIC ${BUILD_INCLUDE_DIR})
#
#  -- Build a wrapper library  --
#
#add_subdirectory("modules/pybind11")
#
file(GLOB_RECURSE WRAP_SRC_FILES "${WRAP_DIR_1}/*.cpp")
#file(GLOB_RECURSE EXC_FILES "${WRAP_DIR_1}/std/vector.cpp")
# list(REMOVE_ITEM WRAP_SRC_FILES ${EXC_FILES})
#
pybind11_add_module("mmciflib" ${WRAP_SRC_FILES})
target_include_directories("mmciflib" PUBLIC ${BUILD_INCLUDE_DIR} )
target_link_libraries("mmciflib" PUBLIC "mmciflib-all")
#
IF(NOT DEFINED ENV{RUN_FROM_DISUTILS})
    message(STATUS "Source directory 1 " ${SOURCE_DIR_1})
    message(STATUS "Include directory 1 " ${INCLUDE_DIR_1})
    message(STATUS "SOURCE_1 LIST " ${SOURCES_1})
    message(STATUS "Source directory 2 " ${SOURCE_DIR_2})
    message(STATUS "Include directory 2 " ${INCLUDE_DIR_2})
    message(STATUS "SOURCE_2 LIST " ${SOURCES_2})
    message(STATUS "Source directory 3 " ${SOURCE_DIR_3})
    message(STATUS "Include directory 3 " ${INCLUDE_DIR_3})
    message(STATUS "SOURCE_3 LIST " ${SOURCES_3})
    message(STATUS "Source directory 4 " ${SOURCE_DIR_4})
    message(STATUS "Include directory 4 " ${INCLUDE_DIR_4})
    message(STATUS "SOURCE_4 LIST " ${SOURCES_4})
    message(STATUS "Source directory 5 " ${SOURCE_DIR_5})
    message(STATUS "Include directory 5 " ${INCLUDE_DIR_5})
    message(STATUS "SOURCE_5 LIST " ${SOURCES_5})
    message(STATUS "Source directory 6 " ${SOURCE_DIR_6})
    message(STATUS "Include directory 6 " ${INCLUDE_DIR_6})
    message(STATUS "SOURCE_6 LIST " ${SOURCES_6})
    message(STATUS "Source directory 7 " ${SOURCE_DIR_7})
    message(STATUS "Include directory 7 " ${INCLUDE_DIR_7})
    message(STATUS "SOURCE_7 LIST " ${SOURCES_7})
    message(STATUS, "---WRAPPER SOURCE ${WRAP_DIR_1} INITIAL FILE LIST " ${WRAP_SRC_FILES})
    message(STATUS, "---EXCLUDING FILE " ${EXC_FILES})
    message(STATUS, "---WRAPPER SOURCE FINAL FILE LIST " ${WRAP_SRC_FILES})
ENDIF()
#
message(STATUS, "---ALL DONE WITH CMAKE")
#
