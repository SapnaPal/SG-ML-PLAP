import pandas as pd
import joblib
import argparse
import os

parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-f", "--feature", required=True, help="name of protein/pdb")
#parser.add_argument("-l", "--ligand_path", required=True, help="path of ligand (sdf)")

args = parser.parse_args()

#DIR = args.ligand_path
#pdbs = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]



model = joblib.load('ecif_redocked_prediction_gbt_model.sav')
feature = pd.read_csv(args.feature, index_col=0)
pdbs = feature.index.to_list()
y_pred = model.predict(feature)
y_pred = y_pred.round(2)
df = pd.DataFrame(y_pred)
df.index = [i[:-4] for i in pdbs]
df.index.name='ligand'
df.columns = ['Binding Affinity (pKa)']
df = df.sort_values(by='Binding Affinity (pKa)', ascending=False)
print(df)
df.to_csv('ECIF_redocked_trained_gbt_prediction.csv')
