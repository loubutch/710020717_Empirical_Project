## Getting and Cleaning the Book Data ##

## This uses webscrapping to access the data

from urllib import request, error
from bs4 import BeautifulSoup

site = 'https://en.wikipedia.org/wiki/List_of_best-selling_books#List_of_best-selling_individual_books'

response = BeautifulSoup(request.urlopen(site),'html.parser')

for i in range(0, 4):
    TAB = response.find_all('table', class_='wikitable sortable')[i]
    print(TAB)

    rows = TAB.find_all('tr')
    print(rows)

    with open('data/top_books{i}.csv'.format(i=i), 'w') as file:
        file.write('Book, Author(s), Original Language, First Published, Approximate Sales, Genre')
        for row in rows:
            cells = row.find_all('td')
            row_contents = []
            for cell in cells:
                # Write the contents of the cell to the file
                row_contents.append(cell.text.strip())
            print(row_contents)    
            file.write(','.join(row_contents) + '\n')   