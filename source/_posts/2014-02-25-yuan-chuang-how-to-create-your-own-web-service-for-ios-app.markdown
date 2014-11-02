---
layout: post
title: '[原创] How to create your own web service for iOS App'
categories:
- 技术
tags: [iOS]
published: true
comments: true
---
<p><h1>1.References:</h1>
1.1. <a href="http://blog.csdn.net/xw13106209/article/details/7049614">Eclipse + webservice 开发实例</a>
1.2. <a href="http://blog.csdn.net/wwwang89123/article/details/8734528">iOS学习之-使用ASIHttpRequest调用WebService</a>
<h1>2. Steps：</h1>
<h2>2.1 Functions definition</h2>
Develop an web service to implement an calculator function: plus/minus/multiple/divide. And use ASIHTTPRequest to access the web service on iOS App.
<h2>2.2 Preparation</h2>
Download and install:</p>

<p>Eclipse (Mac OSX): <a href="http://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/kepler/SR1/eclipse-jee-kepler-SR1-macosx-cocoa-x86_64.tar.gz">http://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/kepler/SR1/eclipse-jee-kepler-SR1-macosx-cocoa-x86_64.tar.gz</a></p>

<p>Axis2: <a href="http://axis.apache.org/axis2/java/core/download.cgi">http://axis.apache.org/axis2/java/core/download.cgi</a>, after get download zip file, extract it. It will be like below.</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.03.27-PM.png"><img class="aligncenter size-medium wp-image-267" alt="Screen Shot 2014-02-25 at 8.03.27 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.03.27-PM-300x297.png" width="300" height="297" /></a></p>

<p>For more information about Axis2, please click <a href="http://zh.wikipedia.org/wiki/Apache_Axis2">here</a>.
<h2>2.3 Configuration</h2>
In eclipse, eclipse-&gt;Preference-&gt;Web Service-&gt;Axis2 Preference, set the "Axis2 runtime location" to the above axis2 extract folder.</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.05.05-PM.png"><img class="aligncenter size-medium wp-image-268" alt="Screen Shot 2014-02-25 at 8.05.05 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.05.05-PM-300x255.png" width="300" height="255" /></a> Then click "OK" button.
<h2>2.4 Develop Web Service:</h2>
<pre lang="java">package com.nj.webservice;</pre></p>

<p>/** <br />
 * 计算器运算 <br />
 * @author jiang, nan <br />
 */ <br />
public class CalculateService {<br />
	//加法  <br />
    public float plus(float x, float y) {  <br />
        return x + y;  <br />
    }  <br />
    //减法  <br />
    public float minus(float x, float y) {  <br />
        return x - y;  <br />
    }  <br />
    //乘法  <br />
    public float multiply(float x, float y) {  <br />
        return x * y;  <br />
    }  <br />
    //除法  <br />
    public float divide(float x, float y) {  <br />
        if(y!=0)  <br />
        {  <br />
            return x / y;  <br />
        }  <br />
        else  <br />
            return -1;  <br />
    }  <br />
}
(3). On the project "WebServiceTest", "new" -&gt; "other", find "Web Service"
<a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.20.35-PM.png"><img class="aligncenter size-medium wp-image-272" alt="Screen Shot 2014-02-25 at 8.20.35 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.20.35-PM-300x284.png" width="300" height="284" /></a> (4). click "next", click "Browse" in "Service implementation" and find "CalculateService".</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.23.11-PM.png"><img class="aligncenter size-medium wp-image-273" alt="Screen Shot 2014-02-25 at 8.23.11 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.23.11-PM-300x249.png" width="300" height="249" /></a> (5). In the Web Service dialog, set "Web Service type" to be "start service". "Client type" to be "no client" (we will use iOS app to access this web service later).</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.25.44-PM.png"><img class="aligncenter size-medium wp-image-275" alt="Screen Shot 2014-02-25 at 8.25.44 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.25.44-PM-234x300.png" width="234" height="300" /></a></p>

<p>&nbsp;</p>

<p>(6). Click "configuration" -&gt; "Service Deployment Configuration", here we will set the server to deploy the web service, I have download tomcat 7.0.4 previously.</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.27.53-PM.png"><img class="aligncenter size-medium wp-image-277" alt="Screen Shot 2014-02-25 at 8.27.53 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.27.53-PM-300x271.png" width="300" height="271" /></a> (7). click "OK", return Web Service dialog. And click "next"</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.29.51-PM.png"><img class="aligncenter size-medium wp-image-278" alt="Screen Shot 2014-02-25 at 8.29.51 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.29.51-PM-235x300.png" width="235" height="300" /></a></p>

<p>&nbsp;</p>

<p>(8). Click "next" until finish. After you start tomcat 7.0.4 server, you could open the URL:</p>

<p><a href="http://localhost:8080/WebServiceProject/services/CalculateService?wsdl">http://localhost:8080/WebServiceProject/services/CalculateService?wsdl</a></p>

<p>You will see the following web page.</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.32.30-PM.png"><img class="aligncenter size-medium wp-image-279" alt="Screen Shot 2014-02-25 at 8.32.30 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.32.30-PM-300x171.png" width="300" height="171" /></a></p>

<p>&nbsp;</p>

<p>Now you have setup your own web service using Axis2.
<h1>3. Set up your own iOS App.</h1>
<h2>3.1 Create an single view application.</h2>
<h2><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.34.55-PM.png"><img class="aligncenter size-medium wp-image-283" alt="Screen Shot 2014-02-25 at 8.34.55 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.34.55-PM-300x205.png" width="300" height="205" /></a> 3.2 Download ASIHTTPRequest and add it into our own Application.</h2>
(1). Download ASIHTTPRequest.</p>

<p><a href="http://github.com/pokeb/asi-http-request/tarball/master">http://github.com/pokeb/asi-http-request/tarball/master</a></p>

<p>(2). Add all the files under "ASIHTTPRequest\Classes" into our project.<br />
We should also add "ASIHTTPRequestExternal\Reachability" into our project.
<a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.39.37-PM.png"><img class="aligncenter size-medium wp-image-284" alt="Screen Shot 2014-02-25 at 8.39.37 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.39.37-PM-132x300.png" width="132" height="300" /></a></p>

<p>(3). Set project configuration.</p>

<p>Click Project-&gt;target-&gt;buildphases-&gt;Link Binary with Libraries,<br />
Click "+" to libz.dylib and libxml2.dylib
<a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.43.30-PM.png"><img class="aligncenter size-medium wp-image-285" alt="Screen Shot 2014-02-25 at 8.43.30 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.43.30-PM-300x121.png" width="300" height="121" /></a></p>

<p>&nbsp;</p>

<p>Click "Building Setting", find "Other Linker Flags" and add "-lxml2"</p>

<p><a href="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.43.40-PM.png"><img class="aligncenter size-medium wp-image-286" alt="Screen Shot 2014-02-25 at 8.43.40 PM" src="http://www.njiang.cn/wp-content/uploads/2014/02/Screen-Shot-2014-02-25-at-8.43.40-PM-300x39.png" width="300" height="39" /></a>
<h2>3.3 Learn SOAP request</h2>
POST /iwscooperationws/todocenter.asmx HTTP/1.1<br />
Host: 192.168.1.11<br />
Content-Type: text/xml; charset=utf-8<br />
Content-Length: length<br />
SOAPAction: "http://iws.CP.ws/GetWorkflowToDoCount"</p>

<p>&lt;?xml version="1.0" encoding="utf-8"?&gt;<br />
&lt;soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"&gt;<br />
&lt;soap:Body&gt;<br />
&lt;GetWorkflowToDoCount xmlns="http://iws.CP.ws/"&gt;<br />
&lt;UserName&gt;string&lt;/UserName&gt;<br />
&lt;/GetWorkflowToDoCount&gt;<br />
&lt;/soap:Body&gt;<br />
&lt;/soap:Envelope&gt;<br />
In this SOAP request, it defines a method - GetWorkflowToDoCount, its parameters is UserName (type is string).
<h2>3.4 Using ASIHTTPRequest to set request.</h2>
You could add the sending request function in the single view controller - touchesBegan:withEvent:</p>

<p>The code is like below. In the test code, I call multiply function with 2*5.</p>

<p>&nbsp;
<pre lang="OBJC">- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    /*
     POST /iwscooperationws/todocenter.asmx HTTP/1.1
     Host: 192.168.1.11
     Content-Type: text/xml; charset=utf-8
     Content-Length: length
     SOAPAction: "http://iws.CP.ws/GetWorkflowToDoCount"</pre></p>

<p>     <!--?xml version="1.0" encoding="utf-8"?--></p>

<p>     string</p>

<p>     */</p>

<p>    NSString* WebURL = @"http://localhost:8080/";<br />
    NSString* wsFile = @"WebServiceProject/services/CalculateService";<br />
    NSString* xmlNS = @"http://service.com/";<br />
    NSString* wsName = @"CalculateService";</p>

<p>    //1、初始化SOAP消息体<br />
    NSString * soapMsg = [[NSString alloc] initWithFormat:<br />
                               @"<!--?xml version=\"1.0\" encoding=\"utf-8\"?-->\n"<br />
                               "\n"<br />
                               "\n"<br />
                               "\n"<br />
                               "2\n"<br />
                               "5\n"<br />
                               "\n"<br />
                               "\n"<br />
                               ""];<br />
    NSURL * url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", WebURL, wsFile]];</p>

<p>    ASIHTTPRequest * theRequest = [ASIHTTPRequest requestWithURL:url];<br />
    NSString *msgLength = [NSString stringWithFormat:@"%d", [soapMsg length]];<br />
    [theRequest addRequestHeader:@"Content-Type" value:@"text/xml; charset=utf-8"];<br />
    [theRequest addRequestHeader:@"SOAPAction" value:[NSString stringWithFormat:@"%@%@", xmlNS, wsName]];<br />
    [theRequest addRequestHeader:@"Content-Length" value:msgLength];<br />
    [theRequest setRequestMethod:@"POST"];<br />
    [theRequest appendPostData:[soapMsg dataUsingEncoding:NSUTF8StringEncoding]];<br />
    [theRequest setDefaultResponseEncoding:NSUTF8StringEncoding];</p>

<p>    [theRequest setDelegate:self];<br />
    [theRequest startAsynchronous];</p>

<p>    [super touchesBegan:touches withEvent:event];<br />
}
The request string is</p>

<p>NSString * soapMsg = [[NSString alloc] initWithFormat:<br />
@"&lt;?xml version=\"1.0\" encoding=\"utf-8\"?&gt;\n"<br />
"&lt;soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" \n"<br />
"xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" \n"<br />
"xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"&gt;\n"<br />
"&lt;soap:Body&gt;\n"<br />
"&lt;multiply xmlns=\"http://webservice.nj.com\"&gt;\n"<br />
"&lt;x&gt;2&lt;/x&gt;\n"<br />
"&lt;y&gt;5&lt;/y&gt;\n"<br />
"&lt;/multiply&gt;\n"<br />
"&lt;/soap:Body&gt;\n"<br />
"&lt;/soap:Envelope&gt;"];
<h2>3.5 Add finished function "requestFinished" in the view controller</h2>
<pre lang="OBJC">- (void)requestFinished:(ASIHTTPRequest *)request
{
    NSString *responseString = [request responseString];
    NSLog(@"%@", responseString);
}</pre>
<h2>3.6 After run the app and tap on the view. Debug, the response string is</h2>
&lt;?xml version="1.0" encoding="utf-8"?&gt;<br />
&lt;soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;<br />
&lt;soapenv:Body&gt;<br />
&lt;multiplyResponse xmlns="http://webservice.nj.com"&gt;<br />
&lt;multiplyReturn&gt;10.0&lt;/multiplyReturn&gt;<br />
&lt;/multiplyResponse&gt;<br />
&lt;/soapenv:Body&gt;<br />
&lt;/soapenv:Envelope&gt;</p>

<p>You could see the result is 10.</p>
