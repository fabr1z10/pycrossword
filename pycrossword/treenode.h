#pragma once

#include "abstractnode.h"
#include "decision.h"

class TreeNode : public AbstractNode {
public:
    TreeNode (const AbstractNode& parent, const Decision& d);
    void init() override;

private:
    Decision m_decision;
};