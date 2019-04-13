# Assembler Parser
from Assembler.Lexer.ALexer import ALexerToken, ALexerTokenType
from Assembler.Assembler import AssemblerRegister, AssemblerValueConstant
import traceback

def dieUnrecognized(some):
    traceback.print_stack()
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
    
    @staticmethod
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

    @staticmethod
    def asOperation(objects):
        if len(objects) != 4:
            return False
        
        handler = AParserOperation.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler


class AParserJump:
    code = 0
    first = 0

    def __init__(self, code, first):
        self.code = code
        self.first = first

    @staticmethod
    def init():
        return AParserJump(0, 0) 
    
    @staticmethod
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

    @staticmethod
    def asJump(objects):
        if len(objects) != 2:
            return False
        
        handler = AParserJump.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

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
    
    @staticmethod
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

    @staticmethod
    def asJumpCMP(objects):
        if len(objects) != 4:
            return False
        
        handler = AParserJumpCMP.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

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
    
    @staticmethod
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
        if not self.second:
            return False
        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

    @staticmethod
    def asMov(objects):
        if len(objects) != 3:
            return False
        
        handler = AParserMov.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

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
            if some.token == ALexerTokenType.store:
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

    @staticmethod
    def asStore(objects):
        if len(objects) != 5:
            return False
        
        handler = AParserStore.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

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
        
        if not self.first:
            if some.token == ALexerTokenType.register:
                self.first = AssemblerRegister.fromString(some.value)
                return self  

        if not self.code:
            if some.token == ALexerTokenType.load:
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

    @staticmethod
    def asLoad(objects):
        if len(objects) != 5:
            return False
        
        handler = AParserLoad.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

class AParserPush:
    code = 0
    first = 0

    def __init__(self, code, first):
        self.code = code
        self.first = first

    @staticmethod
    def init():
        return AParserPush(0, 0) 

    def merge(self, some):  
        if not self.first:
            if some.token == ALexerTokenType.register:
                self.first = AssemblerRegister.fromString(some.value)
                return self  

        if not self.code:
            if some.token == ALexerTokenType.push:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

    @staticmethod
    def asPush(objects):
        if len(objects) != 2:
            return False
        
        handler = AParserPush.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

class AParserPop:
    code = 0
    first = 0

    def __init__(self, code, first):
        self.code = code
        self.first = first

    @staticmethod
    def init():
        return AParserPop(0, 0) 

    def merge(self, some):  
        if not self.first:
            if some.token == ALexerTokenType.register:
                self.first = AssemblerRegister.fromString(some.value)
                return self  

        if not self.code:
            if some.token == ALexerTokenType.pop:
                self.code = some.value
                return self

            dieUnrecognized(some.token)

    def isValid(self):        
        if not self.first:
            return False
        
        if not self.code:
            return False
        
        return True

    @staticmethod
    def asPop(objects):
        if len(objects) != 2:
            return False
        
        handler = AParserPop.init()
        while len(objects) != 0:
            handler = handler.merge(objects.pop())

        if not handler.isValid():
            return False

        return handler

class AParserLine:
    line = 0
    rest = 0
    def __init__(self, line, rest):
        self.line = line
        self.rest = rest

    @staticmethod
    def filter(objects):
        line = []
        first = objects.pop(0)
        if len(objects) == 0:
            print("Assembler Parser error: incomplete instruction")
            quit()
        
        if not first.token.isKeyword():
            print(first.token)
            print("Assembler Parser error: first element should be a instruction keyword")
            quit()
        
        line.append(first)
        size = first.token.countParameters()
        for i in range(0, size):
            ref = objects.pop(0)
            if ref.token == ALexerTokenType.comma:
                print("Assembler Parser error: comma in wrong place")
                quit()

            line.append(ref)
            
            if ref.token == ALexerTokenType.memory and ref.value == "[":
                value = objects.pop(0)
                close = objects.pop(0)

                if value.token == ALexerTokenType.value:
                    line.append(value)
                    value = 0

                if close.token == ALexerTokenType.memory and close.value == "]":
                    line.append(close)
                    close = 0
                
                if value or close:                    
                    print("Assembler Parser error: memory cast")
                    quit()

            if i + 1 == size: #last
                return AParserLine(line, objects)
            
            if len(objects) == 0:
                print("Assembler Parser error: missing instructions")
                quit()
            
            if objects[0].token != ALexerTokenType.comma:
                print("Assembler Parser error: missing comma")
                quit()
            else:
                objects.pop(0)

        print("Assembler Parser error: ERROR")
        quit()

class AParserContext:
    @staticmethod
    def isLoad(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].value == "load"

    @staticmethod
    def isStore(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].value == "store"

    @staticmethod
    def isMov(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].value == "mov"

    @staticmethod
    def isOperation(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].token == ALexerTokenType.operation

    @staticmethod
    def isJump(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].token == ALexerTokenType.jump

    @staticmethod
    def isJumpCmp(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].token == ALexerTokenType.jumpCmp

    @staticmethod
    def isPush(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].token == ALexerTokenType.push

    @staticmethod
    def isPop(objects):
        if len(objects) == 0:
            return False
        
        return objects[0].token == ALexerTokenType.pop

    @staticmethod
    def context(objects):
        if len(objects) == 0:
            return

        if AParserContext.isLoad(objects):
            return AParserLoad.asLoad(objects)

        if AParserContext.isStore(objects):
            return AParserStore.asStore(objects)

        if AParserContext.isMov(objects):
            return AParserMov.asMov(objects)

        if AParserContext.isOperation(objects):
            return AParserOperation.asOperation(objects)

        if AParserContext.isJump(objects):
            return AParserJump.asJump(objects)

        if AParserContext.isJumpCmp(objects):
            return AParserJumpCmp.asJumpCmp(objects)

        if AParserContext.isPush(objects):
            return AParserPush.asPush(objects)

        if AParserContext.isPop(objects):
            return AParserPop.asPop(objects)
        
        print("Assembler Parser: tokens not recognized " + str(objects[0].token) )
        quit()

class AParser:
    @staticmethod
    def run(queue):
        liner = 0
        instructions = []
        while len(queue) >= 1:
            liner = AParserLine.filter(queue)
            queue = liner.rest
            liner = liner.line

            handler = AParserContext.context(liner)
            if not handler:
                print("Assembler Parser: tokens not recognized #")
                quit()
            
            instructions.append(handler)

        return instructions


