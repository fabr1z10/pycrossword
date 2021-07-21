#include "dict.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include "cwexception.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;


Dict::Dict(const std::string& filename, int maxLen) : m_wordCount(0), m_defCount(0), m_maxLength(maxLen) {
    for (int n = 2; n <= m_maxLength; ++n) {
        m_ndicts.push_back(NDict(n));
    }

	std::ifstream file(filename.c_str());
    std::string line;
    while (std::getline(file, line)) {
		size_t commaPos = line.find(',');
		if (commaPos == std::string::npos) {
			throw CrossWordException("Error parsing: " + line);
		}
		m_defCount += addWord(line.substr(0, commaPos));
    }

    for (const auto& n : m_ndicts) {
    	m_wordCount += n.getSize();
    }

    py::print("Loaded " + std::to_string(m_wordCount) + " words and " + std::to_string(m_defCount) + " definitions.");

}

int Dict::addWord(const std::string &word) {
    //    m_wordCount++;
    auto l = word.length();
    if (l <= m_maxLength && l > 1) {
        m_ndicts[l - 2].addWord(word);
        return 1;
    }
    return 0;
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