---
layout: post
title: "C++ CookBook读书笔记"
date: 2014-10-06 11:25:17 +0800
comments: true
categories: 
---
1. C++创建静态库

```cpp
g++ -c -o john.o john.cpp
g++ -c -o paul.o paul.cpp
g++ -c -o johnpaul.o johnpaul.cpp
ar ru libjohnpaul.a john.o paul.o johnpaul.o
ranlib libjohnpaul.a
```

2. 使用预定义宏进行条件编译

```cpp
#ifdef _WIN32
#	include <windows.h>
#else	\\ not windows
#	include <sys/stat.h>
#endif
```

3. 使源文件自动链接到指定的库

```cpp
#ifndef JOHNPAUL_HPP_INCLUDED
#define JOHNPAUL_HPP_INCLUDED
#prama comment(lib, "libjohnpaul")	// 静态库
#endif
```

4. 包含一个内联文件

```cpp
#ifndef VALUE_H_
#define VALUE_H_

#include <string>

class Value
{
public:
	Value(const std::string& val): val_(val){}
	std::string getVal() const;
private:
	std::string val_;
};

#include "Value.inl"

#endif

// Value.inl
inline std::string Value::getVal() const
{
	return (val_);
}
```