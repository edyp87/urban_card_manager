import UrbanCardDataRetriever
import getpass

def getUserDataFromFile():
    lines = open('user_data').read().splitlines()
    return (lines[0], lines[1])

def getUserDataFromConsole():
    username = input("Prosze podac adres mailowy: " , )
    password = getpass.getpass("Prosze podac haslo: ")
    return (username, password)


username, password = getUserDataFromFile()
UrbanCardDataRetriever.UrbanCardDataRetriever(username, password).getCardsData()
