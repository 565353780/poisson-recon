cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
set(CMAKE_CXX_FLAGS "-std=c++17 -O0")
project(PoissonRecon)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Open3D REQUIRED)
if (Open3D_FOUND)
  message(STATUS "Found Open3D ${Open3D_VERSION}")
  link_directories(${Open3D_LIBRARY_DIRS})
  include_directories(${Open3D_INCLUDE_DIRS})
endif()

include_directories(${PROJECT_NAME} PRIVATE)

include_directories(./include)

file(GLOB_RECURSE SRC ./src/*.cpp)

add_executable(${PROJECT_NAME} ./src/main.cpp ${SRC})

target_link_libraries(${PROJECT_NAME} PRIVATE Open3D::Open3D)
