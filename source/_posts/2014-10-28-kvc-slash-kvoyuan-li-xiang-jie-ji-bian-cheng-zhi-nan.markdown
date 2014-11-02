---
layout: post
title: "[iOS]KVC/KVO原理详解及编程指南"
date: 2014-10-28 17:48:12 +0800
comments: true
categories: 技术
tags: iOS
---

##前言：
1. 本文基本不讲KVC/KVO的用法，只结合网上的资料说说对这种技术的理解。
2. 由于KVO内容较少，而且是以KVC为基础实现的，本文将着重介绍KVC部分。

##一、简介

KVC/KVO是观察者模式的一种实现，在Cocoa中是以被万物之源NSObject类实现的`NSKeyValueCoding/NSKeyValueObserving`非正式协议的形式被定义为基础框架的一部分。从协议的角度来说，KVC/KVO本质上是定义了一套让我们去遵守和实现的方法。

当然，KVC/KVO实现的根本是Objective-C的动态性和runtime，这在后文的原理部分会有详述。
另外，KVC/KVO机制离不开访问器方法的实现，这在后文中也有解释。

1. KVC简介
全称是Key-value coding，翻译成键值编码。顾名思义，在某种程度上跟map的关系匪浅。它提供了一种使用字符串而不是访问器方法去访问一个对象实例变量的机制。

2. KVO简介
全称是Key-value observing，翻译成键值观察。提供了一种当其它对象属性被修改的时候能通知当前对象的机制。再MVC大行其道的Cocoa中，KVO机制很适合实现model和controller类之间的通讯。

##二、KVC相关技术

1.Key和Key Path

KVC定义了一种按名称访问对象属性的机制，支持这种访问的主要方法是：

```objc
- (id)valueForKey:(NSString *)key;  
- (void)setValue:(id)value forKey:(NSString *)key;  
- (id)valueForKeyPath:(NSString *)keyPath;  
- (void)setValue:(id)value forKeyPath:(NSString *)keyPath;  
```

前边两个方法用到的Key较容易理解，就是要访问的属性名称对应的字符串。
后面两个方法用到的KeyPath是一个被点操作符隔开的用于访问对象的指定属性的字符串序列。比如KeyPath address.street将会访问消息接收对象所包含的address属性中包含的一个street属性。其实KeyPath说白了就是我们平时使用点操作访问某个对象的属性时所写的那个字符串。

2.点语法和KVC

在实现了访问器方法的类中，使用点语法和KVC访问对象其实差别不大，二者可以任意混用。但是没有访问起方法的类中，点语法无法使用，这时KVC就有优势了。（原因见第三部分的第一节：KVC如何访问属性值。）

3.一对多关系（To-Many）中的集合访问器方法

我们平时大部分使用的属性都是一对一关系（To-One）,比如Person类中的name属性，每个人只有一个名字。但也有一对多的关系，比如Person中有一个friendsName属性，这是个集合（在Objective-C中可以是NSArray，NSSet等），保存的是一个人的所有朋友的名字。

当操作一对多的属性中的内容时，我们有两种选择：

①间接操作
先通过KVC方法取到集合属性，然后通过集合属性操作集合中的元素。

②直接操作
苹果为我们提供了一些方法模板，我们可以以规定的格式实现这些方法来达到访问集合属性中元素的目的。

有序集合对应方法如下：

```objc
-countOf<Key>  //必须实现，对应于NSArray的基本方法count:  
-objectIn<Key>AtIndex:  
-<key>AtIndexes:  //这两个必须实现一个，对应于 NSArray 的方法 objectAtIndex: 和 objectsAtIndexes:  
-get<Key>:range:  //不是必须实现的，但实现后可以提高性能，其对应于 NSArray 方法 getObjects:range:  
-insertObject:in<Key>AtIndex:  
-insert<Key>:atIndexes:  //两个必须实现一个，类似于 NSMutableArray 的方法 insertObject:atIndex: 和 insertObjects:atIndexes:  
-removeObjectFrom<Key>AtIndex:  
-remove<Key>AtIndexes:  //两个必须实现一个，类似于 NSMutableArray 的方法 removeObjectAtIndex: 和 removeObjectsAtIndexes:  
-replaceObjectIn<Key>AtIndex:withObject:  
-replace<Key>AtIndexes:with<Key>:  //可选的，如果在此类操作上有性能问题，就需要考虑实现之  
```

无序集合对应方法如下：

```objc
[java] view plaincopy
-countOf<Key>  //必须实现，对应于NSArray的基本方法count:  
-objectIn<Key>AtIndex:  
-<key>AtIndexes:  //这两个必须实现一个，对应于 NSArray 的方法 objectAtIndex: 和 objectsAtIndexes:  
-get<Key>:range:  //不是必须实现的，但实现后可以提高性能，其对应于 NSArray 方法 getObjects:range:  
-insertObject:in<Key>AtIndex:  
-insert<Key>:atIndexes:  //两个必须实现一个，类似于 NSMutableArray 的方法 insertObject:atIndex: 和 insertObjects:atIndexes:  
-removeObjectFrom<Key>AtIndex:  
-remove<Key>AtIndexes:  //两个必须实现一个，类似于 NSMutableArray 的方法 removeObjectAtIndex: 和 removeObjectsAtIndexes:  
-replaceObjectIn<Key>AtIndex:withObject:  
-replace<Key>AtIndexes:with<Key>:  //这两个都是可选的，如果在此类操作上有性能问题，就需要考虑实现之 
```
 
不过这些方法除非是很有需求，否则个人认为没有实现的必要，间接法也不是很麻烦，基本能满足需求了。值得指出的是，苹果甚至都没有让这些方法以哪怕是非正式协议的形式出现，而只是在编程指南中提了一下。


4.键值验证（Key-Value Validation）

KVC提供了验证Key对应的Value是否可用的方法：

```objc
- (BOOL)validateValue:(inout id *)ioValue forKey:(NSString *)inKey error:(out NSError **)outError;  
```

该方法默认的实现是调用一个如下格式的方法：

```objc
- (BOOL)validate<Key>:error:  
```

比如属性name对应的方法为：

```objc
-(BOOL)validateName:(id *)ioValue error:(NSError * __autoreleasing *)outError {  
    // Implementation specific code.  
    return ...;  
}  
```

这样就给了我们一次纠错的机会。需要指出的是，KVC是不会自动调用键值验证方法的，就是说我们需要手动验证。但是有些技术，比如CoreData会自动调用。

5.KVC对数值和结构体型属性的支持

一套机制如果不支持数值和结构体型的数据，那么它的实用性就会大大折扣。幸运的是KVC中苹果对这方面的支持做的很好。KVC可以自动的将数值或结构体型的数据打包或解包成`NSNumber`或`NSValue`对象，以达到适配的目的。

举个例子，Person类有个个`NSInteger`类型的age属性

①修改值

我们通过KVC技术使用如下方式设置age属性的值：

```objc
[person setValue:[NSNumber numberWithInteger:5] forKey:@"age"];  
```

我们赋给age的是一个`NSNumber`对象，KVC会自动的将`NSNumber`对象转换成`NSInteger`对象，然后再调用相应的访问器方法设置age的值。

②获取值

同样，以如下方式获取age属性值：

```objc
[person valueForKey:@"age"];  
```

这时，会以NSNumber的形式返回age的值。需要说明的是，什么时候返回的是NSNumber，什么时候返回的是NSValue？

③使用`NSNumber`封装

可以使用NSNumber的数据类型有：

```objc
+ (NSNumber *)numberWithChar:(char)value;  
+ (NSNumber *)numberWithUnsignedChar:(unsigned char)value;  
+ (NSNumber *)numberWithShort:(short)value;  
+ (NSNumber *)numberWithUnsignedShort:(unsigned short)value;  
+ (NSNumber *)numberWithInt:(int)value;  
+ (NSNumber *)numberWithUnsignedInt:(unsigned int)value;  
+ (NSNumber *)numberWithLong:(long)value;  
+ (NSNumber *)numberWithUnsignedLong:(unsigned long)value;  
+ (NSNumber *)numberWithLongLong:(long long)value;  
+ (NSNumber *)numberWithUnsignedLongLong:(unsigned long long)value;  
+ (NSNumber *)numberWithFloat:(float)value;  
+ (NSNumber *)numberWithDouble:(double)value;  
+ (NSNumber *)numberWithBool:(BOOL)value;  
+ (NSNumber *)numberWithInteger:(NSInteger)value NS_AVAILABLE(10_5, 2_0);  
+ (NSNumber *)numberWithUnsignedInteger:(NSUInteger)value NS_AVAILABLE(10_5, 2_0);  
```

总之就是一些常见的数值型数据。

④使用`NSValue`封装

`NSValue`主要用于处理结构体型的数据，它本身提供了如下集中结构的支持：

```objc
+ (NSValue *)valueWithCGPoint:(CGPoint)point;  
+ (NSValue *)valueWithCGSize:(CGSize)size;  
+ (NSValue *)valueWithCGRect:(CGRect)rect;  
+ (NSValue *)valueWithCGAffineTransform:(CGAffineTransform)transform;  
+ (NSValue *)valueWithUIEdgeInsets:(UIEdgeInsets)insets;  
+ (NSValue *)valueWithUIOffset:(UIOffset)insets NS_AVAILABLE_IOS(5_0);  
```

只有有限的6种而已！那对于其它自定义的结构体怎么办？别担心，任何结构体都是可以转化成NSValue对象的，具体实现方法参见我之前的一篇文章：
<http://blog.csdn.net/wzzvictory/article/details/8614433>

6.集合运算符（Collection Operators）

集合运算符是一个特殊的Key Path，可以作为参数传递给`valueForKeyPath:`方法，注意只能是这个方法，如果传给了`valueForKey:`方法保证你程序崩溃。

运算符是一个以@开头的特殊字符串，格式如下图所示：

①简单集合运算符

简单集合运算符共有`@avg`，`@count`，`@max`，`@min`，`@sum`5种，都表示啥不用我说了吧，目前还不支持自定义。
有一个集合类的对象：transactions，它存储了一个个的Transaction类的实例，该类有三个属性：payee，amount，date。下面以此为例说明如何使用这些运算符：
要获取amount的平均值可以这样：

```objc
NSNumber *transactionAverage = [transactions valueForKeyPath:@"@avg.amount"];  
```

要获取transactions集合中元素数目可以这样：

```objc
NSNumber *numberOfTransactions = [transactions valueForKeyPath:@"@count"];  
```

需要之处的是，@count是这些集合运算符中比较特殊的一个，因为它没有右路经，原因很容易理解。

②对象运算符

比集合运算符稍微复杂，能以数组的方式返回指定的内容，一共有两种：

```objc
@distinctUnionOfObjects  
@unionOfObjects  
```

它们的返回值都是NSArray，区别是前者返回的元素都是唯一的，是去重以后的结果；后者返回的元素是全集。
用法如下：

```objc
NSArray *payees = [transactions valueForKeyPath:@"@distinctUnionOfObjects.payee"];  
NSArray *payees = [transactions valueForKeyPath:@"@unionOfObjects.payee"];  
```

前者会将收款人的姓名去除重复的以后返回，后者直接返回所有收款人的姓名。

③Array和Set操作符

这种情况更复杂了，说的是集合中包含集合的情况，我们执行了如下的一段代码：

```objc
// Create the array that contains additional arrays.  
self.arrayOfTransactionsArray = [NSMutableArray array];  
// Add the array of objects used in the above examples.  
[arrayOfTransactionsArray addObject:transactions];  
// Add a second array of objects; this array contains alternate values.  
[arrayOfTransactionsArrays addObject:moreTransactions];  
```

得到了一个包含集合的集合：`arrayOfTransactionsArray`, 这时如果我们想操作`arrayOfTransactionsArray`中包含的集合中的元素时，可以使用如下三个运算符：

```objc
@distinctUnionOfArrays  
@unionOfArrays  
@distinctUnionOfSets  
```

前两个针对的集合是Arrays，后一个针对的集合是Sets。因为Sets中的元素本身就是唯一的，所以没有对应的`@unionOfSets`运算符。

它们的用法举例如下：

```objc
NSArray *payees = [arrayOfTransactionsArrays valueForKeyPath:@"@unionOfArrays.payee"];  
```

##三、实现原理

1.KVC如何访问属性值

KVC再某种程度上提供了访问器的替代方案。不过访问器方法是一个很好的东西，以至于只要是有可能，KVC也尽量再访问器方法的帮助下工作。为了设置或者返回对象属性，KVC按顺序使用如下技术：

①检查是否存在`-<key>`、`-is<key>`（只针对布尔值有效）或者`-get<key>`的访问器方法，如果有可能，就是用这些方法返回值；

检查是否存在名为-set<key>:的方法，并使用它做设置值。对于`-get<key>`和`-set<key>:`方法，将大写Key字符串的第一个字母，并与Cocoa的方法命名保持一致；

②如果上述方法不可用，则检查名为`-_<key>`、`-_is<key>`（只针对布尔值有效）、`-_get<key>`和-`_set<key>:`方法；

③如果没有找到访问器方法，可以尝试直接访问实例变量。实例变量可以是名为：`<key>`或`_<key>`;

④如果仍为找到，则调用`valueForUndefinedKey:`和`setValue:forUndefinedKey:`方法。这些方法的默认实现都是抛出异常，我们可以根据需要重写它们。

2.KVC/KVO实现原理

键值编码和键值观察是根据`isa-swizzling`技术来实现的，主要依据runtime的强大动态能力。下面的这段话是引自网上的一篇文章：
<http://blog.csdn.net/kesalin/article/details/8194240>

当某个类的对象第一次被观察时，系统就会在运行期动态地创建该类的一个派生类，在这个派生类中重写基类中任何被观察属性的 setter 方法。

派生类在被重写的 setter 方法实现真正的通知机制，就如前面手动实现键值观察那样。这么做是基于设置属性会调用 setter 方法，而通过重写就获得了 KVO 需要的通知机制。当然前提是要通过遵循 KVO 的属性设置方式来变更属性值，如果仅是直接修改属性对应的成员变量，是无法实现 KVO 的。

同时派生类还重写了 class 方法以“欺骗”外部调用者它就是起初的那个类。然后系统将这个对象的 isa 指针指向这个新诞生的派生类，因此这个对象就成为该派生类的对象了，因而在该对象上对 setter 的调用就会调用重写的 setter，从而激活键值通知机制。此外，派生类还重写了 dealloc 方法来释放资源。

原文写的很好，还举了解释性的例子，大家可以去看看。

在我之前的一篇介绍Objective-C类和元类的文章：
<http://blog.csdn.net/wzzvictory/article/details/8592492>
中介绍过，isa指针指向的其实是类的元类，如果之前的类名为：Person，那么被runtime更改以后的类名会变成：`NSKVONotifying_Person`。

新的`NSKVONotifying_Person`类会重写以下方法：

增加了监听的属性对应的set方法，`class`，`dealloc`，`_isKVOA`。

①class
重写class方法是为了我们调用它的时候返回跟重写继承类之前同样的内容。打印如下内容：

```objc
NSLog(@"self->isa:%@",self->isa);  
NSLog(@"self class:%@",[self class]);
```
  
在建立KVO监听前，打印结果为：

```objc
self->isa:Person  
self class:Person  
```

在建立KVO监听之后，打印结果为：

```objc
self->isa:NSKVONotifying_Person  
self class:Person  
```

这也是isa指针和class方法的一个区别，大家使用的时候注意。

②重写set方法

新类会重写对应的set方法，是为了在set方法中增加另外两个方法的调用：

```objc
- (void)willChangeValueForKey:(NSString *)key  
- (void)didChangeValueForKey:(NSString *)key  
```

其中，`didChangeValueForKey:`方法负责调用：

```objc
- (void)observeValueForKeyPath:(NSString *)keyPath  
                      ofObject:(id)object  
                        change:(NSDictionary *)change  
                       context:(void *)context  
```

方法，这就是KVO实现的原理了！

如果没有任何的访问器方法，`-setValue:forKey`方法会直接调用：

```objc
- (void)willChangeValueForKey:(NSString *)key  
- (void)didChangeValueForKey:(NSString *)key  
```

如果在没有使用键值编码且没有使用适当命名的访问起方法的时候，我们只需要显示调用上述两个方法，同样可以使用KVO！

总结一下，想使用KVO有三种方法：

1)使用了KVC

使用了KVC，如果有访问器方法，则运行时会在访问器方法中调用`will/didChangeValueForKey:`方法；
没用访问器方法，运行时会在`setValue:forKey`方法中调用`will/didChangeValueForKey:`方法。

2)有访问器方法

运行时会重写访问器方法调用`will/didChangeValueForKey:`方法。因此，直接调用访问器方法改变属性值时，KVO也能监听到。

3)显示调用`will/didChangeValueForKey:`方法。

总之，想使用KVO，只要有`will/didChangeValueForKey:`方法就可以了。

③_isKVOA

这个私有方法估计是用来标示该类是一个 KVO 机制声称的类。

##四、优点和缺点

1.优点

①可以再很大程度上简化代码

例子网上很多，这就不举了

②能跟脚本语言很好的配合

才疏学浅，没学过AppleScript等脚本语言，所以没能深刻体会到该优点。

2.缺点

KVC的缺点不明显，主要是KVO的，详情可以参考这篇文章：
<http://www.mikeash.com/pyblog/key-value-observing-done-right.html>

核心思想是说KVO的回调机制，不能传一个selector或者block作为回调，而必须重写-`addObserver:forKeyPath:options:context:`方法所引发的一系列问题。问了解决这个问题，作者还亲自实现了一个`MAKVONotificationCenter`类，代码见<github:
https://github.com/mikeash/MAKVONotificationCenter>不过个人认为这只是苹果做的KVO不够完美，不能算是缺陷。

参考文档：

<http://developer.apple.com/library/ios/#documentation/cocoa/conceptual/KeyValueCoding/Articles/KeyValueCoding.html#//apple_ref/doc/uid/10000107-SW1
http://blog.csdn.net/kesalin/article/details/8194240>

作者：wangzz

原文地址：<http://blog.csdn.net/wzzvictory/article/details/9674431>

转载请注明出处

如果觉得文章对你有所帮助，请通过留言或关注微信公众帐号wangzzstrive来支持我，谢谢！