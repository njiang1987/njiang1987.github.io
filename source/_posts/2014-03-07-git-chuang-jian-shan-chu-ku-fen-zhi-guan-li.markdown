---
layout: post
title: git创建、删除库，分支管理
categories:
- 技术
tags: [iOS]
published: true
comments: true
---
<p><div><span style="font-family: 'Arial Black';"><b>一、创建库</b></span></div>
<div><span style="color: #008080; font-family: 'Arial Black';"><b>git init &lt;库名&gt;</b></span></div>
<span style="font-family: 'Arial Black';"><b>二、创建分支 </b>(打开刚创建的库: <span style="color: #800080;">cd &lt;库名&gt;</span>)</span>
<div><span style="color: #008080; font-family: 'Arial Black';">git branch &lt;分支名&gt;</span></div>
<div><span style="font-family: 'Arial Black';">注：如果创建分支失败，建立一个测试文本文件即可。</span></div>
<div><span style="font-family: 'Arial Black';">1) <span style="color: #008080;">git add .</span></span></div>
<div><span style="font-family: 'Arial Black';">2) <span style="color: #008080;">git commit -a -m "test"</span></span></div>
<div><span style="font-family: 'Arial Black';"><b>三、切换分支</b></span></div>
<div>
<div><span style="color: #008080; font-family: 'Arial Black';">git checkout &lt;分支名&gt; </span></div>
<div><span style="font-family: 'Arial Black';">该语句和上一个语句可以和起来用一个语句表示：<span style="color: #008080;">git checkout -b &lt;分支名&gt;</span></span></div>
</div>
<div><span style="font-family: 'Arial Black';"><b>四、查看当前库所有分支</b></span></div>
<div><span style="font-family: 'Arial Black';"><span style="color: #008080;">git branch</span></span></div>
<div>
<div><span style="font-family: 'Arial Black';"><b>五、分支合并</b></span></div>
<div><span style="font-family: 'Arial Black';">比如，如果要将当前的分支<span style="color: #800080;">develop</span>，合并到主分支<span style="color: #800080;">master</span></span></div>
<div><span style="font-family: 'Arial Black';">首先我们需要切换到<span style="color: #800080;">master</span>主分支：<span style="color: #008080;">git checkout master</span></span></div>
<div><span style="font-family: 'Arial Black';">然后执行合并操作：<span style="color: #008080;">git merge develop</span></span></div>
<div><span style="font-family: 'Arial Black';">如果有冲突，会提示你，调用<span style="color: #008080;">git status</span>查看冲突文件。 </span></div>
<div><span style="font-family: 'Arial Black';">解决冲突，然后调用<span style="color: #008080;">git add</span>或<span style="color: #008080;">git rm</span>将解决后的文件暂存。 </span></div>
<div><span style="font-family: 'Arial Black';">所有冲突解决后，<span style="color: #008080;">git commit </span>提交更改。</span></div>
<div><span style="font-family: 'Arial Black';"><b>六、分支衍合</b></span></div>
<div><span style="font-family: 'Arial Black';">分支衍合和分支合并的差别在于，分支衍合不会保留合并的日志，不留痕迹，而 分支合并则会保留合并的日志。 </span></div>
<div><span style="font-family: 'Arial Black';">要将开发中的分支<span style="color: #800080;">develop</span>，衍合到主分支<span style="color: #800080;">master</span></span></div>
<div><span style="font-family: 'Arial Black';">首先切换的<span style="color: #800080;">master</span>分支：<span style="color: #008080;">git checkout master</span></span></div>
<div><span style="font-family: 'Arial Black';">然后执行衍和操作：<span style="color: #008080;">git rebase develop</span></span></div>
<div><span style="font-family: 'Arial Black';">如果有冲突，会提示你，调用<span style="color: #008080;">git status</span>查看冲突文件。 </span></div>
<div><span style="font-family: 'Arial Black';">解决冲突，然后调用<span style="color: #008080;">git add</span>或<span style="color: #008080;">git rm</span>将解决后的文件暂存。 </span></div>
<div><span style="font-family: 'Arial Black';">所有冲突解决后，<span style="color: #008080;">git rebase –continue</span> 提交更改。</span></div>
<div><span style="font-family: 'Arial Black';"><b>七、删除分支</b></span></div>
<div><span style="color: #008080; font-family: 'Arial Black';">git branch -d &lt;分支名&gt; </span></div>
<div><span style="font-family: 'Arial Black';">如果该分支没有合并到主分支会报错，可以用以下命令强制删除<span style="color: #008080;">git branch -D &lt;分支名&gt;</span></span></div>
</div>
<div><span style="font-family: 'Arial Black';"><b>八、删除库</b></span></div>
<div><span style="color: #008080; font-family: 'Arial Black';">rm -rf &lt;库名&gt;</span></div></p>
