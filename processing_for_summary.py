import pandas as pd
import regex as re

df = pd.read_csv(r'C:\Users\patelp21\Downloads\Code File\Code File\2007_to_2013\summary_09_18_2022.csv')

df = df[df['Forum']== 'FINRA']

Representation_of_Parties = df["Case Summary"].tolist()

Claimant = []
Respondent = []
Respondent_Representative = []
Claimant_Representative = []

for i in Representation_of_Parties:
    ClaimantRepresentation = re.findall('(?<=Claimant).*?(?=Claimant Representative)',str(i), re.DOTALL)
    if len(ClaimantRepresentation) == 1:
        Claimant.append(ClaimantRepresentation[0])
    else:
        Claimant.append(" ")

Claimant_Representative =[]
for i in Representation_of_Parties:
    ClaimantRepresentative = re.findall('(?<=Claimant Representative).*?(?=Respondent)',str(i), re.DOTALL)
    if len(ClaimantRepresentative) == 1:
        Claimant_Representative.append(ClaimantRepresentative[0])
    else:
        Claimant_Representative.append(" ")

for i in Representation_of_Parties:
    Res = re.findall('(?<=Respondent).*?(?=Respondent Representative)',str(i), re.DOTALL)
    if len(Res) == 1:
        Respondent.append(Res[0])
    else:
        Respondent.append(" ")

for i in Representation_of_Parties:
    RespondentRepresentative = re.findall('(?<=Respondent Representative).*?(?=Neutral)',str(i), re.DOTALL)
    if len(RespondentRepresentative) == 1:
        Respondent_Representative.append(RespondentRepresentative[0])
    else:
        Respondent_Representative.append(" ")

Neutral=[]
for i in Representation_of_Parties:
    Neu = re.findall('(?<=Neutral).*?(?=Hearing Site)',str(i), re.DOTALL)
    if len(Neu) == 1:
        Neutral.append(Neu[0])
    else:
        Neutral.append(" ")

Hearing_Site =[]
for i in Representation_of_Parties:
    Hs = re.findall('(?<=Hearing Site).*$',str(i), re.DOTALL)
    if len(Hs) == 1:
        Hearing_Site.append(Hs[0])
    else:
        Hearing_Site.append(" ")

df["Claimant"] = Claimant
df["Claimant_Representative"] = Claimant_Representative
df["Respondent"] = Respondent
df["Respondent_Representative"] = Respondent_Representative
df["Neutral"] = Neutral
df["Hearing_Site"] = Hearing_Site
df = df.dropna(axis=0, subset=['Claimant'])

df.to_csv(r'C:\Users\patelp21\Downloads\Code File\Code File\2007_to_2013\final_09_18_2022.csv')

left_df = pd.read_csv(r'C:\Users\patelp21\Downloads\Code File\Code File\2007_to_2013\processed_data_09_18_2022.csv')

combined_df = pd.merge(left_df,df,left_on='Case_ID',right_on = 'Award Document', how='left')
all_cols = combined_df.columns

ordered_df = combined_df[cols]
ordered_df = ordered_df[ordered_df['Forum'] == 'FINRA']
ordered_df.to_csv('processed_2017_2012.csv', index = False)