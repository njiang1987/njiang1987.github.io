---
layout: post
title: '[CodeJam]Qualification Round 2008 Problem A. Saving the Universe'
categories:
- 技术
tags: [CodeJam]
published: true
comments: true
---
<p><a title="http://code.google.com/codejam/contest/32013/dashboard#s=p0&amp;a=0" href="http://code.google.com/codejam/contest/32013/dashboard#s=p0&amp;a=0">http://code.google.com/codejam/contest/32013/dashboard#s=p0&amp;a=0</a></p>

<p>Problem</p>

<p>The urban legend goes that if you go to the Google homepage and search for "Google", the universe will implode. We have a secret to share... It is true! Please don't try it, or tell anyone. All right, maybe not. We are just kidding.</p>

<p>The same is not true for a universe far far away. In that universe, if you search on any search engine for that search engine's name, the universe does implode!</p>

<p>To combat this, people came up with an interesting solution. All queries are pooled together. They are passed to a central system that decides which query goes to which search engine. The central system sends a series of queries to one search engine, and can switch to another at any time. Queries must be processed in the order they're received. The central system must never send a query to a search engine whose name matches the query. In order to reduce costs, the number of switches should be minimized.</p>

<p>Your task is to tell us how many times the central system will have to switch between search engines, assuming that we program it optimally.</p>

<p>Input</p>

<p>The first line of the input file contains the number of cases, <b>N</b>. <b>N</b> test cases follow.</p>

<p>Each case starts with the number <b>S</b> -- the number of search engines. The next <b>S</b> lines each contain the name of a search engine. Each search engine name is no more than one hundred characters long and contains only uppercase letters, lowercase letters, spaces, and numbers. There will not be two search engines with the same name.</p>

<p>The following line contains a number <b>Q</b> -- the number of incoming queries. The next <b>Q</b>lines will each contain a query. Each query will be the name of a search engine in the case.</p>

<p>Output</p>

<p>For each input case, you should output:
<pre>Case #<b>X</b>: <b>Y</b></pre>
where <b>X</b> is the number of the test case and <b>Y</b> is the number of search engine switches. Do not count the initial choice of a search engine as a switch.</p>

<p>&nbsp;</p>

<p>Limits</p>

<p>0 &lt; <b>N</b> ≤ 20</p>

<p>Small dataset</p>

<p>2 ≤ <b>S</b> ≤ 10</p>

<p>0 ≤ <b>Q</b> ≤ 100</p>

<p>Large dataset</p>

<p>2 ≤ <b>S</b> ≤ 100</p>

<p>0 ≤ <b>Q</b> ≤ 1000</p>

<p>Sample
<div>
<table>
<tbody>
<tr>
<td>
Input</td>
<td>
Output</td>
</tr>
<tr>
<td><code>2<br />
5
Yeehaw<br />
NSM<br />
Dont Ask<br />
B9<br />
Googol<br />
10<br />
Yeehaw<br />
Yeehaw<br />
Googol<br />
B9<br />
Googol<br />
NSM<br />
B9<br />
NSM<br />
Dont Ask<br />
Googol<br />
5
Yeehaw<br />
NSM<br />
Dont Ask<br />
B9<br />
Googol<br />
7
Googol<br />
Dont Ask<br />
NSM<br />
NSM<br />
Yeehaw<br />
Yeehaw<br />
Googol</code></td></tr></tbody></table></div></p>

<p>
<td><code>Case #1: 1<br />
Case #2: 0</code></td></p>

<p>




In the first case, one possible solution is to start by using Dont Ask, and switch to NSM after query number 8.<br />
For the second case, you can use B9, and not need to make any switches.</p>

<p><strong>[Analysis]</strong>
The first task in the new Google Code Jam is about, no surprise, search engines, and also, the grandiose feat of saving the universe in a parsimonious way. However, putting all the fancies aside, the problem itself is easy.</p>

<p>List all queries one by one, and break them up into segments. Each segment will be an interval where we use one search engine, and when we cross from one segment to another we will switch the search engine we use. What can you say about each segment? Well, one thing for sure is:</p>

<p>Never ever ever have all S different search engines appear as queries in one segment. (*)<br />
Why is this? Because if all S names appeared in one segment, then any search engine used for that segment will encounter at least one query that is the same as its name, thus exploding the universe!<br />
Working in the opposite direction, (*) is all we need to achieve; as long as you can partition the list of queries into such segments, it corresponds to a plan of saving the universe. You don't even care about which engine is used for one segment; any engine not appearing as a query on that segment will do. However, you might sometimes pick the same engine for two consecutive segments, laughing at yourself when you realize it; why don't I just join the two segments into one? Because your task is to use as few segments as possible, it is obvious that you want to make each segment as long as possible.</p>

<p>This leads to the greedy solution: Starting from the first query, add one query at a time to the current segment until the names of all S search engines have been encountered. Then we continue this process in a new segment until all queries are processed.</p>

<p>Sample code in C++, where st is the set of queries in the current segment, q is the next query, and count is the number of switches.</p>

<p>st.clear();<br />
count = 0;<br />
for (int i=0; i&lt;Q; i++) {<br />
getline(cin, q);<br />
if (st.find(q) == st.end()) {<br />
if (st.size() == S-1) {<br />
st.clear();<br />
count++;<br />
}
st.insert(q);<br />
}
}<br />
If st is a hashset, you expect the solution run in O(n) time. Note that this solution uses the fact that each query will be a search engine name and so we can ignore the list of names provided in the input.<br />
Let us justify that the greedy approach always gives the optimal answer. Think of the procedure as Q steps, and we want to show that, for each i, there is (at least) one optimal choice which agrees with us on the first i steps. We do this inductively for i = 0, then i = 1, and so on. The proposition for i = Q when proven true will imply that our algorithm is correct.</p>

<p>So, the key points in the inductive step i:<br />
If adding the next query will explode the universe, we must start a new segment. Any optimal choice agrees with us for the first (i-1) steps must also do that.<br />
If adding the next query will not explode the universe, we do not start a new segment. We know there is an optimal solution R agreed with us for (i-1) steps. Even if in R a new segment is started at step i, we can modify it a little bit. Let R' be the plan that agrees with R, but instead of starting a new segment on the i-th step, we delay this to the (i+1)st. It is clear that R' will also make the universe safe, and has no more switches than R does. So, R' is also an optimal solution, and agrees with our choice for the first i steps.<br />
The similar lines of justifications work for many greedy algorithms, including the well beloved minimum spanning trees.
<pre lang="cpp">// CodeJamPratice.cpp : Defines the entry point for the console application.
//</pre></p>

<p>#include "stdafx.h"<br />
#include <br />
#include <br />
#include <br />
#include <br />
#include <br />
#include <br />
using namespace std;</p>

<p>int _tmain(int argc, _TCHAR* argv[])<br />
{
	freopen("../debug/A-large-practice.in", "r", stdin);<br />
	freopen("../debug/A-large-practice.out", "w", stdout);</p>

<p>	int numCase;<br />
	scanf("%d", &amp;numCase);<br />
	for(int c = 0; c &lt; numCase; c++)<br />
	{<br />
		int engineCount = 0;<br />
		scanf("%d", &amp;engineCount);</p>

<p>		vector engines;</p>

<p>		char tmp[100] = {0};<br />
		gets(tmp);<br />
		for(int i = 0; i &lt; engineCount; i++)<br />
		{<br />
			gets(tmp);<br />
			string str = string(tmp);<br />
			engines.push_back(str);<br />
		}</p>

<p>		vector st;<br />
		int count = 0;<br />
		int queueSize = 0;<br />
		scanf("%d", &amp;queueSize);<br />
		gets(tmp);<br />
		for(int i = 0; i &lt; queueSize; i++)<br />
		{<br />
			char tmp[100] = {0};<br />
			gets(tmp);<br />
			string str = string(tmp);<br />
			vector::iterator iter = st.begin();</p>

<p>			bool found = false;<br />
			for(; iter != st.end(); iter++)<br />
			{<br />
				if(iter-&gt;compare(str) == 0)<br />
					found = true;<br />
			}</p>

<p>			if(found == false)<br />
			{<br />
				if(st.size() == engineCount - 1)<br />
				{<br />
					st.clear();<br />
					count++;<br />
				}<br />
				st.push_back(str);<br />
			}<br />
		}</p>

<p>		printf("Case #%d: %d\n", c+1, count);<br />
	}</p>

<p>	fclose(stdin);<br />
	fclose(stdout);<br />
	return 0;<br />
}</p>
