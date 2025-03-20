# SG-ML-PLAP
# Structure-Guided Machine-Learning–based Protein-Ligand Affinity Predictor
<img="http://202.54.226.242/plap/static/Abstract_image.jpg"/>
Go to http://www.nii.ac.in/sg-ml-plap.html server and download the code for follwing steps
## 1) Download the directory SG-ML-PLAP from GitHub
## 2) Go to the directory using the command "cd SG-ML-PLAP"
## 3) create conda environment
conda env create -f MLSF_env.yml
conda activate SG-ML-PLAP

## 4) Or manually create the environment by following steps below:
conda create -n MLSF_env -c conda-forge scikit-learn=1.0.2
conda activate MLSF_env
conda install conda-forge::pandas
conda install anaconda::numpy
pip install rdkit
conda install conda-forge::openbabel

## 5) Install ADFR-suite from a website https://ccsb.scripps.edu/adfr/downloads/
After installing, add exact path of "prepare_ligand" and "prepare_receptor" script provided in ADFRsuite-1.0 folder to all three shell scripts (ecif_vina_redocked_trained.sh, ecif_vina_crystal_trained.sh, and ecif_redocked_trained.sh)

## 6) Update exact location path in ecif_vina_redocked_trained.sh, ecif_vina_crystal_trained.sh, and ecif_redocked_trained.sh scripts before running in the terminal (Unless you want to get ugly errors :p).


# Prediction of protein-ligand affinity

## 1) ENTER SG-ML-PALP_MODEL directory by "cd SG_ML_PLAP/SG_ML_PLAP_prediction"

## 2) ECIF-REDOCKED trained scoring function
## -----------------------------------------
./ecif_redocked_trained.sh --job_name-- --ligand_folder_path{pdb_files of ligands}-- --receptor_file{pdb file of receptor}--
ex. ./ecif_redocked_trained.sh sapna example_folder/pdbbinde_pdb example_folder/new.pdb

## 3) ECIF-VINA crystal trained scoring function
## ---------------------------------------------
./ecif_vina_crystal_trained.sh --job_name-- --ligand_folder_path{pdb_files of ligands}-- --receptor_file{pdb file of receptor}--
ex. ./ecif_vina_crystal_trained.sh sapna example_folder/pdbbinde_pdb example_folder/new.pdb

## 4) ECIF-VINA RDOCKED trained scoring function
## ---------------------------------------------
./ecif_vina_redocked_trained.sh --job_name-- --ligand_folder_path{pdb_files of ligands}-- --receptor_file{pdb file of receptor}--
ex. ./ecif_vina_redocked_trained.sh sapna example_folder/pdbbinde_pdb example_folder/new.pdb
