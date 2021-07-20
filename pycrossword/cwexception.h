#pragma once

#include <exception>
#include <string>

class CrossWordException : public std::exception
{
public:
    CrossWordException(const std::string& msg) : m_msg(msg) {}
    virtual const char* what() const throw()
    {
        return m_msg.c_str();
    }
private:
    std::string m_msg;
};