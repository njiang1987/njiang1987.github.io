title: "[LeetCode]Exercise(Day7)"
categories:
  - 技术
date: 2014-11-22 18:57:32
tags: [LeetCode]
photos:
- /uploads/header/meinv.jpg
---
##Wildcard Matching
###问题描述
Implement wildcard pattern matching with support for '?' and '*'.
```
'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

The function prototype should be:
bool isMatch(const char *s, const char *p)

Some examples:
isMatch("aa","a") → false
isMatch("aa","aa") → true
isMatch("aaa","aa") → false
isMatch("aa", "*") → true
isMatch("aa", "a*") → true
isMatch("ab", "?*") → true
isMatch("aab", "c*a*b") → false
```
###解决方法
开始想着用动态规划，但是没有想到点子上，不知道怎么下手，这里借用戴方勤的解题思路：主要是在匹配‘*’，p每遇到一个‘*’，就保留住当前‘*’的坐标和s的坐标，然后s从前往后扫描，如果不成功，则s++，重新扫描。
```cpp
	bool isMatch(const char *s, const char *p) {
        bool star = false;
        const char *str, *ptr;
        for (str = s, ptr = p; *str != '\0'; str++, ptr++) {
            switch (*ptr) {
                case '?':
                    break;
                case '*':
                	//标记，前面有‘*’出现
                    star = true;
                    //将s，p置到新的位置上面
                    s = str, p = ptr;
                    while (*p == '*') p++;
                    //如果p，后面只有'*',直接返回true
                    if (*p == '\0') return true;
                    //否则将str，ptr置到s，p的初始位置
                    str = s - 1;
                    ptr = p - 1;
                    break;
                default:
                	//如果当前两个字母不相同
                    if (*str != *ptr) {
                    	//如果前面没有‘*’出现，那么直接返回false
                        if (!star) return false;
                        //否则，将s++，移到下个字母上面，p回到初始位置，再进行比较
                        s++;
                        str = s - 1;
                        ptr = p - 1;
                    }
                    break;
            }
        }
        while (*ptr == '*') ptr++;
        return (*ptr == '\0');
    }
```
##Scramble String
###问题描述
Given a string s1, we may represent it as a binary tree by partitioning it to two non-empty substrings recursively.

Below is one possible representation of s1 = `"great"`:
```
    great
   /    \
  gr    eat
 / \    /  \
g   r  e   at
           / \
          a   t
```
To scramble the string, we may choose any non-leaf node and swap its two children.

For example, if we choose the node `"gr"` and swap its two children, it produces a scrambled string `"rgeat"`.
```
    rgeat
   /    \
  rg    eat
 / \    /  \
r   g  e   at
           / \
          a   t
```
We say that `"rgeat"` is a scrambled string of `"great"`.

Similarly, if we continue to swap the children of nodes `"eat"` and `"at"`, it produces a scrambled string `"rgtae"`.
```
    rgtae
   /    \
  rg    tae
 / \    /  \
r   g  ta  e
       / \
      t   a
```
We say that `"rgtae"` is a scrambled string of `"great"`.

Given two strings s1 and s2 of the same length, determine if s2 is a scrambled string of s1.
###解决方法

```cpp
	bool isScramble2(string s1, string s2) {
        if (s1.length() != s2.length()) return false;
        if (s1.length() == 0) return true;
        
        const int N = (int)s1.length();
        
        bool f[N+1][N][N];
        fill_n(&f[0][0][0], (N+1)*(N)*(N), false);
        
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                f[1][i][j] = s1[i] == s2[j];
            }
        }
        //由于此题，递归的话，会重复调用低阶的比对，比如1个字母的比较，调用2^n，所以此处用动态规划
        for (int n = 1; n <= N; n++) {
            for (int i = 0; i + n <= N; i++) {
                for (int j = 0; j + n <= N; j++) {
                    for(int k = 1; k < n; k++){
                    	//分两种情况来处理，s2的话要拆分成2种情况来处理
                        if ((f[k][i][j] && f[n-k][i+k][j+k]) || (f[k][i][j + n - k] && f[n-k][i+k][j])) {
                            f[n][i][j] = true;
                        }
                    }
                }
            }
        }
        
        
        return f[N][0][0];
    }
```
自己写了个巨慢的方法：
```cpp
	bool isScramble(string s1, string s2) {
        if (s1.length() != s2.length()) return false;
        if (s1.length() == 0 && s2.length() == 0) return true;
        
        const int n = (int)s1.length();
        if (n == 1) {
            return s1 == s2;
        }
        
        if (s1 == s2) {
            return true;
        }
        
        //就用的递归
        for (int i = 1; i < n; i++) {
            string sub1_first = s1.substr(0, i);
            string sub1_last = s1.substr(i);
            
            string sub2_first = s2.substr(0, i);
            string sub2_last = s2.substr(i);
            
            bool is_scramble = isScramble(sub1_first, sub2_first) && isScramble(sub1_last, sub2_last);
            
            if (is_scramble) {
                return true;
            }
            
            sub2_first = s2.substr(0, n - i);
            sub2_last = s2.substr(n - i);

            is_scramble = isScramble(sub1_first, sub2_last) && isScramble(sub1_last, sub2_first);
            
            if (is_scramble) {
                return true;
            }
        }
        
        return false;
    }
```