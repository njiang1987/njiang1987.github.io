title: "[iOS]JSPatch实现原理详解：让JS调用/替换任意OC方法"
categories:
  - 技术
date: 2015-07-10 14:58:47
tags:
photos:
- /uploads/header/meinv.jpg
---
[JSPatch](https://github.com/bang590/JSPatch)以小巧的体积做到了让JS调用/替换任意OC方法，让iOS APP具备热更新的能力，在实现 JSPatch 过程中遇到过很多困难也踩过很多坑，有些还是挺值得分享的。本篇文章从基础原理、方法调用和方法替换三块内容介绍整个 JSPatch 的实现原理，并把实现过程中的想法和碰到的坑也尽可能记录下来。

##基础原理

能做到通过JS调用和改写OC方法最根本的原因是 Objective-C 是动态语言，OC上所有方法的调用/类的生成都通过 Objective-C Runtime 在运行时进行，我们可以通过类名/方法名反射得到相应的类和方法：

```objc
Class class = NSClassFromString("UIViewController");
id viewController = [[class alloc] init];
SEL selector = NSSelectorFromString("viewDidLoad");
[viewController performSelector:selector];
```
也可以替换某个类的方法为新的实现：

```objc
static void newViewDidLoad(id slf, SEL sel) {}
class_replaceMethod(class, selector, newViewDidLoad, @"");
```

还可以新注册一个类，为类添加方法：

```objc
Class cls = objc_allocateClassPair(superCls, "JPObject", 0);
objc_registerClassPair(cls);
class_addMethod(cls, selector, implement, typedesc);
```

对于 Objective-C 对象模型和动态消息发送的原理已有很多文章阐述得很详细，例如[这篇](http://blog.csdn.net/kesalin/article/details/6689226)，这里就不详细阐述了。理论上你可以在运行时通过类名/方法名调用到任何OC方法，替换任何类的实现以及新增任意类。所以 JSPatch 的原理就是：JS传递字符串给OC，OC通过 Runtime 接口调用和替换OC方法。这是最基础的原理，实际实现过程还有很多怪要打，接下来看看具体是怎样实现的。

##方法调用

```javascript
require('UIView')
var view = UIView.alloc().init()
view.setBackgroundColor(require('UIColor').grayColor())
view.setAlpha(0.5)
```
引入JSPatch后，可以通过以上JS代码创建了一个 UIView 实例，并设置背景颜色和透明度，涵盖了require引入类，JS调用接口，消息传递，对象持有和转换，参数转换这五个方面，接下来逐一看看具体实现。

###1.require

调用 `require(‘UIView’)`后，就可以直接使用 UIView 这个变量去调用相应的类方法了，require 做的事很简单，就是在JS全局作用域上创建一个同名变量，变量指向一个对象，对象属性`__isCls`表明这是一个 Class，`__clsName`保存类名，在调用方法时会用到这两个属性。

```javascript
var _require = function(clsName) {
  if (!global[clsName]) {
    global[clsName] = {
      __isCls: 1,
      __clsName: clsName
    }
  }
  return global[clsName]
}
```

所以调用`require(‘UIView’)`后，就在全局作用域生成了 UIView 这个变量，指向一个这样一个对象：

```javascript
{
  __isCls: 1,
  __clsName: "UIView"
}
```

###2.JS接口

接下来看看`UIView.alloc()`是怎样调用的。

旧实现

对于这个调用的实现，一开始我的想法是，根据JS特性，若要让 UIView.alloc() 这句调用不出错，唯一的方法就是给 UIView 这个对象添加 alloc 方法，不然是不可能调用成功的，JS对于调用没定义的属性/变量，只会马上抛出异常，而不像OC/Lua/ruby那样会有转发机制。所以做了一个复杂的事，就是在require生成类对象时，把类名传入OC，OC通过 Runtime 方法找出这个类所有的方法返回给JS，JS类对象为每个方法名都生成一个函数，函数内容就是拿着方法名去OC调用相应方法。生成的 UIView 对象大致是这样的：

```javascript
{ 
    __isCls: 1,
    __clsName: "UIView",
    alloc: function() {…},
    beginAnimations_context: function() {…},
    setAnimationsEnabled: function(){…},
    ...
}
```
实际上不仅要遍历当前类的所有方法，还要循环找父类的方法直到顶层，整个继承链上的所有方法都要加到JS对象上，一个类就有几百个方法，这样把方法全部加到JS对象上，碰到了挺严重的问题，引入几个类就内存暴涨，无法使用。后来为了优化内存问题还在JS搞了继承关系，不把继承链上所有方法都添加到一个JS对象，避免像基类 NSObject 的几百个方法反复添加在每个JS对象上，每个方法只存在一份，JS对象复制了OC对象的继承关系，找方法时沿着继承链往上找，结果内存消耗是小了一些，但还是大到难以接受。

新实现

当时继续苦苦寻找解决方案，若按JS语法，这是唯一的方法，但若不按JS语法呢？突然脑洞开了下，CoffieScript/JSX都可以用JS实现一个解释器实现自己的语法，我也可以通过类似的方式做到，再进一步想到其实我想要的效果很简单，就是调用一个不存在方法时，能转发到一个指定函数去执行，就能解决一切问题了，这其实可以用简单的字符串替换，把JS脚本里的方法调用都替换掉。最后的解决方案是，在OC执行JS脚本前，通过正则把所有方法调用都改成调用 __c() 函数，再执行这个JS脚本，做到了类似OC/Lua/Ruby等的消息转发机制：

```objc
UIView.alloc().init()
->
UIView.__c('alloc')().__c('init')()
```
给JS对象基类 Object 的 prototype 加上 __c 成员，这样所有对象都可以调用到 __c，根据当前对象类型判断进行不同操作：

```javascript
Object.prototype.__c = function(methodName) {
  if (!this.__obj && !this.__clsName) return this[methodName].bind(this);
  var self = this
  return function(){
    var args = Array.prototype.slice.call(arguments)
    return _methodFunc(self.__obj, self.__clsName, methodName, args, self.__isSuper)
  }
}
```

_methodFunc() 就是把相关信息传给OC，OC用 Runtime 接口调用相应方法，返回结果值，这个调用就结束了。

这样做不用去OC遍历对象方法，不用在JS对象保存这些方法，内存消耗直降99%，这一步是做这个项目最爽的时候，用一个非常简单的方法解决了严重的问题，替换之前又复杂效果又差的实现。

###3.消息传递

解决了JS接口问题，接下来看看JS和OC是怎样互传消息的。这里用到了 JavaScriptCore 的接口，OC端在启动JSPatch引擎时会创建一个 JSContext 实例，JSContext 是JS代码的执行环境，可以给 JSContext 添加方法，JS就可以直接调用这个方法：

```objc
JSContext *context = [[JSContext alloc] init];
context[@"hello"] = ^(NSString *msg) {
    NSLog(@"hello %@", msg);
};
[_context evaluateScript:@"hello('word')"];     //output hello word
```

JS通过调用 JSContext 定义的方法把数据传给OC，OC通过返回值传会给JS。调用这种方法，它的参数/返回值 JavaScriptCore 都会自动转换，OC里的 NSArray, NSDictionary, NSString, NSNumber, NSBlock 会分别转为JS端的数组/对象/字符串/数字/函数类型。上述 _methodFunc() 方法就是这样把要调用的类名和方法名传递给OC的。

###4.对象持有/转换

UIView.alloc() 通过上述消息传递后会到OC执行 [UIView alloc]，并返回一个UIView实例对象给JS，这个OC实例对象在JS是怎样表示的呢？怎样可以在JS拿到这个实例对象后可以直接调用它的实例方法 (UIView.alloc().init())？

对于一个自定义id对象，JavaScriptCore 会把这个自定义对象的指针传给JS，这个对象在JS无法使用，但在回传给OC时OC可以找到这个对象。对于这个对象生命周期的管理，按我的理解如果JS有变量引用时，这个OC对象引用计数就加1 ，JS变量的引用释放了就减1，如果OC上没别的持有者，这个OC对象的生命周期就跟着JS走了，会在JS进行垃圾回收时释放。

传回给JS的变量是这个OC对象的指针，如果不经过任何处理，是无法通过这个变量去调用实例方法的。所以在返回对象时，JSPatch 会对这个对象进行封装。

首先，告诉JS这是一个OC对象：

```objc
static NSDictionary *toJSObj(id obj)
{
    if (!obj) return nil;
    return @{@"__isObj": @(YES), @"cls": NSStringFromClass([obj class]), @"obj": obj};
}
```
用__isObj表示这是一个OC对象，对象指针也一起返回。接着在JS端会把这个对象转为一个 JSClass 实例：

```javascript
var JSClass
var _getJSClass = function(className) {
  if (!JSClass) {
    JSClass = function(obj, className, isSuper) {
        this.__obj = obj
        this.__isSuper = isSuper
        this.__clsName = className
    }
  }
  return JSClass
}
  
var _toJSObj = function(meta) {
  var JSClass = _getJSClass()
  return new JSClass(meta["obj"], meta["cls"])
}
```
JS端如果发现返回是一个OC对象，会传入 _toJSObj()，生成一个 JSClass 实例，这个实例保存着OC对象指针，类名等。这个实例就是OC对象在 JSPatch 对应的JS对象，生命周期是一样的。

回到我们第二点说的 JS接口， 这个 JSClass 实例对象同样有 __c 函数，调用这个对象的方法时，同样走到 __c 函数， __c 函数会把JSClass实例对象里的OC对象指针以及要调用的方法名和参数回传给OC，这样OC就可以调用这个对象的实例方法了。

接着看看对象是怎样回传给OC的。上述例子中，view.setBackgroundColor(require(‘UIColor’).grayColor())，这里生成了一个 UIColor 实例对象，并作为参数回传给OC。根据上面说的，这个 UIColor 实例在JS中的表示是一个 JSClass 实例，所以不能直接回传给OC，这里的参数实际上会在 __c 函数进行处理，会把对象的 .__obj 原指针回传给OC。

最后一点，OC对象可能会存在于 NSDictionary / NSArray 等容器里，所以需要遍历容器挑出OC对象进行格式化，OC需要把对象都替换成JS认得的格式，JS要把对象转成 JSClass 实例，JS实例回传给OC时需要把实例转为OC对象指针。所以OC流出数据时都会经过 formatOCObj() 方法处理，JS从OC得到数据时都会经过 _formatOCToJS() 处理，JS传参数给OC时会经过 _formatJSToOC() 处理，图示：

![](/uploads/2015/07/10/1436325144537320.jpg)

###5.类型转换

JS把要调用的类名/方法名/对象传给OC后，OC调用类/对象相应的方法是通过 NSInvocation 实现，要能顺利调用到方法并取得返回值，要做两件事：

1.取得要调用的OC方法各参数类型，把JS传来的对象转为要求的类型进行调用。

2.根据返回值类型取出返回值，包装为对象传回给JS。

例如开头例子的`view.setAlpha(0.5)`， JS传递给OC的是一个 NSNumber，OC需要通过要调用OC方法的 NSMethodSignature 得知这里参数要的是一个 float 类型值，于是把NSNumber转为float值再作为参数进行OC方法调用。这里主要处理了 int/float/bool 等数值类型，并对 CGRect/CGRange 等类型进行了特殊转换处理，剩下的就是实现细节了。

##方法替换

JSPatch 可以用 defineClass 接口任意替换一个类的方法，方法替换的实现过程也是颇为曲折，一开始是用 va_list 的方式获取参数，结果发现 arm64 下不可用，只能转而用另一种hack方式绕道实现。另外在给类新增方法、实现property、支持self/super关键字上也费了些功夫，下面逐个说明。

基础原理

OC上，每个类都是这样一个结构体：

```objc
struct objc_class {
  struct objc_class * isa;
  const char *name; 
  ….
  struct objc_method_list **methodLists; /*方法链表*/
};
```
其中 methodList 方法链表里存储的是Method类型：

```objc
typedef struct objc_method *Method;
typedef struct objc_ method {
  SEL method_name;
  char *method_types;
  IMP method_imp;
};
```

Method 保存了一个方法的全部信息，包括SEL方法名，type各参数和返回值类型，IMP该方法具体实现的函数指针。

通过 Selector 调用方法时，会从 methodList 链表里找到对应Method进行调用，这个 methodList 上的的元素是可以动态替换的，可以把某个 Selector 对应的函数指针IMP替换成新的，也可以拿到已有的某个 Selector 对应的函数指针IMP，让另一个 Selector 跟它对应，Runtime 提供了一些接口做这些事，以替换 UIViewController 的 -viewDidLoad: 方法为例：

```objc
static void viewDidLoadIMP (id slf, SEL sel) {
   JSValue *jsFunction = …;
   [jsFunction callWithArguments:nil];
}
  
Class cls = NSClassFromString(@"UIViewController");
SEL selector = @selector(viewDidLoad);
Method method = class_getInstanceMethod(cls, selector);
  
//获得viewDidLoad方法的函数指针
IMP imp = method_getImplementation(method)
  
//获得viewDidLoad方法的参数类型
char *typeDescription = (char *)method_getTypeEncoding(method);
  
//新增一个ORIGViewDidLoad方法，指向原来的viewDidLoad实现
class_addMethod(cls, @selector(ORIGViewDidLoad), imp, typeDescription);
  
//把viewDidLoad IMP指向自定义新的实现
class_replaceMethod(cls, selector, viewDidLoadIMP, typeDescription);
```
这样就把 UIViewController 的 -viewDidLoad 方法给替换成我们自定义的方法，APP里调用 UIViewController 的 viewDidLoad 方法都会去到上述 viewDidLoadIMP 函数里，在这个新的IMP函数里调用JS传进来的方法，就实现了替换 -viewDidLoad 方法为JS代码里的实现，同时为 UIViewController 新增了个方法 -ORIGViewDidLoad 指向原来 viewDidLoad 的IMP，JS可以通过这个方法调用到原来的实现。

方法替换就这样很简单的实现了，但这么简单的前提是，这个方法没有参数。如果这个方法有参数，怎样把参数值传给我们新的IMP函数呢？例如 UIViewController 的 -viewDidAppear: 方法，调用者会传一个Bool值，我们需要在自己实现的IMP（上述的viewDidLoadIMP）上拿到这个值，怎样能拿到？如果只是针对一个方法写IMP，是可以直接拿到这个参数值的：

```objc
static void viewDidAppear (id slf, SEL sel, BOOL animated) {
   [function callWithArguments:@(animated)];
}
```
但我们要的是实现一个通用的IMP，任意方法任意参数都可以通过这个IMP中转，拿到方法的所有参数回调JS的实现。

va_list实现(32位)

最初我是用可变参数va_list实现：

```objc
static void commonIMP(id slf, ...)
  va_list args;
  va_start(args, slf);
  NSMutableArray *list = [[NSMutableArray alloc] init];
  NSMethodSignature *methodSignature = [cls instanceMethodSignatureForSelector:selector];
  NSUInteger numberOfArguments = methodSignature.numberOfArguments;
  id obj;
  for (NSUInteger i = 2; i < numberOfArguments; i++) {
      const char *argumentType = [methodSignature getArgumentTypeAtIndex:i];
      switch(argumentType[0]) {
          case 'i':
              obj = @(va_arg(args, int));
              break;
          case 'B':
              obj = @(va_arg(args, BOOL));
              break;
          case 'f':
          case 'd':
              obj = @(va_arg(args, double));
              break;
          …… //其他数值类型
          default: {
              obj = va_arg(args, id);
              break;
          }
      }
      [list addObject:obj];
  }
  va_end(args);
  [function callWithArguments:list];
}
```
这样无论方法参数是什么，有多少个，都可以通过 va_list 的一组方法一个个取出来，组成NSArray在调用JS方法时传回。很完美地解决了参数的问题，一直运行正常，直到我跑在arm64的机子上测试，一调用就crash。查了资料，才发现arm64下 va_list 的结构改变了，导致无法上述这样取参数。
详情请参考[这篇文章](https://blog.nelhage.com/2010/10/amd64-and-va_arg)。


###ForwardInvocation实现(64位)

后来找到另一种非常hack的方法解决参数获取的问题，利用了OC消息转发机制。

当调用一个 NSObject 对象不存在的方法时，并不会马上抛出异常，而是会经过多层转发，层层调用对象的 -resolveInstanceMethod:, -forwardingTargetForSelector:, -methodSignatureForSelector:, -forwardInvocation: 等方法，[这篇文章](http://bugly.qq.com/blog/?p=64)说得比较清楚，其中最后 -forwardInvocation: 是会有一个 NSInvocation 对象，这个 NSInvocation 对象保存了这个方法调用的所有信息，包括 Selector 名，参数和返回值类型，最重要的是有所有参数值，可以从这个 NSInvocation 对象里拿到调用的所有参数值。我们可以想办法让每个需要被JS替换的方法调用最后都调到 -forwardInvocation:，就可以解决无法拿到参数值的问题了。

具体实现，以替换 UIViewController 的 -viewWillAppear: 方法为例：

1. 把UIViewController的 -viewWillAppear: 方法通过 class_replaceMethod() 接口指向一个不存在的IMP: class_getMethodImplementation(cls, @selector(__JPNONImplementSelector))，这样调用这个方法时就会走到 -forwardInvocation:。
2. 为 UIViewController 添加 -ORIGviewWillAppear: 和 -_JPviewWillAppear: 两个方法，前者指向原来的IMP实现，后者是新的实现，稍后会在这个实现里回调JS函数。
3. 改写 UIViewController 的 -forwardInvocation: 方法为自定义实现。一旦OC里调用 UIViewController 的 -viewWillAppear: 方法，经过上面的处理会把这个调用转发到 -forwardInvocation: ，这时已经组装好了一个 NSInvocation，包含了这个调用的参数。在这里把参数从 NSInvocation 反解出来，带着参数调用上述新增加的方法 -JPviewWillAppear: ，在这个新方法里取到参数传给JS，调用JS的实现函数。整个调用过程就结束了，整个过程图示如下：

![](/uploads/2015/07/10/1436325132941056.jpg)

最后一个问题，我们把 UIViewController 的 -forwardInvocation: 方法的实现给替换掉了，如果程序里真有用到这个方法对消息进行转发，原来的逻辑怎么办？首先我们在替换 -forwardInvocation: 方法前会新建一个方法 -ORIGforwardInvocation:，保存原来的实现IMP，在新的 -forwardInvocation: 实现里做了个判断，如果转发的方法是我们想改写的，就走我们的逻辑，若不是，就调 -ORIGforwardInvocation: 走原来的流程。

实现过程中还碰到一个坑，就是从 -forwardInvocation: 里的 NSInvocation 对象取参数值时，若参数值是id类型，我们会这样取:

```objc
id arg;
[invocation getArgument:&arg atIndex:i];
```
但这样取某些时候会导致莫名其妙的crash，而且不是crash在这个地方，似乎这里的指针取错导致后续的内存错乱，crash在各种地方，这个bug查了我半天才定位到这里，至今不知为什么。后来以这样的方式解决了：

```objc
void *arg;
[invocation getArgument:&arg atIndex:i];
id a = (__bridge id)arg;
```
其他就是实现上的细节了，例如需要根据不同的返回值类型生成不同的IMP，要在各处处理参数转换等。

###新增方法

在 JSPatch 刚开源时，是不支持为一个类新增方法的，因为觉得能替换原生方法就够了，新的方法纯粹添加在JS对象上，只在JS端跑就行了。另外OC为类新增方法需要知道各个参数和返回值的类型，需要在JS定一种方式把这些类型传给OC才能完成新增方法，比较麻烦。后来挺多人比较关注这个问题，不能新增方法导致 action-target 模式无法用，我也开始想有没有更好的方法实现添加方法。一开始想到，反正新增的方法都是JS在用，不如新增的方法返回值和参数全统一成id类型，这样就不用传类型了，但还是需要知道参数个数，后来跟Lancy聊天时找到了解决方案，JS可以获得函数参数个数，直接封装一下把参数个数一并传给OC就行了。

现在 defineClass 定义的方法会经过JS包装，变成一个包含参数个数和方法实体的数组传给OC，OC会判断如果方法已存在，就执行替换的操作，若不存在，就调用 class_addMethod() 新增一个方法，通过传过来的参数个数和方法实体生成新的 Method，把 Method 的参数和返回值类型都设为id。

这里有个问题，若某个类实现了某protocol，protocol方法里有可选的方法，它的参数不全是id类型，例如 UITableViewDataSource 的一个方法：

```objc
- (NSInteger)tableView:(UITableView *)tableView sectionForSectionIndexTitle:(NSString *)title atIndex:(NSInteger)index;
```
若原类没有实现这个方法，在JS里实现了，会走到新增方法的逻辑，每个参数类型都变成id，与这个 protocol 方法不匹配，产生错误。后续会处理 protocol 的问题，若新增的方法是 protocol 实现的方法，会取这个方法的 NSMethodSignature 获得正确的参数类型进行添加。

###Property实现

```javascript
defineClass('JPTableViewController : UITableViewController', {
  dataSource: function() {
    var data = self.getProp('data')
    if (data) return data;
    data = [1,2,3]
    self.setProp_forKey(data, 'data')
    return data;
  }
}
```

JSPatch 可以通过 -getProp:， -setProp:forKey: 这两个方法给对象添加成员变量。实现上用了运行时关联接口 objc_getAssociatedObject() 和 objc_setAssociatedObject() 模拟，相当于把一个对象跟当前对象 self 关联起来，以后可以通过当前对象 self 找到这个对象，跟成员的效果一样，只是一定得是id对象类型。

本来OC有 class_addIvar() 可以为类添加成员，但必须在类注册之前添加完，注册完成后无法添加，这意味着可以为在JS新增的类添加成员，但不能为OC上已存在的类添加，所以只能用上述方法模拟。

###self关键字

```javascript
defineClass("JPViewController: UIViewController", {
  viewDidLoad: function() {
    var view = self.view()
    ...
  },
}
```
JSPatch支持直接在 defineClass 里的实例方法里直接使用 self 关键字，跟OC一样 self 是指当前对象，这个 self 关键字是怎样实现的呢？实际上这个self是个全局变量，在 defineClass 里对实例方法 方法进行了包装，在调用实例方法之前，会把全局变量 self 设为当前对象，调用完后设回空，就可以在执行实例方法的过程中使用 self 变量了。这是一个小小的trick。

###super关键字

```javascript
defineClass("JPViewController: UIViewController", {
  viewDidLoad: function() {
    self.super.viewDidLoad()
  },
}
```

OC里 super 是一个关键字，无法通过动态方法拿到 super，那么 JSPatch 的super是怎么实现的？实际上调用 super 的方法，OC做的事是调用父类的某个方法，并把当前对象当成 self 传入父类方法，我们只要模拟它这个过程就行了。

首先JS端需要告诉OC想调用的是当前对象的 super 方法，做法是调用 self.super时，会返回一个新的 JSClass 实例，这个实例同样保存了OC对象的引用，同时标识 __isSuper=1。

```javascript
JSClass = function(obj, className, isSuper) {
    this.__obj = obj
    this.__isSuper = isSuper
    this.__clsName = className
}
JSClass.prototype.__defineGetter__('super', function(){
  if (!this.__super) {
    this.__super = new JSClass(this.__obj, this.__clsName, 1)
  }
  return this.__super
})
```

调用方法时，__isSuper 会传给OC，告诉OC要调 super 的方法。OC做的事情是，如果是调用 super 方法，找到 superClass 这个方法的IMP实现，为当前类新增一个方法指向 super 的IMP实现，那么调用这个类的新方法就相当于调用 super 方法。把要调用的方法替换成这个新方法，就完成 super 方法的调用了。

```objc
static id callSelector(NSString *className, NSString *selectorName, NSArray *arguments, id instance, BOOL isSuper) {
    ...
    if (isSuper) {
        NSString *superSelectorName = [NSString stringWithFormat:@"SUPER_%@", selectorName];
        SEL superSelector = NSSelectorFromString(superSelectorName);
         
        Class superCls = [cls superclass];
        Method superMethod = class_getInstanceMethod(superCls, selector);
        IMP superIMP = method_getImplementation(superMethod);
         
        class_addMethod(cls, superSelector, superIMP, method_getTypeEncoding(superMethod));
        selector = superSelector;
    }
    ...
}
```

##总结

整个 JSPatch 实现原理就大致描述完了，剩下的一些小点，例如GCD接口，block实现，方法名下划线处理等就不细说了，可以直接看代码。JSPatch 还在持续改进中，希望能成为iOS平台动态更新的最佳解决方案，欢迎大家一起建设这个项目，github地址： https://github.com/bang590/JSPatc

版权声明：本文章在微信公众平台的发表权，已「独家代理」给指定公众帐号：iOS开发(iOSDevTips)。
转自：<http://www.cocoachina.com/ios/20150710/12467.html>