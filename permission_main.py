import cleanData
filename = 'data/testData1.csv'

def main():
    # cleaning data based on inputted raw data
    cleanData.clean_data(filename)

if __name__ == '__main__':
    main()