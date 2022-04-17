import pandas as pd
import numpy as np
import openpyxl
import os
import glob
from pathlib import Path

BDB_GAME = ['DATASET', 'DATE', 'TEAMS','VENUE',
    '1Q', '2Q', '3Q', '4Q', 'OT1', 'OT2', 'OT3', 'OT4', 
    'F', 'MIN', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 
    'OR', 'DR', 'TOT', 'A', 'PF', 'ST', 'TO', 'BL', 'PTS', 'POSS', 'PACE', 'OEFF', 'DEFF', 'REST DAYS']

def combine_xl_data( folder_path : str, file_type : str, sheet_name, data_source : str) -> pd.DataFrame:
    """Take folder path and combine all excels/csv into a dataframe.

    Args:
        folder_path (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # initialize dataframe
    
    df = []
    df_columns = []
    if (file_type == "xlsx"):
        folder_link = glob.glob(folder_path+"/*.xlsx")
    if (file_type == "csv"):
        folder_link = glob.glob(folder_path+"/*.csv")   

    for file in folder_link:
        # Confirm a file 
        if (file_type == "xlsx"):
            temp_pd = pd.read_excel(file, sheet_name = sheet_name)
        if (file_type == "csv"):
            temp_pd = pd.read_csv(file, sheet_name = sheet_name)

        # Rename columns based on source
        if (data_source == "BDB-GAME"):
            # Rename columns based on columns + count
            len_check = len(temp_pd.columns.values.tolist())
            if (len_check == 57):
                # Rename BIGDATABALL\nDATASET + TEAM\nREST DAYS
                temp_pd.rename(
                    columns = {
                        'BIGDATABALL\nDATASET': 'DATASET',
                        'TEAM\nREST DAYS' : 'REST DAYS'
                    }, inplace=True
                )
            try:
                 temp_pd.rename(
                    columns = {'TEAM': 'TEAMS'}, inplace=True
                )
            except:
                continue

            temp_pd = temp_pd[BDB_GAME]

        df_columns.append(temp_pd.columns)
        df.append(temp_pd)

    return pd.concat(df)

def save_combined_df( df_to_save : pd.DataFrame, folder_path : str, file_name : str) -> bool:
    """_summary_

    Args:
        df_to_save (pd.DataFrame): _description_
        folder_path (str): _description_
        file_name (str): _description_

    Returns:
        bool: _description_
    """
    # df_to_save
    try:
        path = folder_path + "\\" + file_name
        df_to_save.to_excel(path)
        return True

    except:

        return False

if __name__ == "__main__":
    # Create intial Dataframe
    folder_path = r"\Users\sebas\Desktop\UChicago - Q6\Sports Analytics\sports_analytics_project\data\Big Data Ball - Game" 
    save_path = r"\Users\sebas\Desktop\UChicago - Q6\Sports Analytics\sports_analytics_project\data"
    file_type, sheet_name = "xlsx" , 0
    data_source = "BDB-GAME"
    combined_df = combine_xl_data(folder_path, file_type, sheet_name, data_source) 
    # Read all Excels within a directory
    print(
        save_combined_df( combined_df, save_path, file_name="BDB-GAME.xlsx",)
        )
    # Clean Combined Dataframe