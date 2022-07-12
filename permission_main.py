import jsonReader
import cleanedData


def main():

    dc = jsonReader.JsonReader()

    cd = cleanedData.CleanedData(dc)
    cd.clean_data()


if __name__ == '__main__':
    main()