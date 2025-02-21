import pandas as pd
import numpy as np
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input_file', type=str,
        help='Input TSV file containing variant and total read counts.'
    )

    parser.add_argument(
        '-o', '--output', type=str, required=True,
        help='Prefix for output files.'
    )

    return parser.parse_args()

def process_input(input_file):
    """
    Processes the input TSV file and extracts variant and total read counts.

    Args:
        input_file (str): Path to the input TSV file.

    Returns:
        tuple: A tuple containing:
               - variant_matrix (numpy.ndarray): A 2D array of variant read counts.
               - total_matrix (numpy.ndarray): A 2D array of total read counts.
    """
    # Load the input TSV file into a DataFrame
    df = pd.read_csv(input_file, sep='\t')

    # Pivot the DataFrame to create matrices
    variant_matrix = df.pivot(index='mutation_index', columns='sample_index', values='var').fillna(0).astype(int).values
    total_matrix = df.pivot(index='mutation_index', columns='sample_index', values='depth').fillna(0).astype(int).values

    return variant_matrix, total_matrix

if __name__ == "__main__":
    args = parse_args()

    # Process the input file to get variant and total read count matrices
    variant_matrix, total_matrix = process_input(args.input_file)

    # Generate the SSM file contents
    ssm_file_contents = "id\tname\tvar_reads\ttotal_reads\tvar_read_prob"
    for i in range(variant_matrix.shape[0]):
        out_str = f"s{i}\ts{i}\t"
        out_str += ",".join(map(str, variant_matrix[i, :]))
        out_str += "\t"
        out_str += ",".join(map(str, total_matrix[i, :]))
        out_str += "\t"
        # Make the last column shape[1] 1.0s
        out_str += ",".join(["1.0"] * variant_matrix.shape[1])
        ssm_file_contents += "\n" + out_str

    # Write the SSM file
    with open(f"{args.output}_mutations.ssm", 'w') as f:
        f.write(ssm_file_contents)

    # Generate the clones_to_mutations mapping
    clones_to_mutations = [[f"s{j}"] for j in range(variant_matrix.shape[0])]

    # Generate the sample names
    samples = [f"sample_{i}" for i in range(variant_matrix.shape[1])]

    # Write the params JSON file
    with open(f"{args.output}_params.json", 'w') as f:
        data = {
            "samples": samples,
            "clusters": clones_to_mutations,
            "garbage": []
        }
        f.write(json.dumps(data))