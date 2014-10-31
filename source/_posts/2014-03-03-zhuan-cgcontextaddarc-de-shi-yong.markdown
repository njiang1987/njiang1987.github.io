---
layout: post
title: '[转]CGContextAddArc的使用'
categories:
- iOS
tags: []
published: true
comments: true
---
<p>[转自]：<a href="http://differentisnotdifferent.diandian.com/post/2012-07-30/40032320467">http://differentisnotdifferent.diandian.com/post/2012-07-30/40032320467</a></p>

<p>这个函数让我在纸上画了半天才搞明白，把我的理解给大家分享下。</p>

<p>void CGContextAddArc(CGContextRef c, CGFloat x, CGFloat y, CGFloat radius, CGFloat startAngle, CGFloat endAngle, int clockwise)</p>

<p>CGContextRef不解释了，x,y为圆点坐标，startAngle为开始的弧度，endAngle为 结束的弧度，clockwise 0为顺时针，1为逆时针。</p>

<p>CGContextAddArc(context, 160, 200, 100, 0, 45*(M_PI/180), 0);</p>

<p>所以对上面这对代码的解释是这样的：</p>

<p>1）startAngle为0,绿色箭头的地方。</p>

<p>2）endAngle为45,黄色箭头的地方。</p>

<p>3）clockwise为0,按照红色箭头往下绘制图形。</p>

<p>4）所以效果就是红色的扇形。</p>

<p>补充：如果clockwise为1，则是蓝色部分区域。</p>

<p><img alt="" src="http://m1.img.papaapp.com/farm5/d/2012/0730/19/0D826787916C7D216CCD2D012DE49C2E_B500_900_286_260.JPEG" width="286" height="260" /></p>
