---
layout: post
title: "Problem B. Always Turn Left"
date: 2013-08-31 10:40:14 +0800
categories:
- 技术
tags: [CodeJam]
comments: true
---
Problem

You find yourself standing outside of a perfect maze. A maze is defined as “perfect” if it meets the following conditions:

It is a rectangular grid of rooms, R rows by C columns.
There are exactly two openings on the outside of the maze: the entrance and the exit. The entrance is always on the north wall, while the exit could be on any wall.
There is exactly one path between any two rooms in the maze (that is, exactly one path that does not involve backtracking).
You decide to solve the perfect maze using the “always turn left” algorithm, which states that you take the leftmost fork at every opportunity. If you hit a dead end, you turn right twice (180 degrees clockwise) and continue. (If you were to stick out your left arm and touch the wall while following this algorithm, you’d solve the maze without ever breaking contact with the wall.) Once you finish the maze, you decide to go the extra step and solve it again (still always turning left), but starting at the exit and finishing at the entrance.

The path you take through the maze can be described with three characters: ‘W’ means to walk forward into the next room, ‘L’ means to turn left (or counterclockwise) 90 degrees, and ‘R’ means to turn right (or clockwise) 90 degrees. You begin outside the maze, immediately adjacent to the entrance, facing the maze. You finish when you have stepped outside the maze through the exit. For example, if the entrance is on the north and the exit is on the west, your path through the following maze would be WRWWLWWLWWLWLWRRWRWWWRWWRWLW:

If the entrance and exit were reversed such that you began outside the west wall and finished out the north wall, your path would be WWRRWLWLWWLWWLWWRWWRWWLW. Given your two paths through the maze (entrance to exit and exit to entrance), your code should return a description of the maze.

Input

The first line of input gives the number of cases, N. N test cases follow. Each case is a line formatted as

entrance_to_exit exit_to_entrance
All paths will be at least two characters long, consist only of the characters ‘W’, ‘L’, and ‘R’, and begin and end with ‘W’.

Output

For each test case, output one line containing “Case #x:” by itself. The next R lines give a description of the R by C maze. There should be C characters in each line, representing which directions it is possible to walk from that room. Refer to the following legend:

Character Can walk north? Can walk south? Can walk west? Can walk east? <br>
1	Yes	No	No	No <br>
2	No	Yes	No	No <br>
3	Yes	Yes	No	No <br>
4	No	No	Yes	No <br>
5	Yes	No	Yes	No <br>
6	No	Yes	Yes	No <br>
7	Yes	Yes	Yes	No <br>
8	No	No	No	Yes <br>
9	Yes	No	No	Yes <br>
a	No	Yes	No	Yes <br>
b	Yes	Yes	No	Yes <br>
c	No	No	Yes	Yes <br>
d	Yes	No	Yes	Yes <br>
e	No	Yes	Yes	Yes <br>
f	Yes	Yes	Yes	Yes <br>

Limits
1 ≤ N ≤ 100.

Small dataset  <br>
2 ≤ len(entrance_to_exit) ≤ 100,
2 ≤ len(exit_to_entrance) ≤ 100.

Large dataset  <br>
2 ≤ len(entrance_to_exit) ≤ 10000,
2 ≤ len(exit_to_entrance) ≤ 10000.

{% codeblock lang:objc %}
// CodeJamPratice.cpp : Defines the entry point for the console application.
//
 
#include "stdafx.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
 
struct Direction
{
	int v;
	int l;
	int r;
	int b;
public:
	Direction(int lv, int ll, int lr, int lb): v(lv), l(ll), r(lr), b(lb){}
};
 
const Direction east((1 << 3), 1, (1 << 1), (1 << 2));
const Direction west((1 << 2), (1 << 1), 1, (1 << 3));
const Direction south((1 << 1), (1 << 3), (1 << 2), 1);
const Direction north(1, (1 << 2), (1 << 3), (1 << 1));
 
static Direction cur = south;
 
int _tmain(int argc, _TCHAR* argv[])
{
	freopen("../debug/B-large-practice.in", "r", stdin);
	freopen("../debug/B-large-practice.out", "w", stdout);
 
	int numCase;
	scanf("%d", &numCase);
	for(int c = 0; c < numCase; c++)
	{
		char entrance_to_exit[10001] = {0};
		char exit_to_entrance[10001] = {0};
		scanf("%s %s", entrance_to_exit, exit_to_entrance);
		cur = south;
		int lmap[200][400] = {0};
		int left = 200, right = 200, bottom = 0;
		int row = -1, col = 200;
		int i = 0;
		while(entrance_to_exit[i] != '\0')
		{
			char t = entrance_to_exit[i];
			switch(t)
			{
				case 'W': 
					{
						lmap[row][col] |= cur.v;
						if(entrance_to_exit[i+1] == 0) break;
						if(cur.v == east.v) {
							col++; 
							if(col > right) right = col;
						}else if(cur.v == west.v){
							col--;
							if(col < left) left = col;
						}else if(cur.v == south.v){
							row++;
							if(row > bottom) bottom = row;
						}else{
							row--;
						}
						lmap[row][col] |= cur.b;
						break;
					}
				case 'L': 
					{
						switch(cur.l){
							case 1: cur = north; break;
							case (1 << 1): cur = south; break;
							case (1 << 2): cur = west; break;
							case (1 << 3): cur = east; break;
							default: break;
						}
						break;
					}
				case 'R': 
					{
						if(entrance_to_exit[i+1] == 'R'){
							switch(cur.b){
								case 1: cur = north; break;
								case (1 << 1): cur = south; break;
								case (1 << 2): cur = west; break;
								case (1 << 3): cur = east; break;
								default: break;
							}
							i++;
						}else{
							switch(cur.r){
								case 1: cur = north; break;
								case (1 << 1): cur = south; break;
								case (1 << 2): cur = west; break;
								case (1 << 3): cur = east; break;
								default: break;
							}
						}
						break;
					}
				default: break;
			}
			i++;
		}
 
		i = 0;
		if(cur.v == east.v) {
			col++; 
		}else if(cur.v == west.v){
			col--;
		}else if(cur.v == south.v){
			row++;
		}else{
			row--;
		}
 
		switch(cur.b){
			case 1: cur = north; break;
			case (1 << 1): cur = south; break;
			case (1 << 2): cur = west; break;
			case (1 << 3): cur = east; break;
			default: break;
		}
 
 
		while(exit_to_entrance[i] != '\0')
		{
			char t = exit_to_entrance[i];
			switch(t)
			{
				case 'W': 
					{
						lmap[row][col] |= cur.v;
						if(exit_to_entrance[i+1] == 0) break;
						if(cur.v == east.v) {
							col++; 
							if(col > right) right = col;
						}else if(cur.v == west.v){
							col--;
							if(col < left) left = col;
						}else if(cur.v == south.v){
							row++;
							if(row > bottom) bottom = row;
						}else{
							row--;
						}
						lmap[row][col] |= cur.b;
						break;
					}
				case 'L': 
					{
						switch(cur.l){
							case 1: cur = north; break;
							case (1 << 1): cur = south; break;
							case (1 << 2): cur = west; break;
							case (1 << 3): cur = east; break;
							default: break;
						}
						break;
					}
				case 'R': 
					{
						if(exit_to_entrance[i+1] == 'R'){
							switch(cur.b){
								case 1: cur = north; break;
								case (1 << 1): cur = south; break;
								case (1 << 2): cur = west; break;
								case (1 << 3): cur = east; break;
								default: break;
							}
							i++;
						}else{
							switch(cur.r){
								case 1: cur = north; break;
								case (1 << 1): cur = south; break;
								case (1 << 2): cur = west; break;
								case (1 << 3): cur = east; break;
								default: break;
							}
						}
						break;
					}
				default: break;
			}
			i++;
		}
 
 
		printf("Case #%d:\n", c+1);
		for(i = 0; i <= bottom; i++)
		{
			for(int j = left; j <= right; j++)
			{
				printf("%x", lmap[i][j]);
			}
			printf("\n");
		}
	}
 
 
	fclose(stdin);
	fclose(stdout);
	return 0;
}
{% endcodeblock %}