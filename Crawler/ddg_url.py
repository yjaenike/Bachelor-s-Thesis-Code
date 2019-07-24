import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
import sys


def main():
    #Reading in substances and websites to crawl
    # if user specfied documents, use them
    substances, url, start = get_input()

    # load the documents into a pandas dataframe
    substances = pd.read_csv(substances)
    url = pd.read_csv(url)

    # list of all the produkt names
    product_name_list = substances["Produkt_Name"].tolist()

    # The pass to the chrome webdriver, has to be specified before usage.
    PATH_TO_WEBDRIVER = "MY/PATH/TO/THE/WEBDRIVER/chromedriver"
    browser = webdriver.Chrome(PATH_TO_WEBDRIVER)
    for i in url.itertuples():
        get_url(i[1], product_name_list, browser, start)
        None
    browser.quit()

def get_url(url,substances, browser, start = 0):
    """
    Get the urls of the specified variables. The start variable specifies the substance, at which
    we will start the list. If the Algorithm stops early, we can specify the indice of the substance, to not run everything all over again.

    url : website to search for
    susbtances : product names of the substances
    browser : the browser object opened
    start : the number (indice) of the substance to start looking
    """

    # Generate specifc document name for each website
    doc_name = url
    doc_name_list= doc_name.split(".")

    # Open Google Chrome and the duckduckgo serach page
    browser.get('https://duckduckgo.com/')

    # Open/create new document for urls
    with open('url_{}.txt'.format(doc_name_list[1]), 'a+') as out_file:
        out_file.write("url source substance\n")
        # Open Browser
        # Iterate over substance list
        for c, substance in enumerate(substances[start:], start+1):
            # Create specific search phrase
            search_phrase = 'site:{} "{}"'.format(url,substance)

            # Terminal User Output
            output = "{}/{} - {} ".format(str(c),str(len(substances)), search_phrase)
            print(output)

            # Find the Search field and search for phrase
            search = browser.find_element_by_name('q')
            search.clear()
            search.send_keys(search_phrase)
            search.send_keys(Keys.RETURN) # hit return after you enter search text

            #Extract url adress from search results
            results = browser.find_elements_by_css_selector('div.result__body.links_main.links_deep')
            for result in results:
                link = result.find_element_by_tag_name("a")
                href = link.get_attribute("href")
                # If no search results found don't write anything
                if "duckduckgo" in href:
                    pass
                else:
                    # write url to file
                    out_file.write(href+" "+search_phrase+" \n")

            # sleep for 5 seconds
            time.sleep(0)


def print_usage_message(error):
    """
    If the User gives an invalid input, give an error message to state how the input should be structured

    Specific flags can be used to specify document names etc.
    -s to specifie the file with the substance names
    -u to specifie the file with the urls
    -l to specify the substance to start with (Integer indice of the line of the substance in -s)
    Example of Usage : python ddg_url.py -s substances.csv -u websites.csv -l 0

    error : The occured error
    """

    usage = """\n    Use:python ddg_url.py FLAGS\n    possible flags are:
            -s to specifie the file with the substance names
            -u to specifie the file with the urls
            -l to specify the substance to start with (Integer indice of the line of the substance in -s)
    \n             For example: python ddg_url.py -s substances.csv -u websites.csv -l 0"""

    # Error messages
    if error == "wrong input length":
        print("Error: Argument error"+usage)
    if error == "wrong flag":
        print("Error: Flag not known"+usage)

def get_input():
    """
    Get the user input if there is any, otherwise use the specified value sfor substance_name,
    url_name, line_name.

    Return
    substance_name : csv file of the substances that we want to search for
    url_name : csv file of the websited, that we want to search
    line_name : integer, indice of a substance in the substance_name file, at that we want to start the serach

    """

    # Initial configuration
    substance_name = "substances.csv"
    url_name = "websites.csv"
    line_name = 0

    # Get the user input
    input = sys.argv[1:]

    #Check if input length is possible
    if not len(input) % 2 == 0:
        print_usage_message("wrong input length")
        sys.exit()
    #Check if flags are konwn
    for flag in input[::2]:
        if flag not in ["-s", "-u", "-l"]:
            print_usage_message("wrong flag")
            sys.exit()

    # Check the flags for the different values
    for indice in range(0,len(input),2):
        if input[indice] == "-s":
            substance_name = input[indice+1]
        if input[indice] == "-u":
            url_name = input[indice+1]
        if input[indice] == "-l":
            line_name = int(input[indice+1])

    return substance_name, url_name, line_name

if __name__ == "__main__":
    main()
