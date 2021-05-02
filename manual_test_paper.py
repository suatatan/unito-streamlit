import pandas as pd
import paper as pa
import standard_data as sdata

sorted = pa.sort_paper_topics(sdata.input_set,0)
print(sorted)

cumsums = pa.cumsums_paper_topics(sdata.input_set,0)
print(cumsums)

reat = pa.number_of_topics_that_are_sufficient_to_reach_the_threshold(sdata.input_set,0)
print(reat['as_df'])
print(reat['as_count'])
print(reat['as_topic_labels'])
