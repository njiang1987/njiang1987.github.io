---
layout: post
title: "NSThread 、NSRunLoop 和 Dispatch Queue"
date: 2014-07-21 21:21:23 +0800
comments: true
categories: 技术
tags: iOS
---
iOS多线程编程中，`NSOperation`和`NSOperationQueue`无疑是最常用的，它们能满足绝大部分情况下的线程操作。但在完成一些特殊的任务时，我们还是要使用的NSThread和NSRunLoop。

`NSThread`很好理解，它等同于Java中的Thread类。`NSRunLoop`却不太好理解。从字面上说，RunLoop可以翻译成“运行回路”或“运行循环”，我们可以把它看成是一种特殊的循环结构——我们知道for或者while循环语句，其实NSRunLoop就是一种类似的循环，只不过它比for/while要复杂得多。我相信你已经看过苹果的《多线程编程指南》，其中“Run Loops”有专门的介绍。但这篇文档太长了，我相信你很难把它从头到尾都看完。本文会以实例的方式演示RunnLoop的使用，没有过于复杂的内容，保证你能看懂——有时候恰恰是我们自己把事情搞复杂了。

#一、当前RunLoop

当前RunLoop是指用 CFRunLoopGetCurrent 函数获取的RunLoop，它是运行在当前线程的RunLoop，在没有使用子线程的情况下，当前线程也可能是应用程序的主线程。如果你直接在主线程的方法里使用 CFRunLoopGetCurrent 函数，那么得到的RunLoop就是主线程的RunLoop。

新建Single View Application。在ViewController.xib中拖入一个按钮和一个TextView。并将两个对象都连接到源代码。

实现按钮的Action如下：
```objc
- (IBAction)RunOrStop:(id)sender 
{
    if ([@"Run"isEqualToString:btRun.titleLabel.text]) {
		tvList.text=nil;
		[btRunsetTitle:@"Stop"forState:UIControlStateNormal];
		CFRunLoopTimerRef timer; 
	    CFRunLoopTimerContext timer_context;
	    bzero(&timer_context, sizeof(timer_context));
	    timer_context.info = self; 
	    timer = CFRunLoopTimerCreate(NULL, CFAbsoluteTimeGetCurrent(), 2, 0, 0, _timer, &timer_context);
	    mRunLoopRef=CFRunLoopGetCurrent();
	    CFRunLoopAddTimer( mRunLoopRef, timer, kCFRunLoopCommonModes); 
	    CFRunLoopRun();

 }else{
	[btRunsetTitle:@"Run"forState:UIControlStateNormal];
	if ( mRunLoopRef )
		CFRunLoopStop( mRunLoopRef );
    }

}
```

按钮btRun是一个乒乓式的按钮，用户点击它时它的title会在Run和Stop之间切换。

RunLoop是一种有源循环，它由各种“输入源”进行驱动。类似地，for语句由循环变量进行驱动，当循环变量到达某个值，循环中止。RunLoop的输入源可以有许多类型，这里我们只使用了最普通的定时器 CFRunLoopTimerRef。构造定时器时，需要一个 CFRunLoopTimerContext作为初始化时的上下文。

这个上下文是个结构体（有5个成员），其中info成员是void*类型（即id类型），对于我们来说可以把一些有用的对象传递进去，比如说self——self相当有用，因为self便于我们在c函数中调用成员方法：
```objc
CFRunLoopTimerContext timer_context;
bzero(&timer_context, sizeof(timer_context));
timer_context.info = self;
```

其他4个结构体成员对于我们来说都没有意义。因此上面3句其实也可以写成：
`
CFRunLoopTimerContext timer_context={0, self, NULL, NULL, NULL};
`
接下来就是用这个上下文构造timer：
`
timer= CFRunLoopTimerCreate(NULL, CFAbsoluteTimeGetCurrent(), 2, 0, 0, _timer, &timer_context);
`
除了NULL和0之外的几个参数分别是：定时器启动时间、间隔秒数、定时执行函数、上下文指针。

其他参数我们都明白了，除了定时执行函数_timer——我们呆会再讨论它。接下来：

`mRunLoopRef=CFRunLoopGetCurrent();`一句获取当前线程的RunLoop；同时把RunLoop保存在`mRunLoopRef中。mRunLoopRef`需要声明为静态变量，这样较方便我们在c函数_timer中访问：

`static CFRunLoopRef mRunLoopRef;`

这一句将Timer添加到RunLoop：

`CFRunLoopAddTimer( mRunLoopRef, timer, kCFRunLoopCommonModes);`

这一句启动RunLoop：

`CFRunLoopRun();`

实现_timer()函数如下：
```objc
void _timer(CFRunLoopTimerRef timer __unused, void *info) 
{ 
    loops++;
    id obj=(id)info;
    [obj performSelectorOnMainThread:@selector(updateTextView) withObject:nilwaitUntilDone:NO];

}
```

_timer函数根据约定，为CFRunLoopTimerCallBack结构，因此它拥有两个参数：

`CFRunLoopTimerRef timer, void *info`

loops变量也声明为静态的（方便在c函数中调用），没有什么意义，我们仅仅是用来记录循环次数的。

info参数（实际上我们指定了一个self对象）在这里排上了用场，我们将会在这里调用self的updateTextView方法。因为updateTextView方法会对UI进行更新，根据UKit的规定，对UI进行刷新应当在主线程中进行，所以我们用performSelectorOnMainThread来强制在主线程执行updateView方法。

updateView方法实现如下：
```objc
-(void) updateTextView
{
    tvList.text=[NSStringstringWithFormat:@"%@\n%d",tvList.text,loops];
    NSRange range;
    range = NSMakeRange ([[tvListtext] length], 0);
    [tvListscrollRangeToVisible:range];
}
```
运行程序，当我们点击Run按钮，RunLoop循环会一遍一遍地去执行，同时TextView中会显示执行的循环次数。

等等，为什么会这样？

当你点击“Stop”按钮，发现RunLoop并不会停下来。相反，当你再次点击“Run”按钮之后，RunLoop似乎循环得更快了！基本上达到1秒钟执行一次。如果你反复点击“Stop/Run”按钮，循环会越来越快！

CFRunLoopStop 似乎并没有被执行。其实，getCurrentRunLoop拿到的是当前线程的RunLoop，对于现在的情况，实际上是主线程的RunLoop。你在主线程的RunLoop中添加了新的源，但你并没有权限停止它。而且，由于你多次点击Run按钮，RunLoop中被加入了多个Timer！这导致_timer函数在同一时间内被执行得更多。

要想停止RunLoop，你必需要创建自己的Thread，然后停止它的RunLoop。这样还可以带来另外一个好处：RunLoop不会阻塞主线程！仔细观察程序运行的结果，你会发现当Run按钮被按下时，按钮的状态始终是在Highlight状态，而不会恢复到Normal状态：

Stop按钮背景始终呈现Highlight的蓝色，是因为主线程被RunLoop阻塞了。除非RunLoop停止，按钮不会恢复为Normal状态。

那么，我们只有创建一个NSThread了。

#二、子线程中的RunLoop

每个线程中都自带RunLoop，用`CFRunLoopGetCurrent()`函数可以获得当前线程的RunLoop。如果RunLoop中没有任何源，RunLoop不会运行。我们可以为这个RunLoop添加新的源。

修改RunOrStop方法代码为：
```objc
- (IBAction)RunOrStop:(id)sender 
{
    if ([@"Run"isEqualToString:btRun.titleLabel.text]) {
        tvList.text=nil;
        [btRunsetTitle:@"Stop"forState:UIControlStateNormal];
        NSThread *thread = [[NSThreadalloc] initWithTarget:selfselector:@selector(aThread) object:nil]; 
       [thread start];
    }
    else{
        [btRunsetTitle:@"Run"forState:UIControlStateNormal];
        if ( mRunLoopRef )
            CFRunLoopStop( mRunLoopRef );
    }
}
```
同时实现aThread方法如下：
```objc
-(void)aThread
{
    CFRunLoopTimerRef timer; 
	CFRunLoopTimerContext timer_context={0, self, NULL, NULL, NULL};
    timer = CFRunLoopTimerCreate(NULL, CFAbsoluteTimeGetCurrent(), 2, 0, 0, _timer, &timer_context);
    mRunLoopRef=CFRunLoopGetCurrent();
    CFRunLoopAddTimer( mRunLoopRef, timer, kCFRunLoopCommonModes); 
    CFRunLoopRun();
}
```
可以看到，RunOrStop方法中，我们创建了新的 NSThread对象并启动了它。而原来的RunLoop代码被移到新的线程方法aThread中来了。

运行程序，你在RunLoop运行之后可以用Stop来停止它了。同时，主线程不会再被阻塞，Stop按钮点下后，经过短暂的Highlight状态即恢复到了Normal状态，Stop按钮终于不再是怪异的蓝色了.

#三、添加自定义源

我们还可以尝试定义自定义的输入源。这样，当timer源触发之后，我们还可以调用自定义源，干点别的事。触发另一个源，使用 函数 CFRunLoopSourceSignal ：

`voidCFRunLoopSourceSignal(CFRunLoopSourceRef source);`

 

在_timer函数中加入此句：

`if(source) CFRunLoopSourceSignal(source);`

参数source指定要触发的输入源。

我们修改aThread方法如下：
```objc
-(void)aThread
{
	CFRunLoopSourceContext source_context;
    bzero(&source_context, sizeof(source_context)); 
    source_context.perform = _perform; 
    source = CFRunLoopSourceCreate(NULL, 0,&source_context); 
    CFRunLoopAddSource(CFRunLoopGetCurrent(), source, kCFRunLoopCommonModes);

}
```
其中，source被声明为静态变量：

`staticCFRunLoopSourceRef source;`

然后实现_perform函数：
```objc
void _perform(void *info) 
{ 
	if (loops%10==0) {
        CFRunLoopStop(mRunLoopRef);
        printf("loops=%d,RunLoop is stopped.\n",loops); 
    }
}
```
 

最后修改RunOrStop方法，注释以下语句，因为RunLoop的停止我们交给_perform函数来做了：
```
//       [btRun setTitle:@"Stop" forState:UIControlStateNormal];
//        [btRun setTitle:@"Run"forState:UIControlStateNormal];
//        if ( mRunLoopRef )
//          	CFRunLoopStop( mRunLoopRef );
```

现在执行程序，RunLoop每运行10次就会自动停下来：

loops=10,Run Loop isstopped.

loops=20,Run Loop isstopped.

loops=30,Run Loop isstopped.

四、dispatch source

在iOS异步编程模型中，线程是最传统的解决方案。然而线程模型仍然有着一些为人所诟病的缺点：难于编写、可伸缩性不强。iOS通过dispathqueue和dispatch source来支持并行编程（参考苹果文档《 Concurrency Programming Guide 》）。上述代码也可以用并行并行编程方式来解决。

修改RunoOrStop:的代码为：
```objc
- (IBAction)RunOrStop:(id)sender 
{
    source = dispatch_source_create(DISPATCH_SOURCE_TYPE_DATA_ADD, 0, 0, dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0));
	dispatch_source_set_event_handler(source, ^{ 
		if (loops%10==0) {
			dispatch_source_cancel(source);
			dispatch_release(source);
			dispatch_source_cancel(timer);
			dispatch_release(timer);
			printf("loops=%d,Dispatchsource is stopped.\n",loops); 
        }
    }); 

    dispatch_resume(source);
    timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)); 
    dispatch_source_set_timer(timer, DISPATCH_TIME_NOW, 1ull * NSEC_PER_SEC, 0);  
    dispatch_source_set_event_handler(timer, ^{
        loops++;
        [selfperformSelectorOnMainThread:@selector(updateTextView) withObject:nilwaitUntilDone:NO];
        dispatch_source_merge_data(source, 1); 
    }); 
    dispatch_resume(timer);

}
```
其中timer和source声明为外部静态变量:

`static dispatch_source_t source,timer;`

运行程序。没有使用线程、没有RunLoop，但仍然实现了同样的效果。从中可以看出，dispatch queue并行编程拥有许多优点：不需要显式地创建线程和为线程分配栈空间、代码极大地简化、块语法支持。
[转自]: <http://blog.csdn.net/kmyhy/article/details/7774618>