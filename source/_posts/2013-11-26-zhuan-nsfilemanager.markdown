---
layout: post
title: '[转]NSFileManager'
categories:
- 未分类
tags: []
published: true
comments: true
---
<p><code>NSFileManager</code> is Foundation's high-level API for working with file systems. It abstracts Unix and Finder internals, providing a convenient way to create, read, move, copy, and delete files &amp; directories on local or networked drives, as well as iCloud ubiquitous containers.</p>

<p>File systems are a complex topic, with decades of history, vestigial complexities, and idiosyncrasies, and is well outside the scope of a single article. And since most applications don't often interact with the file system much beyond simple file operations, one can get away with only knowing the basics.</p>

<p>What follows are some code samples for your copy-pasting pleasure. Use them as a foundation for understanding how to adjust parameters to your particular use case:
<h2>Common Tasks</h2>
<blockquote>Throughout the code samples is the magical incantation<code>NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)</code>. This may be tied with KVO as one of the worst APIs in Cocoa. Just know that this returns an array containing the user documents directory as the first object. Thank goodness for the inclusion of <code>NSArray -firstObject</code>.</blockquote>
<h3>Determining If A File Exists</h3>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [NSFileManager defaultManager];
NSString *documentsPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject];
NSString *filePath = [documentsPath stringByAppendingPathComponent:@"file.txt"];
BOOL fileExists = [fileManager fileExistsAtPath:filePath];
</code></pre>
</div>
<h3>Listing All Files In A Directory</h3>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [NSFileManager defaultManager];
NSURL *bundleURL = [[NSBundle mainBundle] bundleURL];
NSArray *contents = [fileManager contentsOfDirectoryAtURL:bundleURL
                               includingPropertiesForKeys:@[]
                                                  options:NSDirectoryEnumerationSkipsHiddenFiles
                                                    error:nil];</code></pre></div></p>

<p>NSPredicate *predicate = [NSPredicate predicateWithFormat:@"pathExtension ENDSWITH '.png'"];<br />
for (NSString *path in [contents filteredArrayUsingPredicate:predicate]) {<br />
    // Enumerate each .png file in directory<br />
}


<h2>Recursively Enumerating Files In A Directory</h2>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [NSFileManager defaultManager];
NSURL *bundleURL = [[NSBundle mainBundle] bundleURL];
NSDirectoryEnumerator *enumerator = [fileManager enumeratorAtURL:bundleURL
                                      includingPropertiesForKeys:@[NSURLNameKey, NSURLIsDirectoryKey]
                                                         options:NSDirectoryEnumerationSkipsHiddenFiles
                                                    errorHandler:^BOOL(NSURL *url, NSError *error)
{
    NSLog(@"[Error] %@ (%@)", error, url);
}];</code></pre></div></p>

<p>NSMutableArray *mutableFileURLs = [NSMutableArray array];<br />
for (NSURL *fileURL in enumerator) {<br />
    NSString *filename;<br />
    [fileURL getResourceValue:&amp;filename forKey:NSURLNameKey error:nil];</p>

<p>    NSNumber *isDirectory;<br />
    [fileURL getResourceValue:&amp;isDirectory forKey:NSURLIsDirectoryKey error:nil];</p>

<p>    // Skip directories with '_' prefix, for example<br />
    if ([filename hasPrefix:@"_"] &amp;&amp; [isDirectory boolValue]) {<br />
        [enumerator skipDescendants];<br />
        continue;<br />
    }</p>

<p>    if (![isDirectory boolValue]) {<br />
        [mutableFileURLs addObject:fileURL];<br />
    }<br />
}


<h3>Create a Directory</h3>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [NSFileManager defaultManager];
NSString *documentsPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject];
NSString *imagesPath = [documentsPath stringByAppendingPathComponent:@"images"];
if (![fileManager fileExistsAtPath:imagesPath]) {
    [fileManager createDirectoryAtPath:imagesPath withIntermediateDirectories:NO attributes:nil error:nil];
}
</code></pre>
</div>
<h3>Deleting a File</h3>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [NSFileManager defaultManager];
NSString *documentsPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject];
NSString *filePath = [documentsPath stringByAppendingPathComponent:@"image.png"];
NSError *error = nil;</code></pre></div></p>

<p>if (![fileManager removeItemAtPath:filePath error:&amp;error]) {<br />
    NSLog(@"[Error] %@ (%@)", error, filePath);<br />
}


<h3>Determine the Creation Date of a File</h3>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [NSFileManager defaultManager];
NSString *documentsPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject];
NSString *filePath = [documentsPath stringByAppendingPathComponent:@"Document.pages"];</code></pre></div></p>

<p>NSDate *creationDate = nil;<br />
if ([fileManager fileExistsAtPath:filePath]) {<br />
    NSDictionary *attributes = [fileManager attributesOfItemAtPath:filePath error:nil];<br />
    creationDate = attributes[NSFileCreationDate];<br />
}


There are a number of file attributes that are made accessible through <code>NSFileManager</code>, which can be fetched with <code>-attributesOfItemAtPath:error:</code>, and other methods:
<h4>File Attribute Keys</h4>
<blockquote>
<ul>
	<li><code>NSFileAppendOnly</code>: The key in a file attribute dictionary whose value indicates whether the file is read-only.</li>
	<li><code>NSFileBusy</code>: The key in a file attribute dictionary whose value indicates whether the file is busy.</li>
	<li><code>NSFileCreationDate</code>: The key in a file attribute dictionary whose value indicates the file's creation date.</li>
	<li><code>NSFileOwnerAccountName</code>: The key in a file attribute dictionary whose value indicates the name of the file's owner.</li>
	<li><code>NSFileGroupOwnerAccountName</code>: The key in a file attribute dictionary whose value indicates the group name of the file's owner.</li>
	<li><code>NSFileDeviceIdentifier</code>: The key in a file attribute dictionary whose value indicates the identifier for the device on which the file resides.</li>
	<li><code>NSFileExtensionHidden</code>: The key in a file attribute dictionary whose value indicates whether the file's extension is hidden.</li>
	<li><code>NSFileGroupOwnerAccountID</code>: The key in a file attribute dictionary whose value indicates the file's group ID.</li>
	<li><code>NSFileHFSCreatorCode</code>: The key in a file attribute dictionary whose value indicates the file's HFS creator code.</li>
	<li><code>NSFileHFSTypeCode</code>: The key in a file attribute dictionary whose value indicates the file's HFS type code.</li>
	<li><code>NSFileImmutable</code>: The key in a file attribute dictionary whose value indicates whether the file is mutable.</li>
	<li><code>NSFileModificationDate</code>: The key in a file attribute dictionary whose value indicates the file's last modified date.</li>
	<li><code>NSFileOwnerAccountID</code>: The key in a file attribute dictionary whose value indicates the file's owner's account ID.</li>
	<li><code>NSFilePosixPermissions</code>: The key in a file attribute dictionary whose value indicates the file's Posix permissions.</li>
	<li><code>NSFileReferenceCount</code>: The key in a file attribute dictionary whose value indicates the file's reference count.</li>
	<li><code>NSFileSize</code>: The key in a file attribute dictionary whose value indicates the file's size in bytes.</li>
	<li><code>NSFileSystemFileNumber</code>: The key in a file attribute dictionary whose value indicates the file's filesystem file number.</li>
	<li><code>NSFileType</code>: The key in a file attribute dictionary whose value indicates the file's type.</li>
	<li><code>NSDirectoryEnumerationSkipsSubdirectoryDescendants</code>: Perform a shallow enumeration; do not descend into directories.</li>
	<li><code>NSDirectoryEnumerationSkipsPackageDescendants</code>: Do not descend into packages.</li>
	<li><code>NSDirectoryEnumerationSkipsHiddenFiles</code>: Do not enumerate hidden files.</li>
</ul>
</blockquote>
<h2>NSFileManagerDelegate</h2>
<code>NSFileManager</code> may optionally set a delegate to verify that it should perform a particular file operation. This allows the business logic of, for instance, which files to protect from deletion, to be factored out of the controller.</p>

<p>There are four kinds of methods in the <code>&lt;NSFileManagerDelegate&gt;</code> protocol, each with a variation for working with paths, as well as methods for error handling.
<ul>
	<li><code>-fileManager:shouldMoveItemAtURL:toURL:</code></li>
	<li><code>-fileManager:shouldCopyItemAtURL:toURL:</code></li>
	<li><code>-fileManager:shouldRemoveItemAtURL:</code></li>
	<li><code>-fileManager:shouldLinkItemAtURL:toURL:</code></li>
</ul>
If you were wondering when you might <code>alloc init</code> your own <code>NSFileManager</code> rather than using the shared instance, this is it. As per the documentation:
<blockquote>If you use a delegate to receive notifications about the status of move, copy, remove, and link operations, you should create a unique instance of the file manager object, assign your delegate to that object, and use that file manager to initiate your operations.</blockquote>
<div>
<pre><code data-lang="objective-c">NSFileManager *fileManager = [[NSFileManager alloc] init];
fileManager.delegate = delegate;</code></pre></div></p>

<p>NSURL *bundleURL = [[NSBundle mainBundle] bundleURL];<br />
NSArray *contents = [fileManager contentsOfDirectoryAtURL:bundleURL<br />
                               includingPropertiesForKeys:@[]<br />
                                                  options:NSDirectoryEnumerationSkipsHiddenFiles<br />
                                                    error:nil];</p>

<p>for (NSString *filePath in contents) {<br />
    [fileManager removeItemAtPath:filePath error:nil];<br />
}


<h4>CustomFileManagerDelegate.m</h4>
<div>
<pre><code data-lang="objective-c">#pragma mark - NSFileManagerDelegate</code></pre></div></p>

<p>- (BOOL)fileManager:(NSFileManager *)fileManager<br />
shouldRemoveItemAtURL:(NSURL *)URL<br />
{
    return ![[[URL lastPathComponent] pathExtension] isEqualToString:@"pdf"];<br />
}


<h2>Ubiquitous Storage</h2>
Documents can also be moved to iCloud. If you guessed that this would be anything but straight forward, you'd be 100% correct.</p>

<p>This is another occasion when you'd <code>alloc init</code> your own <code>NSFileManager</code> rather than using the shared instance. Because <code>URLForUbiquityContainerIdentifier:</code> and<code>setUbiquitous:itemAtURL:destinationURL:error:</code> are blocking calls, this entire operation needs to be dispatched to a background queue.
<h3>Move Item to Ubiquitous Storage</h3>
<div>
<pre><code data-lang="objective-c">dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
    NSFileManager *fileManager = [[NSFileManager alloc] init];
    NSString *documentsPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject];
    NSURL *fileURL = [NSURL fileURLWithPath:[documentsPath stringByAppendingPathComponent:@"Document.pages"]];</code></pre></div></p>

<p>    // Defaults to first listed in entitlements when `nil`; should replace with real identifier<br />
    NSString *identifier = nil;</p>

<p>    NSURL *ubiquitousContainerURL = [fileManager URLForUbiquityContainerIdentifier:identifier];<br />
    NSURL *ubiquitousFileURL = [ubiquitousContainerURL URLByAppendingPathComponent:@"Document.pages"];</p>

<p>    NSError *error = nil;<br />
    BOOL success = [fileManager setUbiquitous:YES<br />
                                    itemAtURL:fileURL<br />
                               destinationURL:ubiquitousFileURL<br />
                                        error:&amp;error];<br />
    if (!success) {<br />
        NSLog(@"[Error] %@ (%@) (%@)", error, fileURL, ubiquitousFileURL);<br />
    }<br />
});


<blockquote>You can find more information about ubiquitous document storage in Apple's "iCloud File Management" document.</blockquote>
[转自]：<a href="http://nshipster.com/nsfilemanager/">http://nshipster.com/nsfilemanager/</a></p>
