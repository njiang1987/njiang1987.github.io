---
layout: post
title: "NSString应用retain还是copy"
date: 2014-04-17 19:41:07 +0800
comments: true
categories: 技术
tags: [iOS]
---
1. 对NSString应用retain，效率无疑是最好的

2. 用copy最安全，因为NSString 为 NSMutableString 的基类，如果将NSMutableString 以retain的形式赋值给NSString后，后续修改NSMutableString会导致NSString内容的变化，这通常不是我们希望的，所以用copy最安全。

3. 到底用哪个？貌似还是用copy，因为copy并不一定导致一个新对对象创建，而牺牲效率。copy会调用NSCopying中的 -(id)copyWithZone:(NSZone *)，我们可以判断下self是NSString还是NSMutableString，如果是NSString，就地[self  retain]，[return self]。否则老老实实拷贝对象赋值，这样可以实现效率和安全的结合，实验的结果也是如此。

{% codeblock lang:objc %}
NSString* strOrgin = [NSString stringWithFormat:@"curr time is %@", [NSDate date]];
NSLog(@"strOrgin = %p, retainCount = %d", strOrgin, [strOrgin retainCount]);
NSString* strCopy = [strOrgin copy];
NSLog(@"strCopy = %p, retainCount=%d", strCopy, [strCopy retainCount]);
NSLog(@"strOrgin = %p, retainCount = %d", strOrgin, [strOrgin retainCount]);
{% endcodeblock %}

---
output
{% codeblock lang:objc %}
Test[50250:707] strOrgin = 0x1e52e4d0, retainCount = 1
Test[50250:707] strCopy = 0x1e52e4d0, retainCount=2
Test[50250:707] strOrgin = 0x1e52e4d0, retainCount = 2
{% endcodeblock %}
