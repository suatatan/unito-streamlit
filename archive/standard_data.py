import pandas as pd
paper_keys = ["p1", "p2","p3","p4"]
t1 = [10,80,30,40]
t2 = [20,2,60,5]
t3 = [61,8,4,30]
t4 = [9,10,6,25]
df = pd.DataFrame({'paper_key': paper_keys,
                          't1': t1,
                          't2': t2,
                          't3': t3,
                          't4': t4}
                          )
input_set = df