#!/usr/bin/env python
# coding: utf-8


import sys
import os
import argparse


parser = argparse.ArgumentParser(description='This tool harmonizes flow versions in bilingual stf translation files exported from Salesforce to the latest available version. Useful for deploying flow translations in Salesforce with different version numbers.')
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("-f","--file",dest="file", help="specify the bilingual .stf file to be merged or leave empty if all current directory shall be considered.")
group.add_argument("-d","--directory",dest="directory", help="specify a directory with several stf files to be merged")

args=parser.parse_args()
argfile=args.file
directory=args.directory
def merge_flow_translations(filepath):
    filepath = filepath
    headerlines=[]

    if not os.path.isfile(filepath):
        print("File {} does not exist...".format(filepath))

    searchterm="Flow.Flow."
    flow_with_version_and_translatable_items={}
    
    
    with open(filepath, encoding="utf8") as fp:
        cnt=0
        reading_behind_header=False
        for line in fp:
            cnt=cnt+1    
            if not reading_behind_header:
                headerlines.append(line)
                if '-TRANSLATED-' in line:
                    reading_behind_header=True     
                continue                      
            if searchterm in line:     
               
                splittedLine=line.strip().split('.')
                if splittedLine[3].isdigit(): #if flow element has number (applicable for flow elements considered here)
                    flowname=splittedLine[2]
                    flowversion=int(splittedLine[3])
                    lowindex=line.find(str(flowversion))+len(str(flowversion))+1
                    highindex=line.find("\t")
                    translatable_element=line[lowindex:highindex]
                    translation_value='.'.join(splittedLine[4:]).split("\t")[1:-1]
                    if len(translation_value)>0: #has a translation value
                        if flowname not in flow_with_version_and_translatable_items:
                            flow_with_version_and_translatable_items[flowname]={}
                        if translatable_element not in flow_with_version_and_translatable_items[flowname]:
                            flow_with_version_and_translatable_items[flowname][translatable_element]={}                    
                        flow_with_version_and_translatable_items[flowname][translatable_element][flowversion]=translation_value

    newfile='merged_'+filepath
    #print(flow_with_version_and_translatable_items)
    with open(newfile,"w+", encoding="utf8") as f:
        for line in headerlines:
            f.write(line)
        for k in flow_with_version_and_translatable_items.keys():
            highest_flow_version=0
            flow_name=k
            for i in flow_with_version_and_translatable_items[flow_name]:
                translatable_element=i
                
                translation_value=flow_with_version_and_translatable_items[flow_name][translatable_element]
                latest_flow_version_for_translatable_element=max(flow_with_version_and_translatable_items[flow_name][translatable_element])
                
                to_write_default_value=''
                to_write_translated_value=''
                
                for translationValue in flow_with_version_and_translatable_items[k][i].values():   
                    if translationValue!='':
                        to_write_default_value=translationValue[0]
                        to_write_translated_value=translationValue[1]
                if highest_flow_version>latest_flow_version_for_translatable_element:
                    latest_flow_version_for_translatable_element=highest_flow_version
                else:
                    highest_flow_version=latest_flow_version_for_translatable_element
                to_write_part1="Flow.Flow."+flow_name+"."+str(latest_flow_version_for_translatable_element)+'.'+translatable_element
                full_line=to_write_part1+'\t'+to_write_default_value+'\t'+to_write_translated_value+'\t'+'-'
                f.write(full_line+"\n")



if argfile==None:
    print("harmonizing files in directory "+directory)    
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(directory):
        os.chdir(directory)
        path = root.split(os.sep)
        for file in files:       
            if os.path.isfile(file):                
                if '.stf' in file:     
                    print("about to merge "+file)
                    merge_flow_translations(file)
else:
    print("harmonizing single file "+argfile)
    merge_flow_translations(argfile)





