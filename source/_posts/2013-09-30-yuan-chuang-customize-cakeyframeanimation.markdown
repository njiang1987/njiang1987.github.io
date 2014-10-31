---
layout: post
title: '[原创]Customize CAKeyframeAnimation'
categories:
- iOS
tags: []
published: true
comments: true
---
<p>可以个性化设置function函数，easy in or easy out。</p>

<p><pre lang="objc">    KeyframeParametricBlock funciton = ^double(double time){
        return time * time * time;
    };
    NSUInteger steps = 100;</pre></p>

<p>    [CATransaction begin];<br />
    [CATransaction setAnimationDuration:duration];</p>

<p>    CAKeyframeAnimation* animation1 = [CAKeyframeAnimation animationWithKeyPath:@"transform"];<br />
    NSMutableArray* values = [NSMutableArray arrayWithCapacity:steps];<br />
    NSMutableArray* times = [NSMutableArray arrayWithCapacity:steps];<br />
    double fromValue = 0.1f;<br />
    double toValue = 1.0f;<br />
    double time = 0.0f;<br />
    for (NSUInteger i = 0; i &lt; steps; i++) {<br />
        double value = fromValue + (toValue - fromValue) * funciton(time);<br />
        CGAffineTransform trans = CGAffineTransformMakeScale(value, value);<br />
        CATransform3D trans3D = CATransform3DMakeAffineTransform(trans);<br />
        [values addObject:[NSValue valueWithCATransform3D:trans3D]];<br />
        [times addObject:[NSNumber numberWithFloat:time]];<br />
        time += 1 / (double)(steps - 1);<br />
    }<br />
    [animation1 setValues:values];<br />
    [animation1 setKeyTimes:times];<br />
    [animation1 setCalculationMode:kCAAnimationLinear];<br />
    [animation1 setDuration:duration];<br />
    [animation1 setFillMode:kCAFillModeForwards];</p>

<p>    CAKeyframeAnimation* animation2 = [CAKeyframeAnimation animationWithKeyPath:@"position"];<br />
    [values removeAllObjects];<br />
    time = 0.0f;<br />
    fromValue = imageSize.width / 2.0f;<br />
    toValue = imageSize.width / 2.0f + 400;<br />
    for (NSUInteger i = 0; i &lt; steps; i++) {<br />
        double value = fromValue + (toValue - fromValue) * funciton(time);<br />
        CGPoint point = CGPointMake(value, imageSize.height / 2.0);<br />
        [values addObject:[NSValue valueWithCGPoint:point]];<br />
        time += 1 / (double)(steps - 1);<br />
    }<br />
    [animation2 setValues:values];<br />
    [animation2 setKeyTimes:times];<br />
    [animation2 setCalculationMode:kCAAnimationLinear];<br />
    [animation2 setDuration:duration];<br />
    [animation2 setFillMode:kCAFillModeForwards];</p>

<p>    CAAnimationGroup* theGroup = [[CAAnimationGroup alloc] init];<br />
    theGroup.animations = [NSArray arrayWithObjects:animation1, animation2, nil];<br />
    theGroup.duration = duration;<br />
    [_imageView.layer addAnimation:theGroup forKey:@"appear"];<br />
    _imageView.layer.transform = CATransform3DIdentity;<br />
    _imageView.layer.position = CGPointMake(400 + imageSize.width / 2.0, imageSize.height / 2.0);</p>

<p>    [CATransaction commit];</p>

<p>    [CATransaction begin];</p>

<p>    CAKeyframeAnimation* animation3 = [CAKeyframeAnimation animationWithKeyPath:@"transform"];<br />
    [values removeAllObjects];<br />
    NSArray* tArrary = [animation1 values];<br />
    for (int i = 0; i &lt; [tArrary count]; i++) {<br />
        CATransform3D trans3D = [(NSValue*)[tArrary objectAtIndex:i] CATransform3DValue];<br />
        CATransform3D invert3D = CATransform3DInvert(trans3D);<br />
        [values addObject:[NSValue valueWithCATransform3D:invert3D]];<br />
    }<br />
    [animation3 setValues:values];<br />
    [animation3 setKeyTimes:times];<br />
    [animation3 setCalculationMode:kCAAnimationLinear];<br />
    [animation3 setDuration:duration];<br />
    [animation3 setFillMode:kCAFillModeForwards];</p>

<p>    CAKeyframeAnimation* animation4 = [CAKeyframeAnimation animationWithKeyPath:@"position"];<br />
    [values removeAllObjects];<br />
    tArrary = [animation2 values];<br />
    NSArray* transformArray = [animation1 values];<br />
    CGPoint point1 = CGPointMake(400 + imageSize.width / 2.0, imageSize.height / 2.0);<br />
    for (int i = 0; i &lt; [tArrary count]; i++) {<br />
        CGPoint point0 = [(NSValue*)[tArrary objectAtIndex:i] CGPointValue];<br />
        CATransform3D transform3D = [(NSValue*)[transformArray objectAtIndex:i] CATransform3DValue];<br />
        CGAffineTransform ptransform = CGAffineTransformMake(transform3D.m11, transform3D.m12, transform3D.m21, transform3D.m22, transform3D.m41, transform3D.m42);<br />
        double scaleX = transform3D.m11;<br />
        double scaleY = transform3D.m22;<br />
        double x = point1.x - imageSize.width / 2.0 - point0.x + imageSize.width * scaleX / 2.0 + imageSize.width / 2.0;<br />
        double y = point1.y - imageSize.height / 2.0 - point0.y + imageSize.height * scaleY / 2.0 + imageSize.height / 2.0;<br />
        point = CGPointMake(x, y);<br />
        point = CGPointApplyAffineTransform(point, CGAffineTransformInvert(ptransform));<br />
        [values addObject:[NSValue valueWithCGPoint:point]];<br />
    }<br />
    [animation4 setValues:values];<br />
    [animation4 setKeyTimes:times];<br />
    [animation4 setCalculationMode:kCAAnimationLinear];<br />
    [animation4 setDuration:duration];<br />
    [animation4 setFillMode:kCAFillModeForwards];</p>

<p>    theGroup = [[CAAnimationGroup alloc] init];<br />
    theGroup.animations = [NSArray arrayWithObjects:animation3, animation4, nil];<br />
    theGroup.duration = duration;<br />
    [blurredLayer addAnimation:theGroup forKey:@"appear"];<br />
    blurredLayer.transform = CATransform3DIdentity;</p>

<p>    [CATransaction commit];</p>
