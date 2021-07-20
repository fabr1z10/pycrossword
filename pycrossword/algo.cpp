#include "algo.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;
Algo::Algo(std::shared_ptr<AbstractNode> root, int maxIterations) : m_maxIter(maxIterations), m_resultNode(nullptr) {
    root->init();
    m_nodes.push(root);
}

int Algo::start() {

    // fetch the 1st leaf
    int iter = 0;
    while (!m_nodes.empty() && iter < m_maxIter) {
        iter++;
        py::print(std::to_string(iter));
        auto top = m_nodes.top();
        py::print(" # current node : id = " + std::to_string(top->getId()) + ", depth = " + std::to_string(top->getDepth()));
        py::print(top->toString());
        if (m_failures.count(top->getSolution())) {
            //System.out.println("Hey, I already know this!");
            m_nodes.pop();
        } else {
            auto outcome = top->evaluate();
            switch (outcome) {
                case 2:
                    m_failures.insert(top->getSolution());
                    m_nodes.pop();
                    break;
                case 1: {
                    auto child = top->getNextDecision();
                    // the node must be initialized here, otherwise it gets initialized again when backtracking!
                    child->init();
                    m_nodes.push(child);
                    py::print("new node has depth: " + std::to_string(child->getDepth()));
                    }
                    break;
                case 0:
                    m_resultNode = top;
                    //System.out.println("Success! after " + iter + " iterations.");
                    m_solution = m_resultNode->getSolution();
                    //top.Print();
                    py::print("found solution at iter: " + std::to_string(iter));
                    return 0;
            }
        }
    }
    return 1;
}