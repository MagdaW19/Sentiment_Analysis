import pytest
import pandas as pd 
from scripts.utils_visualizations import show_distribution

@pytest.fixture
def prepare_data():
    series = pd.Series(data=[10,9,5,10,4],index=[0,1,2,3,4])
    title = "My Values"
    xlabel = "Important Values"
    yield series, title, xlabel

class TestShowDistribution(object):
    @pytest.mark.mpl_image_compare
    def test_simple_plot(self, prepare_data):
        series_count, title, xlabel = prepare_data
        return show_distribution(series_count, title, xlabel)