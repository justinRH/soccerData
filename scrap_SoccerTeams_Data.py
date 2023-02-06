# This scripts scraps fbref web page to get stats from B5L-UEFA
# Big 5 Ligue of UEFA: La Liga, Premier, Bundes, Ligue-1 and Serie A
# install requeriments (pip install -r requirements.txt )

import sys
import os
import errno
import pandas as pd
import numpy as np
import csv 

import requests
from re import sub
from lxml import html
from bs4 import BeautifulSoup  


if __name__ == '__main__':
    

    links = ['https://fbref.com/en/comps/12/2021-2022/2021-2022-La-Liga-Stats']
#             'https://fbref.com/en/comps/20/2021-2022/2021-2022-Bundesliga-Stats',
#             'https://fbref.com/en/comps/9/2021-2022/2021-2022-Premier-League-Stats']
#             'https://fbref.com/en/comps/13/2021-2022/2021-2022-Ligue-1-Stats'      
#            'https://fbref.com/en/comps/11/2021-2022/2021-2022-Serie-A-Stats',  ]

    stats = ['stats_standard_',
             'stats_shooting_',
             'stats_passing_',
             'stats_passing_types_',
             'stats_gca_',
             'stats_defense_',
             'stats_possession_',
             'stats_playing_time_',
             'stats_misc_'
            ]

       
    for link in links:
            
        page_ligue = requests.get(link) 
        soup = BeautifulSoup(page_ligue.text, 'html.parser') 
        tables  = soup.findAll("table") 
        path_dir = soup.title.get_text()[:-11]
        print(path_dir + "... ")
        for table in tables:

            try:
                os.mkdir(path_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            rows = table.findAll("tr")                  # all teams (estadísticas general de todos los equipos)
            teams_href=[]
            #with open(path_dir  + "/" + table.get('id') + ".csv", "wt+", encoding="utf-8", newline="") as f:
            #os.chdir(path_dir)
            with open(path_dir[:-1] + "\\" + table.get('id') + ".csv", "wt+", encoding="utf-8",newline="") as f:
                writer = csv.writer(f)
                for row in rows:                        # each team 
                    if row.find('a',href=True):
                        teams_href.append(row.find('a',href=True)['href'])
                        
                    csv_row = []
                    for cell in row.findAll(["td", "th"]):
                        csv_row.append(cell.get_text())
                    writer.writerow(csv_row)
            #os.chdir("..")

        for href in teams_href:
            for stat in stats:
                print(href.split('/')[5]) 
                
                try:
                    os.mkdir(path_dir[:-1] + "\\" + "teams")
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
 
                df = pd.read_html('https://fbref.com/'+href,header=1,attrs={'id': stat + link.split('/')[5]})
                df[0].to_csv(path_dir[:-1] + "\\" + "teams" +"\\"  + href.split('/')[5] +"_" + stat +  ".csv" )
            print('... listo')

   
        






    

       

