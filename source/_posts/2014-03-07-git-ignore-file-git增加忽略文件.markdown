---
layout: post
title: git ignore file, Git增加忽略文件
categories:
- iOS
tags:
- git
published: true
comments: true
---
<p><h1><span style="font-size: 16px; font-weight: 400; line-height: 1.5;">最简单的方法在项目根目录与.git目录同一位置创建一个文件: .gitignore</span></h1>
<div>
<div id="cnblogs_post_body" /></div></p>

<p>touch .gitignore<br />
vi .gitignore<br />
:wq</p>

<p>注:如果要忽略的文件已被git管理,需要先移除,命令如下:</p>

<p>e.g.:<br />
git rm -r --cached  WebRoot/WEB-INF/classes/**/*<br />
-r:递归<br />
git commit</p>

<p>然后.gitignore中的忽略,起作用以下参考//-------------------</p>

<p>from:</p>

<p><a href="http://gitready.com/beginner/2009/01/19/ignoring-files.html">http://gitready.com/beginner/2009/01/19/ignoring-files.html</a></p>

<p>The easiest and simplest way is to create a <code>.gitignore</code> file in your project’s root directory. The files you choose to ignore here take affect for all directories in your project, unless if they include their own <code>.gitignore</code> file. This is nice since you have one place to configure ignores unlike SVN’s svn:ignore which must be set on every folder. Also, the file itself can be versioned, which is definitely good.</p>

<p>Here’s a basic <code>.gitignore</code>:
<pre>$ cat .gitignore</pre></p>

<p># Can ignore specific files<br />
.DS_Store</p>

<p># Use wildcards as well<br />
*~<br />
*.swp</p>

<p># Can also ignore all directories and files in a directory.<br />
tmp/**/*
Of course, this could get a lot more complex. You can also add exceptions to ignore rules by starting the line with <code>!</code>. See an example of this at the <a href="http://github.com/guides/ignore-for-git">GitHub guide on ignores</a>.</p>

<p>Two things to keep in mind with ignoring files: First, if a file is already being tracked by Git, adding the file to <code>.gitignore</code> won’t stop Git from tracking it. You’ll need to do <code>git rm --cached &lt;file&gt;</code> to keep the file in your tree and then ignore it. Secondly, empty directories do not get tracked by Git. If you want them to be tracked, they need to have something in them. Usually doing a <code>touch .gitignore</code> is enough to keep the folder tracked.</p>

<p>You can also open up <code>$GIT_DIR/info/exclude</code> (<code>$GIT_DIR</code> is usually your <code>.git</code> folder) and edit that file for project-only ignores. The problem with this is that those changes aren’t checked in, so use this only if you have some personal files that don’t need to be shared with others on the same project.</p>

<p>Your final option with ignoring folders is adding a per-user ignore by setting up a<code>core.excludesfiles</code> option in your config file. You can set up a <code>.gitignore</code> file in yourHOME directory that will affect all of your repositories by running this command:</p>

<p><code>git config --global core.excludesfile ~/.gitignore</code></p>

<p>Read up on the <a href="http://www.kernel.org/pub/software/scm/git/docs/gitignore.html">manpage</a> if you’d like to learn more about how ignores work. As always, if you have other ignore-related tips let us know in the comments.</p>

<p>
</p>
