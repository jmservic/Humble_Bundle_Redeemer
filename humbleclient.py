from abc import ABC, abstractmethod

HUMBLE_MAIN = "https://www.humblebundle.com/"

class GameKeyClient(ABC):

    @abstractmethod
    def Login(self, login, password):
        pass

    @abstractmethod
    def GetGamesInfo():
        pass

    @abstractmethod
    def ChooseContent(gamekey, identifiers):
        pass

    @abstractmethod
    def RedeemKey(keytype, gamekey, keyindex):
        pass

class HumbleClient(GameKeyClient):
    
    def __init__(session):
        if not session:
            raise Exception("session cannot be null")
        self.__session = session

    def Login(self, login, password):
        pass

    def GetGamesInfo():
        pass

    def ChooseContent(gamekey, identifiers):
        pass

    def RedeemKey(keytype, gamekey, keyindex=0):
        pass
