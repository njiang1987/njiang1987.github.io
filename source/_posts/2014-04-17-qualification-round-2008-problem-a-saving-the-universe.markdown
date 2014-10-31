---
layout: post
title: "Qualification Round 2008 Problem A. Saving The Universe"
date: 2013-10-17 23:57:39 +0800
comments: true
categories: CodeJam, C++
---
Problem

The urban legend goes that if you go to the Google homepage and search for “Google”, the universe will implode. We have a secret to share… It is true! Please don’t try it, or tell anyone. All right, maybe not. We are just kidding.

The same is not true for a universe far far away. In that universe, if you search on any search engine for that search engine’s name, the universe does implode!

To combat this, people came up with an interesting solution. All queries are pooled together. They are passed to a central system that decides which query goes to which search engine. The central system sends a series of queries to one search engine, and can switch to another at any time. Queries must be processed in the order they’re received. The central system must never send a query to a search engine whose name matches the query. In order to reduce costs, the number of switches should be minimized.

Your task is to tell us how many times the central system will have to switch between search engines, assuming that we program it optimally.

Input

The first line of the input file contains the number of cases, N. N test cases follow.

Each case starts with the number S – the number of search engines. The next S lines each contain the name of a search engine. Each search engine name is no more than one hundred characters long and contains only uppercase letters, lowercase letters, spaces, and numbers. There will not be two search engines with the same name.

The following line contains a number Q – the number of incoming queries. The next Qlines will each contain a query. Each query will be the name of a search engine in the case.

Output

For each input case, you should output:

Case #X: Y

where X is the number of the test case and Y is the number of search engine switches. Do not count the initial choice of a search engine as a switch.

 

Limits

0 < N ≤ 20

Small dataset

2 ≤ S ≤ 10

0 ≤ Q ≤ 100

Large dataset

2 ≤ S ≤ 100

0 ≤ Q ≤ 1000

Sample

input 	| output
:---: 	| :----:
2	  	|	 Case #1: 1
5		|	Case #2: 0
Yeehaw	|
NSM		|
Dont Ask	|
B9		|
Googol	|
10		|
Yeehaw	|
Yeehaw	|
Googol	|
B9		|
Googol	|
NSM		|
B9		|
NSM		|
Dont Ask	|
Googol	|
5		|
Yeehaw	|
NSM		|
Dont Ask	|
B9		|
Googol	|
7		|
Googol	|
Dont Ask	|
NSM		|
NSM		|
Yeehaw	|
Yeehaw	|
Googol	|

In the first case, one possible solution is to start by using Dont Ask, and switch to NSM after query number 8.
For the second case, you can use B9, and not need to make any switches.

[Analysis]
The first task in the new Google Code Jam is about, no surprise, search engines, and also, the grandiose feat of saving the universe in a parsimonious way. However, putting all the fancies aside, the problem itself is easy.

List all queries one by one, and break them up into segments. Each segment will be an interval where we use one search engine, and when we cross from one segment to another we will switch the search engine we use. What can you say about each segment? Well, one thing for sure is:

Never ever ever have all S different search engines appear as queries in one segment. (*)
Why is this? Because if all S names appeared in one segment, then any search engine used for that segment will encounter at least one query that is the same as its name, thus exploding the universe!
Working in the opposite direction, (*) is all we need to achieve; as long as you can partition the list of queries into such segments, it corresponds to a plan of saving the universe. You don’t even care about which engine is used for one segment; any engine not appearing as a query on that segment will do. However, you might sometimes pick the same engine for two consecutive segments, laughing at yourself when you realize it; why don’t I just join the two segments into one? Because your task is to use as few segments as possible, it is obvious that you want to make each segment as long as possible.

This leads to the greedy solution: Starting from the first query, add one query at a time to the current segment until the names of all S search engines have been encountered. Then we continue this process in a new segment until all queries are processed.

Sample code in C++, where st is the set of queries in the current segment, q is the next query, and count is the number of switches.

{% codeblock lang:objc %}
st.clear();
count = 0;
for (int i=0; i<Q; i++) {
	getline(cin, q);
	if (st.find(q) == st.end()) {
		if (st.size() == S-1) {
			st.clear();
			count++;
		}
		st.insert(q);
	}
}
{% endcodeblock %}
If st is a hashset, you expect the solution run in O(n) time. Note that this solution uses the fact that each query will be a search engine name and so we can ignore the list of names provided in the input.
Let us justify that the greedy approach always gives the optimal answer. Think of the procedure as Q steps, and we want to show that, for each i, there is (at least) one optimal choice which agrees with us on the first i steps. We do this inductively for i = 0, then i = 1, and so on. The proposition for i = Q when proven true will imply that our algorithm is correct.

So, the key points in the inductive step i:
If adding the next query will explode the universe, we must start a new segment. Any optimal choice agrees with us for the first (i-1) steps must also do that.
If adding the next query will not explode the universe, we do not start a new segment. We know there is an optimal solution R agreed with us for (i-1) steps. Even if in R a new segment is started at step i, we can modify it a little bit. Let R’ be the plan that agrees with R, but instead of starting a new segment on the i-th step, we delay this to the (i+1)st. It is clear that R’ will also make the universe safe, and has no more switches than R does. So, R’ is also an optimal solution, and agrees with our choice for the first i steps.
The similar lines of justifications work for many greedy algorithms, including the well beloved minimum spanning trees.

{% codeblock lang:cpp %}
// CodeJamPratice.cpp : Defines the entry point for the console application.
//
 
#include "stdafx.h"
#include 
#include 
#include 
#include 
#include 
#include 
using namespace std;
 
int _tmain(int argc, _TCHAR* argv[])
{
	freopen("../debug/A-large-practice.in", "r", stdin);
	freopen("../debug/A-large-practice.out", "w", stdout);
 
	int numCase;
	scanf("%d", &amp;numCase);
	for(int c = 0; c &lt; numCase; c++)
	{
		int engineCount = 0;
		scanf("%d", &amp;engineCount);
 
		vector engines;
 
		char tmp[100] = {0};
		gets(tmp);
		for(int i = 0; i &lt; engineCount; i++)
		{
			gets(tmp);
			string str = string(tmp);
			engines.push_back(str);
		}
 
		vector st;
		int count = 0;
		int queueSize = 0;
		scanf("%d", &amp;queueSize);
		gets(tmp);
		for(int i = 0; i &lt; queueSize; i++)
		{
			char tmp[100] = {0};
			gets(tmp);
			string str = string(tmp);
			vector::iterator iter = st.begin();
 
			bool found = false;
			for(; iter != st.end(); iter++)
			{
				if(iter-&gt;compare(str) == 0)
					found = true;
			}
 
			if(found == false)
			{
				if(st.size() == engineCount - 1)
				{
					st.clear();
					count++;
				}
				st.push_back(str);
			}
		}
 
		printf("Case #%d: %d\n", c+1, count);
	}
 
	fclose(stdin);
	fclose(stdout);
	return 0;
}
{% endcodeblock %}


