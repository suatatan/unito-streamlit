import os
import pandas as pd
import streamlit as st

input_source = st.selectbox("Select Data:",options=['example01_input.csv','example02_input.csv'])
input_treshold = st.slider("Treshold:",min_value=0,max_value = 100,value=92)
#input_source = "example02_input.csv"
df = pd.read_csv(f"/home/suat/Belgeler/github/unito/tasks/task01/data/{input_source}")
tcols = [col for col in df if col.startswith('t')]
tcolvals = []
for col in tcols:
    selected = st.checkbox(col,value=True)
    if selected:
        tcolvals.append(col)

st.title("Input Value")

index = 0
def preprocess(df,threshold = input_treshold, cols =  tcolvals):
    df_output = pd.DataFrame()
    for index,row in df.iterrows():
        rownum = index
        #get original roww
        orgrow = df.iloc[rownum,].to_frame().transpose()
        sorted_tvals = df[cols].loc[rownum].sort_values(ascending=False).to_frame().reset_index().transpose()
        sorted_tlabs = sorted_tvals.iloc[0]
        sorted_tvals = sorted_tvals.iloc[1]
        a = pd.concat([sorted_tlabs,sorted_tvals]).to_frame().transpose()
        # getting cumsum values of sorted tvals and adding to rightmost of table
        cumsums = df[cols].loc[rownum].sort_values(ascending=False).to_frame().cumsum().reset_index().transpose()
        cumsums_vals = cumsums.iloc[1].to_frame().transpose()
        b = cumsums_vals
        #combining two results and juxtaposing them in the right by right in single row
        c = pd.concat([a, b], axis=1)
        c = pd.concat([a.reset_index(drop=True), b.reset_index(drop=True)], axis=1)

        # get original serie
        out = pd.concat([orgrow.reset_index(drop=True), c.reset_index(drop=True)], axis=1)
        #----number of topic above threshold----
        # we will find the number of topics above threshold (via variable b)
        # CLEAR definition: find the minimum value within the numbers above threshold and get its label
        # add 1 because python starts from zero
        j = b.transpose()
        j.columns = ["tval"]
        k = j[j.tval > threshold]
        kv = k[k.tval == k.tval.min()].index.values[0]+1 if k.count()[0] > 0 else 0
        out['reat'] = kv
        # get the labels of t's that above the threshold
        suffi = ",".join(sorted_tlabs[:kv])
        out['suffi'] = suffi
        # max weight
        out['maxwei'] = max(sorted_tvals)
        out['minwei'] = min(sorted_tvals)
        df_output = df_output.append(out)
    #end of for----------------------------------------------
    #renaming columns

    return df_output

st.title("Results for each paper")
df_result = preprocess(df)
df_result

#def process_for_all_papers(df_result)
st.title("Results for all papers:")

outputs = []
# Step A: Wrangling 'reat'
# TODO:
t_reat_freq = df_result['reat'].value_counts().to_frame().fillna(0).reset_index()
t_reat_perc = round(df_result['reat'].value_counts(normalize = True)*100,2).to_frame().reset_index()
t_reat_dist = t_reat_freq.merge(t_reat_perc,on="index")
t_reat_dist.columns = ['topic','reat_freq','reat_perc']
t_reat_cumsums = t_reat_perc.reat.cumsum()
t_reat_dist['reat_cumsums'] = t_reat_cumsums
outputs.append(t_reat_dist)
st.write("Reat")
st.write(t_reat_dist.astype('object'))

# Step B: Wrangling 'suffi'
melted_topics = pd.DataFrame(",".join(df_result['suffi'].to_list()).split(","))
melted_topics.head(3)
tfreq = melted_topics[0].value_counts().to_frame().reset_index()
tperc = round(melted_topics[0].value_counts(normalize = True)*100,2).to_frame().fillna(0).reset_index()
tdist = tperc.merge(tfreq,on="index")
tdist.columns = ['topic','suffi_perc','suffi_freq']
suffi_cumsums = tdist['suffi_perc'].cumsum()
tdist['suffi_cumsums'] = suffi_cumsums
outputs.append(tdist) #suffi table
st.write("Suffi")
st.write(tdist.astype('object'))

# Step C:
bins = [10,20,30,40,50,60,70,80,90,100]
tmaxwei_freq = pd.cut(df_result.maxwei,bins = bins).value_counts(sort = False).to_frame().fillna(0).reset_index()
tminwei_freq = pd.cut(df_result.minwei,bins = bins).value_counts(sort = False).to_frame().fillna(0).reset_index()
tmaxminwei_freq = tmaxwei_freq.merge(tminwei_freq)
tmaxminwei_freq.columns = ["bin","maxwei_freq","minwei_freq"]
outputs.append(tmaxminwei_freq)
st.write("Max and Min Weight Freqs (tmaxminwei_freq)")
st.write(tmaxminwei_freq.astype('object'))

# Step C-A
tmaxwei_perc=  round(pd.cut(df_result.maxwei,bins = bins).value_counts(sort = False,normalize=True)*100,2).to_frame().fillna(0).reset_index()
tminwei_perc=  round(pd.cut(df_result.minwei,bins = bins).value_counts(sort = False,normalize=True)*100,2).to_frame().fillna(0).reset_index()
tmaxminwei_perc = tmaxwei_freq.merge(tminwei_perc)
tmaxminwei_perc.columns = ["bin","maxwei_perc","minwei_perc"]
t_maxwei_perc_cumsums = tmaxwei_perc.maxwei.cumsum()
t_minwei_perc_cumsums = tminwei_perc.minwei.cumsum()
tmaxminwei_perc['maxwei_cumsums'] = t_maxwei_perc_cumsums
tmaxminwei_perc['minwei_cumsums'] = t_minwei_perc_cumsums
outputs.append(tmaxminwei_perc)
st.write("Max and min weight percentages (tmaxminwei_perc)")
st.write(tmaxminwei_perc.astype('object'))

tmaxwei_desc = df_result.maxwei.describe().to_frame().reset_index()
tminwei_desc = df_result.minwei.describe().to_frame().reset_index()
weidesc = tmaxwei_desc.merge(tminwei_desc)
outputs.append(weidesc)

#return outputs
st.write("Weight Descriptipon (weidesc)")
st.write(weidesc.astype('object'))


#allpapers_results = process_for_all_papers(df_result)
