---
layout: post
title: Merge two repo
categories:
- 未分类
tags: []
published: true
comments: true
---
<p>Let’s keep calling the repos A and B for the moment, assume we are merging B into A, and consider the following simple example first. We’ll create a remote inside A pointing to B, then merge B’s master branch into A’s master branch.</p>

<p>Clone both repositories into the same directory and go into repo A:
<code>
$ git clone A<br />
$ git clone B<br />
$ cd A
</code></p>

<p>Add a remote called B that points to the repo B (do <code>git remote -v</code> to view your remotes), and fetch copies of all B’s branches:
<code>
$ git remote add B ../B<br />
$ git fetch B
</code>
To view all B’s branches that we’ve just fetched, do <code>git branch -a</code>. You should see <code>B/master</code> in the list. Now, still in repo A, create a branch called <code>B-master</code> in repo A that tracks <code>B/master</code>.
<code>
$ git branch B-master B/master
</code></p>

<p>If you’re not already in the master branch, check it out, then merge <code>B-master</code> into A’s master.
<code>
$ git merge B-master
</code></p>

<p>Assuming you have no merge conflicts, you’re done!</p>
