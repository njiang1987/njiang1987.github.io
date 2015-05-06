title: "[iOS]WatchKit简明教程"
categories:
  - 技术
date: 2015-04-29 16:24:49
tags: [iOS]
photos:
- /uploads/header/meinv.jpg
---
##开始
首先，需要下载源程序[BitWatch-Starter-s2](/uploads/2015/04/29/BitWatch-Starter-s2.zip)。注意，这个必须要用XCode 6.3以及以上版本运行。

打开程序，编译运行，如下图所示：
![](/uploads/2015/04/29/watch-bitcoinbillionaire-281x500.png)

定位到`File\New\Target...`，然后选择`iOS\Apple Watch\Watch App`模板。
![](/uploads/2015/04/29/watch-target-700x413.png)

Watch程序会跟随主iOS App，而且会建立一个单独的目标程序，点击`Next`继续。
在下一个页面，Xcode会自动填写信息，并且你无法改动程序的名字。
![](/uploads/2015/04/29/watch-targetoptions-700x407.png)

确保选择的语言室Swift，`Include Notification Scene`和`Include Glance Scene`都没有被选中。点击`Finish`，Xcode会生成一个目标工程。工程的目录如下图所示：
![](/uploads/2015/04/29/watch-groups.png)

1. `Watch App`包含了storyboard和图片文件，没有代码，你可以将这个看做程序的View。
2. `WatchKit Extension`包含了可执行的代码，它会控制上面程序中的View。

![](/uploads/2015/04/29/WatchKit_03.jpg)

>与iOS程序不同的是，iOS的程序包括了View，Control和controllers，WatchKit包含的是Inerfaces, Interfact Objects和Interface Controllers.

##Watch Interface
当设计Watch App的时候，需要用到storyboard和interface Builder。打开`BitWatch Watch App`选中`Interface.storyboard`。
![](/uploads/2015/04/29/watch-storyboard1.png)

你会看到一个空的Interface Controller。现在往里面添加一个Label和一个Button，如下图所示：
![](/uploads/2015/04/29/watch-storyboard2.png)

##Actions和OUtlets
苹果已经负责把Watch和主App之间的无线交流链接起来了。接下来需要添加相应的接口，打开`InterfaceController.swift`，按住Control+Drag，将label拖拽到InterfaceController，并且命名为`priceLabel`，点击`Connect`。
![](/uploads/2015/04/29/watch-outlet.png)

##添加WatchKit代码
这个初始的工程里面，有一个叫做BitWatchKit的framework，它包含了一些去网站下载比特币价格的代码。现在需要将这个framework添加到工程里面。

打开导航，选择`BitWatch WatchKit Extension`，选中`Gnenral`选项卡，然后翻到`Linked Framewoks and Libraries`。
![](/uploads/2015/04/29/watch-extension-700x248.png)

点击`+`按钮，你可以看到能够添加到工程里的framework，选择`BitWatchKit.framework`，然后点击`Add`。
![](/uploads/2015/04/29/watch-framework.png)

现在切换到`WatchKit Extension`下面的`InterfaceController.swift`。添加如下代码：
```swift
import BitWatchKit
```

这段代码允许你访问framework里面的Tracker类。接下来再类的定义中添加如下代码：
```swift
let tracker = Tracker()
var updating = false

private func updatePrice(price: NSNumber) {
  priceLabel.setText(Tracker.priceFormatter.stringFromNumber(price))
}

private func update() {
  // 1
  if !updating {
    updating = true
    // 2
    let originalPrice = tracker.cachedPrice()
    // 3
    tracker.requestPrice { (price, error) -> () in
      // 4
      if error == nil {
        self.updatePrice(price!)
      }
      self.updating = false
    }
  }
}
```

以上代码所做的工作是：
1. 先检测下是否正在更新中。
2. 临时保存当前的价格。
3. `requestPrice()`是在`Tracker`里面定义的一个方法，是用来获取最新的比特币价格。
4. 如果请求成功了，会返回到闭包函数里面更新UI。

##Interface生命周期
用户第一次可以在`awakeWithContext(_:)`函数里面初始化控件，在此时，整个的interface会导入到程序中，outlets也会进行初始化。也就意味着，可以在这个时候，初始化程序所需要的数据。但此时，interface还没有准好显示在屏幕上。

此时你可以添加一部分代价很高的代码，比如在`awakeWithContext:`里面添加如下代码，
```swift
updatePrice(tracker.cachedPrice())
```

接下来，在`willActive()`里面添加
```swift
update()
```

`willActive()`与iOS里面的`viewWillAppear`相似，表示interface快要被激活并显示在watch上。在这个地方用来更新数据是比较好的，所以调用`update()`，它会发一个网络请求。最终，在`refreshTapped`中添加
```swift
update()
```

##测试你的App
为了测试你的程序，需要启用Watch作为`external display`。在菜单中选择`Hardware\External Displays`并选中Apple Watch。
![](/uploads/2015/04/29/watch-simulator.png)

然后回到Xcode，选择`BitWatch Watch App`，然后选中`iPhone6`模拟器。
![](/uploads/2015/04/29/watch-scheme.png)

运行程序，然后切换到模拟器，你可以看到比特币的信息已经现在在Watch的模拟器上了。
![](/uploads/2015/04/29/watch-app1.png)

##更多Interface
接下来，我们再来添加2个功能：
* 最近更新时间
* 一个向上/向下的图片，表示价格上升还是下降

首先，需要将2个图片添加到工程里面，打开`BitWatch Watch App`组底下的`Images.xcassets`。初始的工程里面已经包含了2个图片文件：Down@2x.png 和 Up@2x.png。在Finder窗口中，将2个文件拖拽到里面，
![](/uploads/2015/04/29/watch-assets-700x491.png)

>WatchKit的程序只需要@2x的图片。

接下来打开`Interface.storyboard`，拖拽另外一个Label到storyboard，并将它放到更新的按钮上面。将它的text设置为`Last updated`。
![](/uploads/2015/04/29/watch-storyboard5.png)

在iOS程序中，view的顺序是由z-order来决定的。但是针对watch interface，控件之间不会互相的覆盖，所以没有z-order的概念。
![](/uploads/2015/04/29/watch-outline.png)

##Groups
针对Watch Interface，可以设置top/bottom来设置其上下位置，如果是边横排的布局，可以用到`groups`来设置。Groups更像一个容器，你可以把Interface放在里面。可以设置里面控件的布局是横着还是竖着。

在iPhone上面，图片如下图所示：
![](/uploads/2015/04/29/watch-apparrows.png)

所以接下来要做的，就是将一个图片放置在Label旁边。拖拽一个group，然后放在price label和last updated label之间，在属性设置里面，将其设为`Horizontal`。
![](/uploads/2015/04/29/watch-storyboard6.png)

接下来，拖拽一个图片放到group里面，然后拖拽一个新的label放到group里面，并将其放到image的右边。
![](/uploads/2015/04/29/watch-storyboard7.png)

