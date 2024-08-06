cmake_minimum_required(VERSION 3.10)

project(mips-simulator)

add_executable(mips-simulator src/main.cpp)

target_include_directories(mips-simulator PUBLIC ${PROJECT_SOURCE_DIR}/include)

enable_testing()

add_subdirectory(libs/googletest)

include_directories(libs/googletest/include)

add_executable(myTest tests/test.c++)

target_link_libraries(myTest PRIVATE gtest)

include(GoogleTest)

gtest_discover_tests(myTest)