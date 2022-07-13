"""
This is the main file from which the program is executed
"""

import jsonReader
import cleanedData
import accFormat

def main():

    # creating a jsonReader object
    # reading in json file and putting wallet/addresses in a dictionary format
    data_str = jsonReader.JsonReader()

    # creating a cleanedData object that takes in jsonReader object
    # cleaning data per guidelines listed in cleanData.py
    clean = cleanedData.CleanedData(data_str)

    # putting cleaned data in accountFormat format
    accFormat.AccFormat(data_str, clean.getCleanDataDf())


if __name__ == '__main__':
    main()