---
layout: post
title: "Investigate on CGContext and implement Wifi view"
date: 2014-08-21 23:46:04 +0800
comments: true
categories: 技术
tags: iOS
---
Today, I did some research on CGContext. And implement an animation graph and Wifi view. Please the code below.

Here is the screen shot. 

{% img center /uploads/2014/08/22/1.png 320 568 %}

```objc
//
//  TestView.m
//  Depression
//
//  Created by jn11585852 on 8/21/14.
//  Copyright (c) 2014 JiangNan. All rights reserved.
//

#import "TestView.h"

@interface TestView ()
@property (nonatomic, assign) CGFloat percent;
@property (nonatomic, retain) NSTimer* timer;
@property (nonatomic, assign) CGFloat timeInterval;

@end

@implementation TestView
@synthesize timer = _timer;

- (void)didMoveToWindow
{
    [super didMoveToWindow];
    self.percent = 0.0f;
    self.timeInterval = 0.01;
}

- (void)startAnimation
{
    // start a timer to re-render the view
    self.timer = [NSTimer scheduledTimerWithTimeInterval:self.timeInterval target:self selector:@selector(increaseAndRender) userInfo:nil repeats:YES];
}

- (void)stopAnimation
{
    [self.timer invalidate];
    self.timer = nil;
}

- (void)increaseAndRender
{
    // called once time when time invoke it. so we need to increase the percent by  on step
    CGFloat step = self.finalPercent / (1.0 / self.timeInterval);
    self.percent += step;
    // if the percent is bigger than the final percent, we should stop the timer
    if (self.percent > self.finalPercent) {
        [self.timer invalidate];
        self.timer = nil;
    }
    [self setNeedsDisplay];
}


// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    CGContextRef ctx = UIGraphicsGetCurrentContext();
    CGContextSaveGState(ctx);
    
    [self drawRectangle:ctx];
    [self drawCircle:ctx];
    [self drawWifi:ctx];
    
    CGContextRestoreGState(ctx);
}

- (void)drawRectangle:(CGContextRef)ctx
{
    CGContextSetStrokeColorWithColor(ctx, [[UIColor greenColor] CGColor]);
    CGContextSetFillColorWithColor(ctx, [[UIColor lightGrayColor] CGColor]);
    CGContextMoveToPoint(ctx, 20, 50);
    CGContextAddLineToPoint(ctx, 300, 50);
    CGContextAddLineToPoint(ctx, 300, 60);
    CGContextAddLineToPoint(ctx, 20, 60);
    CGContextClosePath(ctx);
    
    CGPathRef path = CGContextCopyPath(ctx);
    CGContextStrokePath(ctx);
    CGContextAddPath(ctx, path);
    CGContextFillPath(ctx);
    
    CGContextSetFillColorWithColor(ctx, [[UIColor redColor] CGColor]);
    CGContextMoveToPoint(ctx, 20, 50);
    CGContextAddLineToPoint(ctx, 20 + 280 * self.percent, 50);
    CGContextAddLineToPoint(ctx, 20 + 280 * self.percent, 60);
    CGContextAddLineToPoint(ctx, 20, 60);
    CGContextClosePath(ctx);
    CGContextFillPath(ctx);
}

- (void)drawCircle:(CGContextRef)ctx
{
    [self drawCurve:ctx start:0 end:self.percent color:[[UIColor redColor] CGColor]];
    
    if (self.percent > 0.3) {
        [self drawCurve:ctx start:0.3 end:self.percent color:[[UIColor greenColor] CGColor]];
    }
    
    if (self.percent > 0.6) {
        [self drawCurve:ctx start:0.6 end:self.percent color:[[UIColor blackColor] CGColor]];
    }
}

- (void)drawCurve:(CGContextRef)ctx start:(CGFloat)start end:(CGFloat)end color:(CGColorRef)color
{
    [self drawCurve:ctx start:start end:end color:color radius:100 center:CGPointMake(200, 200)];
}

- (void)drawWifi:(CGContextRef)ctx
{
    // it is very interesting here, we will draw it from outside to inside. final there is only a circle.
    for (int radius = 50; radius > 0; ) {
        [self drawCurve:ctx start:0.625 end:0.875 color:[[UIColor greenColor] CGColor] radius:radius center:CGPointMake(100, 400)];
        
        radius -= 20;
    }
}

- (void)drawCurve:(CGContextRef)ctx start:(CGFloat)start end:(CGFloat)end color:(CGColorRef)color radius:(CGFloat)radius center:(CGPoint)center
{
    // draw a big arc
    CGContextSetFillColorWithColor(ctx, color);
    CGContextMoveToPoint(ctx, center.x, center.y);
    CGContextAddArc(ctx, center.x, center.y, radius, 2 * M_PI * start, 2 * M_PI * end, 0);
    CGContextClosePath(ctx);
    CGContextFillPath(ctx);
    
    // then draw the inside small one
    CGContextSetFillColorWithColor(ctx, [[UIColor whiteColor] CGColor]);
    CGContextMoveToPoint(ctx, center.x, center.y);
    CGContextAddLineToPoint(ctx, center.x + radius - 10, center.y);
    CGContextAddArc(ctx, center.x, center.y, radius - 10, 0, 2 * M_PI, 0);
    CGContextClosePath(ctx);
    CGContextFillPath(ctx);
}

@end

```