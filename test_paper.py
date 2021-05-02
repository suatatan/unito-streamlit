import pandas as pd
import paper as pa
from pandas._testing import assert_frame_equal
import standard_data as sdata


def test_vsum():
    assert pa.vsum(1,2) == 3, "Should be 3"
    
def test_sort_paper_topics():
    req_output = pd.DataFrame({
            'topic': ['t3','t2','t1','t4'],
            'weight':[61,20,10,9]
            })
    output = pa.sort_paper_topics(sdata.input_set,0)
    assert_frame_equal(output, req_output), "sort_paper_topics function should be proper"

if __name__ == "__main__":
    test_vsum()
    test_sort_paper_topics
    print("Everything passed")
