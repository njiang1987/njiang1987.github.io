---
layout: post
title: "关于怎么用Instrument查看object retain情况"
date: 2013-09-02 13:53:06 +0800
comments: true
categories: 技术
tags: [iOS]
---
You can use the Allocations instrument to track the lifecycle of your objects. If you use the “Allocations” template, it is configured to record malloc and free events. You may want to configure it to also record retain, release, and autorelease events by turning on the “Record reference counts” checkbox in the Allocations instrument settings:

<img alt="record reference counts checkbox" src="http://i.stack.imgur.com/SotDR.png" />

(You cannot toggle this while Instruments is recording, which it starts by default as soon as you choose your template.)

After your run, you can find your objects using the Allocations > Statistics > Object Summary view, which is the default setting for the Detail pane (the bottom half of the window):

<img alt="Object Summary setting for Detail pane" src="http://i.stack.imgur.com/08ued.png" />

If you want to see objects that had been deallocated before you stopped the run, you need to change the Allocation Lifespan setting from “Created & Still Living” (the default) to “All Objects Created”:

<img alt="Allocation Lifespan setting" src="http://i.stack.imgur.com/4SVf2.png" />

To find objects of a specific class, start by typing the class name into the Search field at the right end of the window toolbar. Then find the class name in the Category column of the list view, mouse over it, and click the arrow that appears next to it. For example, my app has a class named Tile, so I search for that and then click the arrow next to Tile in the list view:

<img alt="Searching" src="http://i.stack.imgur.com/GtLnh.gif" />

Now the list view shows every instance of Tile. (Note that you have to enter the actual class of the object, not a superclass. Entering NSObject will only find objects that were created by [NSObject alloc], not objects that were created by [Tile alloc].) I can see the history for any particular instance by clicking the arrow next to that instance's address:

<img alt="Getting detail" src="http://i.stack.imgur.com/53Lou.gif" />

In the detail view for an object, I can see the malloc and free events and, since I turned on “Record reference counts”, I can also see the retain, release, and autorelease messages and their effect on the object's retain count. If I want to see the call stack for any of those events, I can open the extended detail panel on the right side of the window:

<img alt="extended detail of call stack" src="http://i.stack.imgur.com/KKrT1.gif" />