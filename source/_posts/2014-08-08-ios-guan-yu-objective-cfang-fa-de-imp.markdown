---
layout: post
title: "iOS 关于Objective-C方法的IMP"
date: 2014-08-08 12:39:42 +0800
comments: true
categories: 
---
###一.什么是IMP
IMP是”implementation”的缩写，它是objetive-C 方法(method)实现代码块的地址，可像C函数一样直接调用。通常情况下我们是通过[object method:parameter]或objc_msgSend()的方式向对象发送消息，然后Objective-C运行时(Objective-C runtime)寻找匹配此消息的IMP,然后调用它;但有些时候我们希望获取到IMP进行直接调用。

###二.Objetive-C中的Method结构
在Objecitve-C中，在类中对每一个方法有一个在运行时构建的数据结构，在Objective-C 2.0中，此结构对用户不可见，但仍在内部存在。

```objc
struct objc_method
{
  SEL method_name;
  char * method_types;
  IMP method_imp;
};
typedef objc_method Method;
```

每个方法有3个属性
方法名：方法名为此方法的签名，有着相同函数名和参数名的方法有着相同的方法名。
方法类型：方法类型描述了参数的类型。
IMP: IMP即函数指针，为方法具体实现代码块的地址，可像普通C函数调用一样使用IMP。
由于Method的内部结构不可见，所以不能通过method->method_name的方式访问其内部属性，只能Objective-C运行时提供的函数获取。

```objc
SEL method_getName(Method method);
IMP method_getImplementation(Method method);
const char * ivar_getTypeEncoding(Ivar ivar);
```

还有一些其他函数来获取方法的各种属性，具体可见Objective-C Runtime Reference。

###三.获取当前方法的默认IMP(default IMP)
NSObject对象提供了两个方法来获取的IMP

```objc
- (IMP)methodForSelector:(SEL)aSelector;
+ (IMP)instanceMethodForSelector:(SEL)aSelector;
```

使用`methodForSelector`方法时，若向类(class)发送消息，则aSelector应该是类方法(class method);若向实例对象(instance)发送消息，则aSelector应该为实例对象方法(instance method)。使用`instanceMethodForSelector`可向类请求实例方法的IMP。
那么获取当前方法的IMP,可使用self对象和隐含的_cmd参数。
`IMP current = [self class] instanceMethodForSelector:_cmd];`
methodForSelector返回的IMP是default IMP,即发送消息时会调用的IMP。但可能有其他情况不是这样的,但到底什么情况下呢?不懂，如下:
>methodForSelector: only returns the default IMP that will be invoked by a send message but you could have arrived at the current method through a super invocation, or a direct invocation of the IMP itself. The approach shown in this post gets the correct IMP no matter how it was invoked.

###四. 另一种hack的方式获取当前方法IMP

GCC有个内建(build-in)函数,可获取当前栈帧的返回地址（参数0表示当前栈帧）。
`__builtin_return_address(0)`
这里有两个假设
方法的实现是连续的。
在方法中调用子函数，在子函数中调用__builtin_return_address(0)得到的返回地址在当前方法实现的内部。
那么可以得出结论，当前方法实现的起始地址(即IMP)肯定在的子函数返回地址的前面，而且会比任何其他方法离的更近。则可通过如下方法寻找IMP。
当当前方法中，调用一个寻找IMP的子函数，将当前类和_cmd参数传递给子函数；
在子函数中使用__builtin_return_address(0)获得返回地址，遍历当前类和当前父类的所有方法，寻找method_name与_cmd相等，而method_imp在__builtin_return_address(0)之前，且离其最近，则此IMP即为当前的的IMP。

```objc
#import <objc/objc-class.h>
IMP impOfCallingMethod(id lookupObject, SEL selector)
{
    NSUInteger returnAddress = (NSUInteger)__builtin_return_address(0);
    NSUInteger closest = 0;

    // Iterate over the class and all superclasses
    Class currentClass = object_getClass(lookupObject);
    while (currentClass)
    {
        // Iterate over all instance methods for this class
        unsigned int methodCount;
        Method *methodList = class_copyMethodList(currentClass, &methodCount);
        unsigned int i;
        for (i = 0; i < methodCount; i++)
        {
            // Ignore methods with different selectors
            if (method_getName(methodList[i]) != selector)
            {
                continue;
            }

            // If this address is closer, use it instead
            NSUInteger address = (NSUInteger)method_getImplementation(methodList[i]);
            if (address < returnAddress && address > closest)
            {
                closest = address;
            }
        }

        free(methodList);
        currentClass = class_getSuperclass(currentClass);
    }

    return (IMP)closest;
}
```

其使用方法为:

```objc
- (void)myMethodWithParam1:(int)someParameter andParam2:(int)otherParameter
{
   IMP myImplementation = impOfCallingInstanceMethod([self class], _cmd);

   ...
}
```

另外还有更快速的方法:获取当前方法的返回地址,然后通过此地址回溯到父函数的IMP内部，在父函数IMP中寻找调用当前函数的位置，即可知道当前函数的IMP，不过此方法是平台相关的。
注:此方法假设IMP地址与子函数返回地址之间是连续的，中间不会有其他方法IMP。如果将impOfCallingMethod放到block代码中，则此条件不再满足，不再适用。(待验证)
参考：
IMP of the current method
Objective-C Runtime Reference
NSObject Class Reference

本文出自 清风徐来，水波不兴 的博客，转载时请注明出处及相应链接。
本文永久链接: http://www.winddisk.com/2012/06/13/objective-c-method-imp/