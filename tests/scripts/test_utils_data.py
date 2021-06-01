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

"""Module with tests for utility data preprocessing functions
"""
import pytest 
from scripts.utils_data import read_in_chunks
from scripts.utils_data import range_without_outliers
import pandas as pd
import json

@pytest.fixture
def prepare_file(tmpdir):
    json_path = tmpdir.join("old_file.json")
    csv_path = tmpdir.join("new_file.csv")
    columns_list = ['age','height','name']
    with open(json_path, 'w') as f:
        f.write(json.dumps({'name':'Ola','age':26})+'\n')
        f.write(json.dumps({'name':'Jan','age':46,'height':1.83})+'\n')
        f.write(json.dumps({'age':46,'name':'Tomek','height':1.73})+'\n')
        f.write(json.dumps({'name':'Wiola'})+'\n')
        f.write(json.dumps({'name':'Radek','age':16,'height':1.93})+'\n')
    yield json_path, csv_path, columns_list

@pytest.fixture
def prepare_series():
    series = pd.Series([1,2,3,4,5,6,7,8,9,10])
    mean_value = series.mean()
    std_value = series.std()
    return series, mean_value, std_value

class TestRangeWithoutOutliers(object):
    def test_range_normal(self, prepare_series):
        series, mean_value, std_value = prepare_series
        lower, upper = range_without_outliers(series) 
        assert lower == pytest.approx((mean_value - (3*std_value)), rel=1e-2)
        assert upper == pytest.approx((mean_value + (3*std_value)), rel=1e-2)

    def test_range_with_valid_lower(self, prepare_series):
        series, mean_value, std_value = prepare_series
        lower, upper = range_without_outliers(series, lower=0.) 
        assert lower == pytest.approx(0.)
        assert upper == pytest.approx((mean_value + (3*std_value)), rel=1e-2)

    def test_range_with_valid_upper(self, prepare_series):
        series, mean_value, std_value = prepare_series
        lower, upper = range_without_outliers(series, upper=10.) 
        assert lower == pytest.approx((mean_value - 3*std_value), rel=1e-2)
        assert upper == pytest.approx(10.)


class TestReadInChunks(object):
    def test_normal_chunks(self, prepare_file):
        path, new_path, columns = prepare_file
        read_in_chunks(path, new_path, 2, columns)
        df = pd.read_csv(new_path)
        assert list(df.shape) == [5,3]
        assert df.columns.tolist() == columns
        assert df.name.tolist() == ['Ola', 'Jan', 'Tomek', 'Wiola', 'Radek']

    def test_too_big_chunks(self, prepare_file):
        path, new_path, columns = prepare_file
        read_in_chunks(path, new_path, 10, columns)
        df = pd.read_csv(new_path)
        assert list(df.shape) == [5,3]
        assert df.columns.tolist() == columns
        assert df.name.tolist() == ['Ola', 'Jan', 'Tomek', 'Wiola', 'Radek']