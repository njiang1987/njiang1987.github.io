---
layout: post
title: '[StackOverflow]NSOperation和dispatch_async的区别'
categories:
- 技术
tags: [StackOverflow]
published: true
comments: true
---
<p><code>NSOperation*</code> classes are the higher level api. They hide GCD's lower level api from you so that you can concentrate on getting the task done.</p>

<p>The rule of thumb is: <strong>Use the api of the highest level first and then degrade based on what you need to accomplish.</strong></p>

<p>The advantage of this approach is that your code stays most agnostic to the specific implementation the vendor provides. In this example, using <code>NSOperation</code>, you'll be using Apple's implementation of execution queueing (using GCD). Should Apple ever decide to change the details of implementation behind the scenes they can do so without breaking your application's code.<br />
One such example would be Apple deprecating GCD and using a completely different library (which is unlikely because Apple created GCD and everybody seems to love it).</p>

<p>Regarding the matter i recommend consulting the following resources:
<ul>
	<li><a href="http://cocoasamurai.blogspot.de/2009/09/guide-to-blocks-grand-central-dispatch.html">http://cocoasamurai.blogspot.de/2009/09/guide-to-blocks-grand-central-dispatch.html</a></li>
	<li><a href="http://cocoasamurai.blogspot.de/2009/09/making-nsoperation-look-like-gcd.html">http://cocoasamurai.blogspot.de/2009/09/making-nsoperation-look-like-gcd.html</a></li>
	<li><a href="http://www.raywenderlich.com/19788/how-to-use-nsoperations-and-nsoperationqueues">http://www.raywenderlich.com/19788/how-to-use-nsoperations-and-nsoperationqueues</a></li>
	<li><a href="https://developer.apple.com/library/mac/#documentation/Cocoa/Reference/NSOperationQueue_class/Reference/Reference.html">https://developer.apple.com/library/mac/#documentation/Cocoa/Reference/NSOperationQueue_class/Reference/Reference.html</a></li>
</ul></p>
