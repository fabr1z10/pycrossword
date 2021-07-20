#pragma once

#include "singleton.h"
#include <random>
#include <memory>

class Random : public Singleton<Random> {
private:
    friend class Singleton<Random>;
    Random();
public:
    int getUniform (int min, int max);
    float getUniformReal (float min, float max);
private:
    std::unique_ptr<std::mt19937> m_gen;
};