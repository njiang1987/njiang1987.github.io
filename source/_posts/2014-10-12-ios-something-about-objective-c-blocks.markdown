---
layout: post
title: "[iOS] Something about Objective-C Blocks (Editing)"
date: 2014-10-12 14:56:51 +0800
comments: true
categories: 技术
tags: iOS
---
## 1. Block基础知识

### 1.1 语法 
```objc
^(int event){
	printf("print something");
}
```

即`^ 返回值 参数列表 表达式`，其中返回值可省略。

### 1.2 有关Blocks自动变量

```objc
	__block int val = 0;
    void (^blk)() = ^{ val = 1;};
    blk();
    printf("val = %d\n", val);
```

若想再Block语法的表达式中将值复给在Block语法外声明的自动变量，需要在该自动变量上附加`__block`说明符。

### 1.3 函数指针与Block对比

函数指针定义：`int func (int count)( return count +1) ;  int (*funcptr)(int) = &func;`</br>
函数指针使用：`int result = (*funcptr)(10);`</br>
Blocks定义：`int (^blk)(int) = ^(int count){return count+1;};`</br>
Blocks使用：`int result = blk(10);`</br>

### 1.4 Block的实质

Block实际上是作为极普通的C语言源代码来处理的。通过支持Block的编译器，含有Block语法的源代码转换为一般的C语言编译器能够处理的源代码，并作为极为普通的C语言源代码被编译。运用Clang，通过`-rewrite-objc` 选项就能将含有Block语法的源代码变换为C++源代码（struct结构）。
`clang -rewrite-objc 源代码文件名`

```objc
#include <stdio.h>
int main()
{
	void (^blk)() = ^{printf("Block!\n");};
	blk();
	return 0;
}
```

转化以后为：

```cpp
//用来描述block的数据结构
struct __block_impl {
  void *isa;	//此处可以看出block被当做一个object来处理
  int Flags;
  int Reserved;
  void *FuncPtr;
};

//函数具体的数据结构描述
struct __main_block_impl_0 {
  struct __block_impl impl;
  struct __main_block_desc_0* Desc;
  __main_block_impl_0(void *fp, struct __main_block_desc_0 *desc, int flags=0) {
    impl.isa = &_NSConcreteStackBlock;
    impl.Flags = flags;
    impl.FuncPtr = fp;
    Desc = desc;
  }
};

//此处是block的具体实现，参数就是用来描述block的数据结构指针
static void __main_block_func_0(struct __main_block_impl_0 *__cself) {
	printf("Block!");
}

//用来描述block的数据结构
static struct __main_block_desc_0 {
  size_t reserved;
  size_t Block_size;
} __main_block_desc_0_DATA = { 0, sizeof(struct __main_block_impl_0)};


int main()
{
	//先声明了一个指向描述block的数据结构，参数分别是调用的函数具体实现以及描述数据结构
 	void (*blk)() = (void (*)())&__main_block_impl_0((void *)__main_block_func_0, &__main_block_desc_0_DATA);
 	//获取到block的数据结构以后，直接访问前面设置的函数指针，调用静态函数，参数就是上面得到的block的数据结构
 	((void (*)(__block_impl *))((__block_impl *)blk)->FuncPtr)((__block_impl *)blk);
 	return 0;
}
```

查了下runtime.h, `Class`即`struct objc_class*`的结构如下：

```c
struct objc_class {
    Class isa  OBJC_ISA_AVAILABILITY;
#if !__OBJC2__
    Class super_class                                        OBJC2_UNAVAILABLE;
    const char *name                                         OBJC2_UNAVAILABLE;
    long version                                             OBJC2_UNAVAILABLE;
    long info                                                OBJC2_UNAVAILABLE;
    long instance_size                                       OBJC2_UNAVAILABLE;
    struct objc_ivar_list *ivars                             OBJC2_UNAVAILABLE;
    struct objc_method_list **methodLists                    OBJC2_UNAVAILABLE;
    struct objc_cache *cache                                 OBJC2_UNAVAILABLE;
    struct objc_protocol_list *protocols                     OBJC2_UNAVAILABLE;
#endif
} OBJC2_UNAVAILABLE;
```

### 1.5 Writable Variables

用`__block`在block外部声明block内部使用的变量，全名叫`__block storage-class-specifier`。C语言中的`storage-class-specifier`还有`typedef`,`extern`,`static`,`auto`,`register`。例如

```objc
__block int val = 10;
void (^blk)(void) = ^{val = 1;};
```

转化以后的代码为：

```cpp
// 这个数据结构用来保存变量的，__forwarding指向自己的指针
struct __Block_byref_val_0 {
  void *__isa;
__Block_byref_val_0 *__forwarding;
 int __flags;
 int __size;
 int val;
};

// 这个就是block的数据结构
struct __main_block_impl_0 {
  struct __block_impl impl;
  struct __main_block_desc_0* Desc;
  __Block_byref_val_0 *val; // by ref
  __main_block_impl_0(void *fp, struct __main_block_desc_0 *desc, __Block_byref_val_0 *_val, int flags=0) : val(_val->__forwarding) {
    impl.isa = &_NSConcreteStackBlock;
    impl.Flags = flags;
    impl.FuncPtr = fp;
    Desc = desc;
  }
};

static void __main_block_func_0(struct __main_block_impl_0 *__cself) {
  __Block_byref_val_0 *val = __cself->val; // bound by ref
(val->__forwarding->val) = 1;}
static void __main_block_copy_0(struct __main_block_impl_0*dst, struct __main_block_impl_0*src) {_Block_object_assign((void*)&dst->val, (void*)src->val, 8/*BLOCK_FIELD_IS_BYREF*/);}

static void __main_block_dispose_0(struct __main_block_impl_0*src) {_Block_object_dispose((void*)src->val, 8/*BLOCK_FIELD_IS_BYREF*/);}

static struct __main_block_desc_0 {
  size_t reserved;
  size_t Block_size;
  void (*copy)(struct __main_block_impl_0*, struct __main_block_impl_0*);
  void (*dispose)(struct __main_block_impl_0*);
} __main_block_desc_0_DATA = { 0, sizeof(struct __main_block_impl_0), __main_block_copy_0, __main_block_dispose_0};
int main()
{
 __attribute__((__blocks__(byref))) __Block_byref_val_0 val = {(void*)0,(__Block_byref_val_0 *)&val, 0, sizeof(__Block_byref_val_0), 10};
 void (*blk)() = (void (*)())&__main_block_impl_0((void *)__main_block_func_0, &__main_block_desc_0_DATA, (__Block_byref_val_0 *)&val, 570425344);
 ((void (*)(__block_impl *))((__block_impl *)blk)->FuncPtr)((__block_impl *)blk);
 return 0;
}
```


