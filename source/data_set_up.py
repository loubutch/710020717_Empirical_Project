## Cleaning the Book Data ##


## importing packages
import pandas as pd
import re
import numpy as np

## Below I am loading in the dataframes for individual books
df_book_1 = pd.read_csv('data/top_books0.csv')
df_book_2 = pd.read_csv('data/top_books1.csv')
df_book_3 = pd.read_csv('data/top_books2.csv')
df_book_4 = pd.read_csv('data/top_books3.csv')


# Here I am making a quick pre-join edit to the fourth dataframe
# as there is an incompatible entry 
df_book_4['First_Published'] = df_book_4['First_Published'].str.replace('–1929', '')
  

## Here I am joining the dataframes 
df_list = [df_book_1, df_book_2, df_book_3, df_book_4]
df_book =  pd.concat(df_list)


## Below I am fixing entries with unusual entries

# These entries had the entries in the wrong column 
df_fix = pd.DataFrame(df_book.loc[(df_book['Approximate_Sales'] == '1950') | 
                     (df_book['Approximate_Sales'] == '1981') |
                     (df_book['Approximate_Sales'] == '1982') ])

# I am fixing the first entries to the correct book name
# These were seperated originally due to the commas causing the webscraping to 
# believe they were the end of an entry.
df_fix['Book'] = df_fix['Book'].str.replace('The Lion', 'The Lion, the Witch and the Wardrobe')
df_fix['Book'] = df_fix['Book'].str.replace('The Secret Diary of Adrian Mole', 'The Secret Diary of Adrian Mole, Aged 13¾')
df_fix['Book'] = df_fix['Book'].str.replace("Ronia", "Ronia, the Robber's Daughter")

# Here I am dropping the extra row (Author) and renaming the columns with the correct names
df_fix = df_fix.drop(df_fix.columns[1], axis =1)
df_fix.columns = ["Book", "Author", "Original_Language", "First_Published",
                  "Approximate_Sales", "Genre_1", "Genre_2", 
                  "Genre_3", "Genre_4", "Genre_5"]

# Here I drop the incorrect entries from the original dataframe
df_book = pd.DataFrame(df_book.loc[(df_book['Approximate_Sales'] != '1950') & 
                     (df_book['Approximate_Sales'] != '1981') &
                     (df_book['Approximate_Sales'] != '1982') ])

# Here I join the corrected entries back onto the dataframe
df_book = pd.concat([df_book, df_fix])



## Below I am adding changes to Approximate_Sales 
## this make sure it is all in the correct format for future analysis

# niche changes with decimals
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('36.4 million', '36400000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('31.5 million', '31500000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('22.5 million', '22500000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('15.3 million', '15300000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('15.2 million', '15200000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('12.1 million', '12100000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('10.5 million', '10500000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('10.4 million', '10400000')

# adding extra general changes
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(' million', '000000')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('.', '')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(' ', '')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('>', '')

# adding some regular expression corrections
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\[\d{3}\]', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\[\d{2}\]', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'[A-Za-z]', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\([^)]*\)', r'', regex=True)
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace(r'\[[^)]*\]', r'', regex=True)

# niche changes
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('28–30', '29')
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].str.replace('11–120', '115')


## Below I am fixing datatypes for future analysis
df_book['Approximate_Sales'] = df_book['Approximate_Sales'].map(int)
df_book['First_Published'] = df_book['First_Published'].map(int)


## Here I am making a combined genre column
df_book["All_Genre"] = df_book[["Genre_1", "Genre_2", 
                  "Genre_3", "Genre_4", "Genre_5"]].apply(lambda x: ','.join(x.dropna()), axis=1)



## Here I am adding extra genre information to these with no genres based on main genres found on wikipedia
df_book['All_Genre'] = np.where((df_book['Book'] == "Shōgun") 
                                   | (df_book['Book'] ==  "Perfume (Das Parfum)") 
                                   | (df_book['Book'] == "The Boy in the Striped Pyjamas" )
                                   | (df_book['Book'] == "The Help" )
                                   , "historical fiction", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "The Horse Whisperer") 
                                   | (df_book['Book'] ==  "The Grapes of Wrath") 
                                   | (df_book['Book'] == "The Shadow of the Wind (La sombra del viento)" )
                                   | (df_book['Book'] == "Interpreter of Maladies" )
                                   | (df_book['Book'] == "Peyton Place") 
                                   | (df_book['Book'] == "Norwegian Wood (ノルウェイの森)" )
                                   | (df_book['Book'] == "The Plague (La Peste)" )
                                   | (df_book['Book'] == "No Longer Human (人間失格)" )
                                   | (df_book['Book'] == "Catch-22") 
                                   | (df_book['Book'] == "The Lovely Bones" )
                                   | (df_book['Book'] == "Santa Evita" )  
                                   | (df_book['Book'] == "The Goal" )
                                   | (df_book['Book'] == "Bridget Jones's Diary" )                                  
                                   , "novel", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "The Outsiders")                                  
                                   , "coming-of-age", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "Guess How Much I Love You") 
                                   | (df_book['Book'] == "The Poky Little Puppy") 
                                   | (df_book['Book'] == "Ronia, the Robber's Daughter"), 
                                   "Children's fiction", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "Becoming") 
                                   | (df_book['Book'] ==  "Tuesdays with Morrie") 
                                   | (df_book['Book'] == "Long Walk to Freedom" )
                                   | (df_book['Book'] == "Man's Search for Meaning (Ein Psychologe erlebt das Konzentrationslager)" )
                                   | (df_book['Book'] == "Night (Un di Velt Hot Geshvign)") 
                                   | (df_book['Book'] == "Angela's Ashes" )
                                   | (df_book['Book'] == "The Story of My Experiments with Truth (સત્યના પ્રયોગો અથવા આત્મકથા)")                                 
                                   , "Autobiographical", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "God's Little Acre") 
                                   | (df_book['Book'] == "Tobacco Road") 
                                   , "gothic", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "A Wrinkle in Time")                                  
                                   , "Science fiction", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "The Old Man and the Sea")                                  
                                   , "Fiction", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "Life After Life") 
                                   | (df_book['Book'] ==  "The Bermuda Triangle") 
                                   | (df_book['Book'] == "Knowledge-value Revolution (知価革命)" )
                                   | (df_book['Book'] == "Problems in China's Socialist Economy (中国社会主义经济问题研究)" )
                                   | (df_book['Book'] == "The Dukan Diet") 
                                   | (df_book['Book'] == "The Joy of Sex" )                               
                                   , "Non-fiction", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "Me Before You") 
                                   | (df_book['Book'] == "The Front Runner"),
                                   "romance", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "The Divine Comedy (La Divina Commedia)") 
                                   | (df_book['Book'] == "The Prophet"), 
                                   "poetry", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "Diana: Her True Story") 
                                   | (df_book['Book'] == "Wild Swans"), 
                                   "biographical", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "The Stranger (L'Étranger)") 
                                   | (df_book['Book'] == "Confucius from the Heart (于丹《论语》心得)") 
                                   | (df_book['Book'] == "Life of Pi"), 
                                   "philosophical", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "Eye of the Needle")                                  
                                   , "thriller", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "The Total Woman") 
                                   | (df_book['Book'] == "What Color Is Your Parachute?") 
                                   | (df_book['Book'] == "The Subtle Art of Not Giving a Fuck"), 
                                   "self-help", df_book['All_Genre'] )
df_book['All_Genre'] = np.where((df_book['Book'] == "The Gospel According to Peanuts")                                  
                                   , "comic", df_book["All_Genre"])
df_book['All_Genre'] = np.where((df_book['Book'] == "Fahrenheit 451")                                  
                                   , "dystopian", df_book["All_Genre"])

## Here I am making an age category column
df_book["Age_Category"] = np.where(df_book['All_Genre'].str.contains("children", case = False), "Children", "Adult" )
df_book["Age_Category"] = np.where(df_book['All_Genre'].str.contains("Young adult", case = False, na=False), "Young Adult", df_book["Age_Category"])



## Here I am saving the cleaned dataset into one csv file
df_book.to_csv('data/top_books.csv')



## Below I am loading in the dataframes for series
df_series_1 = pd.read_csv('data/top_series4.csv')
df_series_2 = pd.read_csv('data/top_series5.csv')
df_series_3 = pd.read_csv('data/top_series6.csv')
df_series_4 = pd.read_csv('data/top_series7.csv')
df_series_5 = pd.read_csv('data/top_series8.csv')


## Here I am tidying up the format of the columns 

## Below is an initial one off fix for the third dataframe
df_series_3_book_fix = pd.DataFrame(df_series_3.loc[df_series_3["Book_Series"] == "Rich Dad"])
df_series_3_book_fix['Book_Series'] = df_series_3_book_fix[['Book_Series','Author']].agg(', '.join, axis=1)
df_series_3_book_fix = df_series_3_book_fix.drop(df_series_3_book_fix.columns[1], axis =1)
df_series_3_book_fix.columns = ["Book_Series", "Author", "Original_Language", "No_of_Installments", 
                           "Years_of_Publication", "Approximate_Sales", "Genre_1"]

df_series_3 = pd.DataFrame(df_series_3.loc[df_series_3["Book_Series"] != "Rich Dad"])
df_series_3 = pd.concat([df_series_3, df_series_3_book_fix])

## Start creating combined series dataframe 
## I leave out the fourth dataset as it has genres that the others do not
df_series = pd.concat([df_series_1, df_series_2, df_series_3, df_series_5])

## Below is a one off fix for the fourth dataframe
df_series_4_sales_fix = pd.DataFrame(df_series_4.loc[df_series_4["Book_Series"] == "鬼平犯科帳 (Onihei Hankachō)"])
df_series_4_sales_fix = df_series_4_sales_fix.drop(df_series_4_sales_fix.columns[-2], axis =1)
df_series_4_sales_fix.columns = ["Book_Series", "Author", "Original_Language", "No_of_Installments", 
                           "Years_of_Publication", "Approximate_Sales", "Genre_1"]

df_series_4 = pd.DataFrame(df_series_4.loc[df_series_4["Book_Series"] != "鬼平犯科帳 (Onihei Hankachō)"])
df_series_4 = pd.concat([df_series_4, df_series_4_sales_fix])


## General fixes to all other data
df_series_fix = pd.DataFrame(df_series[df_series.Genre_1.notna()])
df_series_fix['Author'] = df_series_fix[['Author', 'Original_Language']].agg(', '.join, axis=1)
df_series_fix = df_series_fix.drop(df_series_fix.columns[2], axis =1)
df_series_fix.columns = ["Book_Series", "Author", "Original_Language", "No_of_Installments", 
                           "Years_of_Publication", "Approximate_Sales", "Genre_1"]

df_series = pd.DataFrame(df_series[df_series.Genre_1.isna()])
df_series = pd.concat([df_series, df_series_fix])


## Here I finish the combined series dataframe
df_series = pd.concat([df_series, df_series_4])



## I am now making correction to sales column in a similar way to the book dataframe

# niche changes with decimals
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace('36.52 million', '36520000')
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace('33.6 million', '33600000')
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace('21.5 million', '21500000')
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace('24.4 million', '24400000')
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace('23.7 million', '23700000')

# adding extra general changes
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace(' million', '000000')
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace(' Million', '000000')
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace(' ', '')

# adding some regular expression corrections
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace(r'\[\d{3}\]', r'', regex=True)
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace(r'\[\d{2}\]', r'', regex=True)
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].str.replace(r'[A-Za-z]', r'', regex=True)


## Adding a correction to Years_of_Publication for easier processing later
df_series["Years_of_Publication"] = df_series["Years_of_Publication"].str.replace('present', '2025')  
df_series["Years_of_Publication"] = df_series["Years_of_Publication"].str.replace(r'–$', '-2025', regex=True)
df_series["Years_of_Publication"] = df_series["Years_of_Publication"].str.replace(r'–93$', '–1993', regex=True) 
df_series["First_Installment_Published"] = df_series["Years_of_Publication"].str[:4]
df_series["Last_Installment_Published"] = df_series["Years_of_Publication"].str[-4:]


## Adding a correction to No_of_Installments for easier processing later
df_series['No_of_Installments'] = df_series['No_of_Installments'].str.replace(r'\[\d{3}\]', r'', regex=True)
df_series['No_of_Installments'] = df_series['No_of_Installments'].str.replace('more than ', '')
df_series['No_of_Installments'] = df_series['No_of_Installments'].str.replace('over ', '')
df_series['No_of_Installments'] = df_series['No_of_Installments'].str.replace('plus', '+')
df_series['No_of_Installments'] = df_series['No_of_Installments'].str.replace(r'\+$', r'', regex=True)
df_series['No_of_Main_Books'] = df_series['No_of_Installments'].str.extract(r'(^\d{1,3})')
df_series['No_of_Extras'] = df_series['No_of_Installments'].str.replace(r'(^\d{1,3})', r'', regex = True)
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace(r'[A-Za-z]', r'', regex=True)
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace(' ', '')
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace('-', '')
df_series['Extras'] = (df_series['No_of_Extras'] != "")
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace(r'^\+', r'', regex=True)
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace('3+4', '7')
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace('5+4', '9')
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace('2+1', '3')
df_series['No_of_Extras'] = df_series['No_of_Extras'].str.replace('3+1', '4')
df_series["No_of_Extras"] = np.where(df_series["No_of_Extras"] == "", np.nan, df_series["No_of_Extras"])


## Below I am fixing datatypes for future analysis
df_series['Approximate_Sales'] = df_series['Approximate_Sales'].map(int)
df_series['First_Installment_Published'] = df_series['First_Installment_Published'].map(int)
df_series['Last_Installment_Published'] = df_series['Last_Installment_Published'].map(int)
df_series['No_of_Extras'] = df_series['No_of_Extras'].map(float)


## Here I am making a combined genre column
df_series["All_Genre"] = df_series[["Genre_1", "Genre_2"]].apply(lambda x: ','.join(x.dropna()), axis=1)


## Here I am adding a length of years from first to last installment column
df_series["Number_of_Years_Publication"] = df_series["Last_Installment_Published"] - df_series["First_Installment_Published"]

## Here I am saving the cleaned dataset into one csv file
df_series.to_csv('data/top_series.csv')