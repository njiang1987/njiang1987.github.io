title: "[LeetCode]Exercise(Day4)"
categories:
  - 技术
date: 2014-11-06 23:37:13
tags: [LeetCode]
photos:
- /uploads/header/maomi.jpg
---
##Word Ladder
###问题描述
You are given a string, S, and a list of words, L, that are all Given two words (start and end), and a dictionary, find the length of shortest transformation sequence from start to end, such that:

Only one letter can be changed at a time
Each intermediate word must exist in the dictionary
For example,

Given:
start = `"hit"`
end = `"cog"`
dict = `["hot","dot","dog","lot","log"]`
As one shortest transformation is `"hit"` -> `"hot"` -> `"dot"` -> `"dog"` -> `"cog"`,
return its length `5`.

Note:

1. Return 0 if there is no such transformation sequence.
2. All words have the same length.
3. All words contain only lowercase alphabetic characters.

###解决方法
可以先将L中得元素，按照只改变一个字母的原则，简历一颗树，这样问题就简化为，广度优先遍历这棵树，然后找到root到leaf得最短长度。
```cpp
	int ladderLength(string start, string end, unordered_set<string> &dict) {
        queue<string> current, next;
        unordered_set<string> visited;

        auto isEqualToEndString = [&](const string& s){return s == end;};
        auto extendString = [&](const string& s){
            vector<string> result;

            const size_t length = s.length();
            for (int i = 0; i < length; i++) {
                string str(s);
                for (char c = 'a'; c <= 'z'; c++) {
                    if (c == str[i]) continue;

                    swap(c, str[i]);

                    if ((dict.count(str) || (str == end)) > 0 && visited.count(str) == 0) {
                        visited.insert(str);
                        result.push_back(str);
                    }

                    swap(c, str[i]);
                }
            }

            return result;
        };
        bool found = false;
        int level = 0;
        current.push(start);
        while (!current.empty() && !found) {
            ++level;
            while (!current.empty() && !found) {
                const string str = current.front();
                current.pop();

                const auto& extend = extendString(str);
                for(const auto& state : extend){
                    next.push(state);
                    if (isEqualToEndString(state)) {
                        found = true;
                        break;
                    }
                }
            }

            swap(current, next);
        }

        if (found) {
            return level + 1;
        }
        else{
            return 0;
        }
    }
```
##Substring with Concatenation of All Words
###问题描述
You are given a string, S, and a list of words, L, that are all of the same length. Find all starting indices of substring(s) in S that is a concatenation of each word in L exactly once and without any intervening characters.

For example, given:
S: `"barfoothefoobarman"`
L: `["foo", "bar"]`

You should return the indices: [0,9].(order does not matter).
###解决方法
由于我写的代码在另一台机器上，以下是戴方勤的代码，思想就是在`S`中逐个查找，如果是在`L`中得单词，就进入j的循环，查看后面catLength长度的字符串是不是都符合题目中得要求，在L中能找到。
```cpp
	vector<int> findSubstring(string s, vector<string>& dict) {
          size_t wordLength = dict.front().length();
          size_t catLength = wordLength * dict.size();
          vector<int> result;
          if (s.length() < catLength) return result;
          unordered_map<string, int> wordCount;
          for (auto const& word : dict) ++wordCount[word];
          for (auto i = begin(s); i <= prev(end(s), catLength); ++i) {
              unordered_map<string, int> unused(wordCount);
              for (auto j = i; j != next(i, catLength); j += wordLength) {
                  auto pos = unused.find(string(j, next(j, wordLength)));
                  if (pos == unused.end() || pos->second == 0) break;
                  if (--pos->second == 0) unused.erase(pos);
              }
              if (unused.size() == 0) result.push_back(distance(begin(s), i));
          }
          return result;
      }
```
##Path Sum II
###问题描述
Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.

For example:
Given the below binary tree and `sum = 22`,

```
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
```
return
```
[
   [5,4,11,2],
   [5,8,4,5]
]
```
###解决方法
这个题目，拿过来首先想到递归遍历，
```cpp
	vector<vector<int> > pathSum(TreeNode *root, int sum) {
        vector<vector<int>> result;
        if (root == 0) return result;
        
        int val = root->val;
        
        if ((val == sum) && (root->left == NULL) && (root->right == NULL)) {
            vector<int> t = {val};
            result.push_back(t);
            return result;
        }
        
        vector<vector<int>> leftPath = pathSum(root->left, sum - val);
        vector<vector<int>> rightPath = pathSum(root->right, sum - val);
        
        
        for (auto iter = leftPath.begin(); iter != leftPath.end(); iter++) {
            vector<int> tmp = *iter;
            tmp.insert(tmp.begin(), val);
            result.push_back(tmp);
        }
        for (auto iter = rightPath.begin(); iter != rightPath.end(); iter++) {
            vector<int> tmp = *iter;
            tmp.insert(tmp.begin(), val);
            result.push_back(tmp);
        }
        return result;
    }
```
##Binary Tree Preorder Traversal
###问题描述
Given a binary tree, return the preorder traversal of its nodes' values.

For example:
Given binary tree {1,#,2,3},
```
   1
    \
     2
    /
   3
```
return `[1,2,3]`.

Note: Recursive solution is trivial, could you do it iteratively?

###解决方法
戴的解法是：
```cpp
	vector<int> preorderTraversal(TreeNode *root) {
          vector<int> result;
          const TreeNode *p;
          stack<const TreeNode *> s;
          p = root;
          if (p != nullptr) s.push(p);
          while (!s.empty()) {
              p = s.top();
              s.pop();
              result.push_back(p->val);
              if (p->right != nullptr) s.push(p->right);
              if (p->left != nullptr) s.push(p->left);
          }
          return result;
      }
```
我的解法，有点复杂，
```cpp
	vector<int> preorderTraversal(TreeNode *root)
    {
        vector<int> result;
        if (root == NULL) return result;
        
        stack<TreeNode*> lpStack;
        unordered_map<TreeNode*, bool> visited;
        TreeNode* pNode = root;
        
        while (pNode != NULL) {
            
            if (!visited[pNode]) {
                lpStack.push(pNode);
                visited[pNode] = true;
                result.push_back(pNode->val);
            }
            
            if (pNode->left && !visited[pNode->left]) {
                pNode = pNode->left;
            }
            else if(pNode->right && !visited[pNode->right]){
                pNode = pNode->right;
            }
            else{
                if (lpStack.size() > 0) {
                    pNode = lpStack.top();
                    lpStack.pop();
                }
                else{
                    pNode = NULL;
                }
            }
        }
        
        return result;
    }
```

##Unique Paths
###问题描述
A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).

The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).

How many possible unique paths are there?
![](/uploads/2014/11/08/robot_maze.png)
Above is a 3 x 7 grid. How many possible unique paths are there?

Note: m and n will be at most 100.
###解决方法
利用动态规划，a[i][j] = a[i-1][j] + a[i][j-1],最后就可以得出a[m-1][n-1]的值。
```cpp
	int uniquePaths(int m, int n)
    {
        if (m <= 0 || n <= 0) return 0;
        if (m == 1 || n == 1) return 1;
        
        int* a = new int[m*n];
        a[0] = 1;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (j == 0 && i == 0) {
                    continue;
                }
                
                if (j == 0) {
                    a[i*n + j] = a[(i - 1)*n + j];
                }
                else if (i == 0){
                    a[i*n + j] = a[j - 1];
                }
                else{
                    a[i*n + j] = a[(i-1)*n + j] + a[i*n + j - 1];
                }
            }
        }
        return a[(m-1)*n + n-1];
    }
```
##Subsets
###问题描述
Given a set of distinct integers, S, return all possible subsets.

Note:
Elements in a subset must be in non-descending order.
The solution set must not contain duplicate subsets.
For example,
If S = [1,2,3], a solution is:
```
[
  [3],
  [1],
  [2],
  [1,2,3],
  [1,3],
  [2,3],
  [1,2],
  []
]
```
###解决方法
先对队列排序，完了用递归，
```cpp
	vector<vector<int> > subsets(vector<int> &S) {
        vector<vector<int>> result;
        if (S.size() == 0) {
            vector<int> empty;
            result.push_back(empty);
            return result;
        }
        
        sort(S.begin(), S.end());
        
        int val = S.front();
        S.erase(S.begin());
        vector<vector<int>> prevs = subsets(S);
        result = prevs;
        for (auto iter = prevs.begin(); iter != prevs.end(); iter++) {
            vector<int> tmp = *iter;
            tmp.insert(tmp.begin(), val);
            result.push_back(tmp);
        }
        return result;
    }
```