import argparse
import json 
import pandas as pd
import numpy as np

def binomial_log_likelihood(F, V, D, eps=1e-10):
    """
    Computes the binomial log-likelihood given frequency, variant, and total read count matrices.

    Args:
        F (numpy.ndarray): Frequency matrix (samples x mutations).
        V (numpy.ndarray): Variant read count matrix (samples x mutations).
        D (numpy.ndarray): Total read count matrix (samples x mutations).
        eps (float): A small value to avoid log(0). Default is 1e-10.

    Returns:
        float: The binomial log-likelihood.
    """
    # Ensure F is within valid range [0, 1]
    F = np.clip(F, eps, 1 - eps)

    # Compute the log-likelihood
    log_likelihood = np.sum(
        np.where(V > 0, V * np.log(F), 0) +  # Handle V = 0
        np.where(D - V > 0, (D - V) * np.log(1 - F), 0)  # Handle D - V = 0
    )

    return log_likelihood

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tree")
    parser.add_argument("inferred_frequencies")
    parser.add_argument("variant_matrix")
    parser.add_argument("total_matrix")
    args = parser.parse_args()

    parents_dict = {}
    with open(args.tree, "r") as f:
        for line in f:
            words = line.split()
            parent = int(words[0])
            for child in words[1:]:
                parents_dict[int(child)] = parent

    with open(args.inferred_frequencies, "r") as f:
        data = json.load(f)
        frequency_matrix = np.array(data['frequency_matrix'])

    variant_matrix = np.loadtxt(args.variant_matrix)
    total_matrix = np.loadtxt(args.total_matrix)

    num_samples = frequency_matrix.shape[0]
    num_clones  = frequency_matrix.shape[1]

    llh = binomial_log_likelihood(frequency_matrix, variant_matrix, total_matrix)

    print("tree\tllh", end="")
    for i in range(num_clones):
        print(f"\tpi_{i}", end="")
    for i in range(num_samples):
        for j in range(num_clones):
            print(f"\tf_{i}_{j}", end="")

    print()
    print(f"0\t{llh}", end="")
    for i in range(num_clones):
        if i not in parents_dict:
            print("\t-1", end="")
            continue
        print(f"\t{parents_dict[i]}", end="")
    for i in range(num_samples):
        for j in range(num_clones):
            print(f"\t{frequency_matrix[i][j]}", end="")