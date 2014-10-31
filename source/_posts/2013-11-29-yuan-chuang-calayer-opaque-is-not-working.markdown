---
layout: post
title: '[原创] CALayer.opaque is not working'
categories:
- iOS
tags: []
published: true
comments: true
---
<p>We need to set CALayer.opaque before call [CALayer setNeedsDisplay] and [CALayer displayIfNeeded].</p>
