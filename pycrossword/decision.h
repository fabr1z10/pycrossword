#pragma once

#include <string>

class Decision {
public:
    Decision(int row, int col, char letter, double score);

    bool operator<(const Decision &other) const;
    int getRow() const;
    int getCol() const;
    char getLetter() const;
    double getScore() const;
    std::string toString() const;
private:
    int m_row;
    int m_col;
    char m_letter;
    double m_score;
};

inline int Decision::getRow() const {
    return m_row;
}

inline int Decision::getCol() const {
    return m_col;
}

inline char Decision::getLetter() const {
    return m_letter;
}

inline double Decision::getScore() const {
    return m_score;
}