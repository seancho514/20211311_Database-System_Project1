import csv
import time
import random
import math
import sys

# 재귀 깊이 제한 해제
sys.setrecursionlimit(100000)

class BPlusTree_Node:
    def __init__(self, isleaf=False):
        self.isleaf = isleaf
        self.keys = []
        self.children = [] 
        self.next = None    # 리프 노드 간 연결 리스트 포인터

class BPlusTree:
    def __init__(self, d):
        self.d = d
        self.root = BPlusTree_Node(isleaf=True)
        self.split_count = 0

    def _find_leaf(self, key):
        curr = self.root
        while not curr.isleaf:
            i = 0
            while i < len(curr.keys) and key >= curr.keys[i]:
                i += 1
            curr = curr.children[i]
        return curr

    # --- Point Search ---
    def search(self, key):
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.children[i]
        return None

    # --- Range Query ---
    def range_query(self, start_key, end_key):
        results = []
        curr_leaf = self._find_leaf(start_key)
        
        while curr_leaf:
            for i, key in enumerate(curr_leaf.keys):
                if start_key <= key <= end_key:
                    results.append(curr_leaf.children[i])
                elif key > end_key:
                    return results
            curr_leaf = curr_leaf.next # 인덱스 층으로 다시 올라가지 않고 옆 노드로 이동
        return results

    # --- Insertion ---
    def insert(self, item):
        key = item[0]
        if len(self.root.keys) == self.d - 1:
            self.split_count += 1
            new_root = BPlusTree_Node(isleaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, item)

    def _insert_non_full(self, node, item):
        key = item[0]
        if node.isleaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
            node.children.insert(i, item)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            target = node.children[i]
            if len(target.keys) == self.d - 1:
                self.split_count += 1
                self._split_child(node, i)
                if key >= node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], item)

    def _split_child(self, parent, i):
        node = parent.children[i]
        new_node = BPlusTree_Node(isleaf=node.isleaf)
        mid = len(node.keys) // 2
        
        if node.isleaf:
            split_key = node.keys[mid]
            new_node.keys = node.keys[mid:]
            new_node.children = node.children[mid:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid]
            new_node.next = node.next
            node.next = new_node
            parent.keys.insert(i, split_key)
            parent.children.insert(i + 1, new_node)
        else:
            split_key = node.keys[mid]
            new_node.keys = node.keys[mid+1:]
            new_node.children = node.children[mid+1:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid+1]
            parent.keys.insert(i, split_key)
            parent.children.insert(i + 1, new_node)

    # --- Deletion ---
    def delete(self, key):
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                leaf.keys.pop(i)
                leaf.children.pop(i)
                break

    def get_statistics(self):
        total_nodes, total_keys = 0, 0
        def traverse(node):
            nonlocal total_nodes, total_keys
            total_nodes += 1
            total_keys += len(node.keys)
            if not node.isleaf:
                for child in node.children: traverse(child)
        traverse(self.root)
        max_cap = total_nodes * (self.d - 1)
        util = (total_keys / max_cap) * 100 if max_cap > 0 else 0
        return total_nodes, total_keys, util

