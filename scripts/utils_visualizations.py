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

"""Module with utility functions for displaying vizualizations.
"""
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set()

def show_distribution(series_count, title, xlabel, normalize=None, norm_name='', figsize=None):
    """Function displaying distribution based on values count.

    Parameters
    ----------
    series_count : pd.Series
        Series generated as value counts of another pd.Series
    title : str
        title
    xlabel : str
        label on x axis
    normalize : int, optional
        series is divided by this value, by default None
    norm_name : str, optional
        name for normalization like 'millions', 'thousands', by default ''
    figsize : 2-element tuple of int 
        size of the plot
    """
    # Set value to normalize (Count can be displayed in K, Millions etc.)
    if normalize:
        series_count = series_count/normalize
        ylabel = f'Count in {norm_name}'
    else:
        ylabel = 'Count'

    # Set figsize
    if figsize:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = plt.subplots()

    # Display bar for each value count
    sns.barplot(x=series_count.index, y=series_count, ax=ax)
    plt.title(title, fontsize=16)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

