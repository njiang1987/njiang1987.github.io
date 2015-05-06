title: "[iOS]探究iOS Block编程"
categories:
  - 技术
date: 2014-12-01 16:43:32
tags: [iOS]
photos:
- /uploads/header/heliu.jpg
---
##开始使用Block
需要用`^`来生命一个block，如下：
```objc
int multiplier = 7;
int (^myBlock)(int) = ^(int num) {
    return num * multiplier;
};
```

![](/uploads/2014/12/01/blocks.jpg)

###直接使用Block
代码如下：
```objc
char *myCharacters[3] = { "TomJohn", "George", "Charles Condomine" };
 
qsort_b(myCharacters, 3, sizeof(char *), ^(const void *l, const void *r) {
    char *left = *(char **)l;
    char *right = *(char **)r;
    return strncmp(left, right, 1);
});

```

###Cocoa中的Block
```objc
NSComparator finderSortBlock = ^(id string1, id string2) {
 
    NSRange string1Range = NSMakeRange(0, [string1 length]);
    return [string1 compare:string2 options:comparisonOptions range:string1Range locale:currentLocale];
};
 
NSArray *finderSortArray = [stringsArray sortedArrayUsingComparator:finderSortBlock];
```

###__block修饰符
block里面可以修改外面的变量。
```objc
__block NSUInteger orderedSameCount = 0;
NSArray *diacriticInsensitiveSortArray = [stringsArray sortedArrayUsingComparator:^(id string1, id string2) {
 
    NSRange string1Range = NSMakeRange(0, [string1 length]);
    NSComparisonResult comparisonResult = [string1 compare:string2 options:NSDiacriticInsensitiveSearch range:string1Range locale:currentLocale];
 
    if (comparisonResult == NSOrderedSame) {
        orderedSameCount++;
    }
    return comparisonResult;
}];
```

##Block的概念
Block再其他语言中，也被称为闭包"Closure"。

###Block的函数功能
1. 有类型参数，就跟函数一样。
2. 有内涵的或声明的返回参数。
3. 可以根据词汇声明的范围，知道其状态。
4. 可以修改当前的状态。
5. 可以共享


```
永远都要顺着趋势
价格不会高到不能买进，也不会低到不能卖出
始终要用止损单
```

```
按照小时的K线，找出趋势线，还要查看角度趋势线
```