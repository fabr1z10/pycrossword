cmake_minimum_required(VERSION 3.3)

project(pycrossword)

include_directories(${PYBIND_INCLUDE_DIR})

pybind11_add_module(pycrossword params.cpp pycrossword.cpp rand.cpp decision.cpp ndict.cpp dict.cpp grid.cpp definition.cpp
        abstractnode.cpp randomrootnode.cpp treenode.cpp algo.cpp func.cpp)

configure_file(
        "${PROJECT_SOURCE_DIR}/setup.py.in"
        "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
)

configure_file(
        "${PROJECT_SOURCE_DIR}/install.sh"
        "${CMAKE_CURRENT_BINARY_DIR}/install.sh"
)

install(TARGETS pycrossword DESTINATION ${BIN_DIR})

install(CODE "execute_process(COMMAND ${CMAKE_CURRENT_BINARY_DIR}/install.sh)")