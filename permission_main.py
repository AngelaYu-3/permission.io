"""
This is the main file from which the program is executed
"""

import jsonReader
import cleanedData
import accFormat

def main():

    # creating a jsonReader object
    # reading in json file and putting wallet/addresses in a dictionary format
    dc = jsonReader.JsonReader()

    # creating a cleanedData object that takes in jsonReader object
    # cleaning data per guidelines listed in cleanData.py
    cd = cleanedData.CleanedData(dc)

    # putting cleaned data in accountFormat format
    accFormat.AccFormat(dc, cd.getCleanDataDf())


if __name__ == '__main__':
    main()