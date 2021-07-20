#include "decision.h"
#include <sstream>

Decision::Decision(int row, int col, char letter, double score) : m_row(row), m_col(col), m_score(score), m_letter(letter) {}

bool Decision::operator<(const Decision &other) const {
    if (m_score == other.m_score)
        return false;
    return m_score < other.m_score;
}

std::string Decision::toString() const {
    std::stringstream ss;
    ss << "place " << m_letter << " at (" << m_row << ", " << m_col << ")";
    return ss.str();
}