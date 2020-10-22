import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

def add_to_df(row, df):
    if df == 0:
        northern_hemisphere_df_length = len(northern_hemisphere_df)
        northern_hemisphere_df.loc[northern_hemisphere_df_length] = row
    else:
        southern_hemisphere_df_length = len(southern_hemisphere_df)
        southern_hemisphere_df.loc[southern_hemisphere_df_length] = row

if __name__ == "__main__":
    url = "https://www.gamespot.com/articles/animal-crossing-new-horizons-fish-guide-how-to-cat/1100-6474887/"
    html = urlopen(url)
    soup = BeautifulSoup(html)
    rows = soup.findAll('tr')
    
    northern_hemisphere_df = pd.DataFrame({'fish': [], 'seasonality': [], 'location': [], 'time':[], 'price':[]})
    southern_hemisphere_df = pd.DataFrame({'fish': [], 'seasonality': [], 'location': [], 'time':[], 'price':[]})

    current_df = 0
    for current_row in range(1, len(rows)):
        row_content = rows[current_row].findAll('td')
        if (len(row_content) == 0):
            current_df = 1
        else:
            fish_list = []
            for x in rows[current_row].findAll('td'):
                fish_list.append(x.getText())

            add_to_df(fish_list, current_df)

    northern_hemisphere_df['seasonality'] = northern_hemisphere_df['seasonality'].apply(lambda x: x.replace(",", " -"))
    southern_hemisphere_df['seasonality'] = southern_hemisphere_df['seasonality'].apply(lambda x: x.replace(",", " -"))
    northern_hemisphere_df.to_json(r'nh_fish.json')
    southern_hemisphere_df.to_json(r'sh_fish.json')
    northern_hemisphere_df.to_csv('nh_fish.csv')
    southern_hemisphere_df.to_csv('sh_fish.csv')