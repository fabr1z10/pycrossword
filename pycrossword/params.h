#pragma once

#include "singleton.h"

class Params : public Singleton<Params> {
private:
    friend class Singleton<Params>;
    Params();
public:
    int getMaxIter();
    int getRandomScore();
private:
    int m_maxIter;
    int m_randomScore;
};

inline int Params::getMaxIter() {
    return m_maxIter;
}

inline int Params::getRandomScore() {
    return m_randomScore;
}
