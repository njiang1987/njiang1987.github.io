---
layout: post
title: "[CTCI]-StringBuffer simple implementation in Java"
date: 2014-08-17 08:45:50 +0800
comments: true
categories: 技术
tags: iOS
---

Here is an implementation of String Buffer. It use an link list to store the appended string. If there is no enough space for the append string, it will create an new node for the new string.


```java
public class StringBufferTest {
    
    /**
    * Each node represent part of strings.
    */
    private class Node
    {
          public char[] data;
          public Node next;
         
          public Node()
          {
               data = new char[size];
               next = null;
          }
    }
   
    public static int size = 5;
    private Node first;
    private Node currentNode;
    private int index;
   
    public StringBufferTest()
    {
          first = new Node();
          currentNode = first;
          index = 0;
    }
   
   	// Thanks for Robert C, Wang's improve the code.
    public void append(String inputStr) {
        if (inputStr == null)
               return;

        // Copy the string to the node data
        for(int i = 0; i < inputStr.length(); i++) {
            if(index == size) {	// Create a new node at end
                Node newNode = new Node();
                currentNode.next = newNode;
                currentNode = currentNode.next;
                index = 0;
            }
            currentNode.data[index++] = inputStr.charAt(i);
        }
    }
    
    public String toString()
    {
    	String result = "";
    	Node p = first;
    	while(p != null)
    	{
    		result += String.valueOf(p.data);
    		p = p.next;
    	}
    	return result;
    }

    /**
    * @param args
    */
    public static void main(String[] args) {
          StringBufferTest test = new StringBufferTest();
          test.append("123456");
          test.append("789");
          
          String result = test.toString();
          System.out.print(result);
    }

}
```