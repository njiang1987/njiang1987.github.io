---
layout: post
title: '[转]短URL生成转换'
categories:
- 技术
tags: [Other]
published: true
comments: true
---
<p>主要逻辑：</p>

<p>1, 确定一个包括大小写字母、数据的字符串LS，长度为 L = 26+26+10 = 62</p>

<p>2, 初始化L**N个整数，并作为一个序列push到redis里</p>

<p>3, 当需要转换一个长URL时，先从以上的序列中随机pop出一个整数I</p>

<p>4, 对整数I取模（除数为L)，余数对应到LS的一个字母，取完模后再除以L取整，当结果等于0时停止除模，否则结果继续取模。</p>

<p>5, 将所有余数对应的字母按顺序排列得到一个简短的字符串SS</p>

<p>6, 将长URL的md5哈希值作为KEY，将字符串SS作为VALUE，写入redis</p>

<p>7, 将字符串SS作为KEY, 将长URL作为VALUE，写入redis</p>

<p>8, 将前缀(短url域名)加上字符串SS，作为短URL结果返回</p>

<p>9, 当用户使用短url访问时，将短URL中的字符串SS取出，并作为KEY从redis中取出长URL，跳转长URL</p>

<p>注意：</p>

<p>当redis中序列数字快使用完时，要及时增加（可以写个脚本随时监控，数量少于10%时就自动增加数量），切忌不能存已经用过的数字</p>

<p><pre lang="Python" colla="+">
#encoding=utf-8  
import string  
import redis  
import hashlib  
  
LETTERS = string.digits + string.ascii_letters  
LETTERS_NUM = len(LETTERS)  
COUNTER_KEY = 'url:counter'  
  
def init(rd,num):  
    for i in xrange(LETTERS_NUM * num):  
        rd.sadd('url:id:set',i)  
  
#通过urlid取得短url对应的字符串  
def get_url(urlid):  
        result = []  
        q = urlid/LETTERS_NUM  
        r = urlid%LETTERS_NUM  
        result.append(LETTERS[r])  
        while q:  
            r = q%LETTERS_NUM  
            q = q/LETTERS_NUM  
            result = [LETTERS[r]] + result  
        return ''.join(result)  
  
#得到短url字符串  
def parse_url(rd, longurl):  
    ret = longurl  
    if (longurl.startswith("http://") or longurl.startswith("https://")) and len(longurl)>7:   
        m = hashlib.md5()  
        m.update(longurl)  
        urlkey = m.digest()  
        old_param = rd.get(urlkey)  
        if old_param:                   
            ret = old_param  
        else:  
            urlid = int(rd.spop('url:id:set'))  
            param = get_url(urlid)  
            rd.incr(COUNTER_KEY, 1)  
            rd.set(param,longurl)  
            rd.set(urlkey,param)  
            ret = param      
    print "short url:",ret  
    return ret  
  
if __name__ == "__main__":  
    url = "http://www.google.com/"  
    rd = redis.Redis('127.0.0.1',6379,db=0)  
    init(rd,3)  
    parse_url(rd,url) 
</pre>
[转自]：<a href="http://sls0919.iteye.com/blog/1774239">http://sls0919.iteye.com/blog/1774239</a></p>
