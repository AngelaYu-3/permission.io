import argparse
import json as js

class JsonReader:
    
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
        self.toAddressDic()
    
    def toAddressDic(self):
        self.new_dict = {}

        for i in self.df['InternalWalletAddresses']:
            self.new_dict[i['walletname']] = i['address']

    def getAddressDic(self):
        return self.new_dict

    def getInputFile(self):
        return self.df["Input_Output"][0]["input"]

    def getOutputFile(self):
        return self.df["Input_Output"][0]["output"]
