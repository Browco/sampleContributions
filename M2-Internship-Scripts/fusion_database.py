#!/usr/bin/env python3
__description__ = \
"""
This script was created to extract, compare and write fusion genes \
from the FusionHub database in order to compare these fusion genes \
to the predicted fusion genes. 
"""
__author__ = "Coralie Capron"
__date__ = "07.2020"

import os
import csv
from argparse import ArgumentParser

def parse_db(file):
    '''
        This function parses fusionHub database file and creates a dict which 
        allows to access informations as databases names and how many times a
        fusion gene is found in these databases
        args : database file <txt file>
        return : database <dict>
    '''
    
    dict_fusionDB = {}
    with open (file,"r") as file_db: 
        header = file_db.readline().strip().split("\t") #save header for later
        next(file_db) #skip header 
        for line in file_db:
            if "+" in line : 
                db = []
                fusion = line.strip().split("\t")[0]
                found_nb = line.strip().split("\t")[29]
                for i in range(len(line.strip().split("\t"))):
                    if line.strip().split("\t")[i] == "+":
                        db.append(header[i])
                    else: 
                        continue
            dict_fusionDB[fusion]=(found_nb,db) 
            #dict with all fusion as key and (nb, databases).      
    return(dict_fusionDB)
  
def compare_fusion_to_db(predicted_fusion, fusion_db):
    '''
        This function compares the predicted fusion genes found with fusionHub 
        database to see if the fusion gene is recorded in some databases and in 
        how many of them.   
        args : prediction fusion genes <txt file>, fusions database <dict>
        return : database values <tuple>
    '''
    dict_db = parse_db(fusion_db)
    list_fusion=[]
    with open (predicted_fusion,"r") as file_fusions:
        for line in file_fusions:
            FG = line.split("\t")[0]
            tool = line.split("\t")[1]
            fusion = FG.strip().upper()
            reverse_fusion = fusion.split("--")[1]+'--'+fusion.split("--")[0]
            if fusion in dict_db.keys() :
                list_fusion.append((fusion,dict_db.get(fusion),tool))
            elif reverse_fusion in dict_db.keys():
                list_fusion.append((reverse_fusion,dict_db.get(reverse_fusion),tool))
            else:
                continue
    return list_fusion

def write_summary_fusions(predicted_fusion, fusion_db, filename):
    '''
        Write in a csv file the predicted fusion genes and databases associated 
        args : predicted fusions <txt file>, fusion database <dict>, 
        output filename <string>
        return : databases associated with fusion genes <csv file>
    '''

    list_fusion = compare_fusion_to_db(predicted_fusion, fusion_db)
    with open(filename, 'a+') as csvfile:
        writer = csv.writer(csvfile, delimiter = '\t')
        if os.path.getsize(filename) == 0:
            #if file is empty write header then items
            writer.writerow(['fusion_genes', 'Nb_databases', 'db_names'])
            for info_fusion in list_fusion :
                fusion = info_fusion[0]
                nb_db = info_fusion[1][0]
                db_names = info_fusion[1][1]
                tool = info_fusion[2]
                writer.writerow([fusion,nb_db,','.join(db_names),','.join(tool)])  
        else :
            for info_fusion in list_fusion :
                fusion = info_fusion[0]
                nb_db = info_fusion[1][0]
                db_names = info_fusion[1][1]
                tool = info_fusion[2]
                writer.writerow([fusion,nb_db,','.join(db_names),','.join(tool)])  
                
if __name__ == "__main__":
    parser = ArgumentParser(description='Process some integers')
    parser.add_argument("-f", "--pred_fusions", dest="predicted_fusion",
                        help="File with only predicted fusions written as fusion1--fusion2",
                        required=True),
    parser.add_argument("-d", "--fusion_database", dest="fusion_db",
                        help="Database from fusionHub project, txt fusions file",
                        required=True),
    parser.add_argument("-o", "--output_filename", dest="filename",
                        help="Output file name", required=True)
    
    args = parser.parse_args()

    #compare_fusion_to_db(args.predicted_fusion, args.fusion_db)
    write_summary_fusions(args.predicted_fusion, args.fusion_db, args.filename)