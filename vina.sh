./vina_package/build/linux/release/vina --receptor $1 --ligand $2 --score_only --log score.txt
sed -i '/Affinity/,$!d' score.txt
sed -i '/Affinity/i \
feature value' score.txt


