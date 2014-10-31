---
layout: post
title: "关于CALAYER和UIVIEW ANIMATION同步问题"
date: 2014-01-13 18:08:00 +0800
comments: true
categories: iOS CALayer UIViewAnimation 
---
今天在做项目的时候, 同时用到了CABasicAnimation和UIView的animation， 发现会有问题，calayer的animation和uiview的animation不同步，比如CALayer设置position的animation

{% codeblock lang:objc %}
CABasicAnimation* animation = [CABasicAnimation animationWithKeyPath:@"position"];
animation.fromValue = [NSValue valueWithCGPoint:startpoint];
animation.toValue = [NSValue valueWithCGPoint:endpoint];
animation.duration = INFO_WINDOW_SLIDE_ANIMATION_TIME;
animation.timingFunction = [CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseIn];
[blurredLayer addAnimation:animation forKey:@"appear"];
{% endcodeblock %}

UIView 的animation：
{% codeblock lang:objc %}
backgroundView.frame = startframe;
[UIView animateWithDuration:INFO_WINDOW_SLIDE_ANIMATION_TIME delay:0 options:UIViewAnimationOptionCurveEaseIn animations:^{
        backgroundView.frame = endframe;
} completion:NULL];
{% endcodeblock %}

blurredLayer会抖动。后来再stackoverflow上面找到解决方法是将CALayer的animation换成
{% codeblock lang:objc %}
blurredLayer.position = startpoint;
[CATransaction begin];
[CATransaction setAnimationDuration:INFO_WINDOW_SLIDE_ANIMATION_TIME];
[CATransaction setAnimationTimingFunction:[CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseIn]];
blurredLayer.position = endpoint;
[CATransaction commit];
{% endcodeblock %}
这样两个animation就同步了，具体原因不详。