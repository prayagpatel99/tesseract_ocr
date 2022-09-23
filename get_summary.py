import pandas as pd
import regex as re
import requests
from bs4 import BeautifulSoup

df = pd.read_csv(r'processed_data_09_18_2022.csv')
case_id_list = df["Case_ID"].tolist()

url = 'https://www.finra.org/arbitration-mediation/arbitration-awards-online?aao_radios=case_id&field_case_id_text=09-05158&search=&field_forum_tax=All&field_special_case_type_tax=All&field_core_official_dt%5Bmin%5D=&field_core_official_dt%5Bmax%5D='

frame_combined = pd.DataFrame()
url_first_half = 'https://www.finra.org/arbitration-mediation/arbitration-awards-online?aao_radios=case_id&field_case_id_text='
url_second_half = '&search=&field_forum_tax=All&field_special_case_type_tax=All&field_core_official_dt%5Bmin%5D=&field_core_official_dt%5Bmax%5D='

for each_case_id in case_id_list:
    try:
        entire_url = url_first_half + each_case_id + url_second_half
        page = requests.get(entire_url, timeout = 3)
        soup = BeautifulSoup(page.text, 'html.parser')
        dfs = pd.read_html(page.text)
        frame_combined = pd.concat([frame_combined, dfs[0]], axis = 0)
    except:
        pass
#     print(dfs[0])

frame_combined.drop_duplicates(inplace = True)
frame_combined.to_csv('summary_09_18_2022.csv', index = False)