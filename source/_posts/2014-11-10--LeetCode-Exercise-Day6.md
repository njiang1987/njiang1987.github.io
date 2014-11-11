title: "[LeetCode]Exercise(Day6)"
categories:
  - 技术
date: 2014-11-10 23:06:48
tags: [LeetCode]
---
##Search a 2D Matrix
###问题描述
Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:

Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.
For example,

Consider the following matrix:
```
[
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
```
Given target = `3`, return `true`.
###解决方法
二分查找，先找对应序列，找到以后，再进行一次二分查找
```cpp
	bool searchMatrix(vector<vector<int> > &matrix, int target) {
        if (matrix.size() == 0) return false;
        
        int outside_low = 0;
        int outside_high = (int)matrix.size() - 1;
        
        // 先找确定大得list得位置，二分查找
        while (outside_low <= outside_high) {
            int outside_mid = (outside_low + outside_high) / 2;
            
            vector<int>& inside_vector = matrix[outside_mid];
            if (inside_vector.size() == 0) return false;
            
            int inside_count = (int)inside_vector.size();
            
            if (inside_vector[0] > target) {
                outside_high = outside_mid - 1;
                continue;
            }
            else if (inside_vector[inside_count - 1] < target){
                outside_low = outside_mid + 1;
                continue;
            }
            
            //确定了list得位置，再在这个list里面查找对应的值，二分查找
            int inside_low = 0;
            int inside_high = inside_count - 1;
            while (inside_low <= inside_high) {
                int inside_mid = (inside_low + inside_high) / 2;
                if (target == inside_vector[inside_mid]) {
                    return true;
                }
                else if(target < inside_vector[inside_mid]){
                    inside_high = inside_mid - 1;
                    continue;
                }
                else{
                    inside_low = inside_mid + 1;
                }
            }
            return false;
        }
        
        return false;
    }
```
##Merge k Sorted Lists
###问题描述
Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.
###解决方法
想了两种方案，第一种方案的时间复杂度为n*k*k(n代表每一个list里面element的数量，k代表list的数量),
方案一：先建立k大小的vector保存每个链表头结点指针，然后用快排，将head的指针排序，然后每次取第一个element，加到大得list里面，然后去此链表的下一个节点，插入到之前我们创建出来的vector里面-插入排序，效率比较低，在LeetCode里面会超时，代码如下：
```cpp
	// 对于创建的vector，进行快速排序
	void quickSortList(vector<ListNode*>& head_vector, int left, int right)
    {
        if (left >= right) return ;
        if (head_vector.size() == 0) return;
        
        int low = left;
        int high = right;
        int key = head_vector[low]->val;
        ListNode* keyNode = head_vector[low];
        
        while (low < high) {
            while (low < high && head_vector[high]->val >= key) high--;
            head_vector[low] = head_vector[high];
            while (low < high && head_vector[low]->val <= key) low++;
            head_vector[high] = head_vector[low];
        }
        head_vector[low] = keyNode;
        
        quickSortList(head_vector, left, low - 1);
        quickSortList(head_vector, low + 1, right);
    }
    
    ListNode *mergeKLists(vector<ListNode *> &lists)
    {
        ListNode* head = NULL;
        
        if (lists.size() == 0) return NULL;
        
        vector<ListNode*> head_list;
        int lNotNullListCount = 0;
        
        // 初始化pointer的vector，并记录list的数量
        for (auto iter = lists.begin(); iter != lists.end(); iter++) {
            if (*iter != NULL) {
                head_list.push_back(*iter);
                lNotNullListCount++;
            }
        }
        
        if (lNotNullListCount == 0) return NULL;
        
        // 对于此vector，进行快速排序
        quickSortList(head_list, 0, lNotNullListCount - 1);
        
        ListNode* pNode = NULL;
        while (lNotNullListCount > 1) {
        	// 每次取出vector的第一个节点插入到大得list里面
            if (head == NULL) {
                head = head_list[0];
                pNode = head;
            }
            else{
                pNode->next = head_list[0];
                pNode = pNode->next;
            }
            head_list[0] = NULL;
            
            //确定下一个节点指针
            ListNode* nextNode = pNode->next;
            
            // 如果下一个节点指针是空的，那么将剩余的往前移动1个位置
            if (nextNode == NULL) {
                lNotNullListCount--;
                for (int i = 0; i < lNotNullListCount; i++) {
                    head_list[i] = head_list[i+1];
                }
                head_list[lNotNullListCount] = NULL;
                continue;
            }
            
            // 否则，插入排序,顺便移动item pointer的位置
            int i = 0;
            for (; i < lNotNullListCount - 1; i++) {
                if (nextNode->val < head_list[i+1]->val) {
                    head_list[i] = nextNode;
                    break;
                }
                else{
                    head_list[i] = head_list[i+1];
                }
            }
            
            if (i == lNotNullListCount - 1) {
                head_list[i] = nextNode;
            }
        }
        
        // 最后合并
        if (pNode == NULL) {
            pNode = head_list[0];
            head = pNode;
        }
        else{
            pNode->next = head_list[0];
        }
        
        return head;
        
    }
```

方案二：进行两两合并，最终合并为一个list，时间复杂度为n*k*log(k)，代码如下，简洁了许多:
```cpp
	ListNode *mergeKLists2(vector<ListNode *> &lists)
    {
        if (lists.size() == 0) return NULL;
        
        ListNode* head = NULL;
        int lListCount = (int)lists.size();
        
        // 此函数用来合并两个链表，并返回头节点
        auto mergeTwoList = [&](ListNode* list1, ListNode* list2){
            if (list1 == NULL) return list2;
            if (list2 == NULL) return list1;
            
            ListNode* head = NULL;
            ListNode* pNode = NULL;
            
            while (list1 != NULL && list2 != NULL) {
                ListNode* nextNode = NULL;
                if (list1->val > list2->val) {
                    nextNode = list2;
                    list2 = list2->next;
                }
                else{
                    nextNode = list1;
                    list1 = list1->next;
                }
                
                if (head == NULL) {
                    head = nextNode;
                    pNode = nextNode;
                }
                else{
                    pNode->next = nextNode;
                    pNode = pNode->next;
                }
            }
            
            if (list1 != NULL) {
                pNode->next = list1;
            }
            else{
                pNode->next = list2;
            }
            
            return head;
        };
        
        // 当list的数量大于1的时候进行合并
        while (lListCount > 1) {
            
            int index = 0;
            int i = 0;
            // 两两合并
            for (; i < lListCount - 1; i += 2) {
                ListNode* tpHead = mergeTwoList(lists[i], lists[i+1]);
                lists[index++] = tpHead;
            }
            // 如果还剩余一个，将剩下的一个往前移动
            if (i == lListCount - 1) {
                lists[index] = lists[lListCount - 1];
            }
            
            // 标记list的数量
            if (lListCount % 2 == 0) {
                lListCount /= 2;
            }
            else{
                lListCount = lListCount / 2 + 1;
            }
        }
        //最后head指向头节点
        head = lists[0];
        
        return head;
    }
```