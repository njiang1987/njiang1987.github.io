title: "[LeetCode]Exercise(Day5)"
categories:
  - 技术
date: 2014-11-08 17:20:56
tags: [LeetCode]
photos:
- /uploads/header/maomi.jpg
---
##Reverse Linked List II
###问题描述
Reverse a linked list from position m to n. Do it in-place and in one-pass.

For example:
Given `1->2->3->4->5->NULL`, m = 2 and n = 4,

return `1->4->3->2->5->NULL`.

Note:
Given m, n satisfy the following condition:
1 ≤ m ≤ n ≤ length of list.
###解决方法
在遍历链表的时候，记录断点，以及reverse的链表的头和尾，等遍历完全，再将链表重新连接起来。
```cpp
	ListNode *reverseBetween(ListNode *head, int m, int n) {
        if (head == NULL || n < m) return head;
        
        int index = 1;
        ListNode* pNode = head;
        ListNode* partHead = NULL;
        ListNode* reverseHead = NULL;
        ListNode* reverseTail = NULL;
        while (pNode != NULL) {
            if (index < m) {
                partHead = pNode;
                pNode = pNode->next;
                index++;
            }
            else if (index >= m && index <= n) {
                ListNode* tp = pNode->next;
                pNode->next = reverseHead;
                reverseHead = pNode;
                if (reverseTail == NULL) {
                    reverseTail = pNode;
                }
                index++;
                pNode = tp;
            }
            else{
                break;
            }
        }
        
        if (partHead != NULL) {
            partHead->next = reverseHead;
        }
        if (reverseTail != NULL) {
            reverseTail->next = pNode;
        }
        
        if (m == 1) {
            return reverseHead;
        }
        else{
            return head;
        }
    }
```
##Largest Rectangle in Histogram
###问题描述
Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.
![](/uploads/2014/11/09/1.png)
Above is a histogram where width of each bar is 1, given height = `[2,1,5,6,2,3]`.
![](/uploads/2014/11/09/2.png)
The largest rectangle is shown in the shaded area, which has area = 10 unit.

For example,
Given height = `[2,1,5,6,2,3]`,
return `10`.
###解决方法
先贴一个最优解法，此方法由戴方勤提供。维护一个递增的栈，然后每次遍历，判断如果比栈顶得小，那么计算栈里面高于当前值区间的最大面积，然后再将此值压栈。代码如下：
```cpp
	int largestRectangleArea(vector<int> &height) {
        stack<int> s;
        height.push_back(0);
        int result = 0;
        for (int i = 0; i < height.size();) {
            if (s.empty() || height[i] > height[s.top()]) {
                s.push(i++);
            }
            else{
                int pos = s.top();
                s.pop();
                int span = s.empty() ? i : i - s.top() - 1;
                int area = height[pos] * span;
                result = max(result, area);
            }
        }
        return result;
    }
```

自己实现了个O(n2)的方法，在遍历到第i个直方，计算前面i-1个，总得面积，然后再跟当前最大值比较，
```cpp
	int largestRectangleArea(vector<int> &height) {
        if (height.size() == 0) return 0;
        
        int max = INT_MIN;
        int current_start = -1;
        int current_height = 0;
        int current_max = INT_MIN;
        
        for (int i = 0; i < height.size(); i++) {
            if (height[i] == 0) {
                current_start = -1;
                current_height = INT_MAX;
                current_max = INT_MIN;
                continue;
            }
            
            if (current_start == -1) {
                current_start = i;
            }
            
            current_height = INT_MAX;
            for (int j = i; j >= current_start; j--) {
                if (height[j] < current_height) {
                    current_height = height[j];
                }
                
                if ((i - j + 1) * current_height > current_max) {
                    current_max = (i - j + 1) * current_height;
                }
                
                if (current_max > max) {
                    max = current_max;
                }
            }
        }
        return max;
    }
```