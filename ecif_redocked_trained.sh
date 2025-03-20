mkdir result/$1
#cd /data2/sapna/sg_ml_plap_server/result/$1

mkdir result/$1/$1_sdf
for filename in $2/*.pdb; do
        obabel $filename -O ${filename%.*}.sdf
done

mv $2/*.sdf result/$1/$1_sdf/



python ecif_feature.py -p $3 -l result/$1/$1_sdf
mv ecif_features.csv $1_ecif_features.csv
mv $1_ecif_features.csv result/$1
python ecif_redocked_prediction.py -f result/$1/$1_ecif_features.csv

mv ECIF_redocked_trained_gbt_prediction.csv $1_ECIF_redocked_trained_gbt_prediction.csv

mv $1_ECIF_redocked_trained_gbt_prediction.csv result/$1/$1_ECIF_redocked_trained_gbt_prediction.csv


#python ecif_feature.py -p $1 -l $2
#python ecif_redocked_prediction.py -f ecif_features.csv

