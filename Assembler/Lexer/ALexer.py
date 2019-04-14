# Assembler Lexer

from enum import unique, Enum
import regex as re

@unique
class ALexerTokenType(Enum):
    operation = 1

    jump = 2
    jumpCmp = 3

    mov = 4
    store = 5
    load = 6

    memory = 7
    comma = 8

    register = 9
    value = 10

    pop = 11
    push = 12

    def isKeyword(self):
        if self == ALexerTokenType.operation:
            return True
        
        if self == ALexerTokenType.jump:
            return True
        
        if self == ALexerTokenType.jumpCmp:
            return True
        
        if self == ALexerTokenType.mov:
            return True
        
        if self == ALexerTokenType.store:
            return True
        
        if self == ALexerTokenType.load:
            return True

        if self == ALexerTokenType.pop:
            return True
        
        if self == ALexerTokenType.push:
            return True

        return False
    
    def countParameters(self):
        if self == ALexerTokenType.operation:
            return 3
        
        if self == ALexerTokenType.jump:
            return 1
        
        if self == ALexerTokenType.jumpCmp:
            return 3
        
        if self == ALexerTokenType.mov:
            return 2
        
        if self == ALexerTokenType.store:
            return 2
        
        if self == ALexerTokenType.load:
            return 2

        if self == ALexerTokenType.pop:
            return 1
        
        if self == ALexerTokenType.push:
            return 1

        return 0


class ALexerToken:
    value = 0
    token = 0

    def __init__(self, value, token):
        self.value = value
        self.token = token

class ALexerRegister:
    @staticmethod
    def register():
        return [i for i in range(1,9)]

    @staticmethod
    def isRegister(substring):
        for reg in ALexerRegister.register():
            if substring == "R"+str(reg):
                return True
    
        return False

def isNumeric(string):
    if len(string) == 1:
        if string == "0":
            return True
    
    try:
        return int(string) > 0
    except ValueError:
        return False 

class ALexerMemory:
    @staticmethod
    def isMemory(substring):
        if len(substring) <= 2:
            return False
        
        if substring[0] != '[':
            return False
        
        if substring[len(substring)-1] != ']':
            return False
        
        return isNumeric(substring[1:len(substring)-1])

class ALexerOperation:
    @staticmethod
    def isOperation(substring):
        ops = ["add", "sub", "mul", "div", "mod", "pot", "and", "or"]
        for op in ops:
            if op == substring:
                return True

        return False

class ALexerJumpCMP:
    @staticmethod
    def isJump(substring):
        ops = ["beq", "bne", "blt", "ble", "bgt", "bge"]
        for op in ops:
            if op == substring:
                return True
                
        return False
        
class ALexerSppliter:
    @staticmethod
    def split(string):
        ss = ""
        slist = []

        for c in string:
            if c != ' ' and c != '\r' and c != '\n' and c != '\t' and c != ',':
                ss += c
            elif len(ss) >= 1:
                slist.append(ss)
                ss = ""

                if c == ',':
                    slist.append(c)

        if len(ss) >= 1:
            slist.append(ss)
            ss = ""


        return slist

class ALexerMapper:
    @staticmethod
    def _map(substring):
        if ALexerRegister.isRegister(substring):
            return ALexerToken(substring, ALexerTokenType.register)

        if substring == ",":
            return ALexerToken(substring, ALexerTokenType.comma)

        if substring == "mov":
            return ALexerToken(substring, ALexerTokenType.mov)

        if substring == "store":
            return ALexerToken(substring, ALexerTokenType.store)

        if substring == "load":
            return ALexerToken(substring, ALexerTokenType.load)

        if substring == "pop":
            return ALexerToken(substring, ALexerTokenType.pop)

        if substring == "push":
            return ALexerToken(substring, ALexerTokenType.push)

        if substring == "jump":
            return ALexerToken(substring, ALexerTokenType.jump)

        if ALexerMemory.isMemory(substring):
            first = ALexerToken(substring[0], ALexerTokenType.memory)
            second = ALexerToken(substring[1:len(substring)-1], ALexerTokenType.value)
            third = ALexerToken(substring[len(substring)-1], ALexerTokenType.memory)

            return [first, second, third]
        
        if isNumeric(substring):
            return ALexerToken(substring, ALexerTokenType.value)

        if ALexerOperation.isOperation(substring):
            return ALexerToken(substring, ALexerTokenType.operation)

        if ALexerJumpCMP.isJump(substring):
            return ALexerToken(substring, ALexerTokenType.jumpCmp)

        print("Assembler error: can't recognize " +str(substring))
        quit()
    
    @staticmethod
    def map(substring):
        ret = ALexerMapper._map(substring)

        if type(ret) == list:
            return ret
        
        return [ret]

class ALexer:
    @staticmethod
    def run(string):
        subs = ALexerSppliter.split(string)
        ret = []
        for sub in subs:
            tokens = ALexerMapper.map(sub)
            for token in tokens:
                ret.append(token)

        return ret

