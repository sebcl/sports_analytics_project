import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from linearmodels import IV2SLS
# regression analysis

import stargazer
import sys
import os

def ols_base( data : pd.DataFrame, y, x : list, constant : bool):

    try:
        y_est = np.array( data[[y]])
        x_est = np.array( data[x])

        if constant: 
            x_est = sm.add_constant(x_est) 

        model = sm.OLS(y_est, x_est)
        results = model.fit()

        return results

    except Exception as e:
        return f'Error: {e}'

def iv_base( data : pd.DataFrame, y, variable, instruments, x ):
    se = []
    ate = []
    result = []
    for insta in instruments:
        formula = f'{y} ~ {x} + [{variable} ~ {insta}]'
        iv = IV2SLS.from_formula(formula, data).fit()
        result.append(iv)
        se.append(iv.std_errors["T"])
        ate.append(iv.params["T"])

    res_dict =  dict(se=se, ate=ate, returns = result )
    return res_dict

def multi_iv_base( data : pd.DataFrame, y, variable, instruments, x ):
   
    formula = f'{y} ~ {x} + [{variable} ~ {instruments}]'
    iv = IV2SLS.from_formula(formula, data).fit()
    se = iv.std_errors[variable]
    ate = iv.params[variable]

    res_dict =  dict(se=se, ate=ate, results = iv )
    return res_dict


if __name__ == "__main__":
    
    player_path = r"\Users\sebas\Desktop\UChicago - Q6\Sports Analytics\sports_analytics_project\data\BDB_Player.xlsx"
    df_player = pd.read_excel(player_path)
    df_player.columns = ['DATASET', 'DATE', 'PLAYER FULL NAME', 'POSITION', 'OWN TEAM',
       'OPP TEAM', 'VENUE', 'MIN', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'OR',
       'DR', 'TOT', 'A', 'PF', 'ST', 'TO', 'BL', 'PTS', 'PER', 'DATE-DIFF',
       'RR VAL', 'RR SERIES', 'S_PER', 'I_PER', 'SAME_CITY', 'TRAVEL',
       '1_days', '10_days', '11_days', '12_days', '13days',
       '14+_days', '14_days', '2_days', '3_days', '4_days', '5_days',
       '6_days', '7_days', '8_days', '9_days', 'Season_Start',
       'H', 'R', 'H-M1', 'H-M2', 'H-M3', 'R-M1', 'R-M2', 'R-M3', 'M1', 'M2',
       'M3', 'S_OEFF', 'S_DEFF', 'I_OEFF', 'I_DEFF','Bubble']

    df_clean = df_player[df_player['DATASET'] != '2011-2012 Regular Season']
    # Remove Bubble Seasons (2019-2020)
    df_clean = df_player[df_player['DATASET'] != '2019-2020 Regular Season']
    # Create PER Difference Column
#    df_clean['PER_DIFF'] = df_clean['PER'] - df_clean['I_PER']
    res = ols_base(
        data = df_clean, 
        y = 'PER', 
        x = [ 'H', 'TRAVEL', 'I_OEFF','I_DEFF', 'M1', 'M2', 'M3','1_days', '2_days', '3_days', '4_days'], 
        constant = True)

    stargazer(res)
