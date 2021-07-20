#pragma once

#include "dict.h"
#include "grid.h"
#include "decision.h"
#include <queue>

class CellInfo {
public:
    CellInfo(char letter, int horc, int vc);
    bool operator<(const CellInfo& other) const;
    char getLetter() const;
    int getScore() const;
private:
    char m_letter;
    int m_horCount;
    int m_vertCount;
    int m_score;
};

inline char CellInfo::getLetter() const {
    return m_letter;
}

inline int CellInfo::getScore() const {
    return m_score;
}

class AbstractNode {
public:
    AbstractNode(const Grid& grid, const Dict& dict);
    AbstractNode(const AbstractNode& parent);
    bool operator<(const AbstractNode& other) const;
    virtual void init() = 0;
    char getChar(int row, int col) const;
    void setChar(int row, int col, char c);
    void updateData (int rowStart, int h, int colStart, int w);
    std::string getSolution() const;
    int evaluate ();
    virtual std::shared_ptr<AbstractNode> getNextDecision();
    std::string toString() const;
    int getDepth() const;
    int getId() const;
protected:
    int m_id;
    static int g_id;
    int m_width;
    int m_height;
    const Grid& m_grid;
    std::priority_queue<Decision> m_decisions;
    std::vector<std::set<CellInfo>> m_data;

private:
    const Dict& m_dict;
    AbstractNode* m_parent;

    int m_size;
    int m_depth;
    std::string m_solution;
};

inline std::string AbstractNode::getSolution() const {
    return m_solution;
}

inline int AbstractNode::getDepth() const {
    return m_depth;
}

inline int AbstractNode::getId() const {
    return m_id;
}