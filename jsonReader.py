"""
This class takes in a json file from the command line and pulls out the necessary information
from the file. This includes putting the wallets/addresses in a dictionary format and getting the
input and output file paths. 
"""

import argparse
import json as js

class JsonReader:
    
    """
    parses in config.json path from the command-line
    loads json_file using the parsed in path
    creates a dictionary with key value pairs of wallet + address pulled from config.json file
    """
    def __init__(self):
        my_parser = argparse.ArgumentParser(description='List the content of a folder')
        my_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='the path to list')
        args = my_parser.parse_args()
        json_file = open(args.Path)
        self.df = js.load(json_file)
        json_file.close()
        self.__toAddressDic()
    
    """
    creates a dictionary with key value pairs of wallet + address pulled from config.json file
    """
    def __toAddressDic(self):
        self.new_dict = {}

        for i in self.df['InternalWalletAddresses']:
            self.new_dict[i['walletname']] = i['address']

    """
    returns address dictionary
    """
    def getAddressDic(self):
        return self.new_dict

    """
    returns input file path
    """
    def getInputFile(self):
        return self.df["Input_Output"][0]["input"]

    """
    returns output file path
    """
    def getOutputFile(self):
        return self.df["Input_Output"][0]["output"]

    """
    returns accFormat file path
    """
    def getAccFormatFile(self):
        return self.df["Input_Output"][0]["accFormat"]
