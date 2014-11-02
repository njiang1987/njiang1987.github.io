---
layout: post
title: '[转]Why are Objective-C delegates usually given the property assign instead
  of retain?'
categories:
- 技术
tags: [iOS]
published: true
comments: true
---
<p>The reason that you avoid retaining delegates is that you need to avoid a retain loop (more commonly known as retain cycle):</p>

<p>A creates B A sets itself as B's delegate … A is released by its owner</p>

<p>If B had retained A, A wouldn't be released, as B owns A, thus A's dealloc would never get called, causing <em>both A and B</em> to leak.</p>

<p>You shouldn't worry about A going away because it owns B and thus gets rid of it in dealloc.</p>

<p>[转]：<a href="http://stackoverflow.com/questions/918698/why-are-objective-c-delegates-usually-given-the-property-assign-instead-of-retai">http://stackoverflow.com/questions/918698/why-are-objective-c-delegates-usually-given-the-property-assign-instead-of-retai</a></p>
