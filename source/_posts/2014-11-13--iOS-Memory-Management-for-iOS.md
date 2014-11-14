title: "[iOS] Memory Management And Performance Tips"
categories:
  - 技术
date: 2014-11-13 11:37:36
tags: [iOS]
---
##Basic Memory Management Rules
1. You own any object you create
2. You can take ownership of an object using retain
3. When you no longer need it, you must relinquish ownership of an object you own
4. You must not relinquish ownership of an object you do not own

##Performance Overview
###CPU Time
1. If your program has nothing to do, it should not consume CPU time.
2. Move work out of the CPU whenever you can.

###Memory Space
1. Reduce the memory footprint of your program.

###Mass Storage Space
1. Eliminate unnecessary file operations and delay others until the information is actually needed.

###The Perception of Speed
1. Make your program responsive to the user.

##Common Areas to Monitor
1. Code for Your Program’s Key Tasks
2. Drawing Code
	>Live resizing
	>Custom view drawing code, especially if portions of the view can be updated without updating the whole view
	>Textured graphics
	>Entirely opaque views
3. Launch Time Initialization
4. File Access Code
5. Application Footprint
6. Memory Allocation Code

##Fundamental Optimization Tips
1. Be Lazy
2. Take Advantage of Perceived Performance
3. Use Event-Based Handlers
4. Improve the Concurrency of Your Program’s Tasks
5. Use the Accelerate Framework
6. Modernize Your Application