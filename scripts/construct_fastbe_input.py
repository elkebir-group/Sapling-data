#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd


def build_matrices(df: pd.DataFrame):
    required_cols = {"sample_index", "mutation_index", "var", "depth"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Input file is missing required columns: {missing}")

    # Pivot to get matrices indexed by sample_index × mutation_index
    var_table = df.pivot(
        index="sample_index",
        columns="mutation_index",
        values="var"
    ).sort_index(axis=0).sort_index(axis=1)

    depth_table = df.pivot(
        index="sample_index",
        columns="mutation_index",
        values="depth"
    ).sort_index(axis=0).sort_index(axis=1)

    # Fill any missing entries with 0
    var_table = var_table.fillna(0)
    depth_table = depth_table.fillna(0)

    V = var_table.to_numpy(dtype=int)
    D = depth_table.to_numpy(dtype=int)

    # Frequency matrix F = V / D (0 where depth is 0)
    F = np.zeros_like(V, dtype=float)
    np.divide(V, D, out=F, where=(D != 0))

    return V, D, F


def main():
    parser = argparse.ArgumentParser(
        description="Convert TSV of var/depth into variant, total, and frequency matrices."
    )
    parser.add_argument(
        "input_tsv",
        help="Input TSV file with columns: sample_index, mutation_index, cluster_index, var, depth"
    )
    parser.add_argument(
        "prefix",
        help="Prefix for output files: {prefix}_variant_matrix.txt, etc."
    )
    args = parser.parse_args()

    # Read TSV
    df = pd.read_csv(args.input_tsv, sep="\t")

    V, D, F = build_matrices(df)

    # Save outputs as tab-separated text files, no headers/indices
    np.savetxt(f"{args.prefix}_variant_matrix.txt", V, fmt="%d", delimiter="\t")
    np.savetxt(f"{args.prefix}_total_matrix.txt", D, fmt="%d", delimiter="\t")
    np.savetxt(f"{args.prefix}_frequency_matrix.txt", F, fmt="%.6f", delimiter="\t")

if __name__ == "__main__":
    main()