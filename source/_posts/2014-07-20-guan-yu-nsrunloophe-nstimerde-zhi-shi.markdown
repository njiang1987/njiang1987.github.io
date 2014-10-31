---
layout: post
title: "关于NSRunLoop和NSTimer的知识"
date: 2014-07-20 15:26:16 +0800
comments: true
categories: iOS NSRunLoop NSTimer
---
1.什么是`NSRunLoop`

`NSRunLoop`是消息机制的处理模式

`NSRunLoop`的作用在于有事情做的时候使的当前NSRunLoop的线程工作，没有事情做让当前`NSRunLoop`的线程休眠


`NSTimer`默认添加到当前`NSRunLoop`中，也可以手动制定添加到自己新建的`NSRunLoop`



`NSRunLoop`就是一直在循环检测，从线程start到线程end，检测inputsource(如点击，双击等操作)同步事件，检测timesource同步事件，检测到输入源会执行处理函数，首先会产生通知，corefunction向线程添加runloop observers来监听事件，意在监听事件发生时来做处理。



在单线程的app中，不需要注意Run Loop，但不代表没有。程序启动时，系统已经在主线程中加入了Run Loop。它保证了我们的主线程在运行起来后，就处于一种“等待”的状态（而不像一些命令行程序一样运行一次就结束了），这个时候如果有接收到的事件（Timer的定时到了或是其他线程的消息），就会执行任务，否则就处于休眠状态。


runloopmode是一个集合，包括监听：事件源，定时器，以及需通知的runloop observers
模式包括：
default模式：几乎包括所有输入源(除NSConnection) `NSDefaultRunLoopMode`模式 
mode模式：处理modal panels
connection模式：处理NSConnection事件，属于系统内部，用户基本不用
event tracking模式：如组件拖动输入源 UITrackingRunLoopModes 不处理定时事件 
common modes模式：NSRunLoopCommonModes 这是一组可配置的通用模式。将input sources与该模式关联则同时也将input sources与该组中的其它模式进行了关联。 

每次运行一个run loop，你指定（显式或隐式）run loop的运行模式。当相应的模式传递给run loop时，只有与该模式对应的input sources才被监控并允许run loop对事件进行处理（与此类似，也只有与该模式对应的observers才会被通知）


例：
1).在timer与table同时执行情况，当拖动table时，runloop进入`UITrackingRunLoopModes`模式下，不会处理定时事件，此时timer不能处理，所以此时将timer加入到NSRunLoopCommonModes模式(addTimer forMode)
2).在scroll一个页面时来松开，此时connection不会收到消息，由于scroll时runloop为UITrackingRunLoopModes模式，不接收输入源，此时要修改connection的mode
[scheduleInRunLoop:[NSRunLoop currentRunLoop]forMode:NSRunLoopCommonModes];




关于`-(BOOL)runMode:(NSString *)mode beforeDate:(NSDate *)date;`方法
指定runloop模式来处理输入源，首个输入源或date结束退出。
暂停当前处理的流程，转而处理其他输入源，当date设置为`[NSDate distantFuture]`(将来，基本不会到达的时间)，所以除非处理其他输入源结束，否则永不退出处理暂停的当前处理的流程。
{% codeblock lang:objc %}
while(A){
 [[NSRunLoop currentRunLoop] runMode:NSDefaultRunLoopMode beforeDate:[NSDate distantFuture]]; 
}
{% endcodeblock %}
当前A为YES时，当前runloop会一直接收处理其他输入源，当前流程不继续处理，出为A为NO，当前流程继续


performSelector关于内存管理的执行原理是这样的执行 `[self performSelector:@selector(method1:) withObject:self.tableLayer afterDelay:3]; `的时候，系统会将tableLayer的引用计数加1，执行完这个方法时，还会将tableLayer的引用计数减1，由于延迟这时tableLayer的引用计数没有减少到0，也就导致了切换场景dealloc方法没有被调用，出现了内存泄露。
利用如下函数：
`[NSObject cancelPreviousPerformRequestsWithTarget:self]`
当然你也可以一个一个得这样用：
`[NSObject cancelPreviousPerformRequestsWithTarget:self selector:@selector(method1:) object:nil]`
加上了这个以后，顺利地执行了dealloc方法

在touchBegan里面
`[self performSelector:@selector(longPressMethod:) withObject:nil afterDelay:longPressTime]`
然后在end 或cancel里做判断，如果时间不够长按的时间调用：
`[NSObject cancelPreviousPerformRequestsWithTarget:self selector:@selector(longPressMethod:) object:nil]`
取消began里的方法

2.Run Loop和线程的关系：


1. 主线程的run loop默认是启动的，用于接收各种输入sources
2. 对第二线程来说，run loop默认是没有启动的，如果你需要更多的线程交互则可以手动配置和启动，如果线程执行一个长时间已确定的任务则不需要。



3.Run Loop什么情况下使用：


a. 使用ports 或 input sources 和其他线程通信   // 不了解
b. 在线程中使用timers                                             // 如果不启动run loop，timer的事件是不会响应的 
c. 在Cocoa 应用中使用performSelector...方法   // 应该是performSelector...这种方法会启动一个线程并启动run loop吧
d. 让线程执行一个周期性的任务      

注：timer的创建和释放必须在同一线程中。
`[[NSRunLoop currentRunLoop] addTimer:timer forMode:NSRunLoopCommonModes];  `此方法会retain timer对象的引用计数。



关于NSTimer

1.NSTimer会是准时触发事件吗


答案是否定的，而且有时候你会发现实际的触发时间跟你想象的差距还比较大。NSTimer不是一个实时系统，因此不管是一次性的还是周期性的timer的实际触发事件的时间可能都会跟我们预想的会有出入。差距的大小跟当前我们程序的执行情况有关系，比如可能程序是多线程的，而你的timer只是添加在某一个线程的runloop的某一种指定的runloopmode中，由于多线程通常都是分时执行的，而且每次执行的mode也可能随着实际情况发生变化。

　　假设你添加了一个timer指定2秒后触发某一个事件，但是签好那个时候当前线程在执行一个连续运算(例如大数据块的处理等)，这个时候timer就会延迟到该连续运算执行完以后才会执行。重复性的timer遇到这种情况，如果延迟超过了一个周期，则会和后面的触发进行合并，即在一个周期内只会触发一次。但是不管该timer的触发时间延迟的有多离谱，他后面的timer的触发时间总是倍数于第一次添加timer的间隙。

　　原文如下
>“A repeating timer reschedules itself based on the scheduled firing time, not the actual firing time. For example, if a timer is scheduled to fire at a particular time and every 5 seconds after that, the scheduled firing time will always fall on the original 5 second time intervals, even if the actual firing time gets delayed. If the firing time is delayed so far that it passes one or more of the scheduled firing times, the timer is fired only once for that time period; the timer is then rescheduled, after firing, for the next scheduled firing time in the future.”


　　下面请看一个简单的例子:
```objc
- (void)applicationDidBecomeActive:(UIApplication *)application
{
    SvTestObject *testObject2 = [[SvTestObject alloc] init];
    [NSTimer scheduledTimerWithTimeInterval:1 target:testObject2 selector:@selector(timerAction:) userInfo:nil repeats:YES];
    [testObject2 release];
    
    NSLog(@"Simulate busy");
    [self performSelector:@selector(simulateBusy) withObject:nil afterDelay:3];
}

// 模拟当前线程正好繁忙的情况
- (void)simulateBusy
{
    NSLog(@"start simulate busy!");
    NSUInteger caculateCount = 0x0FFFFFFF;
    CGFloat uselessValue = 0;
    for (NSUInteger i = 0; i < caculateCount; ++i) {
        uselessValue = i / 0.3333;
    }
    NSLog(@"finish simulate busy!");
}
```

例子中首先开启了一个timer，这个timer每隔1秒调用一次target的timerAction方法，紧接着我们在3秒后调用了一个模拟线程繁忙的方法(其实就是一个大的循环)。运行程序后输出结果如下:



观察结果我们可以发现，当线程空闲的时候timer的消息触发还是比较准确的，但是在36分12秒开始线程一直忙着做大量运算，知道36分14秒该运算才结束，这个时候timer才触发消息，这个线程繁忙的过程超过了一个周期，但是timer并没有连着触发两次消息，而只是触发了一次。等线程忙完以后后面的消息触发的时间仍然都是整数倍与开始我们指定的时间，这也从侧面证明，timer并不会因为触发延迟而导致后面的触发时间发生延迟。

综上: timer不是一种实时的机制，会存在延迟，而且延迟的程度跟当前线程的执行情况有关。


2.NSTimer为什么要添加到RunLoop中才会有作用


前面的例子中我们使用的是一种便利方法，它其实是做了两件事：首先创建一个timer，然后将该timer添加到当前runloop的default mode中。也就是这个便利方法给我们造成了只要创建了timer就可以生效的错觉，我们当然可以自己创建timer，然后手动的把它添加到指定runloop的指定mode中去。

　　NSTimer其实也是一种资源，如果看过多线程变成指引文档的话，我们会发现所有的source如果要起作用，就得加到runloop中去。同理timer这种资源要想起作用，那肯定也需要加到runloop中才会又效喽。如果一个runloop里面不包含任何资源的话，运行该runloop时会立马退出。你可能会说那我们APP的主线程的runloop我们没有往其中添加任何资源，为什么它还好好的运行。我们不添加，不代表框架没有添加，如果有兴趣的话你可以打印一下main thread的runloop，你会发现有很多资源。 

　　下面我们看一个小例子：　　
```objc
- (void)applicationDidBecomeActive:(UIApplication *)application
{
    [self testTimerWithOutShedule];
}

- (void)testTimerWithOutShedule
{
    NSLog(@"Test timer without shedult to runloop");
    SvTestObject *testObject3 = [[SvTestObject alloc] init];
    NSTimer *timer = [[NSTimer alloc] initWithFireDate:[NSDate dateWithTimeIntervalSinceNow:1] interval:1 target:testObject3 selector:@selector(timerAction:) userInfo:nil repeats:NO];
    [testObject3 release];
    NSLog(@"invoke release to testObject3");
}

- (void)applicationWillResignActive:(UIApplication *)application
{
    NSLog(@"SvTimerSample Will resign Avtive!");
}
```
这个小例子中我们新建了一个timer，为它指定了有效的target和selector，并指出了1秒后触发该消息，运行结果如下:



观察发现这个消息永远也不会触发，原因很简单，我们没有将timer添加到runloop中。

综上: 必须得把timer添加到runloop中，它才会生效。


3.NSTimer加到了RunLoop中但迟迟的不触发事件


为什么明明添加了，但是就是不按照预先的逻辑触发事件呢？？？原因主要有以下两个:

1、runloop是否运行

　　每一个线程都有它自己的runloop，程序的主线程会自动的使runloop生效，但对于我们自己新建的线程，它的runloop是不会自己运行起来，当我们需要使用它的runloop时，就得自己启动。

　　那么如果我们把一个timer添加到了非主线的runloop中，它还会按照预期按时触发吗？下面请看一段测试程序:
```objc
- (void)applicationDidBecomeActive:(UIApplication *)application
{
    [NSThread detachNewThreadSelector:@selector(testTimerSheduleToRunloop1) toTarget:self withObject:nil];
}

// 测试把timer加到不运行的runloop上的情况
- (void)testTimerSheduleToRunloop1
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    
    NSLog(@"Test timer shedult to a non-running runloop");
    SvTestObject *testObject4 = [[SvTestObject alloc] init];
    NSTimer *timer = [[NSTimer alloc] initWithFireDate:[NSDate dateWithTimeIntervalSinceNow:1] interval:1 target:testObject4 selector:@selector(timerAction:) userInfo:nil repeats:NO];
    [[NSRunLoop currentRunLoop] addTimer:timer forMode:NSDefaultRunLoopMode];
    // 打开下面一行输出runloop的内容就可以看出，timer却是已经被添加进去
    //NSLog(@"the thread's runloop: %@", [NSRunLoop currentRunLoop]);
    
    // 打开下面一行, 该线程的runloop就会运行起来，timer才会起作用
    //[[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:3]];
    
    [testObject4 release];
    NSLog(@"invoke release to testObject4");

    [pool release];
}

- (void)applicationWillResignActive:(UIApplication *)application
{
    NSLog(@"SvTimerSample Will resign Avtive!");
}
```
上面的程序中，我们新创建了一个线程，然后创建一个timer，并把它添加当该线程的runloop当中，但是运行结果如下：


观察运行结果，我们发现这个timer知道执行退出也没有触发我们指定的方法，如果我们把上面测试程序中`[[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:3]];`这一行的注释去掉，则timer将会正确的掉用我们指定的方法。




2、mode是否正确

　　我们前面自己动手添加runloop的时候，可以看到有一个参数runloopMode，这个参数是干嘛的呢？

　　前面提到了要想timer生效，我们就得把它添加到指定runloop的指定mode中去，通常是主线程的defalut mode。但有时我们这样做了，却仍然发现timer还是没有触发事件。这是为什么呢？

　　这是因为timer添加的时候，我们需要指定一个mode，因为同一线程的runloop在运行的时候，任意时刻只能处于一种mode。所以只能当程序处于这种mode的时候，timer才能得到触发事件的机会。

　　举个不恰当的例子，我们说兄弟几个分别代表runloop的mode，timer代表他们自己的才水桶，然后一群人去排队打水，只有一个水龙头，那么同一时刻，肯定只能有一个人处于接水的状态。也就是说你虽然给了老二一个桶，但是还没轮到它，那么你就得等，只有轮到他的时候你的水桶才能碰上用场。



综上: 要让timer生效，必须保证该线程的runloop已启动，而且其运行的runloopmode也要匹配。

转自:<http://blog.csdn.net/ioswyl88219/article/details/16996531>