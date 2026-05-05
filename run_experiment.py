import time
import random
import sys
import copy
from B_tree import BTree
from B_star_tree import BStarTree
from B_plus_tree import BPlusTree

# 재귀 깊이 제한 해제
sys.setrecursionlimit(200000)

def print_table_header():
    header = f"{'Tree Type':<12} | {'Order':<5} | {'Insert(s)':<10} | {'Splits':<8} | {'Util%':<8} | {'Search(ms)':<10} | {'Range(s)':<8} | {'Del(s)':<8}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

def run_benchmarks(tree_class, tree_name, d_values, data):
    results = []
    for d in d_values:
        # 1. Insertion & Parameter Tuning
        tree = tree_class(d)
        start_t = time.perf_counter()
        for item in data:
            tree.insert(item)
        ins_time = time.perf_counter() - start_t
        
        node_count, key_count, util = tree.get_statistics()
        splits = tree.split_count

        # 2. Point Search (10,000 random keys)
        sample_keys = [k[0] for k in random.sample(data, 10000)]
        start_t = time.perf_counter()
        for sk in sample_keys:
            tree.search(sk)
        search_time = (time.perf_counter() - start_t) / 10000 * 1000 # ms 변환

        # 3. Range Query
        # 데이터 범위의 1% 구간 검색
        all_ids = [k[0] for k in data]
        min_id, max_id = min(all_ids), max(all_ids)
        r_start = min_id + (max_id - min_id) // 3
        r_end = r_start + (max_id - min_id) // 100
        
        start_t = time.perf_counter()
        _ = tree.range_query(r_start, r_end)
        range_time = time.perf_counter() - start_t

        # 4. Deletion (2,000 random records)
        del_keys = [k[0] for k in random.sample(data, 2000)]
        start_t = time.perf_counter()
        for dk in del_keys:
            tree.delete(dk)
        del_time = time.perf_counter() - start_t

        res = {
            'name': tree_name, 'd': d, 'ins': ins_time, 'split': splits,
            'util': util, 'search': search_time, 'range': range_time, 'del': del_time
        }
        results.append(res)
        print(f"{tree_name:<12} | {d:<5} | {ins_time:<10.4f} | {splits:<8} | {util:<8.2f} | {search_time:<10.6f} | {range_time:<8.4f} | {del_time:<8.4f}")
    return results

def additional_experiment_sorted(data):
    """추가 실험 1: 정렬된 데이터 삽입 시 구조적 오버헤드 분석"""
    print("\n\n" + "="*30)
    print("Additional Experiment 1: Sorted Data Insertion")
    print("="*30)
    sorted_data = sorted(data, key=lambda x: x[0])
    print_table_header()
    # d=10 기준으로 각 트리의 정렬 데이터 처리 능력 비교
    run_benchmarks(BTree, "B-Tree(S)", [10], sorted_data)
    run_benchmarks(BStarTree, "B*Tree(S)", [10], sorted_data)
    run_benchmarks(BPlusTree, "B+Tree(S)", [10], sorted_data)

def additional_experiment_mass_deletion(data):
    """추가 실험 2: 대규모 삭제(50%) 후 트리의 밀도(Utilization) 분석"""
    print("\n\n" + "="*30)
    print("Additional Experiment 2: Mass Deletion (50%) & Density Recovery")
    print("="*30)
    d = 10
    for tree_class, name in [(BTree, "B-Tree"), (BStarTree, "B*Tree"), (BPlusTree, "B+Tree")]:
        tree = tree_class(d)
        for item in data: tree.insert(item)
        
        _, _, util_before = tree.get_statistics()
        
        # 50,000개 무작위 삭제
        del_keys = [k[0] for k in random.sample(data, 50000)]
        start_t = time.perf_counter()
        for dk in del_keys:
            tree.delete(dk)
        del_duration = time.perf_counter() - start_t
        
        _, _, util_after = tree.get_statistics()
        print(f"[{name}] Utilization: {util_before:.2f}% -> {util_after:.2f}% | Del Time: {del_duration:.4f}s")

if __name__ == "__main__":
    # 데이터 생성 (100,000 records)
    print("Generating 100,000 student records...")
    raw_data = [(random.randint(20200000, 20269999), i) for i in range(100000)]
    
    orders = [3, 5, 10]
    
    print("\n" + "="*30)
    print("Standard Workload Experiments")
    print("="*30)
    print_table_header()
    
    # 각 트리에 대해 실험 수행
    run_benchmarks(BTree, "B-Tree", orders, raw_data)
    run_benchmarks(BStarTree, "B*Tree", orders, raw_data)
    run_benchmarks(BPlusTree, "B+Tree", orders, raw_data)
    
    # 추가 실험 진행
    additional_experiment_sorted(raw_data)
    additional_experiment_mass_deletion(raw_data)