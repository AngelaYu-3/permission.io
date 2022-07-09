import pandas as pd
import json as j

_addBook = open('addressBook.json')
_addBook = j.load(_addBook)
_addressBook = []

# takes addresses from json format and puts them in addressBook list
def _addressBookList():
   addBookLen = len(_addBook["InternalWalletAddresses"])
   for a in range(addBookLen):
      _addressBook.append(_addBook["InternalWalletAddresses"][a]["address"])

# determines if in_address is an internal wallet address 
def _inAddressBook(in_address):
   addBookLen = len(_addBook["InternalWalletAddresses"])
   for a in range(addBookLen):
      if in_address == _addBook["InternalWalletAddresses"][a]["address"]:
         return True
   return False

# compares relationship between source + destination addresses to determine transaction type
def _transactionType(source, destination):
   isSource = _inAddressBook(source)
   isDestin = _inAddressBook(destination)

   if (isSource is False) and (isDestin is False):
      return 'N/A'

   elif (isSource is False) and (isDestin is True):
      return 'DEPOSIT'

   elif (isSource is True) and (isDestin is False):
      return 'WITHDRAW'

   elif (isSource is True) and (isDestin is True):
      return 'TRANSFER'


def clean_data(filename):
   _addressBookList()
   df = pd.read_csv(filename)

   # filtering for CONFIRMED under sub-status for all data
   confirmed_filter = df["Sub-Status"] == 'CONFIRMED'
   df = df[confirmed_filter]

   # filtering out API-Wallet under Source tab
   api_filter = df["Source"] != 'API - Wallet'
   df = df[api_filter]

   # filtering out data where both source and address are NOT in addressBook 
   source_address_filter = df["Source Address"].isin(_addressBook)
   destination_address_filter = df["Destination Address"].isin(_addressBook)
   all_address_filter = source_address_filter | destination_address_filter
   df = df[all_address_filter]

   # determining transaction type and creating transaction type column
   numRows = len(df)
   df.insert(0, "Transaction Type", "N/A")
   for r in range(numRows):
      df.iat[r, 0] = _transactionType(df.iat[r, 16], df.iat[r, 19])

   df.to_csv('data/cleanTestData.csv')