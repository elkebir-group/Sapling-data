#!/usr/bin/env bash
set -euo pipefail

RESULT_DIR="results/sims_infer_full_trees_fastbe"
mkdir -p "$RESULT_DIR"

K_VALUES=(1 10 50 100)

# Loop over all frequency matrices
for freq in data/sims/*_frequency_matrix.txt; do
    # Strip suffix → get base e.g. n20_m10_s8
    base_with_path="${freq%_frequency_matrix.txt}"
    base="$(basename "$base_with_path")"

    echo "=== Processing instance: $base ==="

    variant="data/sims/${base}_variant_matrix.txt"
    total="data/sims/${base}_total_matrix.txt"

    # Loop over requested k values
    for k in "${K_VALUES[@]}"; do
        echo "  -> k = $k"

        prefix="$RESULT_DIR/${base}_k${k}"
        mkdir -p "$(dirname "$prefix")"

        #
        # 1) Run fastbe search
        #
        gtime -v fastbe search "$freq" \
            -o "$prefix" \
            -b "$k" \
            &> "${prefix}.time"

        #
        # 2) Run fastppm-cli
        #
        fastppm-cli \
            --tree "${prefix}_tree.txt" \
            --variant "$variant" \
            --total "$total" \
            -o "${prefix}_inferred_frequencies.json" \
            -f verbose \
            -l binomial
    done
done
