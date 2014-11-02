---
layout: post
title: "[CTCI]-Homework Part 1"
date: 2014-08-20 20:21:26 +0800
comments: true
categories: 技术
tags: iOS
---

##1.1 Implement an algorithm to determine if a string has all unique characters. What if you cannot use additional data structures?

####Solution 1. Use hash table
```java
		String testStr = "abca";
		boolean lRepeatChar = false;// = repeatString(testStr);
		for(int i = 0; i < testStr.length(); i++)
		{
			String c = testStr.substring(i, i+1);
			if(lTest.containsKey(c))
			{
				lRepeatChar = true;
				break;
			}
			else
			{
				lTest.put(c, 1);
			}
		}
```

####Solution 2. Recursive
Not Recommend this one.
```java
	public static boolean repeatChar(char c, String substr)
	{	
		if(substr == null || substr.length() == 0)
			return false;
		
		char next = substr.charAt(0);
		if(next == c)
			return true;
		
		boolean lRepeatChar = repeatChar(c, substr.substring(1));
		if(lRepeatChar == true)
			return true;
		else
		{
			lRepeatChar = repeatChar(next, substr.substring(1));
		}
		
		return lRepeatChar;
	}
	
	public static boolean repeatString(String str)
	{
		if(str == null || str.length() == 0)
			return false;
		
		char c = str.charAt(0);
		String substr = str.substring(1);
		return repeatChar(c, substr);
	}
```

##1.2 Implement a function void reverse(char* str) in C or C++ which reverses a null- terminated string.

```c
void reverseString(char* str)
{
    int n = 0;
    // find the end of the char[].
    while (str[n] != '\0') {
        n++;
    }
    
    // using 2 integer to index the char and reverse
    int i = 0, j = n - 1;
    while (i < j) {
        char t = str[i];
        str[i] = str[j];
        str[j] = t;
        i++;
        j--;
    }
}
```

##1.3 Given two strings, write a method to decide if one is a permutation of the other.

```java
public class StringComparer {
	
	private String mString1;
	private String mString2;
	
	public StringComparer(String iStr1, String iStr2)
	{
		mString1 = iStr1;
		mString2 = iStr2;
	}

	// Solution 1, using hash table
	public boolean couldRearrange()
	{
		if(mString1 == null || mString2 == null)
			return false;
		
		if(mString1.length() != mString2.length())
			return false;
		
		Hashtable<String, Integer> lCacheTable = new Hashtable<String, Integer>();
		
		for(int i = 0; i < mString1.length(); i++)
		{
			String c = mString1.substring(i, i+1);
			Integer lCount = lCacheTable.get(c);
			if(lCount == null)
			{
				lCacheTable.put(c, 1);
			}
			else
			{
				lCacheTable.put(c, lCount+1);
			}
		}
		
		for(int i = 0; i < mString2.length(); i++)
		{
			String c = mString2.substring(i, i+1);
			Integer lCount = lCacheTable.get(c);
			if(lCount == null || lCount == 0)
			{
				return false;
			}
			else
			{
				lCount -= 1;
				if(lCount == 0)
				{
					lCacheTable.remove(c);
				}
				else
				{
					lCacheTable.put(c, lCount);
				}
			}
		}
		
		return true;
	}
	
	// solution 2, sort string
	private String sort(String t)
	{
		char[] s = t.toCharArray();
		java.util.Arrays.sort(s);
		return new String(s);
	}
	
	public boolean couldRearrange2()
	{
		String str1 = this.sort(mString1);
		String str2 = this.sort(mString2);
		if(str1.compareTo(str2) == 0)
			return true;
		else
			return false;
	}
	
	// soltion 3. using array to store the char count
	public boolean couldRearrange3()
	{
		if(mString1 == null || mString2 == null ||  mString1.length() != mString2.length())
			return false;
		
		int marks[] = new int[256];
		
		char[] s = mString1.toCharArray();
		for(char c: s)
		{
			int index = (int)c;
			marks[index]++;
		}
		
		for(int i = 0; i < mString2.length(); i++)
		{
			int index = (int)mString2.charAt(i);
			if(marks[index] == 0)
			{
				return false;
			}
			else
			{
				marks[index]--;
			}
		}
		
		return true;
	}
}
```

## 1.4 Write a method to replace all spaces in a string with'%20'. You may assume that the string has sufficient space at the end of the string to hold the additional characters, and that you are given the "true" length of the string. (Note: if imple- menting in Java, please use a character array so that you can perform this opera- tion in place.)

```java
	public static void replaceBlankTest(char[] str, int length)
	{
		if(length == 0)
			return;
		
		int index = 0;
		int blankCount = 0;
		while(str[index] != '\0' && index < length)
		{
			if(str[index] == ' ') blankCount++;
			index++;
		}
		index--;
		
		int externCount = blankCount * 2;
		int endIndex = index + externCount;
		while(index >= 0)
		{
			if(str[index] == ' ')
			{
				blankCount--;
				str[endIndex] = '0';
				str[endIndex-1] = '2';
				str[endIndex-2] = '%';
				endIndex -= 3;
			}
			else
			{
				str[endIndex] = str[index];
				endIndex--;
			}
			
			index--;
		}
	}
```