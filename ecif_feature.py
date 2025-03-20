import pandas as pd
import numpy as np
from ecif import *
from joblib import delayed, Parallel
import os, os.path
import pathlib

import argparse

parser = argparse.ArgumentParser(description="ECIF feature generation for protein-ligand complex",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-p", "--protein_path", required=True, help="path of protein (pdb)")
parser.add_argument("-l", "--ligand_path", required=True, help="path of ligand (sdf)")
args = parser.parse_args()

DIR = args.ligand_path
pdbs = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

Protein = {pdb: str(pathlib.Path(args.protein_path)) for pdb in pdbs}
Ligand = {pdb: str(pathlib.Path(f'{args.ligand_path}/{pdb}')) for pdb in pdbs}

with Parallel(n_jobs=10, verbose=10) as parallel:
    list = parallel(delayed(GetECIF)(Protein[pdb], Ligand[pdb], distance_cutoff=6.0) for pdb in pdbs)

features = {pdb: list for pdb, list in zip(pdbs, list)}
features_new = pd.DataFrame.from_dict(features).T
features_new.columns = PossibleECIF
features_new.to_csv('ecif_features.csv')
