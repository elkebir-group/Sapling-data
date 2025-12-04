#!/bin/sh
for f in ../../data/TRACERx/*_new.tsv
do
	ff=$(basename $f _new.tsv)
	nr_clusters=$(cut -f5 ../../data/TRACERx/$f | sort -u -n | wc -l)
	for (( ell=1; ell<=nr_clusters; ell++ ))
	do
		for rho in 0.4 0.9
		do
			echo python "\$sapling" -f "$f" -l "$ell" --rho "$rho" -o "${ff}_ell${ell}_rho${rho}.tsv --use_clusters --alt_roots"
		done
	done
done
