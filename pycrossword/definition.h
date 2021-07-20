#pragma once

#include <string>

enum class Direction { ACROSS, DOWN };

struct Definition {
    Definition() = default;
    Definition(int id, int irow, int icol, int length, Direction d, int offset)
        : id(id), irow(irow), icol(icol), dir(d), offset(offset), length(length) {}
    std::string toString() const;
    int id;
    int irow;
    int icol;
    int length;
    Direction dir;
    int offset;

};