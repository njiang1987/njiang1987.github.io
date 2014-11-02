---
layout: post
title: "[iOS] Something about Core Animation"
date: 2014-10-11 16:01:25 +0800
comments: true
categories: 技术
tags: iOS
---
##1. Implicit and explicit Animation

Implicit Animation:`￼theLayer.opacity = 0.0;`
Explicit Animation:

```objc
CABasicAnimation* fadeAnim = [CABasicAnimation animationWithKeyPath:@"opacity"];
fadeAnim.fromValue = [NSNumber numberWithFloat:1.0];
fadeAnim.toValue = [NSNumber numberWithFloat:0.0];
fadeAnim.duration = 1.0;
[theLayer addAnimation:fadeAnim forKey:@"opacity"];
// Change the actual data value in the layer to the final value.
theLayer.opacity = 0.0;
```

Unlike an implicit animation, which updates the layer object’s data value, an explicit animation does not modify the data in the layer tree. Explicit animations only produce the animations. At the end of the animation, Core Animation removes the animation object from the layer and redraws the layer using its current data values. If you want the changes from an explicit animation to be permanent, you must also update the layer’s property as shown in the preceding example.

##2. Anchor Point

{% img center /uploads/2014/10/11/1.png %}</br>
{% img center /uploads/2014/10/11/2.png %}</br>

Rotation:
{% img center /uploads/2014/10/11/3.png %}</br>

##3. Layer Trees
An app using Core Animation has three sets of layer objects. Each set of layer objects has a different role in making the content of your app appear onscreen:

1. Objects in the <b>model layer tree</b> (or simply “layer tree”) are the ones your app interacts with the most. 
2. Objects in the <b>presentation tree</b> contain the in-flight values for any running animations. 
3. Objects in the <b>render tree</b> perform the actual animations and are private to Core Animation.

{% img center /uploads/2014/10/11/4.png %}</br>
{% img center /uploads/2014/10/11/5.png %}</br>