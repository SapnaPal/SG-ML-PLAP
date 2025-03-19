import pandas as pd
import numpy as np
from ecif import *
from joblib import delayed, Parallel
import os, os.path
import pathlib


import argparse

parser = argparse.ArgumentParser(description="/data/ankita/sg_ml_plap/ECIF+VINA feature generation for protein-ligand complex",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-p", "--protein_path", required=True, help="path of protein (pdb)")
parser.add_argument("-l", "--ligand_path", required=True, help="path of ligand (sdf)")
parser.add_argument("-s", "--vina_score_path", required=True, help="path of vina score file (txt)")
args = parser.parse_args()


#check if two folders have same ligand names
DIR_sdf = args.ligand_path
DIR_pdbqt = args.vina_score_path

total_sdf = []
total_sdf += [each[:-4] for each in os.listdir(DIR_sdf) if each.endswith('.sdf')]
total_pdbqt = []
total_pdbqt += [each[:-6] for each in os.listdir(DIR_pdbqt) if each.endswith('.pdbqt')]
k = sorted(total_sdf) == sorted(total_pdbqt)
assert(k==True)




DIR = args.ligand_path
pdbs = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]


verbose = 10
n_jobs = 2

Protein = {pdb: str(pathlib.Path(args.protein_path)) for pdb in pdbs}
Ligand = {pdb: str(pathlib.Path(f'{args.ligand_path}/{pdb}')) for pdb in pdbs}

with Parallel(n_jobs=n_jobs, verbose=verbose) as parallel:
    list = parallel(delayed(GetECIF)(Protein[pdb], Ligand[pdb], distance_cutoff=6.0) for pdb in pdbs)


features = {pdb: list for pdb, list in zip(pdbs, list)}
features_new1 = pd.DataFrame.from_dict(features).T
features_new1.columns = PossibleECIF
features_new1


file = pd.read_csv('score.txt')
file.columns = ['feature value']
#file = file.tail(-1)
file = file['feature value'].str.split(r'\s', n=1, expand=True)
file.columns = ['feature', 'value']
term = file['value']
term = pd.to_numeric(term)
terms = term.to_list()
term = file['feature']
term = term.to_list()

def get_vina_terms(file):
    file = pd.read_csv(file, index_col=False)
    file.columns = ['feature value']
    #file = file.tail(-1)
    file = file['feature value'].str.split(r'\s', n=1, expand=True)
    file.columns = ['feature', 'value']
    term = file['value']
    term = pd.to_numeric(term)
    terms = term.to_list()
    return terms


Protein = {pdb: (f'{args.vina_score_path}/{pdb[:-4]}.txt') for pdb in pdbs}

with Parallel(n_jobs=n_jobs, verbose=verbose) as parallel:
    list = parallel(delayed(get_vina_terms)(Protein[pdb]) for pdb in pdbs)

features = {pdb: list for pdb, list in zip(pdbs, list)}
features_new2 = pd.DataFrame.from_dict(features).T
features_new2.columns = term

vina_ecif = pd.merge(features_new2, features_new1, left_index=True, right_index=True)
vina_ecif.to_csv('vina_ecif_features.csv')
