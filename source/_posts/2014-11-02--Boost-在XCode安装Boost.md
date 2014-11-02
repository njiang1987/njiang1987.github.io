title: "[Boost]在XCode安装Boost"
date: 2014-11-02 08:57:50
categories: 技术
tags: LeetCode
photos:
- /uploads/header/maomi.jpg
---
##下载Boost库 
最新的版本可以在<http://www.boost.org/>找到，这里我下载的1.56.0版本，[Download](http://jaist.dl.sourceforge.net/project/boost/boost/1.56.0/boost_1_56_0.tar.gz)

##编译Boost.Build
修改sh的文件属性
```bash
chmod +x bootstrap.sh
```
执行bootstrap.sh
```bash
./bootstrap.sh
```

##编译Boost库
执行b2可执行程序
```bash
//用Clang编译boost file sytem
./b2 toolset=clang cxxflags="-arch x86_64" linkflags="-arch x86_64" --with-filesystem
```

最后生成的文件保存在./stage/lib目录

默认编译出来的是Release版本，编译debug版本：
```bash
./b2 toolset=clang cxxflags="-arch x86_64" linkflags="-arch x86_64" --with-filesystem variant=debug --stagedir=./stage/x64/debug
```

##设置XCode
在 XCode 中，打开项目后 Build settings：
在中  Users Headers Search Paths 中添加，例如：/Users/Shared/boost_1_46_1

在Library Search Paths 中添加 /Users/Shared/include

##重新编译
重新编译就可以了。