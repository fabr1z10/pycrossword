#include "func.h"
#include "grid.h"
#include "randomrootnode.h"
#include "algo.h"
#include "params.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;

int makeCrossword(const Dict& dict, Grid& grid) {

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
            for (auto& m : grid.getAcross()) {
                auto word = algo->getResultNode()->getAcrossWord(m.second.icol, m.second.irow, m.second.length);
                py::print("--- ", word);
                auto clue = dict.getDefinition(word);
                m.second.word = word;
                m.second.clue = clue;
                py::print(m.first, " orizzontale: ", word, clue);
            }
            for (auto& m : grid.getDown()) {
                auto word = algo->getResultNode()->getDownWord(m.second.icol, m.second.irow, m.second.length);
                py::print("--- ", word);

                auto clue = dict.getDefinition(word);
                m.second.word = word;
                m.second.clue = clue;
                py::print(m.first, " verticale: ", word, clue);
            }
            return 0;
        }
    } while (result != 0 && attempt < maxAttempts);
    //py::print("unable to find solution.");
    return 1;
}