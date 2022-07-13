"""
This class cleans data pulled from the read in config.json file per this table: 

IN - address shows wallet is internal
OUT - address shows wallet is not in internal wallet
BRIDGE - address shows wallet is bridge wallet 

___________________________________________________________________________
Source  |Destination  |Data Kept (y/n) |Type
___________________________________________________________________________
IN      |IN           |y               |transfer
___________________________________________________________________________
IN      |OUT          |y               |withdraw
___________________________________________________________________________
IN      |BRIDGE       |y               |transfer
___________________________________________________________________________
OUT     |IN           |y               |deposit
___________________________________________________________________________
OUT     |OUT          |n               |N/A
___________________________________________________________________________
OUT     |BRIDGE       |y               |deposit
___________________________________________________________________________
BRIDGE  |IN           |y               |transfer
___________________________________________________________________________
BRIDGE  |OUT          |y               |withdraw
"""

import pandas as pd

class CleanedData():

   # sourceAddress column index 
   global sourceColIndex 
   sourceColIndex = 16

   # destinatinoAddress column index
   global destColIndex 
   destColIndex = 19

   """
   @jsonRead: a JsonReader object 

   saves JsonReader object as an instance variable
   creates an AddressDictionary and saves it as an instance variable 
   """
   def __init__(self, jsonRead):
      self.jsonRead = jsonRead
      self.addressDic = self.jsonRead.getAddressDic()
      self.__clean_data()

   """
   @in_address: input address 

   determines if in_address is an internal wallet address by looking through addressDic values 
   """
   def __isInAddressBook(self, in_address):
      if in_address in self.addressDic.values(): return True
      else: return False

   """
   @source: source address 
   @destination: destination address

   compares relationship between source + destination addresses to determine transaction type
   """
   def __getTransactionType(self, source, destination):
      isSource = self.__isInAddressBook(source)
      isDestin = self.__isInAddressBook(destination)

      if (isSource is False) and (isDestin is False):
         return 'N/A'

      elif (isSource is False) and (isDestin is True):
         return 'DEPOSIT'

      elif (isSource is True) and (isDestin is False):
         return 'WITHDRAW'

      elif (isSource is True) and (isDestin is True):
         return 'TRANSFER'

   def getCleanDataDf(self):
      return self.clean_data_df

   """
   cleans data and outputs a cleanData csv sheet
   """
   def __clean_data(self):
      # reading in inputfile as a csv, removing index column, and making sure N/A doesn't become NaN
      df = pd.read_csv(self.jsonRead.getInputFile(), index_col=False, keep_default_na=False)

      # filters for CONFIRMED under sub-status 
      confirmed_filter = df["Sub-Status"] == 'CONFIRMED'
      df = df[confirmed_filter]
      

      # filters out API-Wallet under Source tab
      api_filter = df["Source"] != 'API - Wallet'
      df = df[api_filter]

      # filters out data where both source and address are NOT in addressBook 
      source_address_filter = df["Source Address"].isin(self.addressDic.values())
      destination_address_filter = df["Destination Address"].isin(self.addressDic.values())
      all_address_filter = source_address_filter | destination_address_filter
      df = df[all_address_filter]

      # determining transaction type and creating transaction type column
      numRows = len(df)
      df.insert(0, "Transaction Type", "N/A")
      for r in range(numRows):
         df.iat[r, 0] = self.__getTransactionType(df.iat[r, sourceColIndex], df.iat[r, destColIndex])

      self.clean_data_df = df

      # saving cleaned data in a new csv file
      df.to_csv(self.jsonRead.getOutputFile(), index=False)
