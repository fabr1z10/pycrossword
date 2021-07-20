#include "ndict.h"

NDict::NDict(int n) : m_size(0) {
    for (int i = 0; i < n; ++i) {
        m_sets.emplace_back(Compare(i));
    }
}

void NDict::addWord(const std::string& s) {
    for (auto& t : m_sets) {
        t.insert(s);
    }
    ++m_size;
}

int NDict::getNWords(const std::string& pattern) const {
    return getWords(pattern)->size();
}

std::unique_ptr<ICollection> NDict::getWords(const std::string& pattern) const {
    int first = -1;
    int last = -1;
    for (int i = 0; i < pattern.length(); ++i) {
        char c = pattern[i];
        if (c != '.' ) {
            if (first == -1) first = i;
            last = i;
        }
    }

    if (first == -1) {
        return std::make_unique<Coll<decltype(m_sets[0].begin())>>(m_sets[0].begin(), m_sets[0].end());
    }

    int holeStart = -1;
    for (int i = first+1; i < last && holeStart == -1; ++i){
        if (pattern[i] == '.') holeStart = i;
    }

    std::string patternStart(pattern);
    std::string patternEnd(patternStart);
    for (int i = 0; i < pattern.length(); ++i)
    {
        if (pattern[i] == '.') {
            patternStart[i] = 'a';
            patternEnd[i] = 'z';
        }
    }
    std::vector<std::string> ie;
    auto ee = ie.begin();
    auto p1 = m_sets[first].lower_bound(patternStart);
    auto p2 = m_sets[first].upper_bound(patternEnd);


    //NavigableSet<String> s = m_sets.get(first).subSet(patternStart.toString(), true, patternEnd.toString(), true);
    if (holeStart != -1) {
        std::vector<std::string> w;
        for (auto it = p1; it != p2; it++) {
            if (patternMatch(pattern, *it, holeStart, last)) {
                w.push_back(*it);
            }
        }
        return std::make_unique<Coll<decltype(w.begin())>>(w.begin(), w.end());
    } else {
        return std::make_unique<Coll<decltype(m_sets[0].begin())>>(p1, p2);
    }
}

bool NDict::patternMatch(const std::string pattern, const std::string word, int from, int to) const {
    if (word.length() != pattern.length())
        return false;
    for (int i = from; i <= to; ++i) {
        char c = pattern[i];
        if (c != '.' && c != word[i])
            return false;
    }
    return true;
}