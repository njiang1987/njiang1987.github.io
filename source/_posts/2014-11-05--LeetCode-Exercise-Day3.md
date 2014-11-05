title: "[LeetCode]Exercise(Day3)"
categories:
  - 技术
date: 2014-11-05 22:59:35
tags: [LeetCode]
---
##Permutation Sequence
###问题描述
The set [1,2,3,⋯,n] contains a total of n! unique permutations.
By listing and labeling all of the permutations in order, We get the following sequence (ie, for n = 3):
  "123"
  "132"
  "213"
  "231"
  "312"
  "321"
Given n and k, return the kth permutation sequence.<br> Note: Given n will be between 1 and 9 inclusive.
###解决方法
这个可以利用上一个问题里面的方法，暴力破解，逐个查找，直到第K个。
从别人的了解到还有康托编码的方法解决这个问题，
利用康托编码的思路,假设有n个不重复的元素,第k个排列是a1,a2,a3,...,an,那么a1 是 哪一个位置呢?
我们把 a1 去掉,那么剩下的排列为 a2, a3, ..., an, 共计 n − 1 个元素,n − 1 个元素共有 (n − 1)! 个排列,于是就可以知道 a1 = k/(n − 1)!。
同理,a2,a3,...,an 的值推导如下:

![](/uploads/2014/11/05/1.png "Title")

使用 next_permutation()
```cpp
// LeetCode, Permutation Sequence // 使用 next_permutation(),TLE class Solution {
public:
      string getPermutation(int n, int k) {
          string s(n, '0');
          for (int i = 0; i < n; ++i)
              s[i] += i+1;
          for (int i = 0; i < k-1; ++i)
              next_permutation(s.begin(), s.end());
          return s;
	}
      template<typename BidiIt>
      bool next_permutation(BidiIt first, BidiIt last) {
	// 代码见上一题 Next Permutation
    }
};
```

康托编码

```cpp
	template <class Sequence>
    Sequence kth_permutation(const Sequence& seq, int k)
    {
        const int n = (int)seq.size();
        Sequence S(seq);
        Sequence result;
        int base = factorial(n-1);
        --k;
        for (int i = n - 1; i > 0; k %= base, base /= i, i--) {
            auto a = next(S.begin(), k / base);
            result.push_back(*a);
            S.erase(a);
        }
        result.push_back(S[0]);
        return result;
    }
```

###扩展阅读
康托编码<br>
{1,2,3,4,...,n}表示1,2,3,...,n的排列如 {1,2,3} 按从小到大排列一共6个。123 132 213 231 312 321 。
代表的数字 1 2 3 4 5 6 也就是把10进制数与一个排列对应起来。
他们间的对应关系可由康托展开来找到。
如我想知道321是{1,2,3}中第几个小的数可以这样考虑 ：

第一位是3，当第一位的数小于3时，那排列数小于321 如 123、 213 ，小于3的数有1、2 。所以有2*2!个。再看小于第二位2的：小于2的数只有一个就是1 ，所以有1*1!=1 所以小于321的{1,2,3}排列数有2*2!+1*1!=5个。所以321是第6个小的数。 2*2!+1*1!+0*0!就是康托展开。

再举个例子：1324是{1,2,3,4}排列数中第几个大的数：第一位是1小于1的数没有，是0个 0*3! 第二位是3小于3的数有1和2，但1已经在第一位了，所以只有一个数2 1*2! 。第三位是2小于2的数是1，但1在第一位，所以有0个数 0*1! ，所以比1324小的排列有0*3!+1*2!+0*1!=2个，1324是第三个小数。


##Trapping Rain Water
###问题描述
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.

For example, Given [0,1,0,2,1,0,1,3,2,1,2,1], return 6.

![](/uploads/2014/11/05/2.png)

###解决方法
应该从没一个数字去考虑，比如上面序列第2个0的位置，也就是第3个数字，可以查找它两边最高的，然后取两者之间的最小值，减去自己的高度，这个差值就是当前位置的储水量，即`min(max_left, max_right) - height`。问题来了，怎么找到它的左右两边的最大值，遍历一遍，可以找到。以下参考网上的解决方法。

1. 从左往右扫描一遍,对于每个柱子,求取左边最大值;
2. 从右往左扫描一遍,对于每个柱子,求最大右值;
3. 再扫描一遍,把每个柱子的面积并累加。

```cpp
	int trap(int A[], int n)
    {
        int* max_left = new int(n);
        int* max_right = new int(n);

        for (int i = 1; i < n; i++) {
            max_left[i] = max(max_left[i-1], A[i]);
            max_right[n - i - 1] = max(max_right[n - i], A[n - i - 1]);
        }

        int result = 0;
        for (int i = 0; i < n; i++) {
            int heigh = min(max_left[i], max_right[i]) - i;
            if (heigh > 0) {
                result = heigh;
            }
        }

        delete [] max_left;
        delete [] max_right;
        return result;
    }
```

还有一种解决方法，就是用栈来保存峰值信息。小于的话，直接压栈，只要比top的大或相等，就出栈。

```cpp
	static int trap2(int A[], int n)
    {
        stack<Pair<int, int>> lpStack;

        int water = 0;
        for (int i = 0; i < n; i++) {
            int height = 0;

            while (!lpStack.empty()) {
                int bar = lpStack.top().first();
                int pos = lpStack.top().second();

                water += (min(bar, A[i]) - height) * (i - pos - 1);
                height = bar;

                if (bar > A[i]) {
                    break;
                }
                else{
                    lpStack.pop();
                }
            }

            lpStack.push(Pair<int, int>(A[i], i));
        }

        return water;
    }
```

##Rotate Image
###问题描述
You are given an n × n 2D matrix representing an image. Rotate the image by 90 degrees (clockwise).
Follow up: Could you do this in-place?
###解决方法
首先想到,纯模拟,从外到内一圈一圈的转,但这个方法太慢。
  如下图,首先沿着副对角线翻转一次,然后沿着水平中线翻转一次。
![](/uploads/2014/11/05/3.png)

```cpp
	void rotate(vector<vector<int>>& matrix)
    {
        const int n = (int)matrix.size();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i; j++) {
                swap(matrix[i][j], matrix[n - j - 1][n - i - 1]);
            }
        }

        for (int i = 0; i < n / 2; i++) {
            for (int j = 0; j < n; j++) {
                swap(matrix[i][j], matrix[n - i - 1][j]);
            }
        }
    }
```