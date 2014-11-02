---
layout: post
title: '[转]Mac 彻底删除MySQL'
categories:
- 技术
tags: [Other]
published: true
comments: true
---
<p>注意：确保MySQL没有运行。</p>

<p>首先编辑 <em>/etc/hostconfig</em> 删掉MYSQL的配置。
<ol>
	<li>在终端理执行 sudo nano /etc/hostconfig</li>
	<li>删除 “MYSQLCOM=-YES”</li>
	<li>按CTRL+X ， 之后按  “Y” 保存并退出。</li>
	<li>复制如下命令到终端，并执行</li>
</ol>
<pre>sudo rm /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
sudo rm /etc/my.cnf</pre></p>

<p>ok,卸载完毕！</p>
