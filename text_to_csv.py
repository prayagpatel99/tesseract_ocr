from pdf2image import convert_from_path
from pytesseract import image_to_string
import pytesseract
import os
import re

list_of_files = os.listdir(r'C:\Users\patelp21\Downloads\Code File\Code File\2007_to_2013\pdfs')

list_of_txts = [val for val in list_of_files if val.endswith(".txt")]

os.chdir(r'C:\Users\patelp21\Downloads\Code File\Code File\2007_to_2013\pdfs')

def count_of_elements(list):
    dict_count = {}
    element_list = []
    for each_element in list:
        dict_count[each_element] = list.count(each_element)
    b = {key: value for key, value in dict_count.items() if value==1 or key == 'ARBITRATION PANEL'}
#     keyslist = list(b.keys())
    return b.keys()

import pandas as pd
df = pd.DataFrame()
superset = []
pdfs = []
# new_dict = {}
for each_file in list_of_txts:
    new_dict = {}
    f = open(each_file, "r")
    text = f.read()
    text = text.replace('\n', ' ')
    Case_ID = re.findall(r'\d{2}[-.]\d{5}',text)
    if len(Case_ID) >= 1:
        Case_ID = Case_ID[0]
    else:
        Case_ID = " "
    split_strings = (re.findall(r'\b[A-Z]+(?:\s+[A-Z]+)*\b', text))
    split_strings = [s for s in split_strings if(len(s)>5 or s == 'AWARD' or s == 'FEES')]
    try:
        get_index = split_strings.index('REPRESENTATION OF PARTIES')
        split_strings = split_strings[get_index:]       
    except:
        pdfs.append(each_file)
#     split_strings = [item for item in split_strings if item != 'FINRA']
    split_strings = list(count_of_elements(split_strings))
    superset.extend(split_strings)
#     print(each_file)
#     new_dict[each_file] = split_strings
    new_dict['File_Name'] = each_file
    new_dict['Case_ID'] = Case_ID
    for n in range(len(split_strings)):
        if n == len(split_strings) -1:
            new_dict[split_strings[n]] = re.findall('(?<=\s{}).*'.format(split_strings[n]),text)
        else:
            new_dict[split_strings[n]] = re.findall("(?<=\s{}".format(split_strings[n]) + ")(.*)" + "(?=\s{}".format(split_strings[n+1]) + ")",text, re.DOTALL)

#         new_dict[split_strings[n]] = re.findall("(?<=\s{}".format(split_strings[n]) + ")(.*)" + "(?<=\s{}".format(split_strings[n+1]) + ")",text, re.DOTALL)
#     length.append(len(split_strings))
    df = df.append(new_dict, ignore_index=True)
# return (re.findall(r'\w{' + str(count) + ',}', string))

# superset_manual = ['']
superset_unique = list(set(superset))
# superset_unique

dict_count = {}
element_list = []
for each_element in superset:
    dict_count[each_element] = superset.count(each_element)

parent_dict = {'REPRESENTATION OF PARTIES': [], 'CASE INFORMATION':[], 'CASE SUMMARY':[], 'RELIEF REQUESTED':[], 'OTHER ISSUES': [],'DECIDED':[],'OTHER ISSUES CONSIDERED AND DECIDED': [] , 'AWARD':[], 'FEES':[],'ARBITRATION PANEL': [],'ARBITRATOR':[], 'AFFIRMATION': [],'NATURE OF THE DISPUTE':[],'FINDINGS AND CONCLUSIONS':[]}

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

columns_used= []
score_dict = {'REPRESENTATION OF PARTIES': 0.6, 'CASE INFORMATION': 0.8, 'CASE SUMMARY':0.6, 'RELIEF REQUESTED':0.6, 'OTHER ISSUES': 0.9, 'DECIDED':0.6, 'OTHER ISSUES CONSIDERED AND DECIDED': 0.6,'AWARD':0.6, 'FEES':0.6, 'ARBITRATION PANEL':0.7, 'ARBITRATOR':0.8, 'AFFIRMATION': 0.9, 'NATURE OF THE DISPUTE':0.6,'FINDINGS AND CONCLUSIONS':0.5}
for each_key in parent_dict:
    for each_element in df.columns:
        score = similar(each_key, each_element)
        if score>= score_dict[each_key]:
            parent_dict[each_key].append(each_element)
            columns_used.append(each_element)

updated_dictionary = {}
updated_dictionary['File_Name'] = df['File_Name']
updated_dictionary['Case_ID'] = df['Case_ID']
for each_key in parent_dict:
    print(each_key)
    df_subset = df[list(parent_dict[each_key])]
#     df_subset
    for each_column in df_subset:
        df_subset[each_key] = df_subset[each_key].fillna(df_subset[each_column])
    print(df_subset[each_key])
    updated_dictionary[each_key] = df_subset[each_key]
#     updated_df = pd.concat([updated_df, df_subset], axis=1)

updated_df = pd.DataFrame.from_dict(updated_dictionary)

import numpy as np
updated_df['OTHER ISSUES CONSIDERED AND DECIDED'].replace(r"[' &']", np.NaN)

updated_df.to_csv('raw_data_09_18_2022.csv', index = False)