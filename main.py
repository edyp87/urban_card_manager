import UrbanCardDataRetriever
import getpass

username = input("Prosze podac adres mailowy: " , )
password = getpass.getpass("Prosze podac haslo: ")

UrbanCardDataRetriever.UrbanCardDataRetriever(username, password).getCardsData()
