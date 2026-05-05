import csv
import time
import random
import math
import sys

# 재귀 깊이 제한 해제
sys.setrecursionlimit(100000)

class BTree_Node:
    def __init__(self, isleaf=False):
        self.isleaf = isleaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, d):
        self.d = d
        self.root = BTree_Node(isleaf=True)
        self.min_keys = math.ceil(d / 2) - 1
        self.split_count = 0

    # --- Insertion ---
    def insert(self, item):
        root = self.root
        if len(root.keys) == self.d - 1:
            self.split_count += 1
            new_root = BTree_Node(isleaf=False)
            self.root = new_root
            new_root.children.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, item)
        else:
            self._insert_non_full(root, item)

    def _insert_non_full(self, node, item):
        i = len(node.keys) - 1
        key = item[0]
        if node.isleaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = item
        else:
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.d - 1:
                self.split_count += 1
                self._split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], item)

    def _split_child(self, parent, i):
        full_node = parent.children[i]
        new_node = BTree_Node(isleaf=full_node.isleaf)
        mid_idx = len(full_node.keys) // 2
        split_item = full_node.keys[mid_idx]
        new_node.keys = full_node.keys[mid_idx + 1:]
        full_node.keys = full_node.keys[:mid_idx]
        if not full_node.isleaf:
            new_node.children = full_node.children[mid_idx + 1:]
            full_node.children = full_node.children[:mid_idx + 1]
        parent.keys.insert(i, split_item)
        parent.children.insert(i + 1, new_node)

    # --- Point Search ---
    def search(self, key, node=None):
        if node is None: node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            return node.keys[i]
        if node.isleaf:
            return None
        return self.search(key, node.children[i])

    # --- Range Query ---
    def range_query(self, start_key, end_key, node=None, results=None):
        if results is None: results = []
        if node is None: node = self.root
        
        i = 0
        # start_key가 나올 때까지 인덱스 이동
        while i < len(node.keys) and start_key > node.keys[i][0]:
            i += 1
        
        # 범위 내 데이터 수집
        while i < len(node.keys):
            if not node.isleaf:
                self.range_query(start_key, end_key, node.children[i], results)
            
            if start_key <= node.keys[i][0] <= end_key:
                results.append(node.keys[i])
            elif node.keys[i][0] > end_key:
                return results # 범위 초과 시 조기 종료
            i += 1
            
        if not node.isleaf:
            self.range_query(start_key, end_key, node.children[i], results)
        return results

    # --- Deletion ---
    def delete(self, key):
        """삭제 실험을 위해 예외 처리가 강화된 삭제 메서드"""
        if self.search(key) is not None:
            self._delete_recursive(self.root, key)
            # 루트가 비게 되면 자식으로 대체
            if len(self.root.keys) == 0 and not self.root.isleaf:
                if self.root.children:
                    self.root = self.root.children[0]

    def _delete_recursive(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        
        # 키를 찾은 경우
        if i < len(node.keys) and key == node.keys[i][0]:
            if node.isleaf:
                node.keys.pop(i)
            else:
                # 내부 노드 삭제 시 Successor
                successor_item = self._get_successor(node, i)
                if successor_item:
                    node.keys[i] = successor_item
                    self._delete_recursive(node.children[i+1], successor_item[0])
                else:
                    # Successor가 없는 특수 상황 예외 처리
                    node.keys.pop(i)
        # 키를 못 찾은 경우 자식으로 내려감
        elif not node.isleaf:
            if i < len(node.children):
                self._delete_recursive(node.children[i], key)

    def _get_successor(self, node, i):
        """내부 노드 삭제를 위해 오른쪽 자식 트리에서 가장 작은 키를 찾음"""
        if i + 1 >= len(node.children): return None
        curr = node.children[i+1]
        while not curr.isleaf:
            if not curr.children: break
            curr = curr.children[0]
        return curr.keys[0] if curr.keys else None

    def get_statistics(self):
        total_nodes, total_keys = 0, 0
        def traverse(node):
            nonlocal total_nodes, total_keys
            total_nodes += 1
            total_keys += len(node.keys)
            for child in node.children: traverse(child)
        traverse(self.root)
        max_cap = total_nodes * (self.d - 1)
        util = (total_keys / max_cap) * 100 if max_cap > 0 else 0
        return total_nodes, total_keys, util