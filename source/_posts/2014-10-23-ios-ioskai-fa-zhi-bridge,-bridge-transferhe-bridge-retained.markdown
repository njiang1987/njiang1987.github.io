---
layout: post
title: "[iOS]IOS开发之__bridge，__bridge_transfer和__bridge_retained"
date: 2014-10-23 14:18:25 +0800
comments: true
categories: iOS
---
##Core Foundation 框架
Core Foundation框架 (CoreFoundation.framework) 是一组C语言接口，它们为iOS应用程序提供基本数据管理和服务功能。下面列举该框架支持进行管理的数据以及可提供的服务：

1. 群体数据类型 (数组、集合等)
2. 程序包
3. 字符串管理
4. 日期和时间管理
5. 原始数据块管理
6. 偏好管理
7. URL及数据流操作
8. 线程和RunLoop
9. 端口和soket通讯

Core Foundation框架和Foundation框架紧密相关，它们为相同功能提供接口，但Foundation框架提供Objective-C接口。如果您将Foundation对象和Core Foundation类型掺杂使用，则可利用两个框架之间的 “toll-free bridging”。所谓的Toll-free bridging是说您可以在某个框架的方法或函数同时使用Core Foundatio和Foundation 框架中的某些类型。很多数据类型支持这一特性，其中包括群体和字符串数据类型。每个框架的类和类型描述都会对某个对象是否为 toll-free bridged，应和什么对象桥接进行说明。
如需进一步信息，请阅读Core Foundation 框架参考。

自 Xcode4.2 开始导入ARC机制后，为了支持对象间的转型，Apple又增加了许多转型用的关键字。这一讲我们就来了解其用法，以及产生的理由。

###引子
我们先来看一下ARC无效的时候，我们写id类型转void*类型的写法：

```objc
id obj = [[NSObject alloc] init];
void *p = obj;
```
反过来，当把void*对象变回id类型时，只是简单地如下来写，

```objc
id obj = p;
[obj release];
```

但是上面的代码在ARC有效时，就有了下面的错误：

```objc
    error: implicit conversion of an Objective-C pointer
        to ’void *’ is disallowed with ARC
        void *p = obj;
                  ^
 
    error: implicit conversion of a non-Objective-C pointer
        type ’void *’ to ’id’ is disallowed with ARC
        id o = p;
                ^
```

###__bridge
为了解决这一问题，我们使用 __bridge 关键字来实现id类型与void*类型的相互转换。看下面的例子。

```objc
id obj = [[NSObject alloc] init];
void *p = (__bridge void *)obj;
id o = (__bridge id)p;
```

将Objective-C的对象类型用 __bridge 转换为 void* 类型和使用 __unsafe_unretained 关键字修饰的变量是一样的。被代入对象的所有者需要明确对象生命周期的管理，不要出现异常访问的问题。
除过 __bridge 以外，还有两个 __bridge 相关的类型转换关键字：

```objc
__bridge_transfer
__bridge_retained
```

接下来，我们将看看这两个关键字的区别。
 
###__bridge_retained
先来看使用 __bridge_retained 关键字的例子程序：

```objc
id obj = [[NSObject alloc] init];
void *p = (__bridge_retained void *)obj;
```

从名字上我们应该能理解其意义：类型被转换时，其对象的所有权也将被变换后变量所持有。如果不是ARC代码，类似下面的实现：

```objc
id obj = [[NSObject alloc] init];
void *p = obj;
[(id)p retain];
```

可以用一个实际的例子验证，对象所有权是否被持有。

```objc
void *p = 0;
{
    id obj = [[NSObject alloc] init];
    p = (__bridge_retained void *)obj;
}
NSLog(@"class=%@", [(__bridge id)p class]);
```

出了大括号的范围后，p 仍然指向一个有效的实体。说明他拥有该对象的所有权，该对象没有因为出其定义范围而被销毁。

###__bridge_transfer
相反，当想把本来拥有对象所有权的变量，在类型转换后，让其释放原先所有权的时候，需要使用__bridge_transfer 关键字。文字有点绕口，我们还是来看一段代码吧。

如果ARC无效的时候，我们可能需要写下面的代码。

```objc
// p 变量原先持有对象的所有权
id obj = (id)p;
[obj retain];
[(id)p release];
```

那么ARC有效后，我们可以用下面的代码来替换：

```objc
// p 变量原先持有对象的所有权
id obj = (__bridge_transfer id)p;
可以看出来，__bridge_retained 是编译器替我们做了 retain 操作，而 __bridge_transfer 是替我们做了 release1。
```

###Toll-Free bridged
在iOS世界，主要有两种对象：Objective-C 对象和 Core Foundation 对象0。Core Foundation 对象主要是有C语言实现的 Core Foundation Framework 的对象，其中也有对象引用计数的概念，只是不是 Cocoa Framework::Foundation Framework 的 retain/release，而是自身的 CFRetain/CFRelease 接口。

这两种对象间可以互相转换和操作，不使用ARC的时候，单纯的用C原因的类型转换，不需要消耗CPU的资源，所以叫做 Toll-Free bridged。比如 NSArray和CFArrayRef, NSString和CFStringRef，他们虽然属于不同的 Framework，但是具有相同的对象结构，所以可以用标准C的类型转换。

比如不使用ARC时，我们用下面的代码：

```objc
NSString *string = [NSString stringWithFormat:...];
CFStringRef cfString = (CFStringRef)string;
```

同样，Core Foundation类型向Objective-C类型转换时，也是简单地用标准C的类型转换即可。
但是在ARC有效的情况下，将出现类似下面的编译错误：

```objc
    Cast of Objective-C pointer type ‘NSString *’ to C pointer type ‘CFStringRef’ (aka ‘const struct __CFString *’) requires a bridged cast
    Use __bridge to convert directly (no change in ownership)
    Use __bridge_retained to make an ARC object available as a +1 ‘CFStringRef’ (aka ‘const struct __CFString *’)
```
    
错误中已经提示了我们需要怎样做：用 __bridge 或者 __bridge_retained 来转型，其差别就是变更对象的所有权。

正因为Objective-C是ARC管理的对象，而Core Foundation不是ARC管理的对象，所以才要特意这样转换，这与id类型向void*转换是一个概念。也就是说，当这两种类型（有ARC管理，没有ARC管理）在转换时，需要告诉编译器怎样处理对象的所有权。

上面的例子，使用 __bridge/__bridge_retained 后的代码如下：

```objc
NSString *string = [NSString stringWithFormat:...];
CFStringRef cfString = (__bridge CFStringRef)string;
```

只是单纯地执行了类型转换，没有进行所有权的转移，也就是说，当string对象被释放的时候，cfString也不能被使用了。

```objc
NSString *string = [NSString stringWithFormat:...];
CFStringRef cfString = (__bridge_retained CFStringRef)string;
...
CFRelease(cfString); // 由于Core Foundation的对象不属于ARC的管理范畴，所以需要自己release
```

使用 __bridge_retained 可以通过转换目标处（cfString）的 retain 处理，来使所有权转移。即使 string 变量被释放，cfString 还是可以使用具体的对象。只是有一点，由于Core Foundation的对象不属于ARC的管理范畴，所以需要自己release。

实际上，Core Foundation 内部，为了实现Core Foundation对象类型与Objective-C对象类型的相互转换，提供了下面的函数。

```cpp
CFTypeRef  CFBridgingRetain(id  X)  {
    return  (__bridge_retained  CFTypeRef)X;
}
 
id  CFBridgingRelease(CFTypeRef  X)  {
    return  (__bridge_transfer  id)X;
}
```

所以，可以用 CFBridgingRetain 替代 __bridge_retained 关键字：

```objc
NSString *string = [NSString stringWithFormat:...];
CFStringRef cfString = CFBridgingRetain(string);
...
CFRelease(cfString); // 由于Core Foundation不在ARC管理范围内，所以需要主动release。
```

###__bridge_transfer
所有权被转移的同时，被转换变量将失去对象的所有权。当Core Foundation对象类型向Objective-C对象类型转换的时候，会经常用到 __bridge_transfer 关键字。

```objc
CFStringRef cfString = CFStringCreate...();
NSString *string = (__bridge_transfer NSString *)cfString;
// CFRelease(cfString); 因为已经用 __bridge_transfer 转移了对象的所有权，所以不需要调用 release
```

同样，我们可以使用 CFBridgingRelease() 来代替 __bridge_transfer 关键字。

```objc
CFStringRef cfString = CFStringCreate...();
NSString *string = CFBridgingRelease(cfString);
```

###总结
由上面的学习我们了解到 ARC 中类型转换的用法，那么我们实际使用中按照怎样的原则或者方法来区分使用呢，下面我总结了几点关键要素。

明确被转换类型是否是 ARC 管理的对象

Core Foundation 对象类型不在 ARC 管理范畴内

Cocoa Framework::Foundation 对象类型（即一般使用到的Objectie-C对象类型）在 ARC 的管理范畴内
如果不在 ARC 管理范畴内的对象，那么要清楚 release 的责任应该是谁。

各种对象的生命周期是怎样的

1. 声明 id obj 的时候，其实是缺省的申明了一个 __strong 修饰的变量，所以编译器自动地加入了 retain 的处理，所以说 __bridge_transfer 关键字只为我们做了 release 处理。