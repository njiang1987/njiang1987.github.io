---
layout: post
title: '[XCode] 关于怎么用Instrument查看object retain情况'
categories:
- 技术
tags: [XCode]
published: true
comments: true
---
<p>【转自】<a link="http://stackoverflow.com/questions/14890402/instruments-allocations-track-alloc-and-dealloc-of-objects-of-user-defined-class">http://stackoverflow.com/questions/14890402/instruments-allocations-track-alloc-and-dealloc-of-objects-of-user-defined-class</a></p>

<p>You can use the Allocations instrument to track the lifecycle of your objects. If you use the “Allocations” template, it is configured to record <code>malloc</code> and <code>free</code> events. You may want to configure it to also record <code>retain</code>, <code>release</code>, and <code>autorelease</code> events by turning on the “Record reference counts” checkbox in the Allocations instrument settings:</p>

<p><img alt="record reference counts checkbox" src="http://i.stack.imgur.com/SotDR.png" /></p>

<p>{You cannot toggle this while Instruments is recording, which it starts by default as soon as you choose your template.)</p>

<p>After your run, you can find your objects using the Allocations &gt; Statistics &gt; Object Summary view, which is the default setting for the Detail pane (the bottom half of the window):</p>

<p><img alt="Object Summary setting for Detail pane" src="http://i.stack.imgur.com/08ued.png" /></p>

<p>If you want to see objects that had been deallocated before you stopped the run, you need to change the Allocation Lifespan setting from “Created &amp; Still Living” (the default) to “All Objects Created”:</p>

<p><img alt="Allocation Lifespan setting" src="http://i.stack.imgur.com/4SVf2.png" /></p>

<p>To find objects of a specific class, start by typing the class name into the Search field at the right end of the window toolbar. Then find the class name in the Category column of the list view, mouse over it, and click the arrow that appears next to it. For example, my app has a class named <code>Tile</code>, so I search for that and then click the arrow next to <code>Tile</code> in the list view:</p>

<p><img alt="Searching" src="http://i.stack.imgur.com/GtLnh.gif" /></p>

<p>Now the list view shows every instance of <code>Tile</code>. (Note that you have to enter the actual class of the object, not a superclass. Entering <code>NSObject</code> will only find objects that were created by <code>[NSObject alloc]</code>, not objects that were created by <code>[Tile alloc]</code>.) I can see the history for any particular instance by clicking the arrow next to that instance's address:</p>

<p><img alt="Getting detail" src="http://i.stack.imgur.com/53Lou.gif" /></p>

<p>In the detail view for an object, I can see the <code>malloc</code> and <code>free</code> events and, since I turned on “Record reference counts”, I can also see the <code>retain</code>, <code>release</code>, and <code>autorelease</code> messages and their effect on the object's retain count. If I want to see the call stack for any of those events, I can open the extended detail panel on the right side of the window:</p>

<p><img alt="extended detail of call stack" src="http://i.stack.imgur.com/KKrT1.gif" /></p>
