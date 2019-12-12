#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
import argparse


# In[2]:


parser = argparse.ArgumentParser(description='This tool harmonizes flow versions in bilingual stf translation files exported from Salesforce to the latest available version. Useful for deploying flow translations in Salesforce with different version numbers.')
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("-f","--file",dest="file", help="specify the bilingual .stf file to be merged or leave empty if all current directory shall be considered.")
group.add_argument("-d","--directory",dest="directory", help="specify a directory with several stf files to be merged")
#parser.add_argument("-v", "--version", help="specify the target version that the flow elements shall be merged to",de)

args=parser.parse_args()
argfile=args.file
directory=args.directory
#print("directory arg {}".format(directory))
#print("file arg {}".format(argfile))

def merge_flow_translations(filepath):
    #print("File path {}".format(filepath))
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
            #print("line {} contents {}".format(cnt, line))
            cnt=cnt+1    
            if not reading_behind_header:
                headerlines.append(line)
                if '-TRANSLATED-' in line:
                    #print("found keyword in line nr {}, {}".format(cnt, line))
                    reading_behind_header=True     
                continue                      
            if searchterm in line:     
               
                splittedLine=line.strip().split('.')
                #print("found flow item in line {}, content is {}".format(cnt, splittedLine))
                if splittedLine[3].isdigit(): #if flow element has number (applicable for flow elements considered here)
                    flowname=splittedLine[2]
                    flowversion=int(splittedLine[3])
                    lowindex=line.find(str(flowversion))+len(str(flowversion))+1
                    highindex=line.find("\t")
                    #print("lowindex is {}, highindex is {}".format(lowindex, highindex))
                    translatable_element=line[lowindex:highindex]
                    translation_value='.'.join(splittedLine[4:]).split("\t")[1:-1]
                    if len(translation_value)>0: #has a translation value
                        #print("flow version {}".format(flowversion))
                        #print("found element {}, value {}".format(translatable_element, translation_value))
                        #print("adding flowname {}, version {}, translatable element {}, translation value {}".format(flowname, flowversion,translatable_element,translation_value))
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
                #for j in flow_with_version_and_translatable_items[flow_name][translatable_element]:
                    #print("Flow {} with version number {} for item {} contains following translated value: {}".format(flow_name,str(j),translatable_element,flow_with_version_and_translatable_items[flow_name][translatable_element][j]))
                
                translation_value=flow_with_version_and_translatable_items[flow_name][translatable_element]
                latest_flow_version_for_translatable_element=max(flow_with_version_and_translatable_items[flow_name][translatable_element])
                
                to_write_default_value=''
                to_write_translated_value=''
                #print("maximum version for {} is {}".format(translatable_element,latest_flow_version_for_translatable_element))
                #print("to_write_part2: {}".format(flow_with_version_and_translatable_items[k][i].get(latest_flow_version_for_translatable_element)))
                
                for translationValue in flow_with_version_and_translatable_items[k][i].values():   
                    #print("traversing flow {}, for element {}".format(flow_name,translatable_element))
                    #print("translationValue {}".format(translationValue))
                    if translationValue!='':
                        to_write_default_value=translationValue[0]
                        to_write_translated_value=translationValue[1]
                
                #if len(flow_with_version_and_translatable_items[k][i].get(latest_flow_version_for_translatable_element))>0:
                    #to_write_part2=flow_with_version_and_translatable_items[k][i].get(latest_flow_version_for_translatable_element)[0]+'\t'
                #else:
                    #has_translation=False
                #if len(flow_with_version_and_translatable_items[k][i].get(latest_flow_version_for_translatable_element))>1:
                    #to_write_part3=flow_with_version_and_translatable_items[k][i].get(latest_flow_version_for_translatable_element)[1]+'\t'+'-'
                #else:
                    #to_write_part3=''
                    #has_translation=False
                if highest_flow_version>latest_flow_version_for_translatable_element:
                    latest_flow_version_for_translatable_element=highest_flow_version
                else:
                    highest_flow_version=latest_flow_version_for_translatable_element
                to_write_part1="Flow.Flow."+flow_name+"."+str(latest_flow_version_for_translatable_element)+'.'+translatable_element
                #print("to_write_part2: {}".format(to_write_part2))        
                #if to_write_part2=='':
                    #full_line=to_write_part1+'\t'+to_write_part3
                #else:
                full_line=to_write_part1+'\t'+to_write_default_value+'\t'+to_write_translated_value+'\t'+'-'
                #print("writing: {}".format(full_line))
                f.write(full_line+"\n")


# In[3]:


if argfile==None:
    print("harmonizing files in directory "+directory)    
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(directory):
        os.chdir(directory)
        path = root.split(os.sep)
        #print("traversing path "+path)
        for file in files:       
            if os.path.isfile(file):                
                if '.stf' in file:     
                    print("about to merge "+file)
                    merge_flow_translations(file)
else:
    print("harmonizing single file "+argfile)
    merge_flow_translations(argfile)


# In[ ]:




