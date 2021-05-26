import pandas as pd
import re
#df = pd.read_csv("~/Belgeler/github/unito-streamlit/data/t25_completolda_documenti.csv")

def vsum(a,b):
    return a+b

def extract_topic_columns(df):
    topics_dirty = [re.findall(r"^t\d+",topic) for topic in df.columns]
    topics = [x[0] for x in topics_dirty if len(x) > 0]
    return topics

def sort_paper_topics(df,rownum):
    #for any paper
    cols = extract_topic_columns(df)
    sorted_tvals = df[cols].loc[rownum].sort_values(ascending=False).to_frame().reset_index().transpose()
    sorted_tlabs = sorted_tvals.iloc[0]
    sorted_tvals = sorted_tvals.iloc[1]
    result = pd.DataFrame(sorted_tvals)
    result['topic'] = sorted_tlabs
    result.columns = ['weight','topic']
    new_order = [1,0]
    result = result[result.columns[new_order]]
    return result

def cumsums_paper_topics(df,rownum = 0):
    #for any paper
    sorted = sort_paper_topics(df,rownum)
    cumsums = sorted['weight'].cumsum().reset_index().transpose()
    cumsums_vals = cumsums.iloc[1].to_frame().transpose()
    sorted['cumsum'] = cumsums_vals.transpose()
    return sorted

def topics_that_are_sufficient_to_reach_the_threshold(df,rownum = 0,treshold = 0.80):
    #for any paper
    cumsums = cumsums_paper_topics(df,rownum)
    as_df = cumsums[cumsums['cumsum'] >= treshold]
    #all rows under treshold
    as_df_under_treshold = cumsums[cumsums['cumsum'] <= treshold]
    #first row upper treshold (as slice)
    as_df_first_bigger_than_treshold = cumsums[cumsums['cumsum'] > treshold].iloc[0].to_frame().transpose()
    #merge
    as_df = as_df_under_treshold.append(as_df_first_bigger_than_treshold)
    as_count = as_df.count()[0]
    as_topic_labels = ",".join(as_df['topic'])

    return {
        "as_df": as_df,
        "as_count": as_count,
        "as_topic_labels" : as_topic_labels
    }
