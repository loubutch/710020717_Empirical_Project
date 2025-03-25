## Cleaning the Book Data ##


## importing packages
import pandas as pd
import re
import numpy as np

## loading in the dataframes
df_book_1 = pd.read_csv('data/top_books0.csv')
df_book_2 = pd.read_csv('data/top_books1.csv')
df_book_3 = pd.read_csv('data/top_books2.csv')
df_book_4 = pd.read_csv('data/top_books3.csv')

# quick pre-join edit
df_book_4['First_Published'] = df_book_4['First_Published'].str.replace('–1929', '')
  
## joining the dataframes 

df_list = [df_book_1, df_book_2, df_book_3, df_book_4]
df_book =  pd.concat(df_list)

## fixing entries with unusual entries
# fix dodgy entries
df_fix = pd.DataFrame(df_book.loc[(df_book['Approximate_Sales'] == '1950') | 
                     (df_book['Approximate_Sales'] == '1981') |
                     (df_book['Approximate_Sales'] == '1982') ])
df_fix['Book'] = df_fix['Book'].str.replace('The Lion', 'The Lion, the Witch and the Wardrobe')
df_fix['Book'] = df_fix['Book'].str.replace('The Secret Diary of Adrian Mole', 'The Secret Diary of Adrian Mole, Aged 13¾')
df_fix['Book'] = df_fix['Book'].str.replace("Ronia", "Ronia, the Robber's Daughter")
df_fix = df_fix.drop(df_fix.columns[1], axis =1)
df_fix.columns = ["Book", "Author", "Original_Language", "First_Published",
                  "Approximate_Sales", "Genre_1", "Genre_2", 
                  "Genre_3", "Genre_4", "Genre_5"]
df_book = pd.DataFrame(df_book.loc[(df_book['Approximate_Sales'] != '1950') & 
                     (df_book['Approximate_Sales'] != '1981') &
                     (df_book['Approximate_Sales'] != '1982') ])
df_book = pd.concat([df_book, df_fix])



## adding some regular expression corrections
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\[\d{3}\]', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\[\d{2}\]', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(' million', '000000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('.', '')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(' ', '')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('>', '')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'[A-Za-z]', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\([^)]*\)', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\[[^)]*\]', r'', regex=True)

# niche changes
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('28–30', '29')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('11–120', '115')
#df_book['First_Published'] = df_book['First_Published'].str.replace('1925-1929', '')
df_book


## fixing datatypes
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].map(int)
df_book['First_Published'] = df_book['First_Published'].map(int)
print(df_book)
