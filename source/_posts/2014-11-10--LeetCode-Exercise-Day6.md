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