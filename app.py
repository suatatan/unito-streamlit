# Streamlit Application
# Objection: Calculations for UNITO PRIN projects
# Developer: Dr. Suat ATAN
# Depencencies: paper.py dataprocess.py
# PART 1:  Input data
#--------------------------------------
# <editor-fold> PART I
import os
import pandas as pd
import paper as pa
import streamlit as st
import dataprocess as dp
import mycomponents as myc

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
myc.header()
st.markdown("## Input ")
st.markdown("Please select the input data set")
input_source = st.selectbox("Select Data:",options=['example04_input.csv','t10_completolda_documenti.csv','t25_completolda_documenti.csv'])
st.markdown("Please select the treshold")
input_treshold = st.slider("Treshold:",min_value = 0.0, max_value = 1.0,value = 0.80, step=0.01,
        help="Please be patient when you change tresold")
df = pd.read_csv(f"data/{input_source}")
#df = pd.read_csv("~/Belgeler/github/unito-streamlit/data/t25_completolda_documenti.csv")
# Show  input data
st.markdown("Input Table: IN1")
df
# </editor-fold> PART II
# PART 2:  Output tables
#--------------------------------------
# <editor-fold> End of PART I

# <editor-fold> Table1
# Show table 1 over dp

st.markdown("Output")
st.markdown(f"## Table 1: Threshold analysis (Threshold {input_treshold})")
#numeric_df = df.drop(columns=['volume','issue','autori','year','title','chiave'])
table1 = dp.table1(df,TRESHOLD = 0.80)
table1
st.markdown("Summary of Table 1")
sumtab1 = dp.summary_table1(table1)
sumtab1
# </editor-fold>

# <editor-fold> Table2
st.markdown(f"## Table 2: Summary of the number of topics (Threshold: {input_treshold})  ")
table2 = dp.table2(table1)
table2
# </editor-fold>

# <editor-fold> Table3
st.markdown(f"## Table 3: Summary of the topic distribution (Threshold: {input_treshold})")
table3 = dp.table3(table1)
table3
# </editor-fold>

# <editor-fold> Table4
st.markdown(f"## Table 4: Maximum and mininum weights table (Threshold: {input_treshold})")
table4 = dp.table4(table1)
table4
# </editor-fold>

# <editor-fold> Table 4.1
st.markdown(f"## Table 4.1: Maximum and minimum weights table for specific topic (Threshold: {input_treshold})")
selected_topic = st.selectbox("Select Topic:",pa.extract_topic_columns(df),help="Get subset of Table 4 by topic")

st.markdown("Selected topic is: ")
topic_no = selected_topic[1:] # remove t
st.markdown(topic_no)
table4_1 = dp.table4_1(table1, topic_no)
table4_1
# </editor-fold>

# </editor-fold> End of PART II
