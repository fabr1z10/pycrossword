#pragma once

#include <string>

enum class Direction { ACROSS, DOWN };

struct Definition {
    Definition() = default;
    Definition(int id, int irow, int icol, int length, Direction d, int offset)
        : id(id), irow(irow), icol(icol), dir(d), offset(offset), length(length) {}
    std::string toString() const;
    std::string getId() const;
    int id;
    int irow;
    int icol;
    int length;
    std::string word;
    std::string clue;
    Direction dir;
    int offset;
    int getX() const {
        return icol;
    }
    int getY() const {
        return irow;
    }
    int getLen() const {
        return length;
    }
    std::string getWord() const {
        return word;
    }
    std::string getClue() const {
        return clue;
    }

};