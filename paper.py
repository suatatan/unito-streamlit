import pandas as pd

def vsum(a,b):
    return a+b

def sort_paper_topics(df,rownum):
    #for any paper
    cols = [col for col in df if col.startswith('t')]
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

def topics_that_are_sufficient_to_reach_the_threshold(df,rownum = 0,treshold = 90):
    #for any paper
    cumsums = cumsums_paper_topics(df,rownum)
    as_df = cumsums[cumsums['cumsum'] >= treshold] #equal or bigger
    # sign with bigger than Treshold
    cumsums['is_equal_or_bigger_than_treshold'] = cumsums['cumsum'] >= treshold
    as_count = as_df.count()[0]
    as_topic_labels = ",".join(as_df['topic'])
    
    return {
        "as_df": cumsums,
        "as_count": as_count,
        "as_topic_labels" : as_topic_labels
    }
