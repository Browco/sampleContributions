from argparse import ArgumentParser

def fusion_genes_and_tools(fileArriba, fileSF, fileSQUID, filename):
    '''
        Write in a file the predicted fusion genes merged from the 3tools
        and append next to each FG the prediction tools
        args : predicted fusions <txt file>
        return : merged file <txt file>
    '''

    dict_fusions = {}
    # filename= filename+"_with_tools"

    with open (fileArriba,"r") as farriba:
        for fusion in farriba:
            if fusion.strip() not in dict_fusions.keys():
                dict_fusions[fusion.strip()]=["Arriba"]
    with open (fileSF,"r") as fSF:
        for fusion in fSF:
            if fusion.strip() not in dict_fusions.keys():
                dict_fusions[fusion.strip()]=["Star-Fusion"]
            elif fusion.strip() in dict_fusions.keys() and "Star-Fusion" not in dict_fusions[fusion.strip()]:
                dict_fusions[fusion.strip()].append("Star-Fusion")

    with open (fileSQUID,"r") as fsquid:
        for fusion in fsquid:
            if fusion.strip() not in dict_fusions.keys():
                dict_fusions[fusion.strip()]=["Squid"]
            elif fusion.strip() in dict_fusions.keys() and "Squid" not in dict_fusions[fusion.strip()]:
                dict_fusions[fusion.strip()].append("Squid")

    with open (filename,"w") as out:
        for key in dict_fusions.keys():
            tools = ','.join(dict_fusions[key])
            towrite = key+'\t'+tools+'\n'
            out.write(towrite)


def cat_files(fileArriba, fileSF, fileSQUID, filename):
    '''
        Write in a file the predicted fusion genes merged from the 3tools
        args : predicted fusions <txt file>
        return : merged file <txt file>
    '''

    list_fusions = []
    with open (fileArriba,"r") as farriba:
        for fusion in farriba:
            if fusion not in list_fusions:
                list_fusions.append(fusion)
    with open (fileSF,"r") as fSF:
        for fusion in fSF:
            if fusion not in list_fusions:
                list_fusions.append(fusion)
    with open (fileSQUID,"r") as fsquid:
        for fusion in fsquid:
            if fusion not in list_fusions:
                list_fusions.append(fusion)
    with open (filename,"w") as out:
        for elt in list_fusions:
            out.write(elt)
                
if __name__ == "__main__":
    parser = ArgumentParser(description='Process some integers')
    parser.add_argument("-f1", "--arriba_fusions", dest="arriba_fusions",
                        help="File with fusions predicted by arriba",
                        required=True),
    parser.add_argument("-f2", "--SF_fusions", dest="SF_fusions",
                        help="File with fusions predicted by STAR-Fusion",
                        required=True),
    parser.add_argument("-f3", "--squid_fusions", dest="squid_fusions",
                        help="File with fusions predicted by SQUID",
                        required=True),    
    parser.add_argument("-o", "--output_filename", dest="filename",
                        help="Output file name", required=True)
    
    args = parser.parse_args()

    #compare_fusion_to_db(args.predicted_fusion, args.fusion_db)
    # cat_files(args.arriba_fusions, args.SF_fusions, args.squid_fusions, args.filename)
    fusion_genes_and_tools(args.arriba_fusions, args.SF_fusions, args.squid_fusions, args.filename)
