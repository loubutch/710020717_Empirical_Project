# Define File Names
WEBSCRAPE := source/webscrape_data.py
DATA_SETUP := source/data_set_up.py
SUMMARY_VISUALISATIONS := summary_and_visualisations


all:
# Rule to run webscrape_dara Python script
	python3 $(WEBSCRAPE)
# Rule to run data_set_up Python script
	python3 $(DATA_SETUP)
# Rule to run summary_and_visualisations	
	cd source; runpynb $(SUMMARY_VISUALISATIONS)

	