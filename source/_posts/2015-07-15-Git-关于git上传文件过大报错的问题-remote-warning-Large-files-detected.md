title: '[Git]关于git上传文件过大报错的问题 remote: warning: Large files detected'
date: 2015-07-15 11:34:16
tags:
---
今天往git上传了个项目，没有注意有个500m的大家伙在里面，就一并commit+push了，然后噩梦就来了。
首先是报错：

```shell
remote: warning: Large files detected.
# remote: warning: File big_file is 55.00 MB; this is larger than GitHub's
recommended maximum file size of 50 MB
```

一看不就是文件过大报错了嘛，直接文件delete重新commit，没想到问题继续。。
然后又尝试重试新建一个小的同名文件继续commit，问题继续。。

后来找到github上的一个帮助页面 Working with large files，照着"Removing the local file added with the most recent unpushed commit"的步骤操作了一番，最终未遂。但我的问题应该是下面的关于“Removing the file added in an older commit”才能解决的（因为我已经提交并push了），可是教程里只写了通过git-filter-branch解决，但是命令不能用~

想到我的问题一定是这个大文件已经保存到了log中，因此无论我怎么删改，这个文件没有从log中剔除就总会报出相同的错误，最后又是在万能的StackOverflow上有人给出了解决方法，命令如下：

[plain] view plaincopy在CODE上查看代码片派生到我的代码片

```shell
git filter-branch -f --index-filter "git rm -rf --cached --ignore-unmatch FOLDERNAME" -- --all
```

把你的文件或者文件夹位置替换掉那个FOLDERNAME就可以了。
转自：<http://blog.csdn.net/memray/article/details/43154779>