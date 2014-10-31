---
layout: post
title: "2009 Problem A. Alien Language1"
date: 2013-08-31 20:44:32 +0800
comments: true
categories: CodeJam
---
Problem

After years of study, scientists at Google Labs have discovered an alien language transmitted from a faraway planet. The alien language is very unique in that every word consists of exactly L lowercase letters. Also, there are exactly D words in this language.

Once the dictionary of all the words in the alien language was built, the next breakthrough was to discover that the aliens have been transmitting messages to Earth for the past decade. Unfortunately, these signals are weakened due to the distance between our two planets and some of the words may be misinterpreted. In order to help them decipher these messages, the scientists have asked you to devise an algorithm that will determine the number of possible interpretations for a given pattern.

A pattern consists of exactly L tokens. Each token is either a single lowercase letter (the scientists are very sure that this is the letter) or a group of unique lowercase letters surrounded by parenthesis ( and ). For example: (ab)d(dc) means the first letter is either a or b, the second letter is definitely d and the last letter is either d or c. Therefore, the pattern (ab)d(dc) can stand for either one of these 4 possibilities: add, adc, bdd, bdc.

Input

The first line of input contains 3 integers, L, D and N separated by a space. D lines follow, each containing one word of length L. These are the words that are known to exist in the alien language. N test cases then follow, each on its own line and each consisting of a pattern as described above. You may assume that all known words provided are unique.

Output

For each test case, output <br>
Case #X: K
where X is the test case number, starting from 1, and K indicates how many words in the alien language match the pattern.

Limits <br>
Small dataset <br>
1 ≤ L ≤ 10 <br>
1 ≤ D ≤ 25 <br>
1 ≤ N ≤ 10 <br>

Large dataset<br>
1 ≤ L ≤ 15 <br> 
1 ≤ D ≤ 5000 <br>
1 ≤ N ≤ 500 <br>

{% codeblock lang:c++ %}
// CodeJamPratice.cpp : Defines the entry point for the console application.
//
 
#include "stdafx.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
 
int _tmain(int argc, _TCHAR* argv[])
{
	freopen("../debug/A-large-practice.in", "r", stdin);
	freopen("../debug/A-large-practice.out", "w", stdout);
 
	string str;
	vector<string> words;
 
	int lenStr, numWord, numCase;
	scanf("%d %d %d", &lenStr, &numWord, &numCase);
	str.resize(lenStr);
	for(int i = 0; i < numWord; i++)
	{
		scanf("%s", &str[0]);
		words.push_back(str);
	}
 
	str.resize(500);
	for(int i = 0; i < numCase; i++)
	{
		scanf("%s", &str[0]);
		int dict[26][15] = {0};
		bool isInSet = false;
		int col = 0;
		for(int j = 0; j < str.length(); j++)
		{
			if(str[j] == '\0') break;
			if(str[j] == '(') {isInSet = true; continue;}
			if(str[j] == ')') {isInSet = false; col++; continue;}
			char c = str[j];
			dict[c - 'a'][col] = 1;
			if(!isInSet)
				col++;
		}
 
		int num = 0;
		for(int j = 0; j < numWord; j++)
		{
			bool isValid = true;
			string word = words[j];
			for(int k = 0; k < lenStr; k++)
			{
				char c = word[k];
				if(dict[c - 'a'][k] == 0)
					isValid = false;
			}
			if(isValid)
				num++;
		}
 
		printf("Case #%d: %d\n", i+1, num);
	}
 
	fclose(stdin);
	fclose(stdout);
	return 0;
}
{% endcodeblock %}