#!/usr/bin/env bash
set -euo pipefail

RESULT_DIR="results/sims_infer_full_trees_fastbe"

K_VALUES=(1 10 50 100)

for variant in data/sims/*_variant_matrix.txt; do
    # e.g. variant = data/sims/n100_m10_s14_variant_matrix.txt
    base_with_path="${variant%_variant_matrix.txt}"   # data/sims/n100_m10_s14
    base="$(basename "$base_with_path")"              # n100_m10_s14

    total="data/sims/${base}_total_matrix.txt"

    for k in "${K_VALUES[@]}"; do
        tree="${RESULT_DIR}/${base}_k${k}_trees.txt"
        out_tsv="${RESULT_DIR}/${base}_k${k}.tsv"

        if [[ ! -f "$tree" ]]; then
            echo "Skipping $base k=${k} (missing tree)" >&2
            continue
        fi

        echo "Parsing $base k=${k} -> $out_tsv"

        python scripts/parse_fastbe_output.py \
            "$tree" \
            "$variant" \
            "$total" \
            > "$out_tsv" &
    done
done
