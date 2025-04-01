------------------------------------
Title: Blog Post on Book Statistics
Author: 710020717
Date: 2025-03-25
------------------------------------

## Introduction 

This project aims to create a blog post based on book statistics found in the dataset found via https://en.wikipedia.org/wiki/List_of_best-selling_books#List_of_best-selling_individual_books. It will aim to model the data and create visualisation to then add to a blog post analysing the data.

## Repository Overview 
This repository is structured as follows:

├── data/
    ├──top_books0.csv
    ├──top_books1.csv
    ├──top_books2.csv
    ├──top_books3.csv
    ├──top_books.csv
    ├──top_series4.csv
    ├──top_series5.csv
    ├──top_series6.csv
    ├──top_series7.csv
    ├──top_series8.csv
    └──top_series.csv
├── source/
    ├──webscrape_data.py
    ├──data_set_up.py
    └──summary_and_visualisations.ipynb
├── results/ 
    ├──book_language_age.png
    ├──book_language_scatter.png
    ├──cummulative_sales_plot.png
    ├──first_to_last_installment_plot.png
    ├──genre_pie_chart.png
    ├──interactive_book_language_scatter.html
    ├──interactive_genre_pie.html
    ├──number_books_series.png
    └──sales_per_language.png
├── blog.txt 
├── Makefile
└── README.txt

All data is contained in the data sub-directory, all source code is contained
in source, and all output is automatically exported to results. 


## Running Instructions

To replicate the results, set the main 710020717 folder as the working directory.

It should be sufficient to to type "make" in the command line to run the Makefile.

Alternatively, the below can be run individually:
(1) Run the webscrape_data.py script within the source folder. This webscrapes the data from the website linked in the introduction. Then the data is saved to data folder.
(2) Run the data_set_up.py script within the source folder. This cleans and reformats the data created from the webscrape. Then the data is saved to data folder.
(3) Run the summary_and_visualisations.ipynb Jupiter Notebook. This creates the visualisations used in the blog. These visualisations can be viewed either directly in the notebook or will automatically be saved to the results folder.

The blog post and github repository can be accessed using the links within the blog.txt file.

This has been tested using Python 3.9.13 within VSCode via MacOS. 
Within Python, the following libraries and versions were used:
> urllib3 2.3.0
> beautifulsoup4 4.13.3
> pandas 2.2.3
> re 2.2.1
> numpy 2.2.4 (for directly using Jupyter Notebook) and 1.26.4 (for using the Makefile)
> matplotlib 3.10.1
> seaborn 0.13.2
> plotly 6.0.1
> IPython 9.0.2
> runpynb 0.3.0