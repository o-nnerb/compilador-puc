from .LexerEnum import LexerEnum

class LexerToken:
    token = 0
    value = 0

    def __init__(self, token, value):
        self.token = token
        self.value = value
    
    def getToken(self):
        return self.token
    
    def getValue(self):
        return self.value

    @staticmethod
    def endline():
        return LexerToken(LexerEnum.endline, "end")