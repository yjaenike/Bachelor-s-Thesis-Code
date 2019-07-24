import pandas as pd
import numpy as np
import csv
import sys

doc_name = sys.argv[1]
if "." in doc_name:
    doc_name_list= doc_name.split(".")
    doc_name = doc_name_list[0]

with open('{}.txt'.format(doc_name), mode='r') as substances:
    stripped =(line.strip() for line in substances)
    lines = (line.split(" ") for line in stripped if line)

    with open('{}.csv'.format(doc_name), 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
