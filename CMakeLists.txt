cmake_minimum_required(VERSION 3.3)

set(ROOT_VERSION 1)
set(MAJOR_VERSION 0)
set(MINOR_VERSION 0)
set(PATCH_VERSION 0)
set(VERSION ${ROOT_VERSION}.${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION})

set(BIN_DIR ${PROJECT_DIR}/bin)

set(PYBIND_INCLUDE_DIR ${PROJECT_DIR}/pybind11-2.7.0/include)

#set(BIN_DIR ${PROJECT_DIR}/bin)

set(CMAKE_CXX_STANDARD 17)


# source directory
add_subdirectory(pybind11-2.7.0)
add_subdirectory(pycrossword)
