---
layout: post
title: '[转载]objective-C多线程NSThread'
categories:
- 技术
tags: [NSThread]
published: true
comments: true
---
<p>转自：<a href="http://hi.baidu.com/wolf_childer/item/c9509eeae24b070965db00ae">http://hi.baidu.com/wolf_childer/item/c9509eeae24b070965db00ae</a>
iOS 支持多个层次的多线程编程，层次越高的抽象程度越高，使用起来也越方便，也是苹果最推荐使用的方法。下面根据抽象层次从低到高依次列出iOS所支持的多线程编程范式：
<div id="content" /></p>

<p>1, Thread;<br />
2, Cocoa operations;<br />
3, Grand Central Dispatch (GCD) (iOS4 才开始支持)</p>

<p><strong>下面简要说明这三种不同范式：</strong>
Thread 是这三种范式里面相对轻量级的，但也是使用起来最负责的，你需要自己管理thread的生命周期，线程之间的同步。线程共享同一应用程序的部分内存空间，它们拥有对数据相同的访问权限。你得协调多个线程对同一数据的访问，一般做法是在访问之前加锁，这会导致一定的性能开销。在 iOS 中我们可以使用多种形式的 thread:<br />
Cocoa threads: 使用NSThread 或直接从 NSObject 的类方法 performSelectorInBackground:withObject: 来创建一个线程。如果你选择thread来实现多线程，那么 NSThread 就是官方推荐优先选用的方式。<br />
POSIX threads: 基于 C 语言的一个多线程库，</p>

<p>Cocoa operations是基于 Obective-C实现的，类 NSOperation 以面向对象的方式封装了用户需要执行的操作，我们只要聚焦于我们需要做的事情，而不必太操心线程的管理，同步等事情，因为NSOperation已经为我们封装了这些事情。 NSOperation 是一个抽象基类，我们必须使用它的子类。iOS 提供了两种默认实现：NSInvocationOperation 和 NSBlockOperation。</p>

<p>Grand Central Dispatch (GCD): iOS4 才开始支持，它提供了一些新的特性，以及运行库来支持多核并行编程，它的关注点更高：如何在多个 cpu 上提升效率。</p>

<p>有了上面的总体框架，我们就能清楚地知道不同方式所处的层次以及可能的效率，便利性差异。下面我们先来看看 NSThread 的使用，包括创建，启动，同步，通信等相关知识。这些与 win32/Java 下的 thread 使用非常相似。</p>

<p><strong>线程创建与启动</strong>
NSThread的创建主要有两种直接方式：<br />
[NSThread detachNewThreadSelector:@selector(myThreadMainMethod:) toTarget:self withObject:nil];<br />
和
NSThread* myThread = [[NSThread alloc] initWithTarget:self<br />
selector:@selector(myThreadMainMethod:)<br />
object:nil];<br />
[myThread start];</p>

<p>这两种方式的区别是：前一种一调用就会立即创建一个线程来做事情；而后一种虽然你 alloc 了也 init了，但是要直到我们手动调用 start 启动线程时才会真正去创建线程。这种延迟实现思想在很多跟资源相关的地方都有用到。后一种方式我们还可以在启动线程之前，对线程进行配置，比如设置 stack 大小，线程优先级。</p>

<p>还有一种间接的方式，更加方便，我们甚至不需要显式编写 NSThread 相关代码。那就是利用 NSObject 的类方法 performSelectorInBackground:withObject: 来创建一个线程：<br />
[myObj performSelectorInBackground:@selector(myThreadMainMethod) withObject:nil];<br />
其效果与 NSThread 的 detachNewThreadSelector:toTarget:withObject: 是一样的。</p>

<p><strong>线程同步</strong>
线程的同步方法跟其他系统下类似，我们可以用原子操作，可以用 mutex，lock等。<br />
iOS的原子操作函数是以 OSAtomic开头的，比如：OSAtomicAdd32, OSAtomicOr32等等。这些函数可以直接使用，因为它们是原子操作。</p>

<p>iOS中的 mutex 对应的是 NSLock，它遵循 NSLooking协议，我们可以使用 lock, tryLock, lockBeforeData:来加锁，用 unLock来解锁。使用示例：<br />
BOOL moreToDo = YES;<br />
NSLock *theLock = [[NSLock alloc] init];<br />
...<br />
while (moreToDo) {<br />
/* Do another increment of calculation */<br />
/* until there’s no more to do. */<br />
if ([theLock tryLock]) {<br />
/* Update display used by all threads. */<br />
[theLock unlock];<br />
}
}</p>

<p>我们可以使用指令 @synchronized 来简化 NSLock的使用，这样我们就不必显示编写创建NSLock,加锁并解锁相关代码。<br />
- (void)myMethod:(id)anObj<br />
{
@synchronized(anObj)<br />
{
// Everything between the braces is protected by the @synchronized directive.<br />
}
}</p>

<p>还有其他的一些锁对象，比如：循环锁NSRecursiveLock，条件锁NSConditionLock，分布式锁NSDistributedLock等等，在这里就不一一介绍了，大家去看官方文档吧。</p>

<p><strong>用NSCodition同步执行的顺序</strong>
NSCodition 是一种特殊类型的锁，我们可以用它来同步操作执行的顺序。它与 mutex 的区别在于更加精准，等待某个 NSCondtion 的线程一直被 lock，直到其他线程给那个 condition 发送了信号。下面我们来看使用示例：</p>

<p>某个线程等待着事情去做，而有没有事情做是由其他线程通知它的。</p>

<p>[cocoaCondition lock];<br />
while (timeToDoWork &lt;= 0)<br />
[cocoaCondition wait];</p>

<p>timeToDoWork--;<br />
// Do real work here.<br />
[cocoaCondition unlock];</p>

<p>其他线程发送信号通知上面的线程可以做事情了：<br />
[cocoaCondition lock];<br />
timeToDoWork++;<br />
[cocoaCondition signal];<br />
[cocoaCondition unlock];</p>

<p><strong>线程间通信</strong>
线程在运行过程中，可能需要与其它线程进行通信。我们可以使用 NSObject 中的一些方法：<br />
在应用程序主线程中做事情：<br />
performSelectorOnMainThread:withObject:waitUntilDone:<br />
performSelectorOnMainThread:withObject:waitUntilDone:modes:</p>

<p>在指定线程中做事情：<br />
performSelector:onThread:withObject:waitUntilDone:<br />
performSelector:onThread:withObject:waitUntilDone:modes:</p>

<p>在当前线程中做事情：<br />
performSelector:withObject:afterDelay:<br />
performSelector:withObject:afterDelay:inModes:</p>

<p>取消发送给当前线程的某个消息<br />
cancelPreviousPerformRequestsWithTarget:<br />
cancelPreviousPerformRequestsWithTarget:selector:object:</p>

<p>如在我们在某个线程中下载数据，下载完成之后要通知主线程中更新界面等等，可以使用如下接口：- (void)myThreadMainMethod<br />
{
NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];<br />
// to do something in your thread job<br />
...<br />
[self performSelectorOnMainThread:@selector(updateUI) withObject:nil waitUntilDone:NO];<br />
[pool release];<br />
}</p>

<p><strong>RunLoop</strong>
说到 NSThread 就不能不说起与之关系相当紧密的 NSRunLoop。Run loop 相当于 win32 里面的消息循环机制，它可以让你根据事件/消息（鼠标消息，键盘消息，计时器消息等）来调度线程是忙碌还是闲置。<br />
系统会自动为应用程序的主线程生成一个与之对应的 run loop 来处理其消息循环。在触摸 UIView 时之所以能够激发 touchesBegan/touchesMoved 等等函数被调用，就是因为应用程序的主线程在 UIApplicationMain 里面有这样一个 run loop 在分发 input 或 timer 事件。</p>

<p></p>
