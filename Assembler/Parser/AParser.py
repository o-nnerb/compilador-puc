# Assembler Parser
from Assembler.Lexer.ALexer import ALexerToken, ALexerTokenType
from Assembler.Assembler import AssemblerRegister, AssemblerValueConstant

def dieUnrecognized(some):
    print("Assembler Parser error: unrecognized " + str(some))
    quit()

class AParserOperation:
    code = 0
    first = 0
    second = 0
    third = 0

    def __init__(self, code, first, second, third):
        self.code = code
        self.first = first
        self.second = second
        self.third = third

    @staticmethod
    def init():
        return AParserOperation(0, 0, 0, 0) 
    
    @statimethod
    def isSomething(some):
        if some.token == ALexerTokenType.register:
            return AssemblerRegister.fromString(some.value)
        if some.token == ALexerTokenType.value:
            return AssemblerValueConstant(some.value)
        
        dieUnrecognized(some.token)

    def merge(self, some):
        if not self.third:
            self.third = AParserOperation.isSomething(some)
            return self
        
        if not self.second:
            self.second = AParserOperation.isSomething(some)
            return self

        if not self.first:
            if some.token == ALexerTokenType.register:
                self.first = AssemblerRegister.fromString(some.value)
                return self

            dieUnrecognized(some.token)

        if not self.code:
            if some.token == ALexerTokenType.operation:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):
        if not self.third:
            return False
        
        if not self.second:
            return False
        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

class AParserJump:
    code = 0
    first = 0

    def __init__(self, code, first):
        self.code = code
        self.first = first

    @staticmethod
    def init():
        return AParserJump(0, 0) 
    
    @statimethod
    def isSomething(some):
        if some.token == ALexerTokenType.value:
            return AssemblerValueConstant(some.value)
        
        dieUnrecognized(some.token)

    def merge(self, some):
        if not self.first:
            self.first = AParserJump.isSomething(some)
            return self

        if not self.code:
            if some.token == ALexerTokenType.jump:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

class AParserJumpCMP:
    code = 0
    first = 0
    second = 0
    third = 0

    def __init__(self, code, first, second, third):
        self.code = code
        self.first = first
        self.second = second
        self.third = third

    @staticmethod
    def init():
        return AParserJumpCMP(0, 0, 0, 0) 
    
    @statimethod
    def isSomething(some):
        if some.token == ALexerTokenType.register:
            return AssemblerRegister.fromString(some.value)
        if some.token == ALexerTokenType.value:
            return AssemblerValueConstant(some.value)
        
        dieUnrecognized(some.token)

    def merge(self, some):
        if not self.third:
            if some.token == ALexerTokenType.value:
                self.third = AssemblerValueConstant(some.value)
                return self
            
            dieUnrecognized(some.token)
        
        if not self.second:
            self.second = AParserOperation.isSomething(some)
            return self

        if not self.first:
            self.first = AParserOperation.isSomething(some)
            return self

        if not self.code:
            if some.token == ALexerTokenType.jumpCmp:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):
        if not self.third:
            return False
        
        if not self.second:
            return False
        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

class AParserMov:
    code = 0
    first = 0
    second = 0

    def __init__(self, code, first, second):
        self.code = code
        self.first = first
        self.second = second

    @staticmethod
    def init():
        return AParserMov(0, 0, 0) 
    
    @statimethod
    def isSomething(some):
        if some.token == ALexerTokenType.register:
            return AssemblerRegister.fromString(some.value)
        if some.token == ALexerTokenType.value:
            return AssemblerValueConstant(some.value)
        
        dieUnrecognized(some.token)

    def merge(self, some):        
        if not self.second:
            self.second = AParserOperation.isSomething(some)
            return self

        if not self.first:
            if some.token == ALexerTokenType.register:
                self.first = AssemblerRegister.fromString(some.value)
                return self

        if not self.code:
            if some.token == ALexerTokenType.mov:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):
        if not self.third:
            return False
        
        if not self.second:
            return False
        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

class AParserStore:
    code = 0
    first = 0
    second = 0

    def __init__(self, code, first, second):
        self.code = code
        self.first = first
        self.second = second

    @staticmethod
    def init():
        return AParserStore(0, 0, 0) 

    def merge(self, some):  
        if not self.second:
            if some.token == ALexerTokenType.register:
                self.second = AssemblerRegister.fromString(some.value)
                return self  

        if not self.first:
            if some.token == ALexerTokenType.memory and some.value == ']':
                self.first = some
                return self

            dieUnrecognized(some.token)
        else:
            if type(self.first) == ALexerToken:
                if self.first.token == ALexerTokenType.memory:
                    if some.token == ALexerTokenType.value:
                        self.first = some
                        return self

                elif self.first.token == ALexerTokenType.value:
                    if some.token == ALexerTokenType.memory and some.value == '[':
                        self.first = AssemblerValueConstant(self.first.value)
                        return self
            
                dieUnrecognized(some.token)

        if not self.code:
            if some.token == ALexerTokenType.mov:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):        
        if not self.second:
            return False
        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

class AParserLoad:
    code = 0
    first = 0
    second = 0

    def __init__(self, code, first, second):
        self.code = code
        self.first = first
        self.second = second

    @staticmethod
    def init():
        return AParserLoad(0, 0, 0) 

    def merge(self, some):  
        if not self.first:
            if some.token == ALexerTokenType.register:
                self.first = AssemblerRegister.fromString(some.value)
                return self  

        if not self.second:
            if some.token == ALexerTokenType.memory and some.value == ']':
                self.second = some
                return self

            dieUnrecognized(some.token)
        else:
            if type(self.second) == ALexerToken:
                if self.second.token == ALexerTokenType.memory:
                    if some.token == ALexerTokenType.value:
                        self.second = some
                        return self

                elif self.second.token == ALexerTokenType.value:
                    if some.token == ALexerTokenType.memory and some.value == '[':
                        self.second = AssemblerValueConstant(self.second.value)
                        return self
            
                dieUnrecognized(some.token)

        if not self.code:
            if some.token == ALexerTokenType.mov:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):        
        if not self.second:
            return False
        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

class AParserLine:
    @staticmethod
    def filter(objects):
        line = []
        first = objects.pop()
        if len(first) == 0:
            print("Assembler Parser error: incomplete instruction")
            quit()
        
        if not first.isKeyword():
            print("Assembler Parser error: first element should be a instruction keyword")
            quit()
        
        line.append(first)
        size = first.countParameters()
        for i in range(0, size):
            ref = objects.pop()
            if ref.token == ALexerTokenType.comma:
                print("Assembler Parser error: comma in wrong place")
                quit()

            line.append(ref)

            if i + 1 == size: #last
                return line
            
            if len(objects) == 0:
                print("Assembler Parser error: missing instructions")
                quit()
            
            if objects[0].token != ALexerTokenType.comma:
                print("Assembler Parser error: missing comma")
                quit()
            else:
                objects.pop()

        print("Assembler Parser error: ERROR")
        quit()
        