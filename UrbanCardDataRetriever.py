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

    def __init__(self, cardNumber):
        self.cardNumber = cardNumber
        self.slot = { self.Slot(), self.Slot() }

    def getFirstSlot(self):
        return self.slot[0]

    def getSecondSlot(self):
        return self.slot[1]


class UrbanCardDataRetriever:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.card = None
        self.session = None
        self.url = "https://sklep.urbancard.pl/wkz/DefaultIframe.aspx?l=1"
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.1) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/37.0.2062.120 "
                "Safari/537.36"}

    def getCardsData(self):
        if self.card:
            return self.card;
        self.createSession()
        self.login()
        self.getCardData()
        self.logout()

    def createSession(self):
        self.session = Session()
        self.session.headers.update(self.headers)
        self.session.lastResponse = self.session.get(self.url)
        print("GET URL       : " + str(self.session.lastResponse))
        self.saveNewState()

    def login(self):
        login_data = \
            {"__VIEWSTATE": self.session.VIEWSTATE,
             "__VIEWSTATEGENERATOR": self.session.VIEWSTATEGENERATOR,
             "__EVENTVALIDATION": self.session.EVENTVALIDATION,
             "ctl00$tbUserName": self.username,
             "ctl00$tbPassword": self.password,
             "ctl00$btnLogin": "zaloguj"}
        self.postDataAndStore(login_data)
        print("LOGIN         : " + str(self.session.lastResponse))
        self.saveNewState()
        self.storeCardNumber()


    def getCardData(self):
        member_data = \
            {"__VIEWSTATE": self.session.VIEWSTATE,
             "__VIEWSTATEGENERATOR": self.session.VIEWSTATEGENERATOR,
             "__EVENTVALIDATION": self.session.EVENTVALIDATION,
             "ctl00$ContentPlaceHolder1$buyControl$ddlMemberCards": self.memberCard.cardNumber,
             "ctl00$ContentPlaceHolder1$buyControl$btnAcceptCardChoice": "dalej"}
        self.postDataAndStore(member_data)
        print("GET CARD DATA : " + str(self.session.lastResponse))
        self.saveNewState()
        self.storeCardData()


    def logout(self):
        logout_data = \
            {"__VIEWSTATE": self.session.VIEWSTATE,
             "__VIEWSTATEGENERATOR": self.session.VIEWSTATEGENERATOR,
             "__EVENTVALIDATION": self.session.EVENTVALIDATION,
             "ctl00$btnLogout": "wyloguj"}

        self.postDataAndStore(logout_data)
        print("LOGOUT        : " + str(self.session.lastResponse))

    def saveNewState(self):
        self.session.lastSoup = BeautifulSoup(self.session.lastResponse.content, "lxml")
        self.session.VIEWSTATE = self.session.lastSoup.find(id="__VIEWSTATE")['value']
        self.session.VIEWSTATEGENERATOR = self.session.lastSoup.find(id="__VIEWSTATEGENERATOR")['value']
        self.session.EVENTVALIDATION = self.session.lastSoup.find(id="__EVENTVALIDATION")['value']

    def postDataAndStore(self, data):
        self.session.lastResponse = self.session.post(self.session.lastResponse.url, data=data)

    def storeCardNumber(self):
        self.memberCard = Card(
            self.session.lastSoup.find(id="ctl00_ContentPlaceHolder1_buyControl_ddlMemberCards").option['value'])

    def storeCardData(self):
        print(re.sub("<.*?>", "", str(
            BeautifulSoup(self.session.lastResponse.content, "lxml").find(id="pocketRow").find_all("td")[3])))
        print(re.sub("<.*?>", "", str(
            BeautifulSoup(self.session.lastResponse.content, "lxml").find(id="pocketRow").find_all("td")[4])))




