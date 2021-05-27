#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import paper as pa
import streamlit as st
notta = 'number of topics that are sufficient to reach the threshold'
lotta = 'label of topics that are sufficient to reach the threshold'

@st.cache
def table1(df,TRESHOLD = 0.80):
    result_df = pd.DataFrame()
    for index,row in df.iterrows():
        reat = pa.topics_that_are_sufficient_to_reach_the_threshold(df,rownum = index,treshold=TRESHOLD)
        result_df.at[index,'autori'] = df.at[index,'autori']
        result_df.at[index,'title'] =  df.at[index,'title']
        result_df.at[index,'chiave'] = df.at[index,'chiave']
        result_df.at[index,notta] = reat['as_count'] # yeni kolona notta adını ver.
        result_df.at[index,lotta] = reat['as_topic_labels']
        #max min (TODO:Look table 4, maxweight is 40 and min weight 25)
        result_df.at[index,"max weight"] = max(reat['as_df'].weight) #düz weight değeri en yüksek olanı al
        result_df.at[index,"min weight"] = min(reat['as_df'].weight)
    return(result_df)

def summary_table1(table1):
    return table1[notta].describe().to_frame().transpose()

@st.cache
def table2(table_1):
    t_reat_freq = table_1[notta].value_counts().to_frame().fillna(0).reset_index()
    t_reat_perc = round(table_1[notta].value_counts(normalize = True)*100,2).to_frame().reset_index()
    t_reat_dist = t_reat_freq.merge(t_reat_perc,on="index")
    t_reat_dist.columns = ['topic','reat_freq','reat_perc']
    t_reat_dist['cms'] = t_reat_dist.reat_perc.cumsum()
    t_reat_dist.columns = [notta,'number of paper','percentage','cumulative percentage']
    t_reat_dist = t_reat_dist.sort_values(by = notta, ascending=True)
    bottom = t_reat_dist.sum().to_frame().transpose()
    bottom[notta] = "Total"
    bottom['cumulative percentage'] = ""
    t_read_dist_with_summary = pd.concat([t_reat_dist,bottom])
    t_read_dist_with_summary['number of paper'] = t_read_dist_with_summary['number of paper'].astype("int")
    return t_read_dist_with_summary

def get_order(topicno):
    return topicno.split("t")[1]

@st.cache
def table3(table_1):
    melted_topics = pd.DataFrame(",".join(table_1[lotta].to_list()).split(","))
    tfreq = melted_topics[0].value_counts().to_frame().reset_index()
    tfreq.columns = ['topic','number of paper']
    count_of_papers_in_corpus = table_1.count()[0]
    number_of_papers_in_corpus = tfreq['number of paper']/count_of_papers_in_corpus
    tfreq['percentage of papers in the corpus'] = (number_of_papers_in_corpus*100).round(2)
    tfreq['order'] = tfreq['topic'].apply(get_order).astype(int)
    tfreq = tfreq.sort_values(by = "order")
    tfreq = tfreq[['topic','number of paper','percentage of papers in the corpus']]
    return tfreq

@st.cache
def table4(table_1):
    bins = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    tmaxwei_freq = pd.cut(table_1['max weight'],bins = bins).value_counts(sort = False).to_frame().fillna(0).reset_index()
    tminwei_freq = pd.cut(table_1['min weight'],bins = bins).value_counts(sort = False).to_frame().fillna(0).reset_index()
    tmaxminwei_freq = tmaxwei_freq.merge(tminwei_freq)
    tmaxminwei_freq.columns = ["bin","pa_max","pa_min"]
    pa_max_sum = tmaxminwei_freq.pa_max.sum()
    pa_min_sum = tmaxminwei_freq.pa_min.sum()
    #tmaxminwei_freq.append(tmaxminwei_freq.sum(numeric_only=True), ignore_index=True)

    tmaxminwei_freq['perc_max'] = tmaxminwei_freq.pa_max / pa_max_sum
    tmaxminwei_freq['perc_min'] = tmaxminwei_freq.pa_min / pa_min_sum

    tmaxminwei_freq['cumsum_max'] = tmaxminwei_freq.perc_max.cumsum()
    tmaxminwei_freq['cumsum_min'] = tmaxminwei_freq.perc_min.cumsum()
    tmaxminwei_freq = tmaxminwei_freq[['bin','pa_max','perc_max','cumsum_max','pa_min','perc_min','cumsum_min']]
    #tmaxminwei_freq.append(tmaxminwei_freq.sum(numeric_only=True), ignore_index=True) # summary table

    tmaxminwei_freq.loc["Row_Total"] = tmaxminwei_freq.sum()
    return tmaxminwei_freq

@st.cache
def table4_1(table_1,USER_INPUT_T=1):
    bins = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    subset_table = table_1[table_1['number of topics that are sufficient to reach the threshold'] == int(USER_INPUT_T)]
    tmaxwei_freq = pd.cut(subset_table['max weight'],bins = bins).value_counts(sort = False).to_frame().fillna(0).reset_index()
    tminwei_freq = pd.cut(subset_table['min weight'],bins = bins).value_counts(sort = False).to_frame().fillna(0).reset_index()
    tmaxminwei_freq = tmaxwei_freq.merge(tminwei_freq)
    tmaxminwei_freq.columns = ["bin","pa_max","pa_min"]
    pa_max_sum = tmaxminwei_freq.pa_max.sum()
    pa_min_sum = tmaxminwei_freq.pa_min.sum()
    #tmaxminwei_freq.append(tmaxminwei_freq.sum(numeric_only=True), ignore_index=True)

    tmaxminwei_freq['perc_max'] = tmaxminwei_freq.pa_max / pa_max_sum
    tmaxminwei_freq['perc_min'] = tmaxminwei_freq.pa_min / pa_min_sum

    tmaxminwei_freq['cumsum_max'] = tmaxminwei_freq.perc_max.cumsum()
    tmaxminwei_freq['cumsum_min'] = tmaxminwei_freq.perc_min.cumsum()
    tmaxminwei_freq = tmaxminwei_freq[['bin','pa_max','perc_max','cumsum_max','pa_min','perc_min','cumsum_min']]
    #tmaxminwei_freq.append(tmaxminwei_freq.sum(numeric_only=True), ignore_index=True) # summary table

    tmaxminwei_freq.loc["Row_Total"] = tmaxminwei_freq.sum()
    tmaxminwei_freq
    return tmaxminwei_freq
