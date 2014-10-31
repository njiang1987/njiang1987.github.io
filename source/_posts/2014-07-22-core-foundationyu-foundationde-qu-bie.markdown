---
layout: post
title: "Core Foundation与Foundation的区别"
date: 2014-07-22 20:03:39 +0800
comments: true
categories: Core-Foundation Foundation Bridge
---
Core Foundation框架 (CoreFoundation.framework) 是一组C语言接口，它们为iOS应用程序提供基本数据管理和服务功能。下面列举该框架支持进行管理的数据以及可提供的服务：

- 群体数据类型 (数组、集合等)
- 程序包
- 字符串管理
- 日期和时间管理
- 原始数据块管理
- 偏好管理
- URL及数据流操作
- 线程和RunLoop
- 端口和soket通讯

Core Foundation框架和Foundation框架紧密相关，它们为相同功能提供接口，但Foundation框架提供Objective-C接口。如果您将Foundation对象和Core Foundation类型掺杂使用，则可利用两个框架之间的 “toll-free bridging”。所谓的Toll-free bridging是说您可以在某个框架的方法或函数同时使用Core Foundatio和Foundation框架中的某些类型。很多数据类型支持这一特性，其中包括群体和字符串数据类型。每个框架的类和类型描述都会对某个对象是否为 toll-free bridged，应和什么对象桥接进行说明。

###Objective-C指针与CoreFoundation指针之间的转换

ARC仅管理Objective-C指针（retain、release、autorelease），不管理CoreFoundation指针，CF指针由人工管理，手动的CFRetain和CFRelease来管理，注，CF中没有autorelease。

CocoaFoundation指针与CoreFoundation指针转换，需要考虑的是所指向对象所有权的归属。ARC提供了3个修饰符来管理。

1. __bridge，什么也不做，仅仅是转换。此种情况下：

	i). 从Cocoa转换到Core，需要人工CFRetain，否则，Cocoa指针释放后， 传出去的指针则无效。

	ii). 从Core转换到Cocoa，需要人工CFRelease，否则，Cocoa指针释放后，对象引用计数仍为1，不会被销毁。

2. __bridge_retained，转换后自动调用`CFRetain`，即帮助自动解决上述i的情形。

3. __bridge_transfer，转换后自动调用`CFRelease`，即帮助自动解决上述ii的情形。

由于ARC不能管理Core Foundation Object的生命周期，所以在Core Foundation和ARC之间，我们需要使用到`__bridge`,`__bridge_retained`和`__bridge_transfer`三个转换关键字。

根据苹果官方的文档

<https://developer.apple.com/library/ios/#releasenotes/ObjectiveC/RN-TransitioningToARC/Introduction/Introduction.html>

`__bridge`只做类型转换，但是不修改对象（内存）管理权；

`__bridge_retained`（也可以使用`CFBridgingRetain`）将Objective-C的对象转换为Core Foundation的对象，同时将对象（内存）的管理权交给我们，后续需要使用CFRelease或者相关方法来释放对象；

`__bridge_transfer`（也可以使用CFBridgingRelease）将Core Foundation的对象转换为Objective-C的对象，同时将对象（内存）的管理权交给ARC。