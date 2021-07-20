#include "func.h"
#include "grid.h"
#include "randomrootnode.h"
#include "algo.h"
#include "params.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;

void makeCrossword(const Dict& dict, const Grid& grid) {

    int result=0;
    int attempt = 0;
    int maxAttempts = 1;
    do {
        attempt += 1;
        auto node = std::make_shared<RandomRootNode>(grid, dict);
        auto algo = std::make_shared<Algo>(node, Params::get().getMaxIter());
        result = algo->start();
        if (result == 0) {
            // success
            py::print(algo->getResultNode()->toString());
            return;
        }
    } while (result != 0 && attempt < maxAttempts);
    py::print("unable to find solution.");
}