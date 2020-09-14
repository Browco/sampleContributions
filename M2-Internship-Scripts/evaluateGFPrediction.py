#!/usr/bin/env python3

from extract_geneFusions import ParseFusionFile
import csv
from argparse import ArgumentParser
import os
import sys
from os.path import join 
class EstimatePrediction():
    def __init__(self,fusion_files, file_truth):
        self.fusion_files = fusion_files
        self.file_truth = file_truth

    def from_tools_extract_geneFusions(self):
        '''
        Retrieve the fusion genes of all tools and store them in a dict.
        Will be usefull to compare what was predicted by which tool.
        args : fusion_files <file.tsv>
        return : dict_tool_FG <dict>
        '''
        dict_allTools_FG = {}
        dict_predictFG = parseFF.get_predicted_FG()
        dict_allTools_FG.update({tool:geneFusion for tool, geneFusion in dict_predictFG.items()})
        print(dict_allTools_FG)
        return dict_allTools_FG

    def from_merge_extract_geneFusions(self):
        '''
        Retrieve the fusion genes of all tools and store them in a dict.
        Will be usefull to compare what was predicted by which tool.
        args : fusion_files <file.tsv>
        return : dict_tool_FG <dict>
        '''
        dict_allTools_FG = {}
        dict_predictFG = parseFF.get_predicted_FG_from_merged()
        dict_allTools_FG.update({tool:geneFusion for tool, geneFusion in dict_predictFG.items()})
        return dict_allTools_FG
        
    def estimate_TP(self):
        '''
        Compare if fusion genes predicted existed based on the truth set, if
        yes, fusion gene is true positive
        args : dict_allTools_FG <dict> and file_truth <file.dat>
        return : true_positives for each tool <dict>
        '''
        dict_allTools_FG = self.from_merge_extract_geneFusions()
        dict_allTools_TP={}
        tpositives=[]
        list_controlFG = parseFF.get_truth_set()
        for tool, FG_list in dict_allTools_FG.items():
            for FG in FG_list:
                genes=FG.split("--")
                inverted_FG=genes[1]+"--"+genes[0]
                if FG in list_controlFG:
                    tpositives.append(FG)
                elif inverted_FG in list_controlFG:
                    tpositives.append(inverted_FG)
            dict_allTools_TP.update({tool:tpositives})
        return dict_allTools_TP
        
    def estimate_FP(self):
        '''
        Compare if fusion genes predicted are in the truth set, if
        no, fusion genes are false positives
        args : dict_allTools_FG <dict> and file_truth <file.dat>
        return : false_positives for each tool <dict>
        '''
        dict_allTools_FG = self.from_merge_extract_geneFusions()
        dict_allTools_FP = {}
        fpositives = []
        list_controlFG = parseFF.get_truth_set()
        for tool, FG_list in dict_allTools_FG.items():
            for FG in FG_list:
                genes=FG.split("--")
                inverted_FG=genes[1]+"--"+genes[0]
                if FG not in list_controlFG:
                    fpositives.append(FG)
                elif inverted_FG not in list_controlFG:
                    fpositives.append(inverted_FG)
            dict_allTools_FP.update({tool:fpositives})
        return dict_allTools_FP

    def estimate_FN(self):
        '''
        Compare if control fusion genes does not exists in predicted fusion genes
        if no, fusion genes control are false negatives
        args : dict_allTools_FG <dict> and file_truth <file.dat>
        return : false_negarives for each tool <dict>
        '''
        dict_allTools_FG = self.from_merge_extract_geneFusions()
        list_controlFG = parseFF.get_truth_set()
        dict_allTools_FN = {}
        fnegatives = []
        for tool, FG_list in dict_allTools_FG.items():
            for FG_true in list_controlFG:
                genes=FG_true.split("--")
                print("genes controls")
                print(genes)
                inverted_FG_true=genes[1]+"--"+genes[0]
                if FG_true not in FG_list:
                    fnegatives.append(FG_true)
                elif inverted_FG_true not in FG_list:
                    fnegatives.append(inverted_FG_true)
            dict_allTools_FN.update({tool:fnegatives})
        return dict_allTools_FN

    def estimate_PPV(self):
        '''
        Calculates the prediction performance of each tool.
        args : dict_allTools_TP <dict> and dict_allTools_FP <dict>
        return : PPV  <dict>
        '''
        dict_PPV = {}
        dict_allTools_TP = self.estimate_TP()
        dict_allTools_FP = self.estimate_FP()
        print(dict_allTools_TP)
        print(dict_allTools_FP)
        #If tool is the same in dicts FP and TP then retrieve the TP/FP values
        predictions = {tool_TP:(FG_list_TP, dict_allTools_FP[tool_TP]) for tool_TP,
         FG_list_TP in dict_allTools_TP.items() if tool_TP in dict_allTools_FP}
        for tool, pred in predictions.items():
            TP_nb = len(pred[0])
            print("TP_nb")
            print(TP_nb)
            FP_nb = len(pred[1])
            print("FP_nb")
            print(FP_nb)
            PPV = round(TP_nb/(TP_nb+FP_nb),3)
            dict_PPV.update({tool:PPV})
        return dict_PPV

    def estimate_Sensitivity(self):
        '''
        Calculates the sensitivity of each tool.
        args : dict_allTools_TP <dict> and dict_allTools_FP <dict>
        return : sentivity  <dict>
        '''
        dict_sensi = {}
        dict_allTools_TP = self.estimate_TP()
        dict_allTools_FN = self.estimate_FN()
        predictions = {tool_TP:(FG_list_TP, dict_allTools_FN[tool_TP])for tool_TP, 
        FG_list_TP in dict_allTools_TP.items() if tool_TP in dict_allTools_FN}
        print("tpr")
        print(predictions)
        for tool, pred in predictions.items():
            TP_nb = len(pred[0])
            FN_nb = len(pred[1])
            sensitivity = round(TP_nb/(TP_nb + FN_nb),3)
            dict_sensi.update({tool:sensitivity})
        return dict_sensi

    def write_output_metrics(self,output):
        dict_PPV = self.estimate_PPV()
        dict_sensi = self.estimate_Sensitivity()
        print(dict_sensi)
        output_dict = {tool:(PPV, dict_sensi[tool])for tool, PPV in dict_PPV.items() if tool in dict_sensi}
        namefile= join(output,'tools_PPV_metrics.csv')
        with open(namefile, 'a+') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            if os.path.getsize(namefile) == 0:
                writer.writerow(['tool', 'sensitivity', 'precision'])
                for tool, metric in output_dict.items():
                    PPV = metric[0]
                    TPR = metric[1]
                    writer.writerow([tool,PPV, TPR])
            else :
                for tool, metric in output_dict.items():
                    PPV = metric[0]
                    TPR = metric[1]
                    writer.writerow([tool,PPV, TPR])

if __name__ == "__main__":
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument("-t", "--truth_set", dest="truth_set",
                        help="Specify input file with genes fusions if needed")
    parser.add_argument("-f", "--fusion_files", dest="fusion_files",
                        help="Specify input file with genes fusions.",
                        nargs='+', required=True),
    parser.add_argument("-w", "--write_gflist", dest="write_gf",
                        help="If selected, will only write predicted GFusions",
                        action="store_true"),
    parser.add_argument("-o", "--output", dest="output",
                        help="Specify an output directory",
                        nargs='?',default=sys.stdout)

    args = parser.parse_args()
#There is two ways to use this class :
#Either you just want to extract predicted fusion genes (first condition)
#Or you want to estimate gene fusion prediction accuracy (last condition)
    if args.write_gf is True and args.truth_set is None:
        parseFF= ParseFusionFile(args.fusion_files)
        print("HA")
        for file in args.fusion_files:
            parseFF= ParseFusionFile(file)
            parseFF.write_fusionGenes(args.output)
    elif args.write_gf is True and args.truth_set is not None:
        raise ValueError ("Can't write fusion genes if -t option is activated") 
    elif args.write_gf is False and args.truth_set is None:
        raise ValueError ("Can't estimate accuracy of prediction if -t option is deactivated") 
    elif args.write_gf is False and args.truth_set is not None:
        parseFF= ParseFusionFile(args.fusion_files, args.truth_set)

        estimation = EstimatePrediction(args.fusion_files, args.truth_set)
        print(args.fusion_files)
        for file in args.fusion_files:
            parseFF= ParseFusionFile(file, args.truth_set)
            estimation = EstimatePrediction(file, args.truth_set)
            estimation.write_output_metrics(args.output)
            print(estimation.estimate_Sensitivity())
            try:
                print(estimation.estimate_PPV())
            except ZeroDivisionError as err:
                print("ZeroDivisionError")
            
