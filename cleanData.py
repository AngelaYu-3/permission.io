import pandas as pd
import json as j

filename = 'testData.csv'
addBook = open('addressBook.json')
addBook = j.load(addBook)
addressBook = []

# takes addresses from json format and puts them in addressBook list
def addressBookList():
   addBookLen = len(addBook["InternalWalletAddresses"])
   for a in range(addBookLen):
      addressBook.append(addBook["InternalWalletAddresses"][a]["address"])

# determines if in_address is an internal wallet address 
def inAddressBook(in_address):
   addBookLen = len(addBook["InternalWalletAddresses"])
   for a in range(addBookLen):
      if in_address == addBook["InternalWalletAddresses"][a]["address"]:
         return True
   return False

# compares relationship between source + destination addresses to determine transaction type
def transactionType(source, destination):
   isSource = inAddressBook(source)
   isDestin = inAddressBook(destination)

   if (isSource is False) and (isDestin is False):
      return 'N/A'

   elif (isSource is False) and (isDestin is True):
      return 'DEPOSIT'

   elif (isSource is True) and (isDestin is False):
      return 'WITHDRAW'

   elif (isSource is True) and (isDestin is True):
      return 'TRANSFER'


def main():
   addressBookList()
   df = pd.read_csv(filename)

   # filtering for CONFIRMED under sub-status for all data
   confirmed_filter = df["Sub-Status"] == 'CONFIRMED'
   df = df[confirmed_filter]

   # filtering out data where both source and address are NOT in addressBook 
   source_address_filter = df["Source Address"].isin(addressBook)
   destination_address_filter = df["Destination Address"].isin(addressBook)
   all_address_filter = source_address_filter | destination_address_filter
   df = df[all_address_filter]

   # determining transaction type and creating transaction type column
   numRows = len(df)
   df.insert(0, "Transaction Type", "N/A")
   for r in range(numRows):
      df.iat[r, 0] = transactionType(df.iat[r, 16], df.iat[r, 19])

   df.to_csv('cleanTestData.csv')
   

if __name__ == '__main__':
    main()
