for filename in ../../data/sims/n8*.tsv;
do
	for ell in {1..8};
	do
		echo python \$sapling --rho 0.9 --ell $ell --tau -1 -f $filename -o $(basename $filename .tsv)_ell$ell.tsv
	done
done
