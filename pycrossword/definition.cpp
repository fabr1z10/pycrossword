#include "definition.h"
#include <sstream>

std::string Definition::toString() const {
    std::stringstream str;
    str << "(" << irow << ", " << icol << ") " << id << (dir==Direction::ACROSS ? " across " : " down ") << ", offset = " << offset << ", len = " << length;
    return str.str();
}

std::string Definition::getId() const {
    std::stringstream stream;
    stream << id << (dir == Direction::ACROSS ? "a" : "d");
    return stream.str();
}
