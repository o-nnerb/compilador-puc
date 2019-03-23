from Lexer.LexerEnum import LexerEnum
from Lexer.LexerQueue import LexerQueue
from Lexer.LexerToken import LexerToken
from .ParserTree import ParserTree
from enum import Enum, unique

@unique
class ParserEnum(Enum):
    instruction = "INT"
    logical = "LOG"
    runtimeBlock = "RUNBLOCK"
    block = "BLOCK"

    @staticmethod
    def compare(object, values):
        string = object.value
        if type(values) != list:
            return string == values.value
        
        for val in values:
            if string == val.value:
                return True
        
        return False

class Parser:
    queue = 0
    context = []
    warning = []

    def __init__(self, queue):
        self.queue = queue.copy()
        self.queue.needsPersist(True)
    
    def isExpression(self, object, rightSide):
        if compareToken(object, LexerEnum.id):
            return self.shouldEnd(object, rightSide)
        
        if not rightSide:
            return False

        if compareToken(object, [LexerEnum.integer, LexerEnum.float, LexerEnum.boolean]):
            return self.shouldEnd(object, rightSide)
            
        return False

    def isContext(self, context):
        if not len(self.context):
            return False
        
        return self.context[-1] == context

    def shouldEnd(self, prevObject, rightSide):
        #object = self.queue.toRight()
        object = self.queue.getHead()
        self.queue.toRight()

        if object.getValue() == ')' and self.isContext(ParserEnum.runtimeBlock):
            self.queue.toLeft()
            return True

        if compareToken(object, [LexerEnum.logical, LexerEnum.logical_operator]):
            return self.isOperator(rightSide)

        if self.isContext(ParserEnum.logical):
            return False

        if compareToken(object, [LexerEnum.operator, LexerEnum.logical_operator]):
            return self.isOperator(rightSide)
        
        if compareToken(object, LexerEnum.assigment):
            return self.isAssigment(rightSide)
        
        if compareToken(object, LexerEnum.endline):
            return True
        
        if object.getValue() == ';':
            return True
        
        return False

    def isOperator(self, rightSide):
        object = self.queue.getHead()
        self.queue.toRight()

        if not rightSide:
            self.warning.append(True)
            #return False

        if object.getValue() == '(':
            return self.shouldStack()
            
        return self.isExpression(object, True)

    def isAssigment(self, rightSide):
        object = self.queue.getHead()
        self.queue.toRight()

        if rightSide:
            return False
        
        if object.getValue() == '(':
            return self.shouldStack()
   
        return self.isExpression(object, True)

    def shouldPop(self, ret):
        object = self.queue.getHead()
        if compareToken(object, [LexerEnum.operator, LexerEnum.logical_operator]):
            self.queue.toRight()
            return ret and self.isOperator(True)
        
        return ret

    def shouldStack(self):
        self.context.append(ParserEnum.runtimeBlock)
        warningLen = len(self.warning)

        object = self.queue.getHead()
        self.queue.toRight()

        if object.getValue() == '(':
            returnable = self.shouldStack()
        else:
            returnable = self.isExpression(object, True)
            
        if self.queue.getHead().getValue() == ')':
            self.queue.toRight()
        else:
            return False

        if len(self.warning) > warningLen:
            self.warning.pop()

        if not self.isContext(ParserEnum.runtimeBlock):
            return False

        self.context.pop()
        return self.shouldPop(returnable)

    def shouldStart(self):
        line = 1
        flag = True
        
        #self.context.append(ParserEnum.instruction)
        while not self.queue.isEmpty():
            object = self.queue.getHead()
            self.queue.toRight()
            warningLen = len(self.warning)

            #print(str(line) + object.getValue())
            
            if not compareToken(object, LexerEnum.endline):
                if object.getValue() == '}' and self.isContext(ParserEnum.block):
                    self.queue.toLeft()
                    return True

                if compareToken(object, LexerEnum.keyword):
                    if not self.isKeyword(object):
                        print("Parser Error: keyword linha " + str(line))
                        flag = flag and False
                
                else:
                    isExpression = self.isExpression(object, False)
                    if not isExpression:
                        print("Parser Error: linha " + str(line))
                        flag = flag and False
                        
                        last = self.queue.getHead()
                        self.backLine()

                        if len(self.warning) > warningLen:
                            self.warning.pop()

                    elif len(self.warning):
                        print("WARNING: resultado não usado")
                        self.warning.pop()
                        
                        last = self.queue.getHead()
                        self.queue.toLeft()    
                        self.backLine()

            line += 1

        return flag

    def isKeyword(self, object):
        value = object.getValue()
        if value == "if":
            return self.isLogicalBlock()

    def isLogicalBlock(self):
        while True:
            object = self.queue.getHead()
            self.queue.toRight()

            if object.getValue() != "(":
                return False

            self.context.append(ParserEnum.logical)
            validBlock = self.shouldStack()
            self.context.pop()

            if not validBlock or not self.isBlock():
                return False

            if not self.queue.getHead():
                return True
            
            if self.queue.getHead().getValue() != "else":
                #self.queue.toLeft()
                return True

            self.queue.toRight()
            head = self.queue.getHead()

            if head.getValue() != "if":
                #self.queue.toLeft()
                break
            
            self.queue.toRight()
            return self.isKeyword(head)

        return self.isBlock()

    def isBlock(self):
        object = self.queue.getHead()
        self.queue.toRight()

        if object.getValue() != "{":
            return False
    
        object = self.queue.getHead()

        if object and compareToken(object, LexerEnum.endline):
            self.queue.toRight()

        self.context.append(ParserEnum.block)
        returnable = self.shouldStart()

        if not self.isContext(ParserEnum.block):
            return False

        self.context.pop()

        if not self.queue.getHead():
            return False

        if self.queue.getHead().getValue() != '}':
            return False

        self.queue.toRight()

        if self.queue.getHead() and compareToken(self.queue.getHead(), LexerEnum.endline):
            self.queue.toRight()
        
        return returnable

    @staticmethod
    def run():
        self = Parser(LexerQueue.shared())
        if self.queue.isEmpty():
            return
        
        if not self.shouldStart():
            print("Error Parse")
            quit()

    def backLine(self):
        while True:
            last = self.queue.toLeft()
            
            if not last:
                break

            if compareToken(last, LexerEnum.endline) or  last.getValue() == ";":
                self.queue.toRight()
                break
        
        print("AutoGen: ", end="")
        #self.queue.toRight()

        while True:
            next = self.queue.getHead()
            self.queue.toRight()

            if not next:
                break

            if not compareToken(next, LexerEnum.endline):
                print(next.getValue(), end=" ")

            if next.getValue() == ";":
                break

            if compareToken(next, LexerEnum.endline):
                break
        print("\n")

def compareToken(object, values):
    return LexerEnum.compare(object, values)

def compareContext(object, values):
    return ParserEnum.compare(object, values)