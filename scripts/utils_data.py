#    Copyright 2021 Magda Wójcicka

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Module with utility functions for preprocessing data.
"""
# IMPORTS 
import json 
import numpy as np 
import pandas as pd
import datetime

# Dtypes for simplififed version of data
DTYPES_SIMPLE = {'overall':np.int16,
                 'vote':np.int64,
                 'reviewText':object,
                 'reviewMonth':np.int16,
                 'reviewYear':np.int16,
                 }

def read_in_chunks(path, new_path, chunk_size, columns):
    """Reads big json file line by line and saves it to csv file by chunk.
    Each line of json file should be a python dict with keys representing columns names. 
    If column is not included in given line it is filled with None.

    Parameters
    ----------
    path : str
        Path to original json file
    new_path : str
        Path to new csv file where data will be saved.
    chunk_size : int
        Number of rows after which data should be appended to csv file
    columns : List of str
        List of column names
    """


# Test if file in 'path" exists and if first line is valid dict
    try:
        with open(path) as f:
            json.loads(f.readline())
    except IOError:
        print("File is not accessible or first line is not valid python dict")


    rows_list = []
    empty_row = {col:None for col in columns}
    mode = 'w'

    begin_time = datetime.datetime.now()

# Read all lines and save to csv every chunk
    with open(path) as f:
        # iterating over each line and appending to list
        for i, line in enumerate(f):
            new_dict = json.loads(line)
            rows_list.append({**empty_row, **new_dict})

            if ((i+1) % chunk_size) == 0:
                pd.DataFrame(rows_list).to_csv(new_path, mode=mode, index=False, header=(mode=='w'))
                rows_list = []
                mode = 'a'
                print(f'{i} lines processed')
        # appending any leftovers after last full chunk
        if len(rows_list) > 0:
            pd.DataFrame(rows_list).to_csv(new_path, mode=mode, index=False, header=(mode=='w'))

    time = datetime.datetime.now() - begin_time
# Displaying message with summary
    print(f"Saved content of {path} to {new_path} succesfully")
    print(f"Processed {i} lines in {time}")
 
 

