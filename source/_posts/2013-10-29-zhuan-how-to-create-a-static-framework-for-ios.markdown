---
layout: post
title: '[转]How to Create a Static Framework for iOS'
categories:
- iOS
tags: []
published: true
comments: true
---
<p>Building a static iOS framework is a pain in the ass. There are a variety of existing solutions already and each one has its own disadvantages. Presented here is a solution that meets all of the following constraints while having no deal-breaking disadvantages.
<ul>
	<li>Fast iterative compilation times (up to 3x faster than some solutions!).</li>
	<li>Easy distribution and packaging.</li>
	<li>No modifications to Xcode.</li>
	<li>No trickery with fake bundle targets and the likes.</li>
	<li>Simple set-up for third-parties.</li>
	<li>Support for building the framework as a dependent target (i.e. modifying source in the framework and building an app will automatically rebuild the framework and relink as expected).</li>
	<li>Works with the latest version of Xcode</li>
</ul>
Shameless plug: if you appreciate high-speed iOS development, check out <a href="http://nimbuskit.info/">Nimbus</a>, the iOS framework whose growth is bounded by its documentation.</p>

<p><a href="http://creativecommons.org/licenses/by/3.0/" rel="license"><img alt="Creative Commons License" src="https://github-camo.global.ssl.fastly.net/ea7febd364f01e7b3f46f6fb86712fe05925bfbf/687474703a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f332e302f38387833312e706e67" /></a>
This work is licensed under a <a href="http://creativecommons.org/licenses/by/3.0/" rel="license">Creative Commons Attribution 3.0 Unported License</a>.
<h1><a href="https://github.com/jverkoey/iOS-Framework#table-of-contents" name="table-of-contents"></a>Table of Contents</h1>
<ul>
	<li><a href="https://github.com/jverkoey/iOS-Framework#existing_solutions">Existing Solutions</a></li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#walkthrough">How to Create a Static Framework for iOS</a>
<ul>
	<li><a href="https://github.com/jverkoey/iOS-Framework#overview">Overview</a></li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#static_library_target">Create the Static Library Target</a></li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#framework_distribution_target">Create the Framework Distribution Target</a></li>
</ul>
</li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#resources">Resources and Bundles</a></li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#third_parties">Adding the Framework to a Third-Party Application</a></li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#first_parties">Developing the Framework as a Dependent Project</a></li>
	<li><a href="https://github.com/jverkoey/iOS-Framework#license">License</a></li>
</ul>
<a name="existing_solutions"></a>
<h1><a href="https://github.com/jverkoey/iOS-Framework#existing-solutions" name="existing-solutions"></a>Existing Solutions</h1>
Presented below are a few of the most popular solutions for building static iOS frameworks and the reasons why they should be avoided.
<blockquote>Note: Though the tone below is largely critical, credit is owed to those who pioneered these solutions. Much of the proposed solution is based off the work that these amazingly generous people have donated to the ether. Thanks!</blockquote>
<h2><a href="https://github.com/jverkoey/iOS-Framework#ios-universal-framework" name="ios-universal-framework"></a>iOS-Universal-Framework</h2>
Source: <a href="https://github.com/kstenerud/iOS-Universal-Framework">https://github.com/kstenerud/iOS-Universal-Framework</a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#major-problems" name="major-problems"></a>Major problems</h3>
<ul>
	<li>Slow iterative build times</li>
	<li>Has to modify Xcode for "Real" frameworks</li>
	<li>Can't properly add framework as a dependent target for "Fake" frameworks</li>
	<li>No adequate solution for resource loading</li>
</ul>
<h3><a href="https://github.com/jverkoey/iOS-Framework#overview" name="overview"></a>Overview</h3>
This project provides two solutions: "fake" frameworks and "real" frameworks.</p>

<p>A <strong>fake</strong> framework is a bundle target with a .framework extension and some post-build scripts to generate the fat library for the .framework.</p>

<p>A <strong>real</strong> framework modifies the Xcode installation and generates a true .framework target. Real frameworks also use post-build scripts to generate the fat library.
<h3><a href="https://github.com/jverkoey/iOS-Framework#problems-with-fake-frameworks" name="problems-with-fake-frameworks"></a>Problems with Fake Frameworks</h3>
The problem with a fake framework is that you can't link to the framework as a dependent target. You can "trick" Xcode into linking to the framework by using the <code>-framework</code> flag in your <code>LD_FLAGS</code>, but changes to the framework will not be reflected in iterative builds. This requires that you clean build every time you modify the framework, or make a trivial modification to the application itself in order for it to forcefully relink to the new .framework. This bug is discussed <a href="https://github.com/kstenerud/iOS-Universal-Framework/issues/32">here</a>.</p>

<p><em>Example warning when you attempt to link to the .framework target:</em>
<pre><code>warning: skipping file
'/Users/featherless/Library/Developer/Xcode/DerivedData/SimpleApp-cshmhxdgzacibsgaiiryutjzobcb/Build/Products/Debug-iphonesimulator/fakeframework.framework'
(unexpected file type 'wrapper.cfbundle' in Frameworks &amp; Libraries build phase)
</code></pre>
<h3><a href="https://github.com/jverkoey/iOS-Framework#problems-with-real-frameworks" name="problems-with-real-frameworks"></a>Problems with Real Frameworks</h3>
To use real frameworks you need to modify your Xcode installation. This is simply not scalable when you want to work with a team of people. If you use a build farm this problem becomes even worse because it may not be possible to modify the Xcode installations on the build servers.
<h3><a href="https://github.com/jverkoey/iOS-Framework#problems-with-both-fake-and-real-frameworks" name="problems-with-both-fake-and-real-frameworks"></a>Problems with Both Fake and Real Frameworks</h3>
In both frameworks there is a post-build step that builds the "inverse" platform. For example, if you're building the framework for i386, the post-build step will build the framework for armv6/armv7/armv7s and then smush the libraries together into one fat binary within the framework. The problem with this is that it <strong>triples</strong> the build time of the framework. Make one change to a .m file and suddenly you're rebuilding it for three platforms. Change a PCH and your project will effectively perform three clean builds. This is simply not ok from a productivity standpoint.</p>

<p>There is also the problem of distributing resources with the .framework. Both the fake and real frameworks include an "embeddedframework" which is meant to be copied into the application. This results in the .framework binary being distributed with the application! Alternatively we could ask developers to only copy what's in the resources folder to their app, but this is complicated and requires we namespace our resource file names to avoid naming conflicts.
<h2><a href="https://github.com/jverkoey/iOS-Framework#db-ins-solution-fake-frameworks" name="db-ins-solution-fake-frameworks"></a>db-in's solution ("Fake" frameworks)</h2>
Source: <a href="http://db-in.com/blog/2011/07/universal-framework-iphone-ios-2-0/">http://db-in.com/blog/2011/07/universal-framework-iphone-ios-2-0/</a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#major-problems-1" name="major-problems-1"></a>Major problems</h3>
<ul>
	<li>Slow iterative build times</li>
	<li>Can't properly add framework as a dependent target</li>
	<li>No adequate solution for resource loading (recommends a remarkably <em>bad</em> solution)</li>
</ul>
<h3><a href="https://github.com/jverkoey/iOS-Framework#overview-1" name="overview-1"></a>Overview</h3>
db-in's solution is roughly identical to kstenerud's solution of using a bundle target to generate a fake framework. This has the same disadvantages as outlined above so I won't repeat myself.</p>

<p>There is, however, a specific deal-breaker with the recommendations in this blog post: resources. Db-in recommends copying the .framework into your application as a resource bundle; this is <b>NOT OK</b>. This will end up copying not just the resources from your framework, but also the fat binary of the framework! Doing this will inflate the size of your application by several megabytes more than it should be because you're shipping off a fat binary with your application.</p>

<p>And so without further ado...</p>

<p><a name="walkthrough"></a>
<h1><a href="https://github.com/jverkoey/iOS-Framework#how-to-create-a-static-framework-for-ios" name="how-to-create-a-static-framework-for-ios"></a>How to Create a Static Framework for iOS</h1>
There are a few constraints that we want to satisfy when building a .framework:
<ul>
	<li>Fast iterative builds when developing the framework. We may have a simple application that has the .framework as a dependency and we want to quickly iterate on development of the .framework.</li>
	<li>Infrequent distribution builds of the .framework.</li>
	<li>Resource distribution should be intuitive and not bloat the application.</li>
	<li>Setup for third-party developers using the .framework should be <em>easy</em>.</li>
</ul>
I believe that the solution I will outline below satisfies each of these constraints. I will outline how to build a .framework project from scratch so that you can apply these steps to an existing project if you so desire. I will also include project templates for easily creating a .framework.</p>

<p><a name="overview"></a>
<h2><a href="https://github.com/jverkoey/iOS-Framework#overview-2" name="overview-2"></a>Overview</h2>
<blockquote>View a sample project that shows the result of following these steps in the <code>sample/Serenity</code> directory.</blockquote>
Within the project we are going to have three targets: a static library, a bundle, and an aggregate.</p>

<p>The static library target will build the source into a static library (.a) and specify which headers will be "public", meaning they will be accessible from the .framework when we distribute it.</p>

<p>The bundle target will contain all of our resources and will be loadable from the framework.</p>

<p>The aggregate target will build the static library for i386/armv6/armv7/armv7s, generate the fat framework binary, and also build the bundle. You will run this target when you plan to distribute the .framework.</p>

<p>When you are working on the framework you will likely have an internal application that links to the framework. This application will link to the static library target as you normally would and copy the .bundle in the copy resources phase. This has the benefit of only building the framework code for the platform you're actively working on, significantly improving your build times. We'll do a little bit of work in the framework project to ensure that you can use your framework in your app the same way a third party developer would (i.e. importing should work as expected). <a href="https://github.com/jverkoey/iOS-Framework#first_parties">Jump to the dependent project walkthrough</a>.</p>

<p><a name="static_library_target"></a>
<h2><a href="https://github.com/jverkoey/iOS-Framework#create-the-static-library-target" name="create-the-static-library-target"></a>Create the Static Library Target</h2>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-1-create-a-new-cocoa-touch-static-library-project" name="step-1-create-a-new-cocoa-touch-static-library-project"></a>Step 1: Create a New "Cocoa Touch Static Library" Project</h3>
<a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newstaticlib.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newstaticlib.png" /></a></p>

<p>The product name will be the name of your framework. For example, <code>Serenity</code> will generate<code>Serenity.framework</code> once we've set up the project.
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-2-create-the-primary-framework-header" name="step-2-create-the-primary-framework-header"></a>Step 2: Create the Primary Framework Header</h3>
Developers expect to be able to import your framework by importing the <code>&lt;Serenity/Serenity.h&gt;</code> header. Ensure that your project has such a header (if you created a new static library then there should already be a Serenity.h and Serenity.m file; you can delete the .m).</p>

<p>Within this header you are going to import all of the public headers for your framework. For example, let's assume that we have some <code>Widget</code> with a .h and .m. Our Serenity.h file would look like this:
<pre><code>#import &lt;Foundation/Foundation.h&gt;</code></pre></p>

<p>#import &lt;Serenity/Widget.h&gt;

Once you've created your framework header file, you need to make it a "public" header. Public headers are headers that will be copied to the .framework and can be imported by those using your framework. This differs from "project" headers which will <em>not</em> be distributed with the framework. This distinction is what allows you to have a concept of public and private APIs.</p>

<p>To change a file's <a href="http://stackoverflow.com/questions/13571080/cant-change-target-membership-visibility-in-xcode-4-5">target membership visibility in XCode 4.4+</a>, you'll need to select the Static Library target you created (Serenity), open the Build Phases tab:</p>

<p><strong>Xcode 4.X:</strong> Click on Add Build Phase &gt; Add Copy Headers.</p>

<p><strong>Xcode 5:</strong> Add Build Phases from the menu. Click on Editor &gt; Add Build Setting -&gt; Add Copy Headers. Note: If the menu options are grayed out, you'll need to click on the whitespace below the Build Phases to regain focus and retry.</p>

<p>You'll see 3 sections for Public, Private, and Project headers. To modify the scope of any header, drag and drop the header files between the sections. Alternatively you can open the Project Navigator and select the header. Next expand the Utilities pane for the File Inspector. <a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/utilitiesbutton.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/utilitiesbutton.png" /></a> (Cmd+Option+0).</p>

<p>Look at the "Target Membership" group and ensure that the checkbox next to the .h file is checked. Change the scope of the header from "Project" to "Public". You might have to uncheck and check the box to get the dropdown list. This will ensure that the header gets copied to the correct location in the copy headers phase.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/publicheaders.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/publicheaders.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-3-update-the-public-headers-location" name="step-3-update-the-public-headers-location"></a>Step 3: Update the Public Headers Location</h3>
By default the static library project will copy private and public headers to the same folder:<code>/usr/local/include</code>. To avoid mistakenly copying private headers to our framework we want to ensure that our public headers are copied to a separate directory, e.g. <code>$(PROJECT_NAME)Headers</code>. To change this setting, select the project in the Project Navigator and then click the "Build Settings" tab. Search for "public headers" and then set the "Public Headers Folder Path" to "$(PROJECT_NAME)Headers" for all configurations. If you are working with multiple Frameworks make sure that this folder is unique.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/publicheadersconfig.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/publicheadersconfig.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#ongoing-step-adding-new-sources-to-the-framework" name="ongoing-step-adding-new-sources-to-the-framework"></a>Ongoing Step: Adding New Sources to the Framework</h3>
Whenever you add new source to the framework you must decide whether to expose the .h publicly or not. To modify a header's scope you will follow the same process as Step 2. By default a header's scope will be "Project", meaning it will not be copied to the framework's public headers.
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-4-disable-code-stripping" name="step-4-disable-code-stripping"></a>Step 4: Disable Code Stripping</h3>
We do not want to strip any code from the library; we leave this up to the application that is linking to the framework. To disable code stripping we must modify the following configuration settings:
<pre><code>"Dead Code Stripping" =&gt; No (for all settings)
"Strip Debug Symbols During Copy" =&gt; No (for all settings)
"Strip Style" =&gt; Non-Global Symbols (for all settings)
</code></pre>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-5-prepare-the-framework-for-use-as-a-dependent-target" name="step-5-prepare-the-framework-for-use-as-a-dependent-target"></a>Step 5: Prepare the Framework for use as a Dependent Target</h3>
In order to use the static library as though it were a framework we're going to generate the basic skeleton of the framework in the static library target. To do this we'll include a simple post-build script. Add a post-build script by selecting your project in the Project Navigator, selecting the target, and then the "Build Phases" tab.</p>

<p><strong>Xcode 4.X:</strong> Click Add Build Phase &gt; Add Run Script</p>

<p><strong>Xcode 5:</strong> Select Editor menu &gt; Add Build Phase &gt; Add Run Script Build Phase</p>

<p>Paste the following script in the source portion of the run script build phase. You can rename the phase by clicking the title of the phase (I've named it "Prepare Framework", for example).
<h4><a href="https://github.com/jverkoey/iOS-Framework#prepare_frameworksh" name="prepare_frameworksh"></a>prepare_framework.sh</h4>
<div>
<pre lang="bash" colla="+">set -e</pre></div></p>

<p>mkdir -p "${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.framework/Versions/A/Headers"</p>

<p># Link the "Current" version to "A"<br />
/bin/ln -sfh A "${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.framework/Versions/Current"<br />
/bin/ln -sfh Versions/Current/Headers "${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.framework/Headers"<br />
/bin/ln -sfh "Versions/Current/${PRODUCT_NAME}" "${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.framework/${PRODUCT_NAME}"</p>

<p># The -a ensures that the headers maintain the source modification date so that we don't constantly<br />
# cause propagating rebuilds of files that import these headers.<br />
/bin/cp -a "${TARGET_BUILD_DIR}/${PUBLIC_HEADERS_FOLDER_PATH}/" "${BUILT_PRODUCTS_DIR}/${PRODUCT_NAME}.framework/Versions/A/Headers"

<a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/prepareframework.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/prepareframework.png" /></a></p>

<p>This will generate the following folder structure:
<pre><code>-- Note: "-&gt;" denotes a symbolic link --</code></pre></p>

<p>Serenity.framework/<br />
  Headers/ -&gt; Versions/Current/Headers<br />
  Serenity -&gt; Versions/Current/Serenity<br />
  Versions/<br />
    A/<br />
      Headers/<br />
        Serenity.h<br />
        Widget.h<br />
    Current -&gt; A

Try building your project now and look at the build products directory (usually<code>~/Library/Developer/Xcode/DerivedData/&lt;ProjectName&gt;-&lt;gibberish&gt;/Build/Products/...</code>). You should see a<code>libSerenity.a</code> static library, a <code>Headers</code> folder, and a <code>Serenity.framework</code> folder that contains the basic skeleton of your framework.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/buildphase1.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/buildphase1.png" /></a></p>

<p><a name="framework_distribution_target"></a>
<h2><a href="https://github.com/jverkoey/iOS-Framework#create-the-framework-distribution-target" name="create-the-framework-distribution-target"></a>Create the Framework Distribution Target</h2>
When actively developing the framework we only care to build the platform that we're testing on. For example, if we're testing on the iPhone simulator then we only need to build the i386 platform.</p>

<p>This changes when we want to distribute the framework to third party developers. The third-party developers don't have the option of rebuilding the framework for each platform, so we must provide what is called a "fat binary" version of the static library that is comprised of the possible platforms. These platforms include: i386, armv6, armv7, and armv7s.</p>

<p>To generate this fat binary we're going to build the static library target for each platform.
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-1-create-an-aggregate-target" name="step-1-create-an-aggregate-target"></a>Step 1: Create an Aggregate Target</h3>
Click File &gt; New Target &gt; iOS &gt; Other and create a new Aggregate target. Title it something like "Framework".</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/aggregatetarget.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/aggregatetarget.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-2-add-the-static-library-as-a-dependent-target" name="step-2-add-the-static-library-as-a-dependent-target"></a>Step 2: Add the Static Library as a Dependent Target</h3>
Add the static library target to the "Target Dependencies".</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/targetdependencies.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/targetdependencies.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-3-build-the-other-platform" name="step-3-build-the-other-platform"></a>Step 3: Build the Other Platform</h3>
To build the other platform we're going to use a "Run Script" phase to execute some basic commands. Add a new "Run Script" build phase to your aggregate target and paste the following code into it.
<h4><a href="https://github.com/jverkoey/iOS-Framework#build_frameworksh" name="build_frameworksh"></a>build_framework.sh</h4>
<div>
<pre lang="bash" colla="+">set -e
set +u
# Avoid recursively calling this script.
if [[ $SF_MASTER_SCRIPT_RUNNING ]]
then
    exit 0
fi
set -u
export SF_MASTER_SCRIPT_RUNNING=1</pre></div></p>

<p>SF_TARGET_NAME=${PROJECT_NAME}<br />
SF_EXECUTABLE_PATH="lib${SF_TARGET_NAME}.a"<br />
SF_WRAPPER_NAME="${SF_TARGET_NAME}.framework"</p>

<p># The following conditionals come from<br />
# https://github.com/kstenerud/iOS-Universal-Framework</p>

<p>if [[ "$SDK_NAME" =~ ([A-Za-z]+) ]]<br />
then<br />
    SF_SDK_PLATFORM=${BASH_REMATCH[1]}<br />
else<br />
    echo "Could not find platform name from SDK_NAME: $SDK_NAME"<br />
    exit 1<br />
fi</p>

<p>if [[ "$SDK_NAME" =~ ([0-9]+.*$) ]]<br />
then<br />
    SF_SDK_VERSION=${BASH_REMATCH[1]}<br />
else<br />
    echo "Could not find sdk version from SDK_NAME: $SDK_NAME"<br />
    exit 1<br />
fi</p>

<p>if [[ "$SF_SDK_PLATFORM" = "iphoneos" ]]<br />
then<br />
    SF_OTHER_PLATFORM=iphonesimulator<br />
else<br />
    SF_OTHER_PLATFORM=iphoneos<br />
fi</p>

<p>if [[ "$BUILT_PRODUCTS_DIR" =~ (.*)$SF_SDK_PLATFORM$ ]]<br />
then<br />
    SF_OTHER_BUILT_PRODUCTS_DIR="${BASH_REMATCH[1]}${SF_OTHER_PLATFORM}"<br />
else<br />
    echo "Could not find platform name from build products directory: $BUILT_PRODUCTS_DIR"<br />
    exit 1<br />
fi</p>

<p># Build the other platform.<br />
xcodebuild -project "${PROJECT_FILE_PATH}" -target "${TARGET_NAME}" -configuration "${CONFIGURATION}" -sdk ${SF_OTHER_PLATFORM}${SF_SDK_VERSION} BUILD_DIR="${BUILD_DIR}" OBJROOT="${OBJROOT}" BUILD_ROOT="${BUILD_ROOT}" SYMROOT="${SYMROOT}" $ACTION</p>

<p># Smash the two static libraries into one fat binary and store it in the .framework<br />
lipo -create "${BUILT_PRODUCTS_DIR}/${SF_EXECUTABLE_PATH}" "${SF_OTHER_BUILT_PRODUCTS_DIR}/${SF_EXECUTABLE_PATH}" -output "${BUILT_PRODUCTS_DIR}/${SF_WRAPPER_NAME}/Versions/A/${SF_TARGET_NAME}"</p>

<p># Copy the binary to the other architecture folder to have a complete framework in both.<br />
cp -a "${BUILT_PRODUCTS_DIR}/${SF_WRAPPER_NAME}/Versions/A/${SF_TARGET_NAME}" "${SF_OTHER_BUILT_PRODUCTS_DIR}/${SF_WRAPPER_NAME}/Versions/A/${SF_TARGET_NAME}"

<h4><a href="https://github.com/jverkoey/iOS-Framework#important-note" name="important-note"></a>Important Note</h4>
The above script assumes that your library name matches your project name in the following line:
<div>
<pre>SF_TARGET_NAME=${PROJECT_NAME}</pre>
</div>
If this is not the case (e.g. your xcode project is named SerenityFramework and the target name is Serenity) then you need to explicitly set the target name on that line. For example:
<div>
<pre>SF_TARGET_NAME=Serenity</pre>
</div>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-4-build-and-verify" name="step-4-build-and-verify"></a>Step 4: Build and Verify</h3>
You now have everything set up to build a distributable .framework to third-party developers. Try building the aggregate target. Once it's done, expand the Products folder in Xcode, right click the static library and click "Show in Finder". If this doesn't open Finder to where the static library exists then try opening<code>~/Library/Developer/Xcode/DerivedData/&lt;project name&gt;/Build/Products/Debug-iphonesimulator/</code>.</p>

<p>Within this folder you will see your .framework folder.</p>

<p>You can now drag the .framework elsewhere, zip it up, upload it, and distribute it to your third-party developers.</p>

<p><a name="resources"></a>
<h1><a href="https://github.com/jverkoey/iOS-Framework#resources-and-bundles" name="resources-and-bundles"></a>Resources and Bundles</h1>
To distribute resources with a framework, we are going to provide the developer with a separate .bundle that contains all of the strings and resources. This distribution method provides a number of advantages over including the resources in the .framework itself.
<ul>
	<li>Encapsulation of resources. We can scope resource loading to our framework's bundle.</li>
	<li>Easy to add bundles to projects.</li>
	<li>The developer doesn't have to copy the entire .framework into their application.</li>
</ul>
The hard part about bundles is creating the target. Xcode's bundle target doesn't actually create a loadable bundle object, so we have to do some post-build massaging of the bundle. It's important that we create a bundle target because we need to create the bundle using the Copy Bundle Resources phase that will correctly compile .xib files (a Copy Files phase does not accomplish this!).
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-1-create-the-bundle-target" name="step-1-create-the-bundle-target"></a>Step 1: Create the Bundle Target</h3>
In the framework project, create a new bundle target. Click on File &gt; New &gt; Target &gt; OS X &gt; Bundle. You will need to name the bundle something different from your framework name or Xcode will not let you create the target. I've named the target SerenityResources. We will rename the output of the target to Serenity.bundle in a following step.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newbundletarget.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newbundletarget.png" /></a></p>

<p>Ensure that the Framework setting is set to "Core Foundation".</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newbundletarget2.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newbundletarget2.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-2-clean-up-the-bundle-target-settings" name="step-2-clean-up-the-bundle-target-settings"></a>Step 2: Clean up the Bundle Target Settings</h3>
By default the bundle will only show build settings for Mac OS X. It doesn't really matter what it builds for because the bundle isn't actually going to have any code in it, but I prefer to have things nice and consistent. Open the bundle target settings and delete the settings for Architectures, Base SDK, and Build Active Architecture Only.</p>

<p><strong>Xcode 5:</strong> Deleting a build setting will reset it to the Project's build setting. It should switch from OS X to iOS.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundlesettings.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundlesettings.png" /></a></p>

<p>This is also when you should change your bundle target's product name to the name of your framework rather than the target name. Click on your project in the Project Navigator and then select the bundle target. Click Build Settings, search for "Product Name", and then replace the value of Product Name with the name of your framework (e.g. $(TARGET_NAME) replaced by Serenity)</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/serenityproductname.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/serenityproductname.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-3-remove-hidpi-mac-os-x-build-setting" name="step-3-remove-hidpi-mac-os-x-build-setting"></a>Step 3: Remove HIDPI Mac OS X Build Setting</h3>
We created a OS X Bundle and it includes and option to merge HIDPI (retina and non-retina) art assets into a .tiff file. You don't want this behavior and need to disable it, or you will be unable to load your image assets from the bundle.</p>

<p>In the Bundle target go to Build Settings and search for <code>COMBINE_HIDPI_IMAGES</code> and delete the user defined setting. When you build, verify that your @2x.png and .png images are all in the bundle.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/delete_combine_hidpi.png" target="_blank"><img alt="Delete the COMBINE_HIDPI_IMAGES setting" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/delete_combine_hidpi.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#ongoing-step-add-resources-to-the-bundle-target-copy-files-phase" name="ongoing-step-add-resources-to-the-bundle-target-copy-files-phase"></a>Ongoing Step: Add Resources to the Bundle Target Copy Files Phase</h3>
Whenever you add new resources that you want to include with your framework you need to add it to the bundle target that you created.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newbundleresource.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/newbundleresource.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-4-add-the-bundle-target-to-your-aggregate-target" name="step-4-add-the-bundle-target-to-your-aggregate-target"></a>Step 4: Add the Bundle Target to your Aggregate Target</h3>
Whenever we build the framework for distribution we likely also want to build the bundle. Add the bundle target to your aggregate target's dependencies.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundledependency.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundledependency.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-5-loading-bundle-resources" name="step-5-loading-bundle-resources"></a>Step 5: Loading Bundle Resources</h3>
In order to load bundle resources, we must first ask the third-party developer to add the .bundle to their application. To do so they will simply drag the .bundle that you distributed with the .framework to their project and ensure that it is copied in the copy files phase of their app target.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/addbundle.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/addbundle.png" /></a></p>

<p>To load resources from the bundle we will use the following code:
<div>
<pre lang="objc" colla="+">// Load the framework bundle.
+ (NSBundle *)frameworkBundle {
  static NSBundle* frameworkBundle = nil;
  static dispatch_once_t predicate;
  dispatch_once(&amp;predicate, ^{
    NSString* mainBundlePath = [[NSBundle mainBundle] resourcePath];
    NSString* frameworkBundlePath = [mainBundlePath stringByAppendingPathComponent:@"Serenity.bundle"];
    frameworkBundle = [[NSBundle bundleWithPath:frameworkBundlePath] retain];
  });
  return frameworkBundle;
}</pre></div></p>

<p>[UIImage imageWithContentsOfFile:[[[self class] frameworkBundle] pathForResource:@"image" ofType:@"png"]];

You can see an example of loading a resource from within the framework in the Widget object in the included Serenity framework.</p>

<p><strong>Xcode 5:</strong> Do not use the Asset Catalog for any resources within a bundle. On an iOS 7.0 only project, a bug causes the pathForResource method to return nil.</p>

<p><a name="third_parties"></a>
<h1><a href="https://github.com/jverkoey/iOS-Framework#adding-the-framework-to-a-third-party-application" name="adding-the-framework-to-a-third-party-application"></a>Adding the Framework to a Third-Party Application</h1>
<blockquote>View a sample project that shows the result of following these steps in the <code>sample/ThirdParty</code> directory.</blockquote>
This is the easy part (and what your third-party developers will have to do). Simply drag the .framework to your application's project, ensuring that it's being added to the necessary targets.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/thirdparty.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/thirdparty.png" /></a></p>

<p>Import your framework header and you're kickin' ass.
<div>
<pre>#import &lt;Serenity/Serenity.h&gt;</pre>
</div>
<h3><a href="https://github.com/jverkoey/iOS-Framework#resources" name="resources"></a>Resources</h3>
If you're distributing resources with your framework then you will also send the .bundle file to the developers. The developer will then drag the .bundle file into their application and ensure that it's added to the application target.</p>

<p><a name="first_parties"></a>
<h1><a href="https://github.com/jverkoey/iOS-Framework#developing-the-framework-as-a-dependent-project" name="developing-the-framework-as-a-dependent-project"></a>Developing the Framework as a Dependent Project</h1>
<blockquote>View a sample project that shows the result of following these steps in the <code>sample/DependentApp</code>directory.</blockquote>
When developing the framework you want to minimize build times while ensuring that your experience roughly matches that of your third-party developers. We achieve this balance by only building the static library but treating the static library as though it were a framework.
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-1-add-the-framework-project-to-your-application-project" name="step-1-add-the-framework-project-to-your-application-project"></a>Step 1: Add the Framework Project to your Application Project</h3>
To add the framework as a dependent target in your application, from Finder drag the framework's .xcodeproj to Xcode and drop it in your application's frameworks folder. This will add a reference to the framework's xcodeproj folder.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/dependentapp.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/dependentapp.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-2-make-the-framework-static-library-target-a-dependency" name="step-2-make-the-framework-static-library-target-a-dependency"></a>Step 2: Make the Framework Static Library Target a Dependency</h3>
Once you've added the framework project to your app you can add the static library product as a dependency. Select your project in the Project Navigator and open the "Build Phases" tab. Expand the "Target Dependencies" group and click the + button. Select the static library target and click "Add".</p>

<p><strong>Note:</strong> Close your Static Library Project or the dependencies will not appear in the list. You can only have one instance of an Xcode project open.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/addtarget.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/addtarget.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-3-link-your-application-with-the-framework-static-library" name="step-3-link-your-application-with-the-framework-static-library"></a>Step 3: Link your Application with the Framework Static Library</h3>
In order to use the framework's static library we must link it into the application. Expand the "Link Binary With Libraries" phase and click the + button. Select the <code>.a</code> file that's exposed by your framework's project and then click add.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/linker.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/linker.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-4-import-the-framework-header" name="step-4-import-the-framework-header"></a>Step 4: Import the Framework Header</h3>
You now simply need to import the framework header somewhere in your project. I generally prefer the pch so that I don't have to clutter up my application's source with framework headers, but you can obviously choose whatever practice suits your needs.
<div>
<pre>#import &lt;Serenity/Serenity.h&gt;</pre>
</div>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-4-b-adding-resources" name="step-4-b-adding-resources"></a>Step 4-b: Adding Resources</h3>
If you are developing resources for your framework you can also add the bundle target as a dependency.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundledependency2.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundledependency2.png" /></a></p>

<p>You must then add the bundle to the Copy Bundle Resources phase of your application by expanding the products folder of your framework product and dragging the .bundle into that section.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundlecopy.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/bundlecopy.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-5-check-dependent-target-build-settings" name="step-5-check-dependent-target-build-settings"></a>Step 5: Check Dependent Target Build Settings</h3>
Set the setting <code>Skip Install</code> to <code>Yes</code> for any static library or bundle target that you create. Check all the targets that are dependencies of your application project. If the option is <code>No</code> then you will be unable to build an archive of the project containing the target dependencies. Xcode will create a Generic Xcode Archive, which cannot be shared adhoc, validated, or submitted.</p>

<p><a href="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/skip_install.png" target="_blank"><img alt="" src="https://github.com/jverkoey/iOS-Framework/raw/master/gfx/skip_install.png" /></a>
<h3><a href="https://github.com/jverkoey/iOS-Framework#step-6-build-and-test" name="step-6-build-and-test"></a>Step 6: Build and Test</h3>
Build your application and verify a couple things:
<ul>
	<li>Your framework should be built before your application.</li>
	<li>Your framework should be linked into the application.</li>
	<li>You shouldn't get any compiler or linker errors.</li>
</ul></p>

<p>[转自]:https://github.com/jverkoey/iOS-Framework</p>
