---
layout: post
title: "[iOS]UIPopoverPresentationController on iOS 8"
date: 2014-10-14 14:01:02 +0800
comments: true
categories: 技术
tags: iOS
---
In Tumblr for iOS, we have a view controller that gets presented differently on iPhone and on iPad:

	1. iPhone: Modally, as the child of a custom container view controller, presented with a custom animation controller
	2. iPad: In a popover
	
I’m in the process of trying to implement this same behavior using the new UIPresentationController classes introduced in iOS 8, and seem to have already hit an unfortunate limitation.
It’s easy to get the popover showing up correctly on iPad, with just the following code:

```objc
presentedController.modalPresentationStyle = UIModalPresentationPopover;
presentedController.popoverPresentationController.permittedArrowDirections = UIPopoverArrowDirectionUp;
presentedController.popoverPresentationController.sourceRect = button.bounds;
presentedController.popoverPresentationController.sourceView = button;
presentedController.popoverPresentationController.delegate = self;
[self presentViewController:presentedController animated:YES completion:nil];
```

On iPhone, this same controller will be presented modally, but first we need to wrap it in a custom container view controller. To do this, we implement a couple of methods on the UIPopoverPresentationControllerDelegate protocol:

```objc
- (UIModalPresentationStyle)adaptivePresentationStyleForPresentationController:(UIPresentationController *)controller {
    return UIModalPresentationOverFullScreen;
}
- (UIViewController *)presentationController:(UIPresentationController *)presentationController viewControllerForAdaptivePresentationStyle:(UIModalPresentationStyle)style {
    return [[CustomContainerController alloc] initWithRootViewController:presentationController.presentedViewController];
}
```

Simple enough so far.
A “dimming view” is faded in as the view controller transitions on screen. The end result looks something like this:

{% img center /uploads/2014/10/14/1.png %}</br>

The custom container controller is animated on screen using a custom animation controller conforming to `UIViewControllerAnimatedTransitioning`. In iOS 7, this animation controller was also responsible for showing the dimming view.
As of iOS 8, adding the dimming view to the view hierarchy and modifying its opacity should no longer be the responsibility of the animation controller. Instead, a custom `UIPresentationController` subclass should take care of this. The same `UIViewControllerTransitioningDelegate` that vends our custom animation controller can also vend a custom presentation controller, providing for a cleaner separation of concerns.

转自: <http://cocoa.tumblr.com/post/92070238973/how-can-i-use-both-uipopoverpresentationcontroller-and>