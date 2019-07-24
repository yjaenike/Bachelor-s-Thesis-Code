# Bachelor-s-Thesis-Code
The code used in my Bachelor's Thesis

There are four folders in this repository: Crawler, Dataset, Labeling, Sentiment.

## Crawler

ddg_url is the file to extract the urls with help of the DuckDuckGo serach engine.
To use it, one needs a csv file with substances and a csv file with webistes. 
The websites.csv file holds all the websites serached for the substances in substance.csv

You can either use the given files or use your own:

Specific flags can be used to specify document names etc.
    -s to specifie the file with the substance names
    -u to specifie the file with the urls
    -l to specify the substance to start with (Integer indice of the line of the substance in -s)
    Example of Usage : python ddg_url.py -s substances.csv -u websites.csv -l 0

The urls are than saved in a file called: "url_NameOfTheWebsite.csv"

The next script is called crawler.py. It takes a "url\_NameOfTheWebsite.csv" file and extracts all 
the information given on the website. The extracted information can be modified in the get_data() function.

The script creates a "data\_NameOfTheWebsite.csv" file with all the extracted information.

## Dataset

This folder holds the script that cleans and preprocesses the dataset. 
It takes the "data\_NameOfTheWebsite.csv" files, concatenates them and creates two new .csv files:

document.csv - Document with all the articles in one dataset

dataset.csv - Document with the completeley preprocessed dataset.

## Labeling

This script was used for labeling the samples of the dataset. 

dataset.csv is the preporcessed dataset

dataset\_clean\_backup is just a duplicate if dataset.csv

Duiring labeling, the script saves a backup of the current dataset every 10 
labels and overwrites the old dataset.csv file with the new labels.

## Sentiment

SVM\_Sentimnet.ipynb is tthe algorithm for the Suport vector machine used.

fasttext\_dropout.ipynb creates the figure of the differnet dropout rates

fasttext.ipynb is the script of the LSTM (CNN-LSTM). 

the .npy files are importan for the fasttext.ipynb script.



