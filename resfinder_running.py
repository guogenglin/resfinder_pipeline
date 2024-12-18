# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:46:33 2024

@author: Genglin Guo
@e-mail: 2019207025.njau.edu.cn
"""

import pathlib
import subprocess
import sys
import shutil

def run_resfiner(workpath):
    # iterate every genome file in this filefolder
    for genome_file in pathlib.Path(workpath).iterdir():
        if not str(genome_file).endswith('.fasta'):
            continue
        else:
            # pathlib iterdir will return a full-length workpath, we only need the last one, which is the file name
            genome_file = str(genome_file).split('\\')[-1]
            # strip the suffix to get the file name, as the output file 
            output = genome_file.strip('.fasta')
            # run resfinder
            command = 'run_resfinder.py -l 0.6 -t 0.9 --ignore_missing_species -acq -d -ifa {} -o {}'.format(genome_file, output)
            subprocess.run(command, shell=True)


def generate_output(workpath):
    # def a dict, bac_name as key, detected amrg table as value
    amr = dict()
    dis = dict()
    # create collection correspond filefolder
    try:
        pathlib.Path('amr').mkdir()
        pathlib.Path('disinfectant').mkdir()
    except:
        print('"amr" and "disinfectant" is already exist.')
    # then start to manipulate the output
    for res_results in pathlib.Path(workpath).iterdir():
        if not pathlib.Path(res_results).is_dir():
            continue
        # aviod the detection of result file folder
        elif str(res_results).split('\\')[-1] == 'disinfectant' or str(res_results).split('\\')[-1] == 'amr':
            continue
        else:
            try:
                # get the name of bacteria isolate
                bac_name = str(res_results).split('\\')[-1]
                # located the target result files
                res_result_path = res_results / 'ResFinder_results_table.txt'
                dis_result_path = res_results / 'DisinFinder_results_table.txt'
                # copy all result to one filefolder
                collect_all_result(workpath, bac_name, res_result_path, dis_result_path)
                # open the files
                res_result = open(res_result_path, 'rt')
                dis_result = open(dis_result_path, 'rt')
                # summarize the results
                sum_res = summarize_result(bac_name, res_result)
                sum_dis = summarize_result(bac_name, dis_result)
                # add the result to dict
                amr[bac_name] = sum_res
                dis[bac_name] = sum_dis
                # close the file
                res_result.close()
                dis_result.close()
            except:
                print('Please check filefolder {}'.format(res_results))
                sys.exit(0)
    # generate output
    write_to_output(workpath, amr, 'res')
    write_to_output(workpath, dis, 'dis')

def collect_all_result(workpath, bac_name, res_result_path, dis_result_path):
    # set the name of new file
    new_res_path = workpath / 'amr' / str(bac_name + '.txt')
    new_dis_path = workpath / 'disinfectant' / str(bac_name + '.txt')
    # copy to the location
    shutil.copy(res_result_path, new_res_path)
    shutil.copy(dis_result_path, new_dis_path)
            
def summarize_result(bac_name, result_file):
    # create a table with another table composed by amrg and identity as one value
    amrgs = []
    amrg = ''
    identity = ''
    location = ''
    # iterate the result file
    for line in result_file:
        # filter the amrg line.
        if len(line.strip().split('	')) < 9:
            continue
        elif line.strip().startswith('Resistance'):
            continue
        else:
            amrg_info = line.strip().split('	')
            # filter the overlap prediction
            if amrg_info[0] == amrg or amrg_info[6] == location:
                if not ['Overlap', '100.00'] in amrgs:
                    amrgs.append(['Overlap', '100.00'])
                else:
                    continue
            else:
                # location was used to identity the overlap
                amrg = amrg_info[0]
                location = amrg_info[6]
                identity = amrg_info[1]
                # add the amrg information to the table
                amrgs.append([amrg, identity])
    return amrgs
    
def write_to_output(workpath, summarized_result, outname):
    # head line
    all_detected_genes = ['Isolate', 'Total_number']
    # find all amrgs identified in this round of resfinder
    for amrgs in summarized_result.values():
        for amrg in amrgs:
            if amrg[0] not in all_detected_genes:
                all_detected_genes.append(amrg[0])
            else:
                continue
    # set the output path and open the file, write the head line
    output_path = workpath / str(outname + '_sum_results.txt')
    output = open(output_path, 'wt')
    output.write('\t'.join(all_detected_genes))
    output.write('\n')
    # screen the result of every bacteria isolate find the present and absent gene and their identity
    for bac_name, amrgs in summarized_result.items():
        line = [bac_name]
        number = 0
        amrg_table = []
        for ref_amrg in all_detected_genes[1:]:
            identity = 'NA'
            for i in range(len(amrgs)):
                if ref_amrg == amrgs[i][0]:
                    identity = amrgs[i][1]
                    if not ref_amrg ==' Overlap':
                        number += 1
            amrg_table.append(identity)
        line.append(str(number))
        line += amrg_table
        output.write('\t'.join(line))
        output.write('\n')
    output.close()

def main():
    # open the work filefolder and locate it
    workpath = pathlib.Path.cwd()
    # do resfinder
    run_resfiner(workpath)
    # summerize the result
    generate_output(workpath)
    
main()