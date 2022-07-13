"""
This class takes in a jsonReader and cleanedData object. It outputs the cleaned data in the account format ready to be uploaded.
"""

import pandas as pd

class AccFormat:

    """
    @jsonRead: from which AccFormatFile path is taken from
    @clean_data: from which reformatted data is taken from
    creates a new accFormat dataFrame, fills in the columns of the dataFrame, and saves the new dataFrame as a csv file
    """
    def __init__ (self,jsonRead, clean_data):
        self.clean_data = clean_data
        self.jsonRead = jsonRead
        self.accFormat = pd.DataFrame(columns=['type', 'date', 'rQty', 'rPrice', 'sQty', 'sPrice', 'fQty', 'fPrice', 
        'rCoin.symbol', 'rWallet.name', 'sCoin.symbol', 'sWallet.name', 'fCoin.symbol', 'fWallet.name', 
        'ledgeraccount.number', 'notes', 'reference', 'customer.id', 'vendor.id', 'currency', 'txHash'])

        self.__fillCells()
        self.accFormat.to_csv(self.jsonRead.getAccFormatFile(), index=False), 

    """
    fills in accFormat columns respectively with data from cleaned data dataframe
    """
    def __fillCells(self):
        numRows = len(self.clean_data)
        self.accFormat['type'] = self.clean_data["Transaction Type"] 
        self.accFormat['date'] = self.clean_data["Date"]
        self.accFormat['fQty'] = self.clean_data["Network Fee"]
        self.accFormat['rCoin.symbol'] = self.clean_data["Asset Symbol"]
        self.accFormat['fCoin.symbol'] = "MATIC"
        self.accFormat['notes'] = self.clean_data["Note"]
        self.accFormat['reference'] = self.clean_data["Fireblocks TxId"]
        self.accFormat['txHash'] = self.clean_data["TxHash"]

        f_rQtyCol = 2
        f_sQtyCol = 4
        f_rWallet = 9
        f_sWallet = 11
        c_amount = 8
        c_destination = 18
        c_source = 15

        for r in range(numRows):
            tran_type = self.accFormat.iat[r, 0]
            if tran_type == "TRANSFER":
                self.accFormat.iat[r, f_rQtyCol] = self.clean_data.iat[r, c_amount]
                self.accFormat.iat[r, f_sQtyCol] = self.clean_data.iat[r, c_amount]
                self.accFormat.iat[r, f_rWallet] = self.clean_data.iat[r, c_destination]
                self.accFormat.iat[r, f_sWallet] = self.clean_data.iat[r, c_source]
            elif tran_type == "WITHDRAW":
                self.accFormat.iat[r, f_sQtyCol] = self.clean_data.iat[r, c_amount]
                self.accFormat.iat[r, f_sWallet] = self.clean_data.iat[r, c_source]
            elif tran_type == "DEPOSIT":
                self.accFormat.iat[r, f_rQtyCol] = self.clean_data.iat[r, c_amount]
                self.accFormat.iat[r, f_rWallet] = self.clean_data.iat[r, c_destination]
    