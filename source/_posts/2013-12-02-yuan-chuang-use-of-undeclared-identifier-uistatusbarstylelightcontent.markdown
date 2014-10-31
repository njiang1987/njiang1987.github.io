---
layout: post
title: '[原创]Use of undeclared identifier ''UIStatusBarStyleLightContent'''
categories:
- iOS
tags: []
published: true
comments: true
---
<p>These are iOS 7 features that won't compile in XCode 4.6.3 which is trying to compile against iOS 6. You need to conditionally compile them out.</p>

<p>Wrap the offending code with:
<pre><code>#if __IPHONE_OS_VERSION_MAX_ALLOWED &gt;= 70000
    //iOS 7 only stuff here
#endif </code></pre></p>
