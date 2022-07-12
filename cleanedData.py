import pandas as pd

class CleanedData():

   global sourceColIndex 
   sourceColIndex = 16

   global destColIndex 
   destColIndex = 19

   def __init__(self, jsonRead):
      self.jsonRead = jsonRead
      self.jsonRead.toAddressDic()
      self.addressDic = self.jsonRead.getAddressDic()

   # determines if in_address is an internal wallet address 
   def _isInAddressBook(self, in_address):
      if in_address in self.addressDic.values(): return True
      else: return False

   # compares relationship between source + destination addresses to determine transaction type
   def _getTransactionType(self, source, destination):
      isSource = self._isInAddressBook(source)
      isDestin = self._isInAddressBook(destination)

      if (isSource is False) and (isDestin is False):
         return 'N/A'

      elif (isSource is False) and (isDestin is True):
         return 'DEPOSIT'

      elif (isSource is True) and (isDestin is False):
         return 'WITHDRAW'

      elif (isSource is True) and (isDestin is True):
         return 'TRANSFER'


   def clean_data(self):
      df = pd.read_csv(self.jsonRead.getInputFile(), index_col=False, keep_default_na=False)

      # filtering for CONFIRMED under sub-status for all data
      confirmed_filter = df["Sub-Status"] == 'CONFIRMED'
      df = df[confirmed_filter]
      

      # filtering out API-Wallet under Source tab
      api_filter = df["Source"] != 'API - Wallet'
      df = df[api_filter]

      # filtering out data where both source and address are NOT in addressBook 
      source_address_filter = df["Source Address"].isin(self.addressDic.values())
      destination_address_filter = df["Destination Address"].isin(self.addressDic.values())
      all_address_filter = source_address_filter | destination_address_filter
      df = df[all_address_filter]

      # determining transaction type and creating transaction type column
      numRows = len(df)
      df.insert(0, "Transaction Type", "N/A")
      for r in range(numRows):
         df.iat[r, 0] = self._getTransactionType(df.iat[r, sourceColIndex], df.iat[r, destColIndex])

      df.to_csv(self.jsonRead.getOutputFile(), index=False)
