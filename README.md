# Resfinder_pipeline
A python pipeline for running local version resfinder


# What is it?
This pipeline is aiming to predict the antimicrobial resistance genes by resfinder for a batch of bacterial genomes, and summarize the result to one file which is easy to observe and for further analysis.


# Installation of resfinder
The website of resfinder (https://github.com/genomicepidemiology/resfinder) has already introduced one way for installation of resfinder, here I will introduce how to install it using conda.

### Create a environment for resfinder (Optional)
```
# Create environment
conda create -n resfinder

# Activate environment
conda activate resfinder
```
### Install resfinder
You can use conda or mamba to install resfinder.
```
conda install resfinder
```
or
```
mamba install resfinder
```
### Databases
Find the place in the filefolder to save the resfinder database, here I will give out an example.
```
./anaconda3/envs/resfinder/lib/python3.12/site-packages/resfinder
```
Download the database to this location
```
git clone https://bitbucket.org/genomicepidemiology/resfinder_db/
git clone https://bitbucket.org/genomicepidemiology/pointfinder_db/
git clone https://bitbucket.org/genomicepidemiology/disinfinder_db/
```
### Set environment variables
open the ~/.bashrc, add these command into it. Here must notice /path/to/some/dir means the location of the database you've downloaded, you need to modify it manually.
```
export CGE_RESFINDER_RESGENE_DB="/path/to/some/dir/resfinder_db"
export CGE_RESFINDER_RESPOINT_DB="/path/to/some/dir/pointfinder_db"
export CGE_DISINFINDER_DB="/path/to/some/dir/disinfinder_db"
```

# Usage
Put this script and those genome files to one filefolder, then run
```
python resfinder_running.py
```
Beyond the results file for every bacteria isolates, 2 filefolder and 2 files will be generated. 2 filefolder named 'amr' and 'disinfectant' contain all correspond result files for those bacteria isolates, and 2 file named 'res_sum_results.tsv' and 'dis_sum_results.tsv' contain the summarized correspond result.

You must be noticed that an extra result named 'Overlap' could be found in the headline of the summarized table, which means there are one gene was predicted as different antimicrobial resistance genes, you should check the result file in the filefolder for the details, if you want to ignore it, you can just remove this column.

# Reminds
This script will default recognize the file with '.fasta' as suffix as the genome file need to be processed, if the suffix of your sequence is others, such as '.fa', you need to add the suffix in the end of the command, for example:
```
python resfinder_running.py fa
```
