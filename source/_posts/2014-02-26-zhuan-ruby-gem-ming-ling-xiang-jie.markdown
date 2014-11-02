---
layout: post
title: '[转]Ruby Gem命令详解'
categories:
- 技术
tags: [Ruby]
published: true
comments: true
---
<p>[转自]<a href="http://hi.baidu.com/mcspring/item/08545f14808bd0ddbf9042bc">http://hi.baidu.com/mcspring/item/08545f14808bd0ddbf9042bc</a></p>

<p><strong>Gem介绍：</strong></p>

<p><strong></strong>Gem是一个管理Ruby库和程序的标准包，它通过Ruby Gem（如 <a href="http://rubygems.org/" target="_blank">http://rubygems.org/</a> ）源来查找、安装、升级和卸载软件包，非常的便捷。</p>

<p>Ruby 1.9.2版本默认已安装Ruby Gem，如果你使用其它发行版本，请参考“<a href="http://docs.rubygems.org/read/chapter/3" target="_blank">如何安装Ruby Gem</a>”。</p>

<p>&nbsp;</p>

<p><strong>Ruby gem包的安装方式：</strong></p>

<p><strong></strong>所有的gem包，会被安装到 /[Ruby root]/lib/ruby/gems/[ver]/ 目录下，这其中包括了Cache、doc、gems、specifications 4个目录，cache下放置下载的原生gem包，gems下则放置的是解压过的gem包。<br />
当安装过程中遇到问题时，可以进入这些目录，手动删除有问题的gem包，然后重新运行 gem install [gemname] 命令即可。</p>

<p><strong>Ruby Gem命令详解：</strong></p>

<p><strong></strong># 更新Gem自身<br />
# 注意：在某些linux发行版中为了系统稳定性此命令禁止执行<br />
$ gem update --system</p>

<p># 从Gem源安装gem包<br />
$ gem install [gemname]</p>

<p># 从本机安装gem包<br />
$ gem install -l [gemname].gem</p>

<p># 安装指定版本的gem包<br />
$ gem install [gemname] --version=[ver]</p>

<p># 更新所有已安装的gem包<br />
$ gem update</p>

<p># 更新指定的gem包<br />
# 注意：gem update [gemname]不会升级旧版本的包，此时你可以使用 gem install [gemname] --version=[ver]代替<br />
$ gem update [gemname]</p>

<p># 删除指定的gem包，注意此命令将删除所有已安装的版本<br />
$ gem uninstall [gemname]</p>

<p># 删除某指定版本gem<br />
$ gem uninstall [gemname] --version=[ver]</p>

<p># 查看本机已安装的所有gem包<br />
$ gem list [--local]</p>
