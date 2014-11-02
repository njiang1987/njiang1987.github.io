---
layout: post
title: "Template Class - Symbols not found"
date: 2014-10-04 10:03:51 +0800
comments: true
categories: 技术
tags: C++
---
Detailed Explanation available from <http://www.parashift.com/c++-faq-lite/templates.html>

[35.12] Why can't I separate the definition of my templates class from its declaration and put it inside a .cpp file?

If all you want to know is how to fix this situation, read the next two FAQs. But in order to understand why things are the way they are, first accept these facts:

A template is not a class or a function. A template is a "pattern" that the compiler uses to generate a family of classes or functions.
In order for the compiler to generate the code, it must see both the template definition (not just declaration) and the specific types/whatever used to "fill in" the template. For example, if you're trying to use a Foo, the compiler must see both the Foo template and the fact that you're trying to make a specific Foo.
Your compiler probably doesn't remember the details of one .cpp file while it is compiling another .cpp file. It could, but most do not and if you are reading this FAQ, it almost definitely does not. BTW this is called the "separate compilation model."
Now based on those facts, here's an example that shows why things are the way they are. Suppose you have a template Foo defined like this:

```cpp
template<typename T>  
class Foo { 
public:
	Foo();
	void someMethod(T x);  
private:
    T x;  
};
```

Along with similar definitions for the member functions:

```cpp
template<typename T>
Foo<T>::Foo()
{
	...
}
template<typename T>
void Foo<T>::someMethod(T x)
{
   ...
}
```

Now suppose you have some code in file Bar.cpp that uses Foo:

```cpp
// Bar.cpp
void blah_blah_blah()
{
	...
	Foo<int> f;
	f.someMethod(5);
	...
 }
```

Clearly somebody somewhere is going to have to use the "pattern" for the constructor definition and for the someMethod() definition and instantiate those when T is actually int. But if you had put the definition of the constructor and someMethod() into file Foo.cpp, the compiler would see the template code when it compiled Foo.cpp and it would see Foo when it compiled Bar.cpp, but there would never be a time when it saw both the template code and Foo. So by rule #2 above, it could never generate the code for Foo::someMethod().

A note to the experts: I have obviously made several simplifications above. This was intentional so please don't complain too loudly. If you know the difference between a .cpp file and a compilation unit, the difference between a class template and a template class, and the fact that templates really aren't just glorified macros, then don't complain: this particular question/answer wasn't aimed at you to begin with. I simplified things so newbies would "get it," even if doing so offends some experts.

[35.13] How can I avoid linker errors with my template functions?

Tell your C++ compiler which instantiations to make while it is compiling your template function's .cpp file.

As an example, consider the header file foo.h which contains the following template function declaration:

```cpp
// File "foo.h"
template<typename T>
extern void foo();
```

Now suppose file foo.cpp actually defines that template function:

```cpp
// File "foo.cpp"
#include <iostream>
#include "foo.h"
template<typename T>
void foo()
{
   std::cout << "Here I am!\n";
}
```

Suppose file main.cpp uses this template function by calling foo():

```cpp
// File "main.cpp"
#include "foo.h"
int main()
{
	foo<int>();
	...
}
```

If you compile and (try to) link these two .cpp files, most compilers will generate linker errors. There are three solutions for this. The first solution is to physically move the definition of the template function into the .h file, even if it is not an inline function. This solution may (or may not!) cause significant code bloat, meaning your executable size may increase dramatically (or, if your compiler is smart enough, may not; try it and see).

The other solution is to leave the definition of the template function in the .cpp file and simply add the line template void foo(); to that file:

```cpp
// File "foo.cpp"
#include <iostream>
#include "foo.h"
template<typename T> void foo()
{
	std::cout << "Here I am!\n";
}
template void foo<int>();
```

If you can't modify foo.cpp, simply create a new .cpp file such as foo-impl.cpp as follows:

```cpp
// File "foo-impl.cpp"
#include "foo.cpp"
template void foo<int>();
```

Notice that foo-impl.cpp #includes a .cpp file, not a .h file.