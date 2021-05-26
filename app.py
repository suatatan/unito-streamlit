# Streamlit Application
# Objection: Calculations for UNITO PRIN projects
# Developer: Dr. Suat ATAN
# Depencencies: paper.py dataprocess.py
# PART 1:  Input data
#--------------------------------------
# <editor-fold>
import os
import pandas as pd
import streamlit as st
import dataprocess as dp
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
st.markdown("# UNITO APP")
st.markdown("## Input ")
st.markdown("Please select the input data set")
input_source = st.selectbox("Select Data:",options=['t25_completolda_documenti.csv','example02_input.csv'])
st.markdown("Please select the treshold")
input_treshold = st.slider("Treshold:",min_value = 0.0, max_value = 1.0,value = 0.80, step=0.1,
        help="Please be patient when you change tresold")
df = pd.read_csv(f"data/{input_source}")
#df = pd.read_csv("~/Belgeler/github/unito-streamlit/data/t25_completolda_documenti.csv")
# Show  input data
st.markdown("Input Table: IN1")
df
# </editor-fold>
# PART 2:  Output tables
#--------------------------------------
# <editor-fold>
# Table1
# Show table 1 over dp
st.markdown("Output")
st.markdown("## Table 1")
#numeric_df = df.drop(columns=['volume','issue','autori','year','title','chiave'])
table1 = dp.table1(df,TRESHOLD = 0.80)
table1
# Table2

# Table3

# Table4

# Table5
# </editor-fold>
