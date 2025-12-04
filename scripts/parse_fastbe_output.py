import argparse
import json 
import pandas as pd
import numpy as np
import fastppm

def print_row(i, parents_dict, frequency_matrix, llh):
    num_samples = frequency_matrix.shape[0]
    num_clones  = frequency_matrix.shape[1]

    print()
    print(f"{i}\t{llh}", end="")
    for i in range(num_clones):
        if i not in parents_dict:
            print("\t-1", end="")
            continue
        print(f"\t{parents_dict[i]}", end="")

    for i in range(num_samples):
        for j in range(num_clones):
            print(f"\t{frequency_matrix[i][j]}", end="")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("trees")
    parser.add_argument("variant_matrix")
    parser.add_argument("total_matrix")
    args = parser.parse_args()

    variant_matrix = np.loadtxt(args.variant_matrix)
    total_matrix = np.loadtxt(args.total_matrix)

    num_samples = variant_matrix.shape[0]
    num_clones  = variant_matrix.shape[1]

    parents_dicts = []
    with open(args.trees, "r") as f:
        for line in f:
            if line[0] == '#':
                parents_dicts.append({})
                continue

            words = line.split()
            parent = int(words[0])
            for child in words[1:]:
                parents_dicts[-1][int(child)] = parent
    
    clone_trees = []
    for parents_dict in parents_dicts:
        clone_tree = [[] for _ in range(num_clones)]
        for node, parent in parents_dict.items():
            clone_tree[parent].append(node)
        clone_trees.append(clone_tree)

    print("tree\tllh", end="")
    for i in range(num_clones):
        print(f"\tpi_{i}", end="")
    for i in range(num_samples):
        for j in range(num_clones):
            print(f"\tf_{i}_{j}", end="")

    print()
    for i, clone_tree in enumerate(clone_trees):
        res = fastppm.regress_counts(clone_tree, variant_matrix.astype(int).tolist(), total_matrix.astype(int).tolist(), loss_function="binomial")
        print_row(i, parents_dicts[i], np.array(res['frequency_matrix']), -res['objective'])