---
layout: post
title: '[CodeJam]Problem B. Always Turn Left'
categories:
- CodeJam
tags: []
published: true
comments: true
---
<p><a href="http://code.google.com/codejam/contest/32003/dashboard#s=p1">http://code.google.com/codejam/contest/32003/dashboard#s=p1</a>
Problem</p>

<p>You find yourself standing outside of a perfect maze. A maze is defined as "perfect" if it meets the following conditions:</p>

<p>It is a rectangular grid of rooms, R rows by C columns.<br />
There are exactly two openings on the outside of the maze: the entrance and the exit. The entrance is always on the north wall, while the exit could be on any wall.<br />
There is exactly one path between any two rooms in the maze (that is, exactly one path that does not involve backtracking).<br />
You decide to solve the perfect maze using the "always turn left" algorithm, which states that you take the leftmost fork at every opportunity. If you hit a dead end, you turn right twice (180 degrees clockwise) and continue. (If you were to stick out your left arm and touch the wall while following this algorithm, you'd solve the maze without ever breaking contact with the wall.) Once you finish the maze, you decide to go the extra step and solve it again (still always turning left), but starting at the exit and finishing at the entrance.</p>

<p>The path you take through the maze can be described with three characters: 'W' means to walk forward into the next room, 'L' means to turn left (or counterclockwise) 90 degrees, and 'R' means to turn right (or clockwise) 90 degrees. You begin outside the maze, immediately adjacent to the entrance, facing the maze. You finish when you have stepped outside the maze through the exit. For example, if the entrance is on the north and the exit is on the west, your path through the following maze would be WRWWLWWLWWLWLWRRWRWWWRWWRWLW:</p>

<p>If the entrance and exit were reversed such that you began outside the west wall and finished out the north wall, your path would be WWRRWLWLWWLWWLWWRWWRWWLW. Given your two paths through the maze (entrance to exit and exit to entrance), your code should return a description of the maze.</p>

<p>Input</p>

<p>The first line of input gives the number of cases, N. N test cases follow. Each case is a line formatted as</p>

<p>entrance_to_exit exit_to_entrance<br />
All paths will be at least two characters long, consist only of the characters 'W', 'L', and 'R', and begin and end with 'W'.</p>

<p>Output</p>

<p>For each test case, output one line containing "Case #x:" by itself. The next R lines give a description of the R by C maze. There should be C characters in each line, representing which directions it is possible to walk from that room. Refer to the following legend:</p>

<p>Character  	Can walk north?  	Can walk south?  	Can walk west?  	Can walk east?  <br />
1	Yes	No	No	No<br />
2	No	Yes	No	No<br />
3	Yes	Yes	No	No<br />
4	No	No	Yes	No<br />
5	Yes	No	Yes	No<br />
6	No	Yes	Yes	No<br />
7	Yes	Yes	Yes	No<br />
8	No	No	No	Yes<br />
9	Yes	No	No	Yes<br />
a	No	Yes	No	Yes<br />
b	Yes	Yes	No	Yes<br />
c	No	No	Yes	Yes<br />
d	Yes	No	Yes	Yes<br />
e	No	Yes	Yes	Yes<br />
f	Yes	Yes	Yes	Yes<br />
Limits</p>

<p>1 ≤ N ≤ 100.</p>

<p>Small dataset</p>

<p>2 ≤ len(entrance_to_exit) ≤ 100,<br />
2 ≤ len(exit_to_entrance) ≤ 100.</p>

<p>Large dataset</p>

<p>2 ≤ len(entrance_to_exit) ≤ 10000,<br />
2 ≤ len(exit_to_entrance) ≤ 10000.</p>

<p><pre lang="cpp">// CodeJamPratice.cpp : Defines the entry point for the console application.
//</pre></p>

<p>#include "stdafx.h"<br />
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;</vector></string></sstream></iostream></fstream></p>

<p>struct Direction<br />
{
	int v;<br />
	int l;<br />
	int r;<br />
	int b;<br />
public:<br />
	Direction(int lv, int ll, int lr, int lb): v(lv), l(ll), r(lr), b(lb){}<br />
};</p>

<p>const Direction east((1 << 3), 1, (1 << 1), (1 << 2));<br />
const Direction west((1 << 2), (1 << 1), 1, (1 << 3));<br />
const Direction south((1 << 1), (1 << 3), (1 << 2), 1);<br />
const Direction north(1, (1 << 2), (1 << 3), (1 << 1));</p>

<p>static Direction cur = south;</p>

<p>int _tmain(int argc, _TCHAR* argv[])<br />
{
	freopen("../debug/B-large-practice.in", "r", stdin);<br />
	freopen("../debug/B-large-practice.out", "w", stdout);</p>

<p>	int numCase;<br />
	scanf("%d", &numCase);<br />
	for(int c = 0; c < numCase; c++)<br />
	{<br />
		char entrance_to_exit[10001] = {0};<br />
		char exit_to_entrance[10001] = {0};<br />
		scanf("%s %s", entrance_to_exit, exit_to_entrance);<br />
		cur = south;<br />
		int lmap[200][400] = {0};<br />
		int left = 200, right = 200, bottom = 0;<br />
		int row = -1, col = 200;<br />
		int i = 0;<br />
		while(entrance_to_exit[i] != '\0')<br />
		{<br />
			char t = entrance_to_exit[i];<br />
			switch(t)<br />
			{<br />
				case 'W': <br />
					{<br />
						lmap[row][col] |= cur.v;<br />
						if(entrance_to_exit[i+1] == 0) break;<br />
						if(cur.v == east.v) {<br />
							col++; <br />
							if(col > right) right = col;<br />
						}else if(cur.v == west.v){<br />
							col--;<br />
							if(col < left) left = col;<br />
						}else if(cur.v == south.v){<br />
							row++;<br />
							if(row > bottom) bottom = row;<br />
						}else{<br />
							row--;<br />
						}<br />
						lmap[row][col] |= cur.b;<br />
						break;<br />
					}<br />
				case 'L': <br />
					{<br />
						switch(cur.l){<br />
							case 1: cur = north; break;<br />
							case (1 << 1): cur = south; break;<br />
							case (1 << 2): cur = west; break;<br />
							case (1 << 3): cur = east; break;<br />
							default: break;<br />
						}<br />
						break;<br />
					}<br />
				case 'R': <br />
					{<br />
						if(entrance_to_exit[i+1] == 'R'){<br />
							switch(cur.b){<br />
								case 1: cur = north; break;<br />
								case (1 << 1): cur = south; break;<br />
								case (1 << 2): cur = west; break;<br />
								case (1 << 3): cur = east; break;<br />
								default: break;<br />
							}<br />
							i++;<br />
						}else{<br />
							switch(cur.r){<br />
								case 1: cur = north; break;<br />
								case (1 << 1): cur = south; break;<br />
								case (1 << 2): cur = west; break;<br />
								case (1 << 3): cur = east; break;<br />
								default: break;<br />
							}<br />
						}<br />
						break;<br />
					}<br />
				default: break;<br />
			}<br />
			i++;<br />
		}</p>

<p>		i = 0;<br />
		if(cur.v == east.v) {<br />
			col++; <br />
		}else if(cur.v == west.v){<br />
			col--;<br />
		}else if(cur.v == south.v){<br />
			row++;<br />
		}else{<br />
			row--;<br />
		}</p>

<p>		switch(cur.b){<br />
			case 1: cur = north; break;<br />
			case (1 << 1): cur = south; break;<br />
			case (1 << 2): cur = west; break;<br />
			case (1 << 3): cur = east; break;<br />
			default: break;<br />
		}</p>

<p>		while(exit_to_entrance[i] != '\0')<br />
		{<br />
			char t = exit_to_entrance[i];<br />
			switch(t)<br />
			{<br />
				case 'W': <br />
					{<br />
						lmap[row][col] |= cur.v;<br />
						if(exit_to_entrance[i+1] == 0) break;<br />
						if(cur.v == east.v) {<br />
							col++; <br />
							if(col > right) right = col;<br />
						}else if(cur.v == west.v){<br />
							col--;<br />
							if(col < left) left = col;<br />
						}else if(cur.v == south.v){<br />
							row++;<br />
							if(row > bottom) bottom = row;<br />
						}else{<br />
							row--;<br />
						}<br />
						lmap[row][col] |= cur.b;<br />
						break;<br />
					}<br />
				case 'L': <br />
					{<br />
						switch(cur.l){<br />
							case 1: cur = north; break;<br />
							case (1 << 1): cur = south; break;<br />
							case (1 << 2): cur = west; break;<br />
							case (1 << 3): cur = east; break;<br />
							default: break;<br />
						}<br />
						break;<br />
					}<br />
				case 'R': <br />
					{<br />
						if(exit_to_entrance[i+1] == 'R'){<br />
							switch(cur.b){<br />
								case 1: cur = north; break;<br />
								case (1 << 1): cur = south; break;<br />
								case (1 << 2): cur = west; break;<br />
								case (1 << 3): cur = east; break;<br />
								default: break;<br />
							}<br />
							i++;<br />
						}else{<br />
							switch(cur.r){<br />
								case 1: cur = north; break;<br />
								case (1 << 1): cur = south; break;<br />
								case (1 << 2): cur = west; break;<br />
								case (1 << 3): cur = east; break;<br />
								default: break;<br />
							}<br />
						}<br />
						break;<br />
					}<br />
				default: break;<br />
			}<br />
			i++;<br />
		}</p>

<p>		printf("Case #%d:\n", c+1);<br />
		for(i = 0; i <= bottom; i++)<br />
		{<br />
			for(int j = left; j <= right; j++)<br />
			{<br />
				printf("%x", lmap[i][j]);<br />
			}<br />
			printf("\n");<br />
		}<br />
	}</p>

<p>	fclose(stdin);<br />
	fclose(stdout);<br />
	return 0;<br />
}</p>
