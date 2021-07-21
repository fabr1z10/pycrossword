#pragma once

#include <string>
#include <unordered_map>
#include "ndict.h"

class Dict {
public:
    Dict(const std::string& dir, int maxLen = 10);
    int getWordCount() const;
    int getNWords(const std::string& pattern) const;
    std::vector<std::string> getWords(const std::string& pattern) const;
private:
    int addWord(const std::string& word);
    int m_wordCount;
	int m_defCount;
    // the maximum length allowed for a word
    int m_maxLength;
    mutable std::unordered_map<std::string, int> m_cache;
    std::vector<NDict> m_ndicts;
};

inline int Dict::getWordCount() const {
    return m_wordCount;
}