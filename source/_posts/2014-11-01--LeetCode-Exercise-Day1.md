title: "[LeetCode]Exercise(Day1)"
date: 2014-11-01 15:34:59
categories: 技术
tags: LeetCode
---
##Remove Duplicates from Sorted Array
###问题描述
Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.
Do not allocate extra space for another array, you must do this in place with constant memory.
For example, Given input array A = [1,1,2],
Your function should return length = 2, and A is now [1,2].
###解决方案
```cpp
int removeDuplicates(int* A, int n)
{
    if (n == 0) return 0;
    
    int index = 0;
    for (int i = 1; i < n; i++) {
        if (A[index] != A[i]) {
            A[++index] = A[i];
        }
    }
    return index+1;
}
```
###扩展阅读
在编代码的时候看到了一种实现是
```cpp
// LeetCode, Remove Duplicates from Sorted Array 
// 使用 STL,时间复杂度 O(n),空间复杂度 O(1) class Solution {
public:
      int removeDuplicates(int A[], int n) {
          return removeDuplicates(A, A + n, A) - A;
        }
        
      template<typename InIt, typename OutIt>
      OutIt removeDuplicates(InIt first, InIt last, OutIt output) {
          while (first != last) {
              *output++ = *first;
              first = upper_bound(first, last, *first);
            }
          return output;
      }
};
```
在XCode上面编译会报错"Use of undeclared identifier 'upder_bound'"，顺便查了下`upper_bound`的用法；
```cpp
iterator lower_bound( const key_type &key ): //返回一个迭代器，指向键值>= key的第一个元素。
iterator upper_bound( const key_type &key )://返回一个迭代器，指向键值> key的第一个元素。
```
以下是测试用例
```cpp
        map<int, string>mapStudent;
        mapStudent[1]="student_one";
        mapStudent[3]="student_three";
        mapStudent[5]="student_five";
        map<int, string>::iterator iter;
        iter=mapStudent.lower_bound(2);
        {
            //返回的是下界3的迭代器
            cout<<iter->second<<endl;
        }
        iter=mapStudent.lower_bound(3);
        {
            //返回的是下界3的迭代器
            cout<<iter->second<<endl;
        }
        iter=mapStudent.upper_bound(2);
        {
            //返回的是上界3的迭代器
            cout<<iter->second<<endl;
        }
        iter=mapStudent.upper_bound(3);
        {
            //返回的是上界5的迭代器
            cout<<iter->second<<endl;
        }
```
输出结果为：
```
student_three
student_three
student_three
student_five
```
##Remove Duplicates from Sorted Array II
###问题描述
Follow up for ”Remove Duplicates”: What if duplicates are allowed at most twice? For example, Given sorted array A = [1,1,1,2,2,3],
Your function should return length = 5, and A is now [1,1,2,2,3]
###解决方案
```cpp
// LeetCode, Remove Duplicates from Sorted Array II // 时间复杂度 O(n),空间复杂度 O(1)
// @author hex108 (https://github.com/hex108) class Solution {
  public:
      int removeDuplicates(int A[], int n) {
          if (n <= 2) return n;
          int index = 2;
          for (int i = 2; i < n; i++){
              if (A[i] != A[index - 2])
                  A[index++] = A[i];
}
          return index;
      }
};
```
期间自己写了一个解决方法，太冗长，不好理解，贴出代码，已被以后反省。
```cpp
        int index = 0;
        int repeatCount = 0;
        for(int i = 1; i < n; i++)
        {
            if (A[index] == A[i]) {
                repeatCount++;
                if (repeatCount > 1) {
                    continue;
                }
                else{
                    A[++index] = A[i];
                }
            }
            else{
                repeatCount = 0;
                A[++index] = A[i];
            }
        }
        return index+1;
```

##Search in Rotated Sorted Array
###问题描述
Suppose a sorted array is rotated at some pivot unknown to you beforehand.
(i.e., 0 1 2 4 5 6 7 might become 4 5 6 7 0 1 2).
You are given a target value to search. If found in the array return its index, otherwise return -1. You may assume no duplicate exists in the array.
###解决方法
解决方法就是努力找到有顺序的一边，然后根据所要查找的数字进行二分查找。
```cpp
class Solution {
public:
    int search(int A[], int n, int target)
    {
        int low = 0;
        int high = n - 1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (target == A[mid]) {
                return mid;
            }
            else if (A[low] < A[mid]){
                if (A[low] <= target && target < A[mid]) {
                    high = mid - 1;
                }
                else{
                    low = mid + 1;
                }
            }
            else{
                if (target > A[mid] && target <= A[high])                 {
                    low = mid + 1;
                }
                else{
                    high = mid - 1;
                }
            }
        }
    }
```
之前写得另外一段程序，也列出来，以后进行比对，效率和理解性上不及上一个程序。
```cpp
    int search(int A[], int n, int target)
    {
        int low = 0;
        int high = n - 1;
        while (low <= high) {
            if (A[low] >= A[high]) {
                if (target > A[high] && target < A[low]) {
                    return -1;
                }
                
                int mid = (low + high) / 2;
                if (target == A[mid]) {
                    return mid;
                }
                else if (target < A[mid]){
                    if (target >= A[low]) {
                        high = mid - 1;
                    }
                    else{
                        low = mid + 1;
                    }
                }
                else if (target > A[mid]){
                    low = mid + 1;
                }
            }
            else{
                int mid = (low + high) / 2;
                if (target == A[mid]) {
                    return mid;
                }
                else if(target < A[mid]){
                    high = mid - 1;
                }
                else{
                    low = mid + 1;
                }
            }
        }
        
        return -1;
    }
```

##Longest Consecutive Sequence
###问题描述
Given an unsorted array of integers, find the length of the longest consecutive elements sequence.
For example, Given [100, 4, 200, 1, 3, 2], The longest consecutive elements sequence is [1, 2, 3, 4]. Return its length: 4.
Your algorithm should run in O(n) complexity.
###解决方法
看到时间复杂度要求O(n)，第一直觉就是要用数据结构来保存相应信息来索引，开始没想出来，后来看了提示，用HashMap来保存相应信息，当时想到的是算hash值以后，在存hash值的时候，再遍历以存储的数值，计算出最大的连续序列。开始方向错掉了，后来看了提示，取到某值，先看齐前面一个值是否存在，然后再更新后面的值，代码如下：
```cpp
// 100, 4, 200, 1, 3, 2
    int longestConsecutive(const vector<int> &num)
    {
        if (num.size() == 0) return 0;
        
        size_t count = num.size();
        int result = 0;
        unordered_map<int, int> lRecords;
        
        // update the map
        for (int i = 0; i < count; i++) {
            int key = num[i];
            int pre = key - 1;
            int length = lRecords[pre];
            lRecords[key] = ++length;
            
            // update next
            int next = key + 1;
            while (lRecords[next] != 0) {
                lRecords[next] = ++length;
                next++;
            }
            
            if (length > result) {
                result = length;
            }
        }  
        return result;
    }
```
因为这篇里面运用到了Boost的unordered_map,索性就百度了下unorderred_map和map的区别：
###扩展阅读
`boost::unordered_map`， 它与 `stl::map`的区别就是，`stl::map`是按照operator<比较判断元素是否相同，以及比较元素的大小，然后选择合适的位置插入到树中。所以，如果对map进行遍历（中序遍历）的话，输出的结果是有序的。顺序就是按照operator< 定义的大小排序。

而`boost::unordered_map`是计算元素的Hash值，根据Hash值判断元素是否相同。所以，对`unordered_map`进行遍历，结果是无序的。

用法的区别就是，stl::map 的key需要定义operator< 。 而`boost::unordered_map`需要定义`hash_value`函数并且重载`operator==`。对于内置类型，如string，这些都不用操心。对于自定义的类型做key，就需要自己重载operator< 或者`hash_value()`了。 