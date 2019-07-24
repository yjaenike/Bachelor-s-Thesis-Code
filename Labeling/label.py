import pandas as pd
import time
from datetime import datetime


def display_text(paragraph,spacer = False):
    """
    Dispaly text to the user if space = True, make a big space between old and new output
    """
    if spacer:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(paragraph)


def get_input(message):
    """
    Ask the user for user input
    message : is the question the user is asked.

    Return
    my_input : is the value the user gave back on teh console
    """
    my_input = input(message+"\n> ")
    return my_input

def main():

    df = pd.read_csv("dataset.csv")
    length = len(df)

    # Print initial instructions
    instructions = """
    #----------------------------------------------------------------------------------------------------------------------------------------------#
    In der Folgenden Aufgabe sollst du die Ansicht des Folgenden Paragraphen categorisieren in entweder 'neutral', 'positiv' oder 'negativ'.
    Um die Ansicht zu categorisieren, benutze den folgenden code:\n
        Negativ = 1
        Neutral  = 2
        Positiv = 3

    Du sollst nicht die Emotionen bewerten, sondern die rationale Ansicht der Paragraphen.
    #----------------------------------------------------------------------------------------------------------------------------------------------#
    """
    display_text(instructions,1)



    # Ask if the Annotator is ready
    beginn = get_input("Bist du bereit? [j/n]")
    while not beginn == "j":
        beginn = get_input("Bist du bereit? [j/n]")



    # Check where to start labeling.
    #Create iterator object
    check_start = df.iterrows()
    for numerator, start in enumerate(check_start):
        # if the label is 0, the paragraph is not yet labeled
        if start[1]["label"] == 0:
            display_text("\nStaring at row number: {}\n".format(numerator))
            break
    time.sleep(3)



    # Create new iterator object
    rows = df.iterrows()
    for numerator, row in enumerate(rows):

        # save backup and overwrite dataset every 10 paragraphs
        if numerator % 10 == 0:
            df.to_csv("dataset.csv", index = False)
            df.to_csv("backup_dataset_{}.csv".format(str(datetime.now()).split(".")[0]), index = False)

        # if the paragraph label is 0 (not yet labeled)
        if row[1]["label"] == 0:
            # Display the text to the user
            display_text(row[1]["text"],1)
            # Ask for a label
            label = get_input("\nBerichtet dieser Paragraph negativ(1), neutral(2), positiv(3)?")
            # Check if the label is allowed
            while label not in ['1', '2', '3']:
                display_text("\nBitte wähle zwischn 1 , 2 , 3.")
                label = get_input("Berichtet dieser Paragraph negativ(1), neutral(2), positiv(3)?")
            # change label in dataset
            df.loc[numerator,"label"] = label

    # All paragraphs have been labled
    display_text("Finished.")


if __name__ == "__main__":
    main()
