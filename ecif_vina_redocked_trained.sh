mkdir result/$1

mkdir result/$1/$1_pdbqt
mkdir result/$1/$1_sdf

cp /home/sapna/Downloads/y/ADFRsuite_x86_64Linux_1.0/bin/prepare_ligand $2   #add full path of prepare_ligand

for filename in $2/*.pdb; do
        cd $2
        ./prepare_ligand -l $filename
        cd /home/sapna/Downloads/SG_ML_PLAP/SG_ML_PLAP_prediction/    #add full path of current working directory
done

mv $2/*pdbqt result/$1/$1_pdbqt/  #add full path of result directory

for filename in $2/*.pdb; do
        obabel $filename -O ${filename%.*}.sdf
done

mv $2/*.sdf result/$1/$1_sdf/     #add full path of result directory

./prepare_receptor -r $3 -o vina_receptor.pdbqt

for filename in result/$1/$1_pdbqt/*.pdbqt; do
    echo "${filename%.*}"
    ./vina_package/build/linux/release/vina --receptor vina_receptor.pdbqt --ligand $filename --score_only --log ${filename%.*}.txt  #make sure the vina used used from the vina_package
    sed -i '/Affinity/,$!d' ${filename%.*}.txt
    sed -i '/Affinity/i \
    feature value' ${filename%.*}.txt
done



python vina_ecif_feature.py -p vina_receptor.pdbqt -l result/$1/$1_sdf -s result/$1/$1_pdbqt  #add full path of current working directory
mv vina_ecif_features.csv $1_vina_ecif_features.csv
mv $1_vina_ecif_features.csv result/$1/                                                 #add full path of result folder directory
python ecif_vina_redocked_prediction.py -f result/$1/$1_vina_ecif_features.csv
mv ECIF_VINA_redocked_trained_gbt_prediction.csv $1_ECIF_VINA_redocked_trained_gbt_prediction.csv
mv $1_ECIF_VINA_redocked_trained_gbt_prediction.csv result/$1/$1_ECIF_VINA_redocked_trained_gbt_prediction.csv #path of result directory
