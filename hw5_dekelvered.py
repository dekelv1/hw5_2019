import pathlib
from typing import Union
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import re
from typing import Union, Tuple


class QuestionnaireAnalysis:

    def __init__(self, data_fname: Union[pathlib.Path, str]):

        if isinstance(data_fname, str):
            self.data_fname = pathlib.Path(data_fname)
        else:
            self.data_fname = data_fname
        if not (self.data_fname.exists() and self.data_fname.is_file()):
            raise ValueError("Non existant file, try again")
        self.data = None


    def read_data(self):

        with open(self.data_fname) as datafile:
            self.data = pd.read_json(datafile)

                    
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
     
        bin_edges = np.arange(0, 110, 10)
        hist = self.data.hist(column='age', bins=bin_edges)
        values = pd.cut(self.data['age'], bins=bin_edges, right=False).value_counts().sort_index().values
#        plt.hist
#        print(plt.show())
        return values, bin_edges


    def remove_rows_without_mail(self) -> pd.DataFrame:

        bool_mask = self.data['email'].str.contains('[0-9A-Za-z]+@[0-9A-Za-z]+.[A-Za-z]+')
        valid_email_data = self.data[bool_mask]     
        len_curr_idxs = len(valid_email_data.index)
        correct_idxs = np.arange(0,len_curr_idxs)
        valid_email_data.index = correct_idxs
        return(valid_email_data)


    def fill_na_with_mean(self) -> Union[pd.DataFrame, np.ndarray]:

        mask = self.data.loc[:,['q1','q2','q3','q4','q5']].isnull().any(axis='columns')
        row_nums = np.where(mask==True)
        return (self.data.fillna(self.data.mean()), row_nums)
      
    def correlate_gender_age(self) -> pd.DataFrame:

        multi_df = self.data.loc[:,['gender','age','q1','q2','q3','q4','q5']]
        return multi_df.groupby(['gender',multi_df.age > 40]).mean()