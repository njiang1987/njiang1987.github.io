title: "[iOS]Core Animation 读书笔记"
categories:
  - 技术
date: 2014-11-14 16:42:38
tags: [iOS]
photos:
- /uploads/header/meinv.jpg
---

##摘要
Core Animation的核心是layer objects，它被用来控制并操作显示的内容。Layer其实是内容的到bitmap得映射，这个bitmap很容易被硬件操作。
如果修改layer的property，例如opacity，会触发隐式动画(implicit animation)，也可以设置显示的动画。隐式的动画是通过action object来实现的。在OS X上面的程序，需要显示的激活layer。
Core Animation位于AppKit和UIKit之下，
![](/uploads/2014/11/14/ca_architecture_2x.png)

##Core Animation基本知识
###Layer提供了渲染以及动画的基本逻辑
layer objects表面是2d的，但从从组织形式上是3d的。
	与view的共同点：位置，内容，和虚拟的属性。
	与view的不同点：layer不会定义他们自己的样子。

基于layer的渲染模型：
layer也可以叫做backing store，它会将内容备份到bitmap里面。等需要触发动画时，Core Animation会将layer的bitmap和状态信息发送给图像硬件，根据最新的信息，由图像硬件来负责渲染，这个要比软件实现动画要快很多。如下图显示：
![](/uploads/2014/11/14/basics_layer_rendering_2x.png)

基于view的渲染，通过在drawRect：里面读取状态值来画content，代价非常高。

基于layer的动画：L
只需要设置开始与结束的状态信息，Core Animation来负责一帧一帧的渲染。
![](/uploads/2014/11/14/basics_animation_types_2x.png)

###Layer Objects用自己的几何位置
layer的一个职责就是来管理内容的虚拟位置，可使用基于点坐标系统和统一的坐标系统。在iOS和Mac OS上面用得不同的坐标系，
基于点坐标
![](/uploads/2014/11/14/layer_coords_bounds_2x.png)
从上图可以看出layer的position时位于中间的。
基于统一的坐标系统
![](/uploads/2014/11/14/layer_coords_unit_2x.png)
不管是点坐标还是统一坐标 用floating-point数字。

Anchor Points回影响到位置的变化：
![](/uploads/2014/11/14/layer_coords_anchorpoint_position_2x.png)
下图显示了anchor point是怎么影响旋转的
![](/uploads/2014/11/14/layer_coords_anchorpoint_transform_2x.png)

layer可以进行三维操作
一般transform可以用来改变layer的大小及旋转角度。一般情况下不会直接用这个旋转矩阵，可以通过KVC来设置layer属性达到动画效果。如下图所示：
![](/uploads/2014/11/14/transform_basic_math_2x.png)
以下是几个常用的旋转矩阵，
![](/uploads/2014/11/14/transform_manipulations_2x.png)

###Layer Tree从不同方面反应动画时期
一共有3种layer objects：
Model layer tree：是跟app交互最多的，它存储了动画所要修改的属性的目标值。
Presentation tree：包含了动画运行中的值。这个tree里面的值不能直接修改，而是在动画过程中读取，根据状态来创建新的动画。
Render tree：负责具体动画效果，对于Core Animation是私有的。

Layer Tree的初始状态跟View hierarchy是完全一样的。Layer Hierarchy如下：
![](/uploads/2014/11/14/sublayer_hierarchy_2x.png)

通过presentaionLayer来获取动画种某个属性值，并且render tree跟presentation tree是一一对应的，如下图
![](/uploads/2014/11/14/sublayer_hierarchies_2x.png)

###Layer与View的关系
首先layer不能替代view，layer提供了view的基础设施，它会让绘制以及让内容运动起来更容易，

Layer与View的不同：Layer不处理事件，渲染内容参与响应连。

##配置Layer Objects
###激活Core Animation
对于OS X来说，需要显示的激活layer，需要做如下几部：
1. 添加QuartzCore framework.
2. 激活NSView的layer支持。

可以重写`+[UIVIew layerClass]`方法来创建个性化的layer，一般来说iOS回创建`CALayer`。如下几种情况可以替换layer class
1. view的内容是用OpenGL ES画的，你会用到`CAEAGLLayer`。
2. Layer提供了更好的性能。
3. 希望更好的利用Core Animation layer的类。

###配置Layer的内容
可以通过以下3种方法来设置Layer的内容：
1. 将一个image的object设到Layer的`contents`上去。
2. 设置Layer的delegate，由delegate来提供layer的内容。
3. 重新定义一个layer的子类，在内部重画layer的content。

如果设置layer的delegate来绘制内容，需要实现`displayLayer:`或`drawLayer:inContext:`方法，前者优先级高。例如：
```objc
- (void)displayLayer:(CALayer *)theLayer {
    // Check the value of some state property
    if (self.displayYesImage) {
        // Display the Yes image
        theLayer.contents = [someHelperObject loadStateYesImage];
    }
    else {
        // Display the No image
        theLayer.contents = [someHelperObject loadStateNoImage];
    }
}
```
```objc
- (void)drawLayer:(CALayer *)theLayer inContext:(CGContextRef)theContext {
    CGMutablePathRef thePath = CGPathCreateMutable();
 
    CGPathMoveToPoint(thePath,NULL,15.0f,15.f);
    CGPathAddCurveToPoint(thePath,
                          NULL,
                          15.f,250.0f,
                          295.0f,250.0f,
                          295.0f,15.0f);
 
    CGContextBeginPath(theContext);
    CGContextAddPath(theContext, thePath);
 
    CGContextSetLineWidth(theContext, 5);
    CGContextStrokePath(theContext);
 
    // Release the path
    CFRelease(thePath);
}
```
可以设置layer contentsGravity的属性，总体可以分为2类
1. 基于位置的gravity。
![](/uploads/2014/11/14/layer_contentsgravity1_2x.png)
2. 基于缩放的gravity。
![](/uploads/2014/11/14/positioningmask_2x.png)

###调整Layer的显示及外观
Layer有自己的背景和边框
![](/uploads/2014/11/14/layer_border_background_2x.png)

Layer还支持圆角：`cornerRadius`，圆角会触发layer的transparency的属性，只有设置了`masksToBounds = YES`才会影响里面内容。
![](/uploads/2014/11/14/layer_corner_radius_2x.png)

Layer支持阴影：可以通过设置Layer的`content`,`opacity`和`shape`来控制shadow的颜色位置。
shadow是超出layer的content的，如果设置了`masksToBounds`，shadow就会没掉，所以如果即需要`masksToBounds`又需要shadow，就需要用2个layer来模拟。
如图：
![](/uploads/2014/11/14/layer_shadows_2x.png)

还可以未layer添加滤镜，`filters`是一个list，它只会影响到前面的内容，`backgroundFilters`只会影响到背后内容，`compositingFilter`定义了怎么将前面的内容和后面的内容融合在一起。
```objc
CIFilter* aFilter = [CIFilter filterWithName:@"CIPinchDistortion"];
[aFilter setValue:[NSNumber numberWithFloat:500.0] forKey:@"inputRadius"];
[aFilter setValue:[NSNumber numberWithFloat:1.25] forKey:@"inputScale"];
[aFilter setValue:[CIVector vectorWithX:250.0 Y:150.0] forKey:@"inputCenter"];
myLayer.filters = [NSArray arrayWithObject:aFilter];
```
##让Layer内容动起来
###通过修改属性来生成动画
可以显式和隐式的触发动画。直接设置Layer属性就可以触发隐式动画。

###用关键帧动画
设置values的最主要的方式就是用array来保存值，不过像`anchorPoint`和`position`的话，可以用`CGPathRef`来代替。
指定关键帧动画的时间：`calculationMode`定义了动画时间的算法

###使当前正在进行的显式动画停止
停止一个可以调用`removeAnimationForKey:`，与之对应的是`addAnimation:forKey:`。
停止多个动画可以调用`removeAllAnimations`。
隐式动画不能中途停止。

###让多个改动同时进行动画
可以将动画打包成`CAAnimationGroup`

###判定动画的结束时刻
1. 设置`setCompletionBlock:`来表示当前的动画已结束。
2. 设置`CAAnimation`的delegate，病实现`animationDidStart:`和`animationDidStop:finished:`。

##建立Layer Hierarchy
再添加子layer的时候，必须设置大小和位置属性，要用整数来设置layer的高度和宽度。
Layer Hierarchies是通过speed来影响动画的，而且会叠加。

###Sublayer以及裁剪
可以通过设置`masksToBounds`为YES来达到裁剪的目的。
![](/uploads/2014/11/14/clipping_2x.png)

可以通过以下几个API进行坐标切换
```objc
convertPoint:fromLayer:
convertPoint:toLayer:
convertRect:fromLayer:
convertRect:toLayer:
```

##动画的高级技巧
###过度动画
过度动画可以让你进行显示、推送、移动或者交叉动画。创建果冻动画，首先需要创建一个`CATransition`，然后将它添加到layer里面。
```objc
CATransition* transition = [CATransition animation];
transition.startProgress = 0;
transition.endProgress = 1.0;
transition.type = kCATransitionPush;
transition.subtype = kCATransitionFromRight;
transition.duration = 1.0;
 
// Add the transition animation to both layers
[myView1.layer addAnimation:transition forKey:@"transition"];
[myView2.layer addAnimation:transition forKey:@"transition"];
 
// Finally, change the visibility of the layers.
myView1.hidden = YES;
myView2.hidden = NO;
```

###个性化设置动画时间
可以通过`CAMediaTiming`协议定义的属性和方法来设置动画的时间，`CAAnimation`和`CALayer`都遵循这个协议。每个Layer都有其自己的时间系统，用来控制动画的计时。子layer的时间系统可以被其父节点的layer修改。可以通过以下方法获取layer的当前时间：
```objc
CFTimeInterval localLayerTime = [myLayer convertTime:CACurrentMediaTime() fromLayer:nil];
```
可以通过以下方法来设置动画时间：
1. `beginTime`设置动画开始时间，而且需要设置`fillMode = kCAFillModebackwards`，如果不设置，就会看到再动画开始之前，就瞬间完成了。
2. `autoreverses`用来控制动画在特定的时间点，回到动画开始的值。可以结合`repeatCount`来设置重复的次数。
3. `timeOffset`可以设置group animation的延迟开始时间。

###暂停和恢复动画
可以通过设置`CAMediaTiming`协议的`speed = 0`来暂停动画。

##修改Layer默认的行为
Core Animation是用action objects来实现的隐式动画，Action objects其实就是一个遵循`CAAction`协议的变量，且定义了对于layer的相关行为。所有的`CAAnimation`都实现了这个协议。

###创建遵循`CAAction`协议的Action Objects
需要实现函数`runActionForKey:object:arguments:`，当定义action object的时候，必须确定这个怎么触发：
1. layer的属性改变，包括哪些没有定义动画的属性。
2. layer再显示出来或者加到layer hierarchy的时候，会触发key - `kCAOnOrderIn`。
3. layer再参与渐变的动画过程中，会触发key - `kCATransition`。

###Action Object必须设置再layer上
当相应的事件再layer上面触发时，layer的`actionForKey:`会被调用到。寻找action object的优先级如下：
1. 如果有delegate 定义了`actionForLayer:forKey:`，就会调用delegate这个方法：如果是action object直接返回；如果是nil，继续寻找；如果是`NSNull`，直接退出。
2. 查找`actions`这个字典中的变量。
3. 需要两级，先查找`style`的字典，找到定义action的字典，再在这个字典中查找action objects。
4. 直接调用`defaultActionForKey:`方法。
5. 如果有隐式的动画，执行隐式动画。

示例代码如下：
```objc
- (id<CAAction>)actionForLayer:(CALayer *)theLayer
                        forKey:(NSString *)theKey {
    CATransition *theAnimation=nil;
 
    if ([theKey isEqualToString:@"contents"]) {
 
        theAnimation = [[CATransition alloc] init];
        theAnimation.duration = 1.0;
        theAnimation.timingFunction = [CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseIn];
        theAnimation.type = kCATransitionPush;
        theAnimation.subtype = kCATransitionFromRight;
    }
    return theAnimation;
}
```

###暂时禁掉动画
代码如下：
```objc
[CATransaction begin];
[CATransaction setValue:(id)kCFBooleanTrue
                 forKey:kCATransactionDisableActions];
[aLayer removeFromSuperlayer];
[CATransaction commit];
```

##改善动画的技巧
1. 用不透明的layer，
2. 用更简单的paths - `CAShapeLayer`
3. 对于可区分的layer，显式设置layer的内容
4. 总是将layer的size设成整数
5. 在需要的时候，用异步方法去绘制layer - `drawAsynchronously`
6. 当添加阴影的时候，指定阴影的path - `shadowpath`