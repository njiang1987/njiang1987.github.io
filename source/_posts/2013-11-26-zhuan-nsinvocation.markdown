---
layout: post
title: '[转]NSInvocation'
categories:
- iOS
tags: []
published: true
comments: true
---
<p>An NSInvocation is an Objective-C message rendered static, that is, it is an action turned into an object. NSInvocation objects are used to store and forward messages between objects and between applications, primarily by NSTimer objects and the distributed objects system.</p>

<p>An NSInvocation object contains all the elements of an Objective-C message: a target, a selector, arguments, and the return value. Each of these elements can be set directly, and the return value is set automatically when the NSInvocation object is dispatched.</p>

<p>An NSInvocation object can be repeatedly dispatched to different targets; its arguments can be modified between dispatch for varying results; even its selector can be changed to another with the same method signature (argument and return types). This flexibility makes NSInvocation useful for repeating messages with many arguments and variations; rather than retyping a slightly different expression for each message, you modify the NSInvocation object as needed each time before dispatching it to a new target.</p>

<p>NSInvocation does not support invocations of methods with either variable numbers of arguments or union arguments. You should use the invocationWithMethodSignature: class method to create NSInvocation objects; you should not create these objects using <a href="https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSObject_Class/Reference/Reference.html#//apple_ref/occ/clm/NSObject/alloc">alloc</a> and <a href="https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSObject_Class/Reference/Reference.html#//apple_ref/occ/instm/NSObject/init">init</a>.</p>

<p>This class does not retain the arguments for the contained invocation by default. If those objects might disappear between the time you create your instance of NSInvocation and the time you use it, you should explicitly retain the objects yourself or invoke the retainArguments method to have the invocation object retain them itself.</p>

<p><b>Note:</b> NSInvocation conforms to the <a href="https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Protocols/NSCoding_Protocol/Reference/Reference.html#//apple_ref/occ/intf/NSCoding">NSCoding</a> protocol, but only supports coding by an <a href="https://developer.apple.com/library/mac/documentation/Cocoa/Reference/Foundation/Classes/NSPortCoder_Class/Reference/Reference.html#//apple_ref/occ/cl/NSPortCoder">NSPortCoder</a>. NSInvocation does not support archiving.</p>

<p>TestProject<br />
File - MyClass.h
<pre lang="OBJC">#import &lt;Foundation/Foundation.h&gt;</pre></p>

<p>@interface MyClass : NSObject</p>

<p>- (NSString*)appendMyString:(NSString*)string;</p>

<p>@end
File - MyClass.m
<pre lang="OBJC">#import "MyClass.h"</pre></p>

<p>@implementation MyClass</p>

<p>- (id)init<br />
{
    self = [super init];<br />
    if (self) {<br />
        // init<br />
    }<br />
    return self;<br />
}</p>

<p>- (NSString*)appendMyString:(NSString *)string<br />
{
    NSString* myString = [NSString stringWithFormat:@"%@ after append method", string];<br />
    return myString;<br />
}</p>

<p>- (void)dealloc<br />
{
    [super dealloc];<br />
}</p>

<p>@end
File - main.m
<pre lang="OBJC">#import &lt;Foundation/Foundation.h&gt;
#import "MyClass.h"</pre></p>

<p>int main(int argc, const char * argv[])<br />
{
    NSAutoreleasePool* pool = [[NSAutoreleasePool alloc] init];</p>

<p>    MyClass* myClass = [[MyClass alloc] init];<br />
    NSString* myString = @"My string";</p>

<p>    NSString* normalInvokeString = [myClass appendMyString:myString];<br />
    NSLog(@"The normal invoke string is: %@", normalInvokeString);</p>

<p>    SEL mySelector = @selector(appendMyString:);<br />
    NSMethodSignature* sig = [MyClass instanceMethodSignatureForSelector:mySelector];<br />
    NSInvocation* myInvocation = [NSInvocation invocationWithMethodSignature:sig];<br />
    [myInvocation setTarget:myClass];<br />
    [myInvocation setSelector:mySelector];</p>

<p>    [myInvocation setArgument:&amp;myString atIndex:2];</p>

<p>    NSString* result = nil;<br />
    [myInvocation retainArguments];<br />
    [myInvocation invoke];<br />
    [myInvocation getReturnValue:&amp;result];<br />
    NSLog(@"The NSInvocation invoke string is: %@", result);</p>

<p>    [myClass release];</p>

<p>    [pool drain];<br />
    return 0;<br />
}
The result is like below
<img src="http://www.njiang1987.com/wp-content/gallery/testprojectscreenshot/screen-shot-2013-11-26-at-11-07-56-am.png" alt="" /></p>
