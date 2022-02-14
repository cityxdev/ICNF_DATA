# -*- coding: utf-8 -*-
"""CONCATS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iTEbYi39Jl0R287heSeXj3IBct-E5eYa

# ICFN DATA
"""

# import libraries
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import io
from io import StringIO  
import time 
import datetime

"""## GET DATA FOR 2022"""

# Get latest data from 2022 
url = f"https://fogos.icnf.pt/localizador/webserviceocorrencias.asp?ANO=2022" 
resp = requests.get(url)
et = ET.parse(io.StringIO(resp.text))

# Create Dataframe 
df_2022 = pd.DataFrame([
    {f.tag: f.text for f in e.findall('./')} for e in et.findall('./')]
).reset_index()

# reset dataframe index 
df_2022.reset_index(drop=True, inplace=True)

"""## GET CURRENT DATASET """

# import full dataset to dataframe
df_actual = pd.read_csv('https://raw.githubusercontent.com/vostpt/ICNF_DATA/main/ICNF_2013_2022_full.csv')

# Drop data from 2022 
df_actual.drop(df_actual[df_actual.ANO == 2022].index, inplace=True)

"""## JOIN DATAFRAMES"""

# Define dict with both dataframes
frames = [df_actual,df_2022]

frame = pd.concat(frames, axis=0, ignore_index=True)

final_df = pd.concat(frames)

"""## Save updated dataframe"""

final_df.to_csv("ICNF_2013_2022_full.csv",index=False)

"""## Create Dataframe for Sankey"""

df_sankey = final_df.groupby(['ANO','DISTRITO','CONCELHO'])[['NCCO']].nunique().reset_index()

"""## Save Sankey DataFrame to CSV"""

df_sankey.to_csv("ICNF_2013_2022_SANKEY.csv",index=False)



