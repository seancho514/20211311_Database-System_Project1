# CSE321 Project #1: B-tree Index Structures Implementation

This repository contains the implementation and experimental analysis of B-tree, B*-tree, and B+-tree index structures for the CSE321: Database Systems course.

## 1. Project Information
- **Course**: CSE321: Database Systems
- **Student Name**: Minsung Cho
- **Student ID**: 20211311

## 2. Development Environment
- **Language**: Python 3.10+
- **Libraries**: None (Uses standard libraries: `csv`, `time`, `random`, `math`, `sys`)
- **Dataset**: `student.csv` (100,000 student records)

## 3. File Structure
- `B_tree.py`: Implementation of a standard B-tree where internal nodes store both keys and RIDs.
- `B_star_tree.py`: Implementation of a B*-tree featuring sibling redistribution and 2-to-3 split strategies to maximize node utilization.
- `B_plus_tree.py`: Implementation of a B+-tree with linked leaf nodes for optimized sequential and range scans.
- `run_experiment.py`: A unified integration script that imports all three tree classes to execute benchmarks and additional experiments.
- `student.csv`: The dataset containing 100,000 student records used for all evaluations.

## 4. Execution Instructions

### Prerequisites
1. Ensure that Python 3.x is installed on your system.
2. Verify that `student.csv` is located in the same directory as the source code files.

### Running the Experiments
To execute the entire experimental workload, including fundamental evaluations and creative additional experiments, run the following command in your terminal:
```bash
python run_experiment.py
