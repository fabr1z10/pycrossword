#include "dict.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include "cwexception.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;


Dict::Dict(const std::string& directory, int maxLen) : m_wordCount(0), m_maxLength(maxLen) {
    for (int n = 2; n <= m_maxLength; ++n) {
        m_ndicts.push_back(NDict(n));
    }

    std::stringstream mdir;
    mdir << directory;
    if (directory.back() != '/')
        mdir << "/";
    mdir << "words/";
    for (char c = 'a'; c <= 'z'; ++c) {
        std::stringstream ss;
        ss << mdir.str() << c << ".txt";
        std::ifstream file(ss.str().c_str());
        //py::print(" # opening " + ss.str());
        if (!file.good()) {
            throw CrossWordException("Cannot open " + ss.str());
        }
        std::string line;
        while (std::getline(file, line)) {
            addWord(line);
        }
    }
}

void Dict::addWord(const std::string &word) {
    m_wordCount++;
    auto l = word.length();
    if (l <= m_maxLength && l > 1) {
        m_ndicts[l - 2].addWord(word);
    }
}

int Dict::getNWords(const std::string& pattern) const {
    // first, see if I already have this cached
    auto it = m_cache.find(pattern);
    if (it == m_cache.end()) {
        int l = pattern.length();
        if (l <= m_maxLength) {
            int n = m_ndicts[l - 2].getNWords(pattern);
            m_cache[pattern] = n;
            return n;
        }
        return 0;
    }
    return it->second;

}

std::vector<std::string> Dict::getWords(const std::string& pattern) const {
    int l = pattern.length();
    if (l <= m_maxLength) {
        auto n = m_ndicts[l - 2].getWords(pattern);
        return n->toVec();
    }
    return std::vector<std::string>();
}