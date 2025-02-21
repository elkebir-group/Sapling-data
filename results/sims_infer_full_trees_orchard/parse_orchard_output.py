import numpy as np
import argparse

def parse_orchard_output(result_file, output_file):
    """
    Parses a Orchard result file in NPZ format and generates a TSV file with the Sapling output format.

    Args:
        result_file (str): Path to the input NPZ file.
        output_file (str): Path to the output TSV file.
    """
    # Load the NPZ file
    result = np.load(result_file)

    # Extract the best tree structure, log-likelihood, and frequency matrix
    best_tree_parents = result['struct'][0]   # Parent indices for each node
    best_tree_llh = result['llh'][0]          # Log-likelihood of the best tree
    best_tree_freq = result['phi'][0].T[:,1:] # Frequency matrix (samples x mutations)

    # Prepare the output data
    output_data = []
    for tree_idx in range(len(result['struct'])):
        parents = result['struct'][tree_idx]
        llh = result['llh'][tree_idx]
        freq = result['phi'][tree_idx].T[:,1:]  # Drop superfluous GL mutation that Orchard adds

        # Create a row for the output
        row = {
            'tree': tree_idx,
            'llh': llh
        }

        # Add parent indices (pi)
        for mut_idx in range(len(parents)):
            row[f'pi_{mut_idx}'] = parents[mut_idx] - 1  # Adjust for 0-based indexing

        # Add frequency values (f)
        for sample_idx in range(freq.shape[0]):
            for mut_idx in range(freq.shape[1]):
                row[f'f_{sample_idx}_{mut_idx}'] = freq[sample_idx, mut_idx]

        output_data.append(row)

    # Write the output to a TSV file
    with open(output_file, 'w') as f:
        # Write the header
        header = ['tree', 'llh']
        header += [f'pi_{i}' for i in range(len(best_tree_parents))]
        header += [f'f_{s}_{m}' for s in range(best_tree_freq.shape[0]) for m in range(best_tree_freq.shape[1])]
        f.write('\t'.join(header) + '\n')

        # Write the rows
        for row in output_data:
            row_values = [str(row.get(col, '')) for col in header]
            f.write('\t'.join(row_values) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Orchard output.')
    parser.add_argument('result', type=str, help='Result file in NPZ format.')
    parser.add_argument('--output', type=str, required=True, help='Output TSV file.')
    args = parser.parse_args()

    parse_orchard_output(args.result, args.output)