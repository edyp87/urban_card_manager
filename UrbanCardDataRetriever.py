import datetime
from requests import Session
from bs4 import BeautifulSoup
import re

class Card:
    class Slot:
        def __init__(self):
            self.expirationDate = None
            self.ticketType = None
            self.lines = None

        def __str__(self):
             return "Ważna do   : %s\n"\
                    "Typ biletu : %s\n"\
                    "Linie      : %s\n" % (self.expirationDate, self.ticketType, self.lines)

    def __init__(self, cardNumber):
        self.cardNumber = cardNumber
        self.slot = ( self.Slot(), self.Slot() )

    def getCardNumber(self):
        return self.cardNumber

    def getFirstSlot(self):
        return self.slot[0]

    def getSecondSlot(self):
        return self.slot[1]

    def __str__(self):
        return "Numer karty : %s\n%s\n%s\n" % (self.getCardNumber(), self.getFirstSlot(), self.getSecondSlot())

class UrbanCardDataRetriever:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.card = None
        self.session = None
        self.url = "https://sklep.urbancard.pl/wkz/DefaultIframe.aspx?l=1"

    def getCardsData(self):
        if self.card:
            return self.card
        self.createSession()
        self.login()
        self.getCardData()
        self.logout()
        return self.card

    def createSession(self):
        self.session = Session()
        self.session.lastResponse = self.session.get(self.url)
        print("GET URL       : " + str(self.session.lastResponse))
        self.saveNewState()

    def login(self):
        self.postAndStoreResults(self.createLoginData())
        print("LOGIN         : " + str(self.session.lastResponse))
        self.saveNewState()
        self.storeCardNumber()


    def getCardData(self):
        self.postAndStoreResults(self.createMemberData())
        print("GET CARD DATA : " + str(self.session.lastResponse))
        self.saveNewState()
        self.storeCardData()


    def logout(self):
        self.postAndStoreResults(self.createLogoutData())
        print("LOGOUT        : " + str(self.session.lastResponse))

    def saveNewState(self):
        self.session.lastSoup = BeautifulSoup(self.session.lastResponse.content, "lxml")
        self.session.VIEWSTATE = self.session.lastSoup.find(id="__VIEWSTATE")['value']
        self.session.VIEWSTATEGENERATOR = self.session.lastSoup.find(id="__VIEWSTATEGENERATOR")['value']
        self.session.EVENTVALIDATION = self.session.lastSoup.find(id="__EVENTVALIDATION")['value']

    def postAndStoreResults(self, data):
        self.session.lastResponse = self.session.post(self.session.lastResponse.url, data=data)

    def storeCardNumber(self):
        self.card = Card(
            self.session.lastSoup.find(id="ctl00_ContentPlaceHolder1_buyControl_ddlMemberCards").option['value'])

    def storeCardData(self):
        rowCardFirstSlot  = self.getRowCardSlot(0).split('\n')
        rowCardSecondSlot = self.getRowCardSlot(1).split('\n')
        self.card.getFirstSlot().expirationDate = rowCardFirstSlot[2]
        self.card.getFirstSlot().ticketType = rowCardFirstSlot[4]
        self.card.getFirstSlot().lines = rowCardFirstSlot[6]
        self.card.getSecondSlot().expirationDate = rowCardSecondSlot[2]
        self.card.getSecondSlot().ticketType = rowCardSecondSlot[4]
        self.card.getSecondSlot().lines = rowCardSecondSlot[6]

    def getRowCardSlot(self, index):
        return re.sub("<.*?>", "", str( self.session.lastSoup.find(id="pocketRow").find_all("td")[index + 3]))

    def createLoginData(self):
        return { "__VIEWSTATE"          : self.session.VIEWSTATE,
                 "__VIEWSTATEGENERATOR" : self.session.VIEWSTATEGENERATOR,
                 "__EVENTVALIDATION"    : self.session.EVENTVALIDATION,
                 "ctl00$tbUserName"     : self.username,
                 "ctl00$tbPassword"     : self.password,
                 "ctl00$btnLogin"       : "zaloguj" }

    def createMemberData(self):
        return { "__VIEWSTATE"                                              : self.session.VIEWSTATE,
                 "__VIEWSTATEGENERATOR"                                     : self.session.VIEWSTATEGENERATOR,
                 "__EVENTVALIDATION"                                        : self.session.EVENTVALIDATION,
                 "ctl00$ContentPlaceHolder1$buyControl$ddlMemberCards"      : self.card.cardNumber,
                 "ctl00$ContentPlaceHolder1$buyControl$btnAcceptCardChoice" : "dalej"}

    def createLogoutData(self):
        return { "__VIEWSTATE"          : self.session.VIEWSTATE,
                 "__VIEWSTATEGENERATOR" : self.session.VIEWSTATEGENERATOR,
                 "__EVENTVALIDATION"    : self.session.EVENTVALIDATION,
                 "ctl00$btnLogout"      : "wyloguj"}



