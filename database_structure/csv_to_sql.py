import os
import pandas as pd
import numpy as np
import unidecode

#------------------------------------------------------------------------------------------------------------------------#

def clean_player_tables():
    
    non_player_file = ["./dataframes/divisions.csv", "./dataframes/teams.csv"]
    
    for i in os.listdir("./dataframes"):
        workfile = f"./dataframes/{i}" 
        
        if workfile in non_player_file:
            continue
        
        df = pd.read_csv(workfile, sep=',', encoding='utf-8', header=1, skiprows=0, index_col=False)
        range_rows = len(df)

        # rename players
        ls = [x for x in range(range_rows)]
        ls = ['player_' + str(x) for x in ls]
    
        if 'Nombre' in df.columns:
            df['Nombre'] = ls

        for j in df.columns:
            if df[j].dtype == 'O':
                df[j] = df[j].astype(str).apply(unidecode.unidecode)
            
        df = df.iloc[:-2, 2:]
        df.to_csv(f'./dataframes_sql/{i}', index=False)
        
def countries():
    
    df = pd.read_csv("./dataframes_sql/players_general.csv", sep=',', encoding='utf-8', header=0, skiprows=0, index_col=False)
    
    nationalities = np.unique(df['Nac'])
    range_nums = np.array(range(len(nationalities)))
    
    df = pd.DataFrame(data  ={'countries':nationalities,'none':range_nums})
    df.to_csv("./dataframes_sql/countries.csv", index=False)
    
def divisions():
    
    df = pd.read_csv("./dataframes/divisions.csv", sep=',', encoding='utf-8', header=1, skiprows=0, index_col=False)
    
    for j in df.columns:
        if df[j].dtype == 'O':
            df[j] = df[j].astype(str).apply(unidecode.unidecode)
            
    divisions = set(df['División'])
    
    # cambiar columna nombre a reputacion de la division
    df = df.rename(columns={'Nombre': 'Reputacion'})
    df = df.rename(columns={'División': 'Division'})
    
    for i in divisions:
        if i == 'Primera Division espanola':
            df.loc[df['Division'] == i, 'Reputacion'] = 'Excelente'
        elif i == 'Segunda Division espanola':
            df.loc[df['Division'] == i, 'Reputacion'] = 'Buena'
        elif i == 'Primera Division Federacion A espanola':
            df.loc[df['Division'] == i, 'Reputacion'] = 'Decente'
        elif i == 'Primera Division Federacion B espanola':
            df.loc[df['Division'] == i, 'Reputacion'] = 'Decente'
        else:
            df.loc[df['Division'] == i, 'Reputacion'] = 'Media'

    # df with only unique divisions
    df = df.drop_duplicates(subset='Division')
    df = df.iloc[:-1,2:]

    df.to_csv(f'./dataframes_sql/divisions.csv', index=False)

def teams():
    
    df = pd.read_csv("./dataframes/teams.csv", sep=',', encoding='utf-8', header=1, skiprows=0, index_col=False)
    df = df.drop_duplicates(subset='Club')
    
    for j in df.columns:
        if df[j].dtype == 'O':
            df[j] = df[j].astype(str).apply(unidecode.unidecode)
            
    df = df.iloc[:, 2:-1]
    df.to_csv(f'./dataframes_sql/teams.csv', index=False)

#------------------------------------------------------------------------------------------------------------------------#

player_tables = clean_player_tables()
nationalities = countries()
division = divisions()
team = teams()

