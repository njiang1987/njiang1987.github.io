---
layout: post
title: "Given a linked list, reverse alternate nodes and append at the end"
date: 2014-07-12 21:11:31 +0800
comments: true
categories: GeeksForGeeks LinkList
---
Given a linked list, reverse alternate nodes and append them to end of list. Extra allowed space is O(1) 
Examples

Input List:  1->2->3->4->5->6
Output List: 1->3->5->6->4->2

Input List:  12->14->16->18->20
Output List: 12->16->20->18->14
We strongly recommend to minimize the browser and try this yourself first.

The idea is to maintain two linked lists, one list of all odd positioned nodes (1, 3, 5 in above example) and other list of all even positioned nodes (6, 4 and 2 in above example). Following are detailed steps.
1) Traverse the given linked list which is considered as odd list. Do following for every visited node.
……a) If the node is even node, remove it from odd list and add it to the front of even node list. Nodes are added at front to keep the reverse order.
2) Append the even node list at the end of odd node list.

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

struct ListNode
{
    int data;
    struct ListNode* next;
};

struct ListNode* newListNode(int data)
{
    struct ListNode* node = new (struct ListNode);
    node->data = data;
    node->next = NULL;
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

void printList(struct ListNode* first)
{
    struct ListNode* p = first;
    while (p) {
        cout<<p->data;
        if (p->next) {
            cout<<"->";
        }
        p = p->next;
    }
    cout<<endl;
}

void test(struct ListNode* first)
{
    if (first == NULL || first->next == NULL || first->next->next == NULL) {
        return;
    }
    
    struct ListNode* p1 = first;
    struct ListNode* p2 = first->next;
    struct ListNode* t = NULL;
    struct ListNode* q = NULL;
    int i = 1;
    while (p2) {
        if (i%2 != 0) {
            t = p2;
            p1->next = t->next;
            t->next = q;
            q = t;
            p2 = p1->next;
        }
        else{
            p1 = p2;
            p2 = p1->next;
        }
        i++;
    }
    p1->next = q;
}

// driver program to test above function
int main()
{
    struct ListNode* first = newListNode(1);
    first->next = newListNode(2);
    first->next->next = newListNode(3);
    first->next->next->next = newListNode(4);
    first->next->next->next->next = newListNode(5);
    first->next->next->next->next->next = newListNode(6);
    
    printList(first);
    test(first);
    printList(first);

    return 0;
}
{% endcodeblock %}