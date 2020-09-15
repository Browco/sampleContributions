#!/usr/bin/env python3
__description__ = \
"""
This script was created to extract the fusion genes \
names from each prediction tool file according to each file caracteristics .
"""
__author__ = "Coralie Capron"
__date__ = "05.2020"

from argparse import ArgumentParser
#import json  # read FG Pizzly prediction file
from os.path import join 
import os
class ParseFusionFile():
    def __init__(self, fusion_file, file_truth=None):
        self.fusion_file = fusion_file
        self.file_truth = file_truth if file_truth is not None else []

    def get_truth_set(self):
        '''
        Get gene fusions from the truth set
        args : file_truth <file.dat> 
        return :  FG_truth <list>
        '''
        with open(self.file_truth, "r") as file:
            FG_truth = [line.strip().split("|")[1] for line in file]
        print("truth")
        print(FG_truth)
        return FG_truth

    def recognize_FGDetection_tool(self):
        '''
        Recognize by which tool the FG file was created
        args : fusion_file <file.tsv> 
        return :  toolName  <str>
        '''
        toolName = None
        with open(self.fusion_file) as ffile:
            first_line = ffile.readline()
            if first_line.startswith("#FusionName") and (len(first_line.strip().split("\t")) > 14):
                toolName = "STARFUSION"
            elif first_line.startswith("#gene1"):
                toolName = "ARRIBA"
            elif first_line.startswith("# chrom1"):
                toolName = "SQUID"
    #            elif first_line.startswith("#FusionName") && (len(first_line.strip().split("\t")) <14:
    #                toolName = "TRINITYFUSION"
    #       elif ffile.name.endswith(".json"):
                # toolName = "PIZZLY"
        return toolName

    def get_predicted_FG_from_merged(self):
        ''' Retrieve the Gene fusions and tool used according to their specific
        columns in the different FG detection tools output. Gene Fusion will be named
        like the STAR-FUSION output : GENE1--GENE2 
        args : fusion_file <file.tsv>  
        dict_tool_FG <dict> 
        '''
        gene_fusion = []
        dict_tool_FG = {}
        with open(self.fusion_file) as ffile:
            if os.path.getsize(self.fusion_file) != 0:
                gene_fusion = [line.strip() for line in ffile if not line.startswith(".") and line not in gene_fusion]
                print(gene_fusion)
            else:
                gene_fusion = [] #if file is empty, no fusion genes are predicted
        dict_tool_FG["combinedPred"] = gene_fusion
        print("predicted")
        print(dict_tool_FG)
        return dict_tool_FG
        
    def get_predicted_FG(self):
        ''' Retrieve the Gene fusions and tool used according to their specific
        columns in the different FG detection tools output. Gene Fusion will be named
        like the STAR-FUSION output : GENE1--GENE2 
        args : fusion_file <file.tsv>  
        dict_tool_FG <dict> 
        '''
        gene_fusion = []
        toolName = self.recognize_FGDetection_tool()
        dict_tool_FG = {}
        with open(self.fusion_file) as ffile:
            next(ffile)
            if toolName == "STARFUSION":
                gene_fusion = [line.strip().split("\t")[0].upper()
                               for line in ffile]
            elif toolName == "ARRIBA":
                gene_fusion = [line.strip().split("\t")[0].upper(
                    ) + "--" + line.strip().split("\t")[1].upper() for line in ffile]
            elif toolName == "SQUID":
                gene_fusion = [line.strip().split("\t")[11].upper().replace(":","--") for line in ffile]
#            If Pizzly was used : 
#           elif ffile.name.endswith(".json"):
                # gene_fusion=[]
                # jsonFile = json.load(ffile)
                # i = 0
                # FG_elements = jsonFile['genes']
                # for i in FG_elements:
                #     i += 1
                #     gene_fusion.append(FG_elements["geneA"]["name"]+
                # "--"+FG_elements["geneB"]["name"])
        dict_tool_FG[toolName] = gene_fusion
        return dict_tool_FG

    def write_fusionGenes(self,output):
        ''' Write a file with only fusion genes
        args : predicted_FG <dict>
        return : FG_file <list_FG.txt>
        '''

        prefix=self.fusion_file
        fg_dict = self.get_predicted_FG()
        print(fg_dict)
        for tool, FGs in fg_dict.items():
            fusionGenes = {}
            basefile="list_FG_"+str(tool)+".txt"
            namefile= join(output,basefile)
            with open(namefile,"a+") as FG_file:
                for FG in FGs:
                    if FG not in fusionGenes.values() and (FG != "." and FG.split("--")[0]!= FG.split("--")[1]) and ("," not in FG):
                        fusionGenes[tool]=FG
                        FG_file.write(FG+"\n")

def main():
    parse = ParseFusionFile(fusion_file,file_truth)
if __name__ == "__main__":
    main()

