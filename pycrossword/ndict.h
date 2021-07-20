#pragma once

#include <vector>
#include <set>
#include <string>
#include <memory>

// dictionary of words with N letters

class ICompare {
public:
    virtual bool operator() (const std::string& a, const std::string& b) const = 0;
};


class Compare {
public:
    Compare(int letter) : m_letter(letter) {}
    bool operator() (const std::string& a, const std::string& b) const {
        int i = m_letter;
        int n = a.length();
        while (i < n) {
            if (a[i] < b[i]) {
                return true;
            } else if (a[i] > b[i]) {
                return false;
            }
            ++i;
        }
        for (i = 0; i < n; ++i) {
            if (a[i] < b[i]) {
                return true;
            } else if (a[i] > b[i]) {
                return false;
            }
        }
        return false;
    }
private:
    int m_letter;
};


class ICollection {
public:
    virtual ~ICollection() = default;
    virtual size_t size() const = 0;
    virtual std::vector<std::string> toVec() const = 0;

};

template<typename T>
class Coll : public ICollection {
public:
    Coll(T begin, T end, size_t s = -1) : m_begin(begin), m_end(end), m_size(s) {}
    size_t size() const override {
        if (m_size != -1) {
            return m_size;
        }
        m_size = 0;
        auto it = m_begin;
        while (it != m_end) {
            it++;
            m_size++;
        }
        return m_size;
    };
    std::vector<std::string> toVec() const override {
        std::vector<std::string> out;
        for (auto it = m_begin; it != m_end; it++) {
            out.push_back(*it);
        }
        return out;
    }

private:
    mutable size_t m_size;
    T m_begin;
    T m_end;
};

class NDict {
public:
    NDict(int n);
    void addWord(const std::string&);
    std::unique_ptr<ICollection> getWords(const std::string&) const;
    int getNWords(const std::string& pattern) const;
    bool patternMatch (const std::string pattern, const std::string word, int from ,int to) const;
private:
    int m_size;
    std::vector <std::set<std::string, Compare>> m_sets;
};