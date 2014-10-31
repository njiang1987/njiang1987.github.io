---
layout: post
title: '[CodeJam]Problem A. Alien Numbers'
categories:
- CodeJam
tags: []
published: true
comments: true
---
<p><a title="http://code.google.com/codejam/contest/32003/dashboard" href="http://code.google.com/codejam/contest/32003/dashboard">http://code.google.com/codejam/contest/32003/dashboard</a></p>

<p>Problem</p>

<p>The decimal numeral system is composed of ten digits, which we represent as "0123456789" (the digits in a system are written from lowest to highest). Imagine you have discovered an alien numeral system composed of some number of digits, which may or may not be the same as those used in decimal. For example, if the alien numeral system were represented as "oF8", then the numbers one through ten would be (F, 8, Fo, FF, F8, 8o, 8F, 88, Foo, FoF). We would like to be able to work with numbers in arbitrary alien systems. More generally, we want to be able to convert an arbitrary number that's written in one alien system into a second alien system.</p>

<p>Input</p>

<p>The first line of input gives the number of cases, <b>N</b>. <b>N</b> test cases follow. Each case is a line formatted as
<pre>alien_number source_language target_language</pre>
Each language will be represented by a list of its digits, ordered from lowest to highest value. No digit will be repeated in any representation, all digits in the alien number will be present in the source language, and the first digit of the alien number will not be the lowest valued digit of the source language (in other words, the alien numbers have no leading zeroes). Each digit will either be a number 0-9, an uppercase or lowercase letter, or one of the following symbols <code>!"#$%&amp;'()*+,-./:;&lt;=&gt;?@[\]^_`{|}~</code></p>

<p>Output</p>

<p>For each test case, output one line containing "Case #<b>x</b>: " followed by the alien number translated from the source language to the target language.</p>

<p>Limits</p>

<p>1 ≤ <b>N</b> ≤ 100.</p>

<p>Small dataset</p>

<p>1 ≤ num digits in <b>alien_number</b> ≤ 4,<br />
2 ≤ num digits in <b>source_language</b> ≤ 16,<br />
2 ≤ num digits in <b>target_language</b> ≤ 16.</p>

<p>Large dataset</p>

<p>1 ≤ <b>alien_number</b> (in decimal) ≤ 1000000000,<br />
2 ≤ num digits in <b>source_language</b> ≤ 94,<br />
2 ≤ num digits in <b>target_language</b> ≤ 94.</p>

<p>Sample
<div>
<table>
<tbody>
<tr>
<td>Input</td>
<td>Output</td>
</tr>
<tr>
<td><code><code>4<br />
9 0123456789 oF8<br />
Foo oF8 0123456789<br />
13 0123456789abcdef 01<br />
CODE O!CDE? A?JM!.</code></code>&nbsp;</td>
<td><code>Case #1: Foo<br />
Case #2: 9<br />
Case #3: 10011<br />
Case #4: JAM!
</code></td>
</tr>
</tbody>
</table>
</div></p>

<p>这个题可以简单的理解为从一个n进制的数转换为m进制的数，n进制、m进制跟10进制的唯一区别就是所用的表达符号不一样了，其实转换的道理是一样的，如果上过计算机的课程应该都知道10进制、2进制、16进制相互转化的过程的，n进制数直接转m进制数不好转，我们可以先将n进制的奇怪符号转换成10进制，再将10进制转换成m进制的奇怪符号，就这样。以下是源程序，直接贴代码了，注视的化以后等有时间再加吧，累。。。。。。。。。。。。。。。。。。</p>

<p><pre lang="cpp">
//
//  main.cpp
//  CodeJamProject
//
//  Created by Jiang, Nan on 8/26/13.
//  Copyright (c) 2013 Jiang, Nan. All rights reserved.
//</pre></p>

<p>//#include <br />
#include <br />
#include
<map>
#include </map><br />
using namespace std;</p>

<p>int main(int argc, const char * argv[])<br />
{
    freopen("/Users/jiangnan/Develop/Code Jam/2008/CodeJamProject/CodeJamProject/A-large-practice.in.txt", "r", stdin);<br />
    freopen("/Users/jiangnan/Develop/Code Jam/2008/CodeJamProject/CodeJamProject/A-large-practice.out.txt", "w", stdout);</p>

<p>    int numCase;<br />
    scanf("%d", &amp;numCase);<br />
    for (int c = 0; c &lt; numCase; c++) {<br />
        char number[100] = {0};<br />
        char source[100] = {0};<br />
        char target[100] = {0};<br />
        scanf("%s %s %s", number, source, target);<br />
        int srcSize = 0, tarSize = 0;<br />
        map&lt;char, int&gt; srcmap;<br />
        map&lt;char, int&gt; tarmap;<br />
        int i = 0;<br />
        while (source[i] != '\0') {<br />
            srcmap[source[i]] = i;<br />
            i++;<br />
        }<br />
        srcSize = i;<br />
        i = 0;<br />
        while (target[i] != '\0') {<br />
            tarmap[target[i]] = i;<br />
            i++;<br />
        }<br />
        tarSize = i;<br />
        int decimal = 0;<br />
        i = 100;<br />
        while (number[i] == '\0') {<br />
            i--;<br />
        }<br />
        int k = 1;<br />
        while (i &gt; -1) {<br />
            decimal += k * srcmap[number[i]];<br />
            k *= srcSize;<br />
            i--;<br />
        }<br />
        i = 0;<br />
        char tarnum[100] = {0};<br />
        while (decimal != 0) {<br />
            int t = decimal % tarSize;<br />
            tarnum[i] = target[t];<br />
            decimal = (decimal - t) / tarSize;<br />
            i++;<br />
        }<br />
        int start = 0, end = i-1;<br />
        while (start &lt;= end) {<br />
            char t = tarnum[start];<br />
            tarnum[start] = tarnum[end];<br />
            tarnum[end] = t;<br />
            start++;<br />
            end--;<br />
        }</p>

<p>        printf("Case #%d: %s\n", c+1, tarnum);<br />
    }</p>

<p>    fclose(stdin);<br />
    fclose(stdout);<br />
    return 0;<br />
}
</p>
