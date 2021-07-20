#include "randomrootnode.h"
#include "rand.h"
#include "treenode.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;

RandomRootNode::RandomRootNode(const Grid &grid, const Dict &dict) : AbstractNode(grid, dict) {}

void RandomRootNode::init() {
    py::print(" # init random node");
    updateData(0, m_height, 0, m_width);
    auto& r = Random::get();

    // After initializing, we want to rank the decisions. Each decision is a pair ((i,j), letter).
    // When we call evaluate, we get the current top of the queue, and generate a child node.
    // If the queue becomes empty, we return outcome = fail.

    // The strategy is to begin with cells with highest number of neighbors, ideally with 8 neighbors.
    // So let's rank cells by number of neighbors
    for (int i = 0; i < m_height; ++i) {
        for (int j = 0; j < m_width; ++j) {
            bool isCellBelowBlack = (i == m_height-1) || m_grid.isBlack(j, i+1);
            bool isCellRightBlack = (j == m_width-1) || m_grid.isBlack(j+1, i);
            if (isCellBelowBlack && isCellRightBlack) {
                m_decisions.push(Decision(i, j, 'a', r.getUniformReal(0.0f, 1.0f)));
                m_decisions.push(Decision(i, j, 'e', r.getUniformReal(0.0f, 1.0f)));
                m_decisions.push(Decision(i, j, 'i', r.getUniformReal(0.0f, 1.0f)));
                m_decisions.push(Decision(i, j, 'o', r.getUniformReal(0.0f, 1.0f)));
            }
        }
    }
    py::print("size of22 " + std::to_string(m_data.size()));

}

std::shared_ptr<AbstractNode> RandomRootNode::getNextDecision() {
    Decision nextDec = m_decisions.top();
    py::print(" # decision: " + nextDec.toString());
    m_decisions.pop();
    return std::make_shared<TreeNode>(*this, nextDec);
}