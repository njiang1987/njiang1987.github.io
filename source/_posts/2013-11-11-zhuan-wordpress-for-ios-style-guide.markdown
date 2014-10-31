---
layout: post
title: '[转]WordPress-for-iOS-Style-Guide'
categories:
- iOS
tags: []
published: true
comments: true
---
<p><div id="head">
<h1>WordPress for iOS Style Guide</h1>
</div>
<div id="wiki-content">
<div>
<div id="wiki-body">
<div /></div></div></div></p>

<p>So you want to write some code for WordPress for iOS. That’s nice, thanks a lot. But before that take some minutes to read some tips that will probably make everyone’s life easier. Much of this guide is adapted from <a href="http://google-styleguide.googlecode.com/svn/trunk/objcguide.xml">Google's Objective-C Style Guide</a>. You should read that as well as<a href="https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html">Apple's Coding Guidelines for Cocoa</a>.
<h2><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#before-you-commit" name="before-you-commit"></a>Before You Commit</h2>
<ul>
	<li>Review what you commit: make sure you’re not leaving out anything, and that everything that you commit is meant to be there.<code>git add -p</code> is your friend here.</li>
	<li>Check for whitespace. Not the most critical thing, but if you follow the previous step, you might see unnecessary white space added at the end of a line. Get rid of it</li>
	<li>No NSLog in commits. We all use NSLog (or our WP* FileLogger variants) to debug. Unless you really want that to be on production, and logged into the wordpress.log file, remove it before commit. Our app is verbose enough already.</li>
	<li>No commented out code. If the code was already there and you’re removing it to test something, don’t comment it, just remove it. You can always go back by checking out a previous version from source control.</li>
	<li>Avoid new compiler warnings. A compiler warning might seem harmless, but when we compile for the app store, we use <code>-Werror</code>, so those insignificant warnings turn into real errors and force us to investigate what’s wrong at the last minute. You really don’t want to be messing with the code at that point.</li>
</ul>
If there’s a ticket associated, make sure to use “refs #123″ or “fixes #123″ in the commit message. It makes easier to track why things changed
<h2><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#spacing-and-formatting" name="spacing-and-formatting"></a>Spacing and Formatting</h2>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#spaces-vs-tabs" name="spaces-vs-tabs"></a>Spaces vs Tabs</h3>
Use only spaces, and indent 4 spaces at a time.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#line-length" name="line-length"></a>Line Length</h3>
Each line of text in your code should try to be at most 100 characters long. Objective C is a fairly verbose language and occasionally it makes sense to extend past the 100 character limit. However, this should be a rare occurrence and not commonplace.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#method-declarations-and-definitions" name="method-declarations-and-definitions"></a>Method Declarations and Definitions</h3>
One space should be used between the - or + and the return type, and no spacing in the parameter list except between parameters. Methods should look like this:
<div>
<pre>- (void)doSomethingWithString:(NSString *)theString
{
  ...
}</pre>
</div>
If you have too many parameters to fit on one line, giving each its own line is preferred. If multiple lines are used, align each using the colon before the parameter.
<div>
<pre>- (void)doSomethingWith:(GTMFoo *)theFoo
                   rect:(NSRect)theRect
               interval:(float)theInterval
{
  ...
}</pre>
</div>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#method-invocations" name="method-invocations"></a>Method Invocations</h3>
Method invocations should be formatted much like method declarations. When there's a choice of formatting styles, follow the convention already used in a given source file. Invocations should have all arguments on one line:
<div>
<pre>[myObject doFooWith:arg1 name:arg2 error:arg3];</pre>
</div>
or have one argument per line, with colons aligned:
<div>
<pre>[myObject doFooWith:arg1
               name:arg2
              error:arg3];</pre>
</div>
Don't use any of these styles:
<div>
<pre>[myObject doFooWith:arg1 name:arg2  // some lines with &gt;1 arg
              error:arg3];</pre></div></p>

<p>[myObject doFooWith:arg1<br />
               name:arg2 error:arg3];</p>

<p>[myObject doFooWith:arg1<br />
          name:arg2  // aligning keywords instead of colons<br />
          error:arg3];

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#protocols" name="protocols"></a>Protocols</h3>
There should not be a space between the type identifier and the name of the protocol encased in angle brackets. This applies to class declarations, instance variables, and method declarations. For example:
<div>
<pre>@interface MyProtocoledClass : NSObject&lt;NSWindowDelegate&gt; {
  id&lt;MyFancyDelegate&gt; _delegate;
}
- (void)setDelegate:(id&lt;MyFancyDelegate&gt;)aDelegate;
@end</pre>
</div>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#blocks" name="blocks"></a>Blocks</h3>
Blocks are preferred to the target-selector pattern when creating callbacks, as it makes code easier to read. Code inside blocks should be indented four spaces. There are several appropriate style rules, depending on how long the block is:
<ul>
	<li>If the block can fit on one line, no wrapping is necessary.</li>
	<li>If it has to wrap, the closing brace should line up with the first character of the line on which the block is declared.</li>
	<li>Code within the block should be indented four spaces.</li>
	<li>If the block is large, e.g. more than 20 lines, it is recommended to move it out-of-line into a local variable.</li>
	<li>If the block takes no parameters, there are no spaces between the characters ^{. If the block takes parameters, there is no space between the ^( characters, but there is one space between the ) { characters.</li>
	<li>Two space indents inside blocks are also allowed, but should only be used when it's consistent with the rest of the project's code.</li>
</ul>
<div>
<pre>// The entire block fits on one line.
[operation setCompletionBlock:^{ [self onOperationDone]; }];</pre></div></p>

<p>// The block can be put on a new line, indented four spaces, with the<br />
// closing brace aligned with the first character of the line on which<br />
// block was declared.<br />
[operation setCompletionBlock:^{<br />
    [self.delegate newDataAvailable];<br />
}];</p>

<p>// Using a block with a C API follows the same alignment and spacing<br />
// rules as with Objective-C.<br />
dispatch_async(_fileIOQueue, ^{<br />
    NSString* path = [self sessionFilePath];<br />
    if (path) {<br />
      // ...<br />
    }<br />
});</p>

<p>// An example where the parameter wraps and the block declaration fits<br />
// on the same line. Note the spacing of |^(SessionWindow *window) {|<br />
// compared to |^{| above.<br />
[[SessionService sharedService]<br />
    loadWindowWithCompletionBlock:^(SessionWindow *window) {<br />
        if (window) {<br />
          [self windowDidLoad:window];<br />
        } else {<br />
          [self errorLoadingWindow];<br />
        }<br />
    }];</p>

<p>// Large blocks can be declared out-of-line.<br />
void (^largeBlock)(void) = ^{<br />
    // ...<br />
};<br />
[_operationQueue addOperationWithBlock:largeBlock];

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#if-statements" name="if-statements"></a>If Statements</h3>
When writing if statements, make sure to use a curly brace even if it's a one line statement.
<div>
<pre>// Good
if (someValue != nil) {
  [self doSomething];
}</pre></div></p>

<p>// Bad</p>

<p>if (someValue != nil)<br />
  [self doSomething];

The exception to this rule is if the statement being executed is a return statement.
<div>
<pre>if (someValue != nil)
  return;</pre>
</div>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#ternary-operators" name="ternary-operators"></a>Ternary Operators</h3>
Be cautious about using the ternary operator as it can make code very difficult to read. Only use a ternary operator if using it makes the code easier to read.
<div>
<pre>// Good
  int minVal = (a &lt; b) ? a : b</pre></div></p>

<p>// Bad<br />
  [self.view addSubview:((currentlyVisibleView == self.photoSelectorView) ? self.textEditorView : self.photoSelectorView)];

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#multi-line-declarations" name="multi-line-declarations"></a>Multi Line Declarations</h3>
Don't declare a series of variables on one line but rather split them up into individual lines. The reason for this is that splitting them into multiple lines makes the code easier to read and it makes diffs easier to analyze.
<div>
<pre>// Bad
@property (nonatomic, strong) NSString *username, *url, *password;</pre></div></p>

<p>// Good<br />
@property (nonatomic, strong) NSString *username;<br />
@property (nonatomic, strong) NSString *url;<br />
@property (nonatomic, strong) NSString *password;

<h2><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#naming" name="naming"></a>Naming</h2>
Naming rules are very important in maintainable code. Objective-C method names tend to be very long, but this has the benefit that a block of code can almost read like prose, thus rendering many comments unnecessary.</p>

<p>When writing pure Objective-C code, we mostly follow standard <a href="http://developer.apple.com/documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html">Objective-C naming rules</a>.</p>

<p>Any class, category, method, or variable name may use all capitals for initialisms within the name. This follows Apple's standard of using all capitals within a name for initialisms such as URL, TIFF, and EXIF. An exception to this is when passing a URL as a <em>NSString</em> we prefer to not to use all capitals. The reason for this is that a non all capitalized URL stands out as more obvious that the variable in question is a <em>NSString</em>instead of a <em>NSURL</em>.
<div>
<pre>- (void)displayWebsite:(NSURL *)websiteURL {
  ...
}</pre></div></p>

<p>- (void)displayWebsite:(NSString *)websiteUrl {<br />
  ...<br />
}

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#file-names" name="file-names"></a>File Names</h3>
File names should reflect the name of the class implementation that they contain—including case.</p>

<p>File names for categories should include the name of the class being extended, e.g. <em>NSString+Helpers.h</em> or <em>UIColors+Helpers.h</em>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#class-names" name="class-names"></a>Class Names</h3>
Class names (along with category and protocol names) should start as uppercase and use mixed case to delimit words.</p>

<p>In application-level code, prefixes on class names should generally be avoided. Having every single class with same prefix impairs readability for no benefit. When designing code to be shared across multiple applications, prefixes are acceptable and recommended (e.g.<em>WPXMLRPCEncoder</em>).
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#objective-c-method-names" name="objective-c-method-names"></a>Objective-C Method Names</h3>
Method names should start as lowercase and then use mixed case. Each named parameter should also start as lowercase.<br />
The method name should read like a sentence if possible, meaning you should choose parameter names that flow with the method name. (e.g.<em>convertPoint:fromRect</em>: or <em>replaceCharactersInRange:withString:</em>). See <a href="https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CodingGuidelines/Articles/NamingMethods.html#//apple_ref/doc/uid/20001282-BCIGIJJF">Apple's Guide to Naming Methods</a> for more details.</p>

<p>Accessor methods should be named the same as the variable they're "getting", but they should not be prefixed with the word "get". For example:
<div>
<pre>- (id)getDelegate;  // AVOID
- (id)delegate;    // GOOD</pre>
</div>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#variable-names" name="variable-names"></a>Variable Names</h3>
Variables names start with a lowercase and use mixed case to delimit words. Instance variables have leading underscores. For example:<em>myLocalVariable</em>, <em>_myInstanceVariable</em>.</p>

<p><strong>Common Variable Names</strong></p>

<p>Do not use Hungarian notation for syntactic attributes, such as the static type of a variable (int or pointer). Give as descriptive a name as possible, within reason. Don't worry about saving horizontal space as it is far more important to make your code immediately understandable by a new reader. For example:
<div>
<pre>// Bad
int w;
int nerr;
int nCompConns;
tix = [[NSMutableArray alloc] init];
obj = [someObject object];
p = [network port];</pre></div></p>

<p>// Good<br />
int numErrors;<br />
int numCompletedConnections;<br />
tickets = [[NSMutableArray alloc] init];<br />
userInfo = [someObject object];<br />
port = [network port];

<strong>Instance Variables</strong>
Instance variables are mixed case and should be prefixed with an underscore e.g. <em>_usernameTextField</em>.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#comments" name="comments"></a>Comments</h3>
Though a pain to write, they are absolutely vital to keeping our code readable. The following rules describe what you should comment and where. But remember: while comments are very important, the best code is self-documenting. Giving sensible names to types and variables is much better than using obscure names and then trying to explain them through comments.</p>

<p>When writing your comments, write for your audience: the next contributor who will need to understand your code. Be generous—the next one may be you!</p>

<p><strong>File Comments</strong>
A file may optionally start with a description of its contents. Every file should contain the following items, in order:
<ul>
	<li>GPL License</li>
	<li>a basic description of the contents of the file if necessary.</li>
</ul>
If you make significant changes to a file with an author line, consider deleting the author line since revision history already provides a more detailed and accurate record of authorship.</p>

<p><strong>Declaration Comments</strong>
Every interface, category, and protocol declaration should have an accompanying comment describing its purpose and how it fits into the larger picture.
<div>
<pre>// A delegate for NSApplication to handle notifications about app
// launch and shutdown. Owned by the main app controller.
@interface MyAppDelegate : NSObject {
  ...
}
@end</pre>
</div>
If you have already described an interface in detail in the comments at the top of your file feel free to simply state "See comment at top of file for a complete description", but be sure to have some sort of comment.Additionally, each method in the public interface should have a comment explaining its function, arguments, return value, and any side effects.</p>

<p>Document the synchronization assumptions the class makes, if any. If an instance of the class can be accessed by multiple threads, take extra care to document the rules and invariants surrounding multithreaded use.
<h2><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#cocoa-and-objective-c-features" name="cocoa-and-objective-c-features"></a>Cocoa and Objective-C Features</h2>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#interface-files" name="interface-files"></a>Interface files</h3>
Interface files should be as short as possible: don't declare instance variables, and declare only properties and methods that need to be exposed to other classes. Everything else should go into an interface extension inside the implementation file. Remember that you don't need to declare private methods anymore with a modern Xcode version.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#overridden-nsobject-method-placement" name="overridden-nsobject-method-placement"></a>Overridden NSObject Method Placement</h3>
It is strongly recommended and typical practice to place overridden methods of <em>NSObject</em> at the top of an <em>@implementation</em>. This commonly applies (but is not limited) to the <em>init...</em>, <em>copyWithZone:</em>, and <em>dealloc</em> methods. <em>init</em>... methods should be grouped together, followed by the<em>copyWithZone:</em> method, and finally the <em>dealloc</em> method.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#initialization" name="initialization"></a>Initialization</h3>
Don't initialize variables to <em>0</em> or <em>nil</em> in the init method; it's redundant.</p>

<p>All memory for a newly allocated object is initialized to <em>0</em> (except for isa), so don't clutter up the init method by re-initializing variables to <em>0</em> or <em>nil</em>.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#keep-the-public-api-simple" name="keep-the-public-api-simple"></a>Keep the Public API Simple</h3>
Keep your class simple; avoid "kitchen-sink" APIs. If a method doesn't need to be public, don't make it so.
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#use-root-frameworks" name="use-root-frameworks"></a>Use Root Frameworks</h3>
Include root frameworks over individual files.</p>

<p>While it may seem tempting to include individual system headers from a framework such as Cocoa or Foundation, in fact it's less work on the compiler if you include the top-level root framework. The root framework is generally pre-compiled and can be loaded much more quickly. In addition, remember to use #import rather than #include for Objective-C frameworks.
<div>
<pre>// good
#import &lt;Foundation/Foundation.h&gt;</pre></div></p>

<p>// avoid<br />
#import &lt;Foundation/NSArray.h&gt;<br />
...

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#avoid-accessors-during-init-and-dealloc" name="avoid-accessors-during-init-and-dealloc"></a>Avoid Accessors During init and dealloc</h3>
Instance subclasses may be in an inconsistent state during <em>init</em> and <em>dealloc</em> method execution, so code in those methods should avoid invoking accessors.</p>

<p>Subclasses have not yet been initialized or have already deallocated when <em>init</em> and <em>dealloc</em> methods execute, making accessor methods potentially unreliable. Whenever practical, directly assign to and release ivars in those methods rather than rely on accessors.
<div>
<pre>// Good</pre></div></p>

<p>- (id)init {<br />
  self = [super init];<br />
  if (self) {<br />
    _bar = [[NSMutableString alloc] init];<br />
  }<br />
  return self;<br />
}</p>

<p>- (void)dealloc {<br />
  [_bar release];<br />
  [super dealloc];<br />
}</p>

<p>// Avoid</p>

<p>- (id)init {<br />
  self = [super init];<br />
  if (self) {<br />
    self.bar = [NSMutableString string];<br />
  }<br />
  return self;<br />
}</p>

<p>- (void)dealloc {<br />
  self.bar = nil;<br />
  [super dealloc];<br />
}

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#setters-copy-nsstrings" name="setters-copy-nsstrings"></a>Setters copy NSStrings</h3>
Setters taking an <em>NSString</em>, should always copy the string it accepts.</p>

<p>Never just retain the string. This avoids the caller changing it under you without your knowledge. Don't assume that because you're accepting an <em>NSString</em> that it's not actually an <em>NSMutableString</em>.
<div>
<pre>- (void)setFoo:(NSString *)aFoo {
  [_foo autorelease];
  _foo = [aFoo copy];
}</pre>
</div>
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#nil-checks" name="nil-checks"></a>nil Checks</h3>
Use <em>nil</em> checks for logic flow only.</p>

<p>Use <em>nil</em> checks for logic flow of the application, not for crash prevention. Sending a message to a nil object is handled by the Objective-C runtime. If the method has no return result, you're good to go. However if there is one, there may be differences based on runtime architecture, return size, and OS X version (see Apple's documentation for specifics).
<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#bool-pitfalls" name="bool-pitfalls"></a>BOOL Pitfalls</h3>
Be careful when converting general integral values to <em>BOOL</em>. Avoid comparing directly with <em>YES</em>.</p>

<p><em>BOOL</em> is defined as a signed char in Objective-C which means that it can have values other than <em>YES</em> (1) and <em>NO</em> (0). Do not cast or convert general integral values directly to <em>BOOL</em>. Common mistakes include casting or converting an array's size, a pointer value, or the result of a bitwise logic operation to a <em>BOOL</em> which, depending on the value of the last byte of the integral result, could still result in a <em>NO</em> value. When converting a general integral value to a <em>BOOL</em> use ternery operators to return a <em>YES</em> or <em>NO</em> value.</p>

<p>You can safely interchange and convert <em>BOOL</em>, <em>_Bool</em> and <em>bool</em> (see C++ Std 4.7.4, 4.12 and C99 Std 6.3.1.2). You cannot safely interchange<em>BOOL</em> and <em>Boolean</em> so treat <em>Booleans</em> as a general integral value as discussed above. Only use <em>BOOL</em> in Objective C method signatures.</p>

<p>Using logical operators (<em>&amp;&amp;</em>, <em>||</em> and <em>!</em>) with <em>BOOL</em> is also valid and will return values that can be safely converted to <em>BOOL</em> without the need for a ternery operator.
<div>
<pre>// Bad</pre></div></p>

<p>- (BOOL)isBold {<br />
  return [self fontTraits] &amp; NSFontBoldTrait;<br />
}
- (BOOL)isValid {<br />
  return [self stringValue];<br />
}</p>

<p>// Good<br />
- (BOOL)isBold {<br />
  return ([self fontTraits] &amp; NSFontBoldTrait) ? YES : NO;<br />
}
- (BOOL)isValid {<br />
  return [self stringValue] != nil;<br />
}
- (BOOL)isEnabled {<br />
  return [self isValid] &amp;&amp; [self isBold];<br />
}

Also, don't directly compare <em>BOOL</em> variables directly with <em>YES</em>. Not only is it harder to read for those well-versed in C, the first point above demonstrates that return values may not always be what you expect.
<div>
<pre>// Bad
BOOL great = [foo isGreat];
if (great == YES)
  // ...be great!</pre></div></p>

<p>//Good<br />
BOOL great = [foo isGreat];<br />
if (great)<br />
  // ...be great!

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#properties" name="properties"></a>Properties</h3>
Use of the <em>@property</em> directive is preferred. Dot notation is allowed only for access to a declared @property.</p>

<p>Use of automatically synthesized instance variables is preferred.</p>

<p><strong>Location</strong></p>

<p>A property's declaration must come immediately after the instance variable block of a class interface. A property's definition (if not using automatic synthesis) must come immediately after the <em>@implementation</em> block in a class definition. They are indented at the same level as the<em>@interface</em> or <em>@implementation</em> statements that they are enclosed in.
<div>
<pre>@interface MyClass : NSObject
@property(copy, nonatomic) NSString *name;
@end</pre></div></p>

<p>@implementation MyClass</p>

<p>- (id)init {<br />
  ...<br />
}
@end

<strong>Use Copy Attribute For Strings</strong>
NSString properties should always be declared with the <em>copy</em> attribute.This logically follows from the requirement that setters for NSStrings always must use <em>copy</em> instead of <em>retain</em>.</p>

<p><strong>Dot notation</strong>
Dot notation is idiomatic style for Objective-C 2.0. It may be used when doing simple operations to get and set a <em>@property</em> of an object, but should not be used to invoke other object behavior.
<div>
<pre>// Good
NSString *oldName = myObject.name;
myObject.name = @"Alice";
NSArray *array = [[NSArray arrayWithObject:@"hello"] retain];</pre></div></p>

<p>// Bad<br />
NSUInteger numberOfItems = array.count;  // not a property<br />
array.release;                           // not a property

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#interfaces-without-instance-variables" name="interfaces-without-instance-variables"></a>Interfaces Without Instance Variables</h3>
Omit the empty set of braces on interfaces that do not declare any instance variables.
<div>
<pre>// Good
@interface MyClass : NSObject
// Does a lot of stuff
- (void)fooBarBam;
@end</pre></div></p>

<p>// Bad<br />
@interface MyClass : NSObject {<br />
}
// Does a lot of stuff<br />
- (void)fooBarBam;<br />
@end

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#nsnumber-nsarray-and-nsdictionary--literals" name="nsnumber-nsarray-and-nsdictionary--literals"></a>NSNumber, NSArray and NSDictionary Literals</h3>
For projects that use Xcode 4.4 or later with clang, the use of NSNumber, NSArray and NSDictionary <a href="http://clang.llvm.org/docs/ObjectiveCLiterals.html">literals</a> is allowed and preferred.</p>

<p>NSNumber literals are used just like Objective C string literals. Boxing is used when necessary.
<div>
<pre>// NSNumber
NSNumber *fortyTwo = @42;
NSNumber *piOverTwo = @(M_PI / 2);
typedef NS_ENUM(NSUInteger, MyEnum) {
  MyEnumOne,
  MyEnumTwo = 2,
};
NSNumber *myEnum = @(MyEnumTwo);</pre></div></p>

<p>// NSArray<br />
NSArray *continents = @[@"North America", @"South America", @"Europe", @"Asia", @"Africa", @"Antarctica", @"Australia"];</p>

<p>// NSDictionary<br />
NSDictionary *personInfo = @{ @"name" : @"John Doe", @"age" : @(25) };

<h3><a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide#constant-definitions" name="constant-definitions"></a>Constant definitions</h3>
Avoid using <code>#define</code> for constants, they should be defined using <code>const</code>. Constant names should start with an uppercase letter and use mixed case.
<div>
<pre>// Good
NSInteger const ReaderPostsToSync = 20;
NSString *const ReaderLastSyncDateKey = @"ReaderLastSyncDate";</pre></div></p>

<p>// Bad<br />
#define READER_POSTS_TO_SYNC 20;<br />
#define READER_SYNC_DATE_KEY @"ReaderLastSyncDate";

Constants should be defined in the implementation file. If a class needs to expose a constant, it should be defined as <code>extern</code> on the interface file, then initialised in the implementation file:
<div>
<pre>//  Blog+Jetpack.h
extern NSString * const BlogJetpackErrorDomain;</pre></div></p>

<p>//  Blog+Jetpack.m<br />
NSString * const BlogJetpackErrorDomain = @"BlogJetpackError";





<div id="gollum-footer">
<p id="last-edit">[转]: <a href="https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide">https://github.com/wordpress-mobile/WordPress-iOS/wiki/WordPress-for-iOS-Style-Guide</a></p></div></p>

<p></p>
