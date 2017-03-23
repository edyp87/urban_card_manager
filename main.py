import UrbanCardDataRetriever
import getpass

class ColorPrinter:
    @staticmethod
    def printBlue(str):
        print('\033[94m' + str + '\033[0m')

    @staticmethod
    def printGreen(str):
        print('\033[92m' + str + '\033[0m')


def getUserDataFromFile():
    lines = open('user_data').read().splitlines()
    return (lines[0], lines[1])

def getUserDataFromConsole():
    username = input("Prosze podac adres mailowy: " , )
    password = getpass.getpass("Prosze podac haslo: ")
    return (username, password)




username, password = getUserDataFromConsole()
Card = UrbanCardDataRetriever.UrbanCardDataRetriever(username, password).getCardsData()

ColorPrinter.printBlue(str(Card.getCardNumber()))
ColorPrinter.printGreen(str(Card.getFirstSlot()))
ColorPrinter.printGreen(str(Card.getSecondSlot()))
