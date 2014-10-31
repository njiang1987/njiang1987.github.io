---
layout: post
title: '[CodeJam]2009Problem A. Alien Language1'
categories:
- CodeJam
tags: []
published: true
comments: true
---
<p><a href="http://code.google.com/codejam/contest/90101/dashboard" title="2009 Qualification Round">2009 Qualification Round</a>
Problem</p>

<p>After years of study, scientists at Google Labs have discovered an alien language transmitted from a faraway planet. The alien language is very unique in that every word consists of exactly L lowercase letters. Also, there are exactly D words in this language.</p>

<p>Once the dictionary of all the words in the alien language was built, the next breakthrough was to discover that the aliens have been transmitting messages to Earth for the past decade. Unfortunately, these signals are weakened due to the distance between our two planets and some of the words may be misinterpreted. In order to help them decipher these messages, the scientists have asked you to devise an algorithm that will determine the number of possible interpretations for a given pattern.</p>

<p>A pattern consists of exactly L tokens. Each token is either a single lowercase letter (the scientists are very sure that this is the letter) or a group of unique lowercase letters surrounded by parenthesis ( and ). For example: (ab)d(dc) means the first letter is either a or b, the second letter is definitely d and the last letter is either d or c. Therefore, the pattern (ab)d(dc) can stand for either one of these 4 possibilities: add, adc, bdd, bdc.</p>

<p>Input</p>

<p>The first line of input contains 3 integers, L, D and N separated by a space. D lines follow, each containing one word of length L. These are the words that are known to exist in the alien language. N test cases then follow, each on its own line and each consisting of a pattern as described above. You may assume that all known words provided are unique.</p>

<p>Output</p>

<p>For each test case, output</p>

<p>Case #X: K<br />
where X is the test case number, starting from 1, and K indicates how many words in the alien language match the pattern.</p>

<p>Limits</p>

<p>Small dataset</p>

<p>1 ≤ L ≤ 10<br />
1 ≤ D ≤ 25<br />
1 ≤ N ≤ 10<br />
Large dataset</p>

<p>1 ≤ L ≤ 15<br />
1 ≤ D ≤ 5000<br />
1 ≤ N ≤ 500</p>

<p><pre lang="cpp">// CodeJamPratice.cpp : Defines the entry point for the console application.
//</pre></p>

<p>#include "stdafx.h"<br />
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;</algorithm></vector></string></sstream></iostream></fstream></p>

<p>int _tmain(int argc, _TCHAR* argv[])<br />
{
	freopen("../debug/A-large-practice.in", "r", stdin);<br />
	freopen("../debug/A-large-practice.out", "w", stdout);</p>

<p>	string str;<br />
	vector<string> words;</string></p>

<p>	int lenStr, numWord, numCase;<br />
	scanf("%d %d %d", &lenStr, &numWord, &numCase);<br />
	str.resize(lenStr);<br />
	for(int i = 0; i < numWord; i++)<br />
	{<br />
		scanf("%s", &str[0]);<br />
		words.push_back(str);<br />
	}</p>

<p>	str.resize(500);<br />
	for(int i = 0; i < numCase; i++)<br />
	{<br />
		scanf("%s", &str[0]);<br />
		int dict[26][15] = {0};<br />
		bool isInSet = false;<br />
		int col = 0;<br />
		for(int j = 0; j < str.length(); j++)<br />
		{<br />
			if(str[j] == '\0') break;<br />
			if(str[j] == '(') {isInSet = true; continue;}<br />
			if(str[j] == ')') {isInSet = false; col++; continue;}<br />
			char c = str[j];<br />
			dict[c - 'a'][col] = 1;<br />
			if(!isInSet)<br />
				col++;<br />
		}</p>

<p>		int num = 0;<br />
		for(int j = 0; j < numWord; j++)<br />
		{<br />
			bool isValid = true;<br />
			string word = words[j];<br />
			for(int k = 0; k < lenStr; k++)<br />
			{<br />
				char c = word[k];<br />
				if(dict[c - 'a'][k] == 0)<br />
					isValid = false;<br />
			}<br />
			if(isValid)<br />
				num++;<br />
		}<br />
		<br />
		printf("Case #%d: %d\n", i+1, num);<br />
	}</p>

<p>	fclose(stdin);<br />
	fclose(stdout);<br />
	return 0;<br />
}</p>
