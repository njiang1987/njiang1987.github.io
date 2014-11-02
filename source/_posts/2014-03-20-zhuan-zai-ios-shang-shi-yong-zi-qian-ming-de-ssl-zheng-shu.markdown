---
layout: post
title: '[转]在iOS上使用自签名的SSL证书'
categories:
- 技术
tags: [iOS]
published: true
comments: true
---
<p>[转]<a href="http://beyondvincent.com/blog/2014/03/17/five-tips-for-using-self-signed-ssl-certificates-with-ios/">http://beyondvincent.com/blog/2014/03/17/five-tips-for-using-self-signed-ssl-certificates-with-ios/</a></p>

<p>上周苹果release了iOS 7.1，用户升级至此版本，去下载企业级应用时，如果应用不是用https部署的，那么会提示服务器上的证书无效，如下图所示：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/11.PNG" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/11.PNG" /></a></p>

<p>小引:</p>

<p>在iOS 7.1中需要将plists文件的url路径设置为https才能下载安装，如果之前是用http部署的，这就需要对服务器做一些修改。网上流传着(<a href="http://stackoverflow.com/questions/20276907/enterprise-app-deployment-doesnt-work-on-ios-7-1/22325916#22325916">Enterprise app deployment doesn’t work on iOS 7.1</a>)把plist放到公开的具有https功能的文件服务器上即可(dropbox或SkyDrive)，经试验，都是可行的。不过如要企业内部的网络无法访问外网，这又如何是好呢？网上也流传需要受信任的证书才行，这样一来对于某些企业的内部部署就比较麻烦了(局域网、主机名变动等都会引起很麻烦的事情)，各区域可能还要用不同的证书(对应不同的host name)。</p>

<p>经查苹果的相关文档(2014年2月份)，是可以使用http或者https的，后来打电话咨询苹果技术支持人员，告知文档还没来得及更新，不过自签名的证书也可以使用，最好首先要把证书(最好是CA根证书)通过mail或者配置工具安装到iOS设备上，然后根据这个CA构建web 服务器上用到的证书，这样当iOS设备访问web服务器来安装app时，就可以正常进行了。这样的话，我们只需要根据不同的服务器制作对应的自签名证书即可，有问题也方便修改跟进。</p>

<p>下面这篇文章就是介绍如何在iOS上面使用自签名的SSL证书。</p>

<p>先来看看目录：
<ol>
	<li>在iPhone或者iPad上的Safari中不要接受自签名证书</li>
	<li>像安装iOS的Configuration Profile一样安装自签名证书</li>
	<li>不要用IIS创建自签名证书</li>
	<li>利用OpenSSL创建自签名证书</li>
	<li>创建自己的证书颁发机构(CA)</li>
</ol>
虽说SSL证书的购买价格不是太贵，不过有时候我们自行创建的话要更加方便一些，例如我们需要在开发环境配置SSL时、我们的测试服务器有不同的主机名或者开发的系统只有本地局域网才能访问。</p>

<p>实际上我们可以免费的创建<a href="http://en.wikipedia.org/wiki/Self-signed_certificate">自签名SSL证书</a>，并不需要给证书颁发机构(CA)支付任何费用，也不需要遵守任何审计要求。</p>

<p>使用自签名SSL证书的缺点就是浏览器不会自动的信任相关的站点。如果用iPhone或者iPad上的Safari打开相关站点，会看到如下提示界面：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/01.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/01.png" /></a></p>

<p>这里的HttpWatch iOS app还会有更详细的提示内容：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/02.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/02.png" /></a></p>

<p>本文剩余内容将介绍如何对iOS做配置，以避免上面遇到的问题，以及如何方便的创建和管理自签名证书。
<h2>在iPhone或者iPad上的Safari中不要接受自签名证书</h2>
当在Safari中第一次访问自签名证书的站点时，会有如下提示(Continue或Details-&gt;Accept)：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/03.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/03.png" /></a></p>

<p>如果你照着选择的话，是可以在Safari中打开站点的，不过这样会有两个明显的缺点：
<ol>
	<li>在Safari中接受证书只会添加一个<code>SSL例外</code>：防止Safari对此站点做出的警告提示。实际上并不会将证书安装到iOS中，以成为可信任的证书。同台设备的其它程序在连接该站点时仍然会失败。</li>
	<li>一旦将<code>SSL例外</code>添加到iOS 7中了，就无法从iOS 7中移除。在之前的版本还可以通过Settings-&gt;Safari，选中”Clear Cookies and Data”进行删除。在iOS 7中这好像没有效果。———除非<code>General &gt; Reset &gt; Reset Settings</code>。</li>
</ol>
当然，苹果官方也提供了一个工具<a href="http://support.apple.com/downloads/#iphone%20configuration%20utility">iPhone configuration utility for Mac and PC</a>，通过该工具可以把证书安装至设备中。如果邮件不可用，或者要批量安装的话，这是一个好方法。
<h2>像安装iOS的Configuration Profile一样安装自签名证书</h2>
要想把SSL证书在iOS设备上安装为可信任的，可以通过发邮件到设备上，并将证书以附件的形式带在邮件中：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/04.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/04.png" /></a></p>

<p>选择邮件中的附件，以将证书安装至iOS设备中。选择附件之后，选择<code>Install</code>来安装证书。完成安装之后，再在Safari或者其它iOS应用中使用该证书时，就不会有相关提醒了。</p>

<p>并且这与Safari添加的<code>SSL例外</code>有一个很大的区别，你可以在任意时刻通过<code>Settings-&gt;General-&gt;Profiles</code>来查看相关证书，如果有必要的话，还可以将其移除：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/05.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/05.png" /></a></p>

<p>当然，苹果也提供了一个工具<a href="http://support.apple.com/downloads/#iphone%20configuration%20utility">iPhone configuration utility for Mac and PC</a>，通过该工具可以把证书安装到设备中，如果邮件不可用，或者要批量安装证书的话，可以用这个工具。
<h2>不要用IIS创建自签名证书</h2>
在IIS中创建自签名证书非常的简单。只需要选择菜单中的<code>Create Self-Signed Certificate</code>即可：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/06.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/06.png" /></a></p>

<p>不过IIS简单的使用计算机名称当做证书的主机名：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/07.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/07.png" /></a></p>

<p>大多数时候，计算机名称与主机名是不匹配的，这样的话自签名的证书永远都不会受信任——即使已经安装至iOS设备中：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/08.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/08.png" /></a></p>

<p>要修复这个问题可以安装并运行IIS 6 Toolkit中的SelfSSL。不过，要是使用OpenSSL则非常简单，下面我们就来看看吧。
<h2>利用OpenSSL创建自签名证书</h2>
创建自签名证书最简单的一种方法就是使用<a href="http://www.openssl.org/related/binaries.html">OpenSSL命令行工具</a>，这个工具在许多平台上面都可以使用，并且在Mac OSX上面是默认安装好了的。</p>

<p>首先，创建一个私钥文件：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1</pre>
</td>
<td>
<pre><code>openssl genrsa -out myselfsigned.key 2048</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>然后创建自签名证书：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1
2</pre>
</td>
<td>
<pre><code>openssl req -new -x509 -key myselfsigned.key -out myselfsigned.cer -days 365
-subj /CN=www.mysite.com</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>上面的命令中，关于私钥和证书(cer)的文件名可以是任意的。其中<code>CN</code>参数需要设置为主机名(例如<a href="https://www.mysite.com/">https://www.mysite.com</a>)。而<code>days</code>参数则指定证书从创建开始的有效天数。</p>

<p>在Apache服务器上面可以直接使用私钥和证书文件(做相关的SSL配置即可)。在IIS中需要一个PFX文件，通过该文件，可以将证书导入至IIS的Server Certificates中。当然通过OpenSSL可以创建PFX文件：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1
2</pre>
</td>
<td>
<pre><code>openssl pkcs12 -export -out myselfsigned.pfx -inkey myselfsigned.key
-in myselfsigned.cer</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>
<h2>创建自己的证书颁发机构(CA)</h2>
使用自签名证书会有这样的问题：需要为每台设备中用到的每个证书设置相关的信任关系。有一个解决办法就是创建自己的证书颁发机构(CA)根证书，然后基于该根证书创建别的证书。</p>

<p>这样一来就是自己扮演着CA，取代了商业性质的CA。这样做的好处就是自己的CA证书只需要在每台设备上安装一次即可。之后，设备会自动的信任基于CA根证书创建的证书。</p>

<p>创建CA证书只需要两个步骤即可，首先是创建私钥文件(跟之前的一样)：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1</pre>
</td>
<td>
<pre><code>openssl genrsa -out myCA.key 2048</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>然后是创建证书：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1
2</pre>
</td>
<td>
<pre><code>openssl req -x509 -new -key myCA.key -out myCA.cer -days 730
-subj /CN="My Custom CA"</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>上面创建的证书(myCA.key)可以公开发布出去，并安装在iOS或者其它OS上，以此当做内置的受信任根CA。自制的CA证书存储在<code>General-&gt;Settings-&gt;Profile</code>：</p>

<p><a title="" href="http://beyondvincent.com/images/2014/03/10.png" rel="gallery0"><img alt="" src="http://beyondvincent.com/images/2014/03/10.png" /></a></p>

<p>其中私钥文件(myCA.key)只用是再创建新的SSL证书时使用。</p>

<p>上面的CA创建好之后，我们可以基于该证书创建许多证书。注意，这里多了一个步骤：必须创建一个CSR(客户端证书请求文件)——就像购买商业的SSL证书一样。</p>

<p>首先需要创建一个私钥文件：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1</pre>
</td>
<td>
<pre><code>openssl genrsa -out mycert1.key 2048</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>然后是创建CSR:</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1</pre>
</td>
<td>
<pre><code>openssl req -new -out mycert1.req -key mycert1.key -subj /CN=www2.mysite.com</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>接着用这个CSR创建证书：</p>

<p><figure>
<div>
<table>
<tbody>
<tr>
<td>
<pre>1
2</pre>
</td>
<td>
<pre><code>openssl x509 -req -in mycert1.req -out mycert1.cer -CAkey myCA.key
-CA myCA.cer -days 365 -CAcreateserial -CAserial serial</code></pre>
</td>
</tr>
</tbody>
</table>
</div>
</figure>这里创建的证书(mycert.cer)可以安装在一台web服务器上，并且已经安装了相关CA证书的iOS设备都可以访问该web服务器。</p>
