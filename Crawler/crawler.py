from newsplease import NewsPlease
import pandas as pd
import csv
import sys
from urllib.error import URLError, HTTPError
import urllib


def get_data(url):
    """
    Extract the data from a specific url of a news article

    url : the url of the article, that we want to extract information from_url

    Return
    article.title : the title of the article
    article.text : the text block of the article
    article.date_publish :the data the article was published
    article.description : a short description of the article
    article.language : the language in that the article is written
    article.date_modify : the date the article was modifeied if it was
    article.url : the url of the article (same as input url)

    """

    # Try downloading the article
    try:
        article = NewsPlease.from_url(url)
    # catch HTTPError and return empty values instead
    except urllib.error.HTTPError as err:
        # Print the error code
        print("HTTPError Found: ",err.code)
        return "", "", "", "", "", "", ""
    print("Data Extracted.")
    return article.title, article.text, article.date_publish, article.description, article.language, article.date_modify, article.url

def get_doc_name():
    """
    Get the name of the input file the user has to specified
    The file has to have the format url_SOMEWEBSITENAME.csv and the file has to have the
    Return:
    doc_name : a stripped down version of the document name.
    """

    # Check if an input file was given
    if len(sys.argv) == 1:
        sys.exit("No input file given")

    # remove the type if it exists
    doc_name = sys.argv[1].split(".")[0]
    # remove the frontpart
    doc_name = doc_name.split("_")[1]
    print("Doc Name Loaded.")
    return doc_name

def main():
    # Get the input document name
    doc_name = get_doc_name()
    # load the file with the url adresses
    source = pd.read_csv("url_{}.csv".format(doc_name))

    # Create the Dataframe
    df = pd.DataFrame(columns=['substance', 'product', 'year', 'month', 'title', 'text', 'date_published', 'description', 'language', 'isModified', 'url'])

    # Number of items for terminal user output
    print(source.head())
    n = len(source["url"].tolist())
    # Create Dictionary with information from the substance list
    substances = pd.read_csv("substances.csv")
    substances = substances.set_index('Produkt_Name').T.to_dict('list')

    # for each url in the url file, and the according product name, and its index in the list:
    for link, product_name, item in zip(source["url"].tolist(), source["substance"].tolist(), list(range(len(source["url"].tolist())))):
        # Get data from website
        title, text, date, desc, lang, date_modify, url = get_data(link)
        # Get data from subatnce.csv file
        substance_values = substances[product_name.split('"')[1].split('"')[0]]

        # Append current article to the data frame
        df = df.append({'substance' : substance_values[0], 'product' : product_name, 'year' : substance_values[2], 'month' : substance_values[1], 'title' : title, 'text': text, 'date_published' : date, 'description' : desc, 'language' : lang, 'isModified' : 1 if date_modify else 0, 'url' : url} , ignore_index=True)
        # Generate Userotput
        print("{}/{} - {}".format(item, n, product_name))
        #df.to_csv('data_{}.csv'.format(doc_name), index = None)




    # Convert the pandas dataframe to a csv file and save
    df.to_csv('data_{}.csv'.format(doc_name), index = None)
    print("Created CSV file.")

if __name__ == "__main__":
    main()
