---
layout: post
title: '[iOS]关于CALayer和UIView Animation同步问题'
categories:
- 技术
tags: [iOS]
published: true
comments: true
---
<p>今天在做项目的时候, 同时用到了CABasicAnimation和UIView的animation， 发现会有问题，calayer的animation和uiview的animation不同步，比如CALayer设置position的animation
<pre lang="objc" colla="+">CABasicAnimation* animation = [CABasicAnimation animationWithKeyPath:@"position"];
animation.fromValue = [NSValue valueWithCGPoint:startpoint];
animation.toValue = [NSValue valueWithCGPoint:endpoint];
animation.duration = INFO_WINDOW_SLIDE_ANIMATION_TIME;
animation.timingFunction = [CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseIn];
[blurredLayer addAnimation:animation forKey:@"appear"];
</pre></p>

<p>UIView 的animation：
<pre lang="objc" colla="+">backgroundView.frame = startframe;
[UIView animateWithDuration:INFO_WINDOW_SLIDE_ANIMATION_TIME delay:0 options:UIViewAnimationOptionCurveEaseIn animations:^{
        backgroundView.frame = endframe;
} completion:NULL];
</pre>
blurredLayer会抖动。后来再stackoverflow上面找到解决方法是将CALayer的animation换成
<pre lang="objc" colla="+">
blurredLayer.position = startpoint;
[CATransaction begin];
[CATransaction setAnimationDuration:INFO_WINDOW_SLIDE_ANIMATION_TIME];
[CATransaction setAnimationTimingFunction:[CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseIn]];
blurredLayer.position = endpoint;
[CATransaction commit];
</pre>
这样两个animation就同步了，具体原因不详。</p>
