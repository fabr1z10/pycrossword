#pragma once

#include "abstractnode.h"

class RandomRootNode : public AbstractNode {
public:
    RandomRootNode(const Grid& grid, const Dict& dict);
    void init() override;
    std::shared_ptr<AbstractNode> getNextDecision() override;
};