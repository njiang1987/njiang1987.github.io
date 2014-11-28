title: "[LeetCode]Exercise(Day8)"
categories:
  - 技术
date: 2014-11-24 17:47:56
tags: [LeetCode]
photos:
- /uploads/header/meinv.jpg
---
##Remove Duplicates from Sorted List
###问题描述
Given a sorted linked list, delete all duplicates such that each element appear only once.

For example,
Given `1->1->2`, return `1->2`.
Given `1->1->2->3->3`, return `1->2->3`.
###解决方法
方法很简单，直接上代码：
```cpp
	ListNode *deleteDuplicates(ListNode *head) {
        ListNode* result = head;
        
        ListNode* preNode = NULL;
        ListNode* curNode = head;
        
        while (curNode != NULL) {
            if (preNode == NULL) {
                preNode = curNode;
                curNode = curNode->next;
            }
            else{
                if (preNode->val == curNode->val) {
                    ListNode* tmp = curNode;
                    curNode = curNode->next;
                    delete tmp;
                    preNode->next = curNode;
                }
                else{
                    preNode = curNode;
                    curNode = curNode->next;
                }
            }
        }
        
        return result;
    }
```

##Pow(x, n)
###问题描述
Implement pow(x, n).
###解决方法
运用二分查找法进行分治，代码如下：
```cpp
	double pow2(double x, int n)
    {
        if (n < 0) return 1.0 / power(x, -n);
        else return power(x, n);
    }
    
    double power(double x, int n)
    {
        if (n == 0) return 1;
        double v = power(x, n / 2);
        if (n % 2 == 0) return v*v;
        else return v*v*x;
    }
```
之前写了一个比较笨得函数
```cpp
	double pow(double x, int n) {
        if(n == 0) return 1;
        if (x == 0) {
            if (n < 0) return -1;
            return 0;
        }
        if (x == 1) return 1;
        if (x == -1) {
            if (n % 2 == 0) return 1;
            else return -1;
        }
        
        int N = abs(n);
        double result = 1;
        for (int i = 0; i < N; i++) {
            if (n > 0) {
                result *= x;
            }
            else{
                result /= x;
            }
            
            if (fabs(result) < 0.000001) {
                result = 0;
                break;
            }
        }
        
        return result;
    }
```

##First Missing Positive
###问题描述
Given an unsorted integer array, find the first missing positive integer.

For example,
Given `[1,2,0]` return `3`,
and `[3,4,-1,1]` return `2`.

Your algorithm should run in O(n) time and uses constant space.
###解决方法
首先可以确定算法的时间复杂度需要O(n)，就需要O(n)的空间复杂度来实现，首先创建大小为n的数组，遍历数组，如果这个数大于0，就将他加到数组相应的位置，然后再遍历此数组查找第一个缺失的数字。
```cpp
	int firstMissingPositive(int A[], int n) {
        int record[n];
        for (int i = 0; i < n; i++) {
            record[i] = -1;
        }
        
        //记录大于0的值
        for (int i = 0; i < n; i++) {
            if (A[i] > 0 && A[i] <= n) {
                record[A[i] - 1] = A[i];
            }
        }
        
        //查找第一个缺失的大于0的数字
        int result = -1;
        for (int i = 0; i < n; i++) {
            if (record[i] == -1) {
                result = i+1;
                break;
            }
        }
        if (result == -1) {
            result = n+1;
        }
        
        return result;
    }
```
###扩展阅读
桶排序:
无序数组有个要求,就是成员隶属于固定(有限的)的区间,如范围为[0-9](考试分数为1-100等)

例如待排数字[6 2 4 1 5 9]

准备10个空桶,最大数个空桶

[6 2 4 1 5 9]           待排数组

[0 0 0 0 0 0 0 0 0 0]   空桶

[0 1 2 3 4 5 6 7 8 9]   桶编号(实际不存在)

1,顺序从待排数组中取出数字,首先6被取出,然后把6入6号桶,这个过程类似这样:空桶[ 待排数组[ 0 ] ] = 待排数组[ 0 ]

[6 2 4 1 5 9]           待排数组

[0 0 0 0 0 0 `6` 0 0 0]   空桶

[0 1 2 3 4 5 `6` 7 8 9]   桶编号(实际不存在)

2,顺序从待排数组中取出下一个数字,此时2被取出,将其放入2号桶,是几就放几号桶

[6 2 4 1 5 9]           待排数组

[0 0 `2` 0 0 0 6 0 0 0]   空桶

[0 1 `2` 3 4 5 6 7 8 9]   桶编号(实际不存在)

3,4,5,6省略,过程一样,全部入桶后变成下边这样

[6 2 4 1 5 9]           待排数组

[0 `1` `2` 0 `4` `5` `6` 0 0 `9`]   空桶

[0 `1` `2` 3 `4` `5` `6` 7 8 `9`]   桶编号(实际不存在)

0表示空桶,跳过,顺序取出即可:1 2 4 5 6 9

![](/uploads/2014/11/27/1.png)