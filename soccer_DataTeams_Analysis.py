import sys
import os
import errno
import pandas as pd
import numpy as np
import csv 
import glob
import re

PATH = "C:\\Users\\USUARIO\\Documents\\pyProjects\\soccerData\\"


if __name__ == '__main__':
    
    dirs = ['2021-2022 La Liga Stats',
            #'2021-2022 Serie A Stats'
            #'2021-2022 Ligue 1 Stats',
            #'2021-2022 Premier League Stats',
            #'2021-2022 Bundesliga Stats'
            ]

    for dir_ in dirs:

        file_overall=glob.glob(dir_ + "\\" + "*overall.csv")
        team_rank    = pd.read_csv(file_overall[0])
        team_rank.Squad = [re.sub(r"^\s+", "", tr) for tr in team_rank.Squad]
        
        txtfiles = []
        for file in glob.glob(PATH + dir_ +  "/*_for.csv"):
            print(file)                
            txtfiles.append(file)
            df=pd.read_csv(file,header=1)
            d = pd.merge(team_rank,df,on='Squad')
            m=d.describe()
            M = pd.DataFrame(columns=d.columns,index=['all','top','med','low'])
            M.loc['all'] = m.loc['mean']
            
            k=np.int0(np.round(len(team_rank)/3))
            
            m=d.iloc[0:k].describe()
            M.loc['top'] = m.loc['mean'] 
               
            m=d.iloc[k+1:2*k].describe()
            M.loc['med'] = m.loc['mean'] 
            
            m=d.iloc[2*k+1:3*k-1].describe()
            M.loc['low'] = m.loc['mean']

            M = M.astype(float).round(2)
            M.to_csv(file[:-7] + '_DESCRIPTIVE.csv') 

            




