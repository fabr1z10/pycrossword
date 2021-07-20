#pragma once

#include <queue>
#include <memory>
#include "abstractnode.h"

struct pointed_to_less {
    bool operator () (const std::shared_ptr<AbstractNode> &a, const std::shared_ptr<AbstractNode> &b) const { return !(*a < *b);}
};

class Algo {
public:
    Algo(std::shared_ptr<AbstractNode> root, int maxIterations);
    int start();
    const AbstractNode* getResultNode() const;
private:
    int m_maxIter;
    std::priority_queue<std::shared_ptr<AbstractNode>, std::vector<std::shared_ptr<AbstractNode>>, pointed_to_less> m_nodes;
    std::set<std::string> m_failures;
    std::shared_ptr<AbstractNode> m_resultNode;
    std::string m_solution;
};

inline const AbstractNode* Algo::getResultNode() const {
    return m_resultNode.get();
}