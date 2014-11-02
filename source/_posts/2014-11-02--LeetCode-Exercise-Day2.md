title: "[LeetCode]Exercise(Day2)"
categories:
  - 技术
date: 2014-11-02 10:20:43
tags: LeetCode
photos:
- /uploads/header/meinv.jpg
---
##Two Sum
###问题描述
Given an array of integers, find two numbers such that they add up to a specific target number.
The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.
You may assume that each input would have exactly one solution. Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
###解决方法
我们可以用一个hashmap来保存之前已经遍历的值，然后在便利到某个值的时候，可以先找与它匹配的值是否已经加到hashmap里面；如果有，返回此值，否则继续，知道遍历完整个数组。
```cpp
    vector<int> twoSum(vector<int> &num, int target)
    {
        unordered_map<int, int> mapping;
        vector<int> result;
        
        size_t size = num.size();
        for (int i = 0; i < size; i++) {
            int key = num[i];
            if (mapping[key] == 0) {
                mapping[key] = i+1;
            }
            
            // find the next one
            int other = target - key;
            if (mapping[other] != 0) {
                result.push_back(mapping[other]);
                result.push_back(i+1);
                break;
            }
        }
        
        return result;
    }
```
##3Sum
###问题描述
Given an array S of n integers, are there elements a,b,c in S such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.
Note:
• Elements in a triplet (a, b, c) must be in non-descending order. (ie, a ≤ b ≤ c) • Thesolutionsetmustnotcontainduplicatetriplets.
For example, given array S = {-1 0 1 2 -1 -4}.
A solution set is:
  (-1, 0, 1)
  (-1, -1, 2)
###解决方法
有2个方法可以解决，时间复杂度都是O(n^2);
方法1：利用2个函数的和的那个函数，先拿出一个值来，再确定另外2个值，
方法2：先排序再从外向内的查找第3个数。
```cpp
    void quickSort(vector<int>& num, int left, int right)
    {
        if (left >= right) return;
        
        // 1 partition
        int key = num[left];
        int l = left;
        int h = right;
        while(l < h){
            while(h > l && num[h] >= key) h--;
            num[l] = num[h];
            while(l < h && num[l] <= key) l++;
            num[h] = num[l];
        }
        num[l] = key;
        
        // quick left and right
        quickSort(num, left, l - 1);
        quickSort(num, l + 1, right);
    }
    
    // -1, 0, 1, 2, -1, -4
    vector<vector<int>> threeSum(vector<int>& num)
    {
        // 1. quick sort
        quickSort(num, 0, num.size() - 1);
        
        // 2. find the right value
        vector<vector<int>> result;
        
        int target = 0;
        int l = 0;
        int h = (int)num.size() - 1;
        while(h - l > 1){
            int key1 = num[l];
            int key2 = num[h];
            
            int key3 = target - key1 - key2;
            int index = -1;
            
            for(int i = l + 1; i < h; i++){
                if (num[i] == key3) {
                    index = i;
                    break;
                }
            }
            
            if(index != -1){
                vector<int> t;
                t.push_back(key1);
                t.push_back(key3);
                t.push_back(key2);
                result.push_back(t);
            }

            if (key3 >= 0) {
                do {l++;} while (num[l] == key1);
            }
            else if(key3 < 0){
                do {h--;} while (num[h] == key2);
            }
        }
        
        sort(result.begin(), result.end());
        result.erase(unique(result.begin(), result.end()), result.end());
        
        return result;
    }
```
###扩展阅读
STL Unique函数的作用是去除相邻重复元素
##Remove Element
###问题描述
Given an array and a value, remove all instances of that value in place and return the new length. The order of elements can be changed. It doesn’t matter what you leave beyond the new length.
###解决方法
```cpp
    int removeElement(int A[], int n, int elem)
    {
        int index = -1;
        for (int i = 0; i < n; i++) {
            if (A[i] != elem) {
                A[++index] = A[i];
            }
        }
        return index + 1;
    }
```
##Next Permutation
###问题描述
Implement next permutation, which rearranges numbers into the lexicographically next greater permu- tation of numbers.
If such arrangement is not possible, it must rearrange it as the lowest possible order (ie, sorted in ascend- ing order).
The replacement must be in-place, do not allocate extra memory.
Here are some examples. Inputs are in the left-hand column and its corresponding outputs are in the right-hand column.
  1,2,3 → 1,3,2
  3,2,1 → 1,2,3
  1,1,5 → 1,5,1
###解决方法
之前碰到过类似的题目，先从后面往前查找，第一个减小的数字，比如[1, 2, 3]，查找的时候因为3>2，所以就停下，进行替换，替换的时候需要找到2后面：大于2且最小的值；置换2和此数字之后，再降后面的数组进行排序（因为我们之前判定过了是递增的，从后往前方向，所以这边直接reverse就可以）。
```cpp
    template<class _Iter>
    bool next_permutation2(_Iter first, _Iter last)
    {
        const auto rfirst = reverse_iterator<_Iter>(last);
        const auto rlast = reverse_iterator<_Iter>(first);
        
        auto pivot = next(rfirst);
        
        while (pivot != rlast && *pivot > *(prev(pivot)))
            pivot++;
        
        if (pivot == rlast) {
            reverse(first, last);
            return false;
        }
        
        auto change = find_if(rfirst, pivot, bind1st(less<int>(), *pivot));
        swap(*change, *pivot);
        reverse(rfirst, pivot);
        return true;
    }
```
此程序是参考的其他人用STL编写的，其中用到了大量的STL操作，后续再做介绍。我自己实现了一个较难理解的程序，如下：
```cpp
    void quickSort(vector<int>& num, int left, int right)
    {
        if (left >= right) return;
        
        // 1 partition
        int key = num[left];
        int l = left;
        int h = right;
        while(l < h){
            while(h > l && num[h] >= key) h--;
            num[l] = num[h];
            while(l < h && num[l] <= key) l++;
            num[h] = num[l];
        }
        num[l] = key;
        
        // quick left and right
        quickSort(num, left, l - 1);
        quickSort(num, l + 1, right);
    }
    void nextPermutation(vector<int> &num)
    {
        //1. find the first lower num
        const int lCount = (int)num.size();
        int lChangeIndex = -1;
        for (int i = lCount - 1; i > 0; i--) {
            if (num[i-1] < num[i]) {
                lChangeIndex = i-1;
                break;
            }
        }
        
        // if the vec is like 3, 2, 1, reverse it automatically
        if (lChangeIndex == -1) {
            int l = 0;
            int h = lCount - 1;
            while (l < h) {
                int t = num[l];
                num[l] = num[h];
                num[h] = t;
                l++; h--;
            }
        }
        else{
            int lNextNum = INT_MAX;
            int lNextIndex = -1;
            for (int i = lChangeIndex + 1; i < lCount; i++) {
                if(num[i] > num[lChangeIndex] && num[i] < lNextNum){
                    lNextNum = num[i];
                    lNextIndex = i;
                }
            }
            int t = num[lChangeIndex];
            num[lChangeIndex] = num[lNextIndex];
            num[lNextIndex] = t;
            quickSort(num, lChangeIndex + 1, lCount - 1);
        }
    }
```
###扩展阅读
####reverse_iterator
对于left_null>1->2->3->4->right_null,这样一个有4个元素(1,2,3,4)的链表.
    1->2->3->4->尾
```cpp
list<int>iteraotr c1=intList.begin()      // *c1=1;
list<int>iteraotr c2=intList.end()         // *c2=right_null;
```

    尾<-1<-2<-3<-4
`iterator++`,则对于上边正向链表从左向右遍历
```cpp
*(--c2)=4;
for(c1=.begin(),c1!=.end();c1++)
       cout<<...1,2,3,4
list<int>reverse_iteraotr c1=intList.rbegin()      // *c1=4;   rbegin:相当于reverse_begin即反着看的头
list<int>reverse_iteraotr c1=intList.rend()         // *c1=left_null; rend相当于reverse_end即反着看的尾
```
`reverse_iterator++`,则对于上边正向链表从右向左遍历.
```cpp
*(--c2)=1;
for(c2=.rbegin();r2!=.rend();c2++)
```
相当于:4 3 2 1

####bind1st和bind2nd函数
`bind1st`和`bind2nd`函数用于将一个二元算子（binary functor，bf）转换成一元算子（unary functor，uf）。为了达到这个目的，它们需要两个参数：要转换的bf和一个值（v）。

值（v）是一个固定的参数。换言之，uf(x)等价于：

bf( x, v) – 当使用bind2nd时
bf( v, x) – 当使用bind1st时
bind1st和bind2nd函数在处理谓词时非常有用。它们使得二元谓词能够转换成一元谓词；这常用于将一个范围内的所有值与一个特定的值比较：
```cpp
std::vector< int> a;
// ……填充a
// 移除所有小于30的元素
a.erase( std::remove_if( a.begin(), a.end(),
    std::bind2nd( std::less< int>(), 30)), a.end());
```