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

