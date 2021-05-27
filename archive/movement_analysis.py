# This Analysis for checking result table values while treshold changes
# Is there any value that stays same and is that normal?
import os
import pandas as pd
import paper as pa
import dataprocess as dp

TRESHOLD = 0.9
while  TRESHOLD < 1:
    try:
        df = pd.read_csv("~/Belgeler/github/unito-streamlit/data/t25_completolda_documenti.csv")
        table1 = dp.table1(df,TRESHOLD)
        table1.to_csv(f"~/Belgeler/github/unito-streamlit/output/table1_{TRESHOLD}.csv")
        TRESHOLD = TRESHOLD + 0.05
        print(f"OK T: {TRESHOLD}")
    except Exception as ex:
        print(f"Hata: {str(ex)}")
        pass
