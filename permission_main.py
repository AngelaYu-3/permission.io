"""
This is the main file from which the program is executed
"""

import jsonReader
import cleanedData

def main():

    # creating a jsonReader object
    # reading in json file and putting wallet/addresses in a dictionary format
    dc = jsonReader.JsonReader()

    # creating a cleanedData object that takes in jsonReader object
    # cleaning data per guidelines listed in cleanData.py
    cd = cleanedData.CleanedData(dc)
    cd.clean_data()


if __name__ == '__main__':
    main()