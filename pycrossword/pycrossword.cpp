#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "grid.h"
#include "dict.h"
#include "func.h"
#include "abstractnode.h"

namespace py = pybind11;

PYBIND11_MODULE(pycrossword, m) {
    m.doc() = "pycrossword plugin"; // optional module docstring

    py::class_<Definition>(m, "Clue")
        .def_property_readonly("x", &Definition::getX)
        .def_property_readonly("y", &Definition::getY)
        .def_property_readonly("len", &Definition::getLen)
        .def_property_readonly("word", &Definition::getWord)
        .def_property_readonly("clue", &Definition::getClue)
        .def_property_readonly("id", &Definition::getId);


    py::class_<Dict>(m, "Dict")
            .def(py::init<const std::string&, int>())
            .def_property_readonly("word_count", &Dict::getWordCount)
            .def("get_words", &Dict::getWords)
            .def("get_wc", &Dict::getNWords);


    py::class_<Grid>(m, "Grid")
            .def(py::init<int, int, const std::vector<int> &>())
            .def_property_readonly("width", &Grid::getWidth)
            .def_property_readonly("height", &Grid::getHeight)
            .def_property_readonly("size", &Grid::getSize)
            .def("isBlack", &Grid::isBlack)
            .def("getAcross", &Grid::getAcrossDefAt, py::return_value_policy::reference)
            .def("getDown", &Grid::getDownDefAt, py::return_value_policy::reference);



    m.def("make", &makeCrossword, "Creates a new crossword gith a given grid");
//    py::class_<AbstractNode>(m, "Node")
//            .def(py::init<const Grid&, const Dict&>());


}