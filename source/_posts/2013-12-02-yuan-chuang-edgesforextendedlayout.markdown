---
layout: post
title: '[StackOverflow]edgesForExtendedLayout'
categories:
- 技术
tags: [iOS]
published: true
comments: true
---
<p>Starting in iOS7, the view controllers use full-screen layout by default. At the same time, you have more control over how it lays out its views, and that's done with those properties:</p>

<p><strong>edgesForExtendedLayout</strong></p>

<p>Basically, with this property you set which sides of your view can be extended to cover the whole screen. Imagine that you push a <code>UIViewController</code> into a <code>UINavigationController</code>, when the view of that view controller is laid out, it will start where the navigation bar ends, but this property will set which sides of the view (top, left, right, bottom) can be extended to fill the whole screen.</p>

<p>Let see it with an example:
<pre><code>UIViewController *viewController = [[UIViewController alloc] init];
viewController.view.backgroundColor = [UIColor redColor];
UINavigationController *mainNavigationController = [[UINavigationController alloc] initWithRootViewController:viewController];</code></pre>
Here you are not setting the value of edgesForExtendedLayout, therefore the default value is taken (UIRectEdgeAll), so the view extends its layout to fill the whole screen.</p>

<p>This is the result:</p>

<p><img alt="enter image description here" src="http://i.stack.imgur.com/MOB6v.png" /></p>

<p>As you can see, the red background extends behind the navigation bar and the status bar.</p>

<p>Now, you are going to set that value to UIRectEdgeNone, so you are telling the view controller to not extend the view to cover the screen:
<pre><code>UIViewController *viewController = [[UIViewController alloc] init];
viewController.view.backgroundColor = [UIColor redColor];
viewController.edgesForExtendedLayout = UIRectEdgeNone;
UINavigationController *mainNavigationController = [[UINavigationController alloc] initWithRootViewController:viewController];</code></pre>
And the result:</p>

<p><img alt="enter image description here" src="http://i.stack.imgur.com/ojAvO.png" /></p>

<p><strong>automaticallyAdjustsScrollViewInsets</strong></p>

<p>This property is used when your view is a <code>UIScrollView</code> or similar, like a <code>UITableView</code>. You want your table to start where the navigation bar ends, because you wont see the whole content if not, but at the same time you want your table to cover the whole screen when scrolling. In that case, setting edgesForExtendedLayout to None won't work because your table will start scrolling where the navigation bar ends and it wont go behind it.</p>

<p>Here is where this property comes handy, if you let the view controller automatically adjust the insents (setting this property to YES, also the default value) it will add inset to the top of the table, so the table will start where the navigation bar ends, but the scroll will cover the whole screen.</p>

<p>This is when is set to NO:</p>

<p><img alt="enter image description here" src="http://i.stack.imgur.com/9Iapl.png" /></p>

<p>And YES (by default):</p>

<p><img alt="enter image description here" src="http://i.stack.imgur.com/VVQHQ.png" /></p>

<p>In both cases, the table scrolls behind the navigation bar, but in the second case (YES), it will start from below the navigation bar.</p>

<p><strong>extendedLayoutIncludesOpaqueBars</strong></p>

<p>This value is just an addition to the previous ones. If the status bar is opaque, the views won't be extended to include the status bar too, unless this parameter is YES.</p>

<p>So, if you extend your view to cover the navigation bar (edgesForExtendedLayout to UIRectEdgeAll) and the parameter is NO (default) it wont covert the status bar if it's opaque.</p>

<p>If something is not clear, write a comment and I'll answer to it.</p>
