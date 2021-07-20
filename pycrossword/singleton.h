#pragma once

template<class T>
class Singleton
{
public:
    static T & get()
    {
        static T instance;
        return instance;
    }
protected:
    Singleton() = default;
public:
    Singleton(const Singleton&) = delete;
    Singleton & operator=(Singleton const &) = delete;
};
