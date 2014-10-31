---
layout: post
title: "auto_ptr的实现及CTCI"
date: 2014-09-03 21:47:49 +0800
comments: true
categories: C++
---

1. 代码是参考auto_ptr的真实实现，其实大部分都一样，只是自己实现了一遍。

```cpp
template <class T>
class auto_ptr_t {
private:
    T* __ptr;
    
public:

	/*
	* Use a T pointer to init the auto_ptr
	*/
    inline explicit auto_ptr_t(T* __t = 0) {__ptr = __t;}
    inline ~auto_ptr_t() {delete __ptr;}
    inline T* release() { T* __tmp = __ptr; __ptr = NULL; return __tmp; }
    inline void reset(T* __t)
    {
        if (__ptr != __t)
            delete __ptr;
        __ptr = __t;
    }
    
    inline auto_ptr_t& operator=(auto_ptr_t& __t)
    {
        reset(__t.release());
        return *this;
    }
    
    template<class __up> inline auto_ptr_t& operator=(auto_ptr_t<__up>& __p)
    {
        reset(__p.release());
        return *this;
    }
    
    inline auto_ptr_t& operator=(auto_ptr_ref<T> __p)
    {
        reset(__p.release());
        return *this;
    }
    
    inline T* operator->() { return __ptr; }
    inline T& operator*() {return *__ptr;}
    inline T* get() {return __ptr;}
    
    template<class __up> inline operator auto_ptr_t<__up>()
    {
        return auto_ptr_t<__up>(release());
    }
    
};
```