#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include "definition.h"

static const inline char WHITE = '.';
static const inline char BLACK = '#';


class Grid {
public:
    Grid (int, int, const std::vector<int>& black);
    int getWidth() const;
    int getHeight() const;
    int getSize() const;
    std::string getChars() const;
    bool isBlack(int x, int y) const;
    const Definition* getAcrossDefAt(int row, int col) const;
    const Definition* getDownDefAt(int row, int col) const;
private:
    char getChar(int row, int col) const;
    void setupDefinitions();
    void computeNeighboers();

    int m_width;
    int m_height;
    int m_size;
    std::string m_chars;
    std::vector<int> m_numbers;
    std::vector<int> m_horizontal;
    std::vector<int> m_vertical;
    std::vector<int> m_neighbors;

    std::unordered_map<int, Definition> across;
    std::unordered_map<int, Definition> down;
};

inline int Grid::getWidth() const {
    return m_width;
}

inline int Grid::getHeight() const {
    return m_height;
}

inline int Grid::getSize() const {
    return m_size;
}

inline std::string Grid::getChars() const {
    return m_chars;
}

inline bool Grid::isBlack(int x, int y) const {
    return m_chars[y * m_width + x] == BLACK;
}