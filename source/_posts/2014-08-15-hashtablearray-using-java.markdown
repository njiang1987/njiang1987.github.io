---
layout: post
title: "[CTCI]-HashTableArray using Java"
date: 2014-08-15 13:58:07 +0800
comments: true
categories: CTCI
---

Using an array to store hash key/value.

```java
package cn.njiang.base;

import java.util.*;

public class HashTableArray<Key, Value> 
{	
	
	public class HTEntity<Key, Value>
	{
		public Key mKey;
		public Value mValue;
		
		public HTEntity()
		{
			this.mKey = null;
			this.mValue = null;
		}
		
		public HTEntity(Key iKey, Value iValue)
		{
			this.mKey = iKey;
			this.mValue = iValue;
		}
	}
	
	HTEntity<Key, Value>[] mTable;
	public int mCapicity = 5;
	public int mCount;
	private int mSeed;
	
	public HashTableArray()
	{
		mTable = new HTEntity[mCapicity];
		mCount = 0;
		mSeed = 13;
	}
	
	private int hash(final Key iKey)
	{
		int lIndex = (mSeed^iKey.hashCode()) % mCapicity;
		return lIndex;
	}
	
	public void push(Key iKey, Value iValue)
	{
		if(iKey == null || iValue == null)
			return;
		
		if(mCount == mCapicity)
		{
			HTEntity<Key, Value>[] mTmpTable = new HTEntity[2*mCapicity];
			mCapicity = 2 * mCapicity;
			for(int i = 0; i < mCount; i++)
			{
				Key lKey = mTable[i].mKey;
				int index = this.hash(lKey);
				while(mTmpTable[index] != null)
				{
					index = (index + 1) % mCapicity;
				}
					
				mTmpTable[index] = mTable[i];
			}
			mTable = mTmpTable;
		}
		
		int index = this.hash(iKey);
		while(mTable[index] != null)
		{
			if (mTable[index].mKey.equals(iKey))
			{
				break;
			}
			
			index = (index + 1) % mCapicity;
		}
		
		mTable[index] = new HTEntity(iKey, iValue);
		mCount++;
	}

	public void remove(Key iKey)
	{
		if(iKey == null)
		{
			return;
		}
		
		int index = this.hash(iKey);
		while(mTable[index] != null)
		{
			if(mTable[index].mKey.equals(iKey))
			{
				break;
			}
			index = (index + 1) % mCapicity;
		}
		
		if(mTable[index] == null)
		{
			System.out.print("There is no element with key " + iKey);
			return ;
		}
		mTable[index] = null;
		mCount--;
	}
}

```