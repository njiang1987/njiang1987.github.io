---
layout: post
title: "Reverse alternate levels of a perfect binary tree"
date: 2014-07-12 16:10:38 +0800
comments: true
categories: 技术
tags: Other
---

Given a Perfect Binary Tree, reverse the alternate level nodes of the binary tree.

  
Given tree: 
               a
            /     \
           b       c
         /  \     /  \
        d    e    f    g
       / \  / \  / \  / \
       h  i j  k l  m  n  o 

Modified tree:
  	       	   a
            /     \
           c       b
         /  \     /  \
        d    e    f    g
       / \  / \  / \  / \
      o  n m  l k  j  i  h 
We strongly recommend to minimize the browser and try this yourself first.

A simple solution is to do following steps.
1) Access nodes level by level.
2) If current level is odd, then store nodes of this level in an array.
3) Reverse the array and store elements back in tree.

A tricky solution is to do two inorder traversals. Following are steps to be followed.
1) Traverse the given tree in inorder fashion and store all odd level nodes in an auxiliary array. For the above example given tree, contents of array become {h, i, b, j, k, l, m, c, n, o}

2) Reverse the array. The array now becomes {o, n, c, m, l, k, j, b, i, h}

3) Traverse the tree again inorder fashion. While traversing the tree, one by one take elements from array and store elements from array to every odd level traversed node.
For the above example, we traverse ‘h’ first in above array and replace ‘h’ with ‘o’. Then we traverse ‘i’ and replace it with n.

{% codeblock lang:cpp %}
// C++ program to find maximum path sum between two leaves of
// a binary tree
#include <iostream>
#include <vector>
using namespace std;

// A binary tree node
struct Node
{
    int data;
    struct Node* left, *right;
};

// Utility function to allocate memory for a new node
struct Node* newNode(int data)
{
    struct Node* node = new(struct Node);
    node->data = data;
    node->left = node->right = NULL;
    return (node);
}

void traverseNode(struct Node* root, int level, vector<vector<int> >& lists)
{
    if (root == NULL) {
        return;
    }
    
    if (lists.size() < level + 1) {
        lists.push_back(vector<int>());
    }
    
    lists[level].push_back(root->data);
    traverseNode(root->left, level+1, lists);
    traverseNode(root->right, level+1, lists);
}

void printTree(struct Node* root)
{
    if (root == NULL) {
        return;
    }
    vector<vector<int> > lists;
    traverseNode(root, 0, lists);
    
    for (int i = 0; i < lists.size(); i++) {
        cout<< "Level "<<i<<":";
        for (int j = 0; j < lists[i].size(); j++) {
            cout<<" "<<lists[i][j];
        }
        cout<<endl;
    }
}

void replaceNode(struct Node* root, int level, vector<vector<int> >& lists)
{
    if (root == NULL) {
        return;
    }
    if (lists[level].size() == 0) {
        return;
    }
    
    if (level%2 != 0) {
        size_t count = lists[level].size();
        root->data = lists[level][count - 1];
        lists[level].pop_back();
    }
    
    replaceNode(root->left, level+1, lists);
    replaceNode(root->right, level+1, lists);
}

void reverseTree(struct Node* root)
{
    if (root == NULL) {
        return;
    }
    vector<vector<int> > lists;
    traverseNode(root, 0, lists);
    replaceNode(root, 0, lists);
}

// driver program to test above function
int main()
{
    struct Node *root = newNode(1);
    root->left = newNode(2);
    root->right = newNode(3);
    
    root->left->left = newNode(4);
    root->left->right = newNode(5);
    root->right->left = newNode(6);
    root->right->right = newNode(7);
    
    root->left->left->left = newNode(8);
    root->left->left->right = newNode(9);
    root->left->right->left = newNode(10);
    root->left->right->right = newNode(11);
    
    root->right->left->left = newNode(12);
    root->right->left->right = newNode(13);
    root->right->right->left = newNode(14);
    root->right->right->right = newNode(15);
    
    printTree(root);
    
    reverseTree(root);
    
    printTree(root);

    return 0;
}
{% endcodeblock %}