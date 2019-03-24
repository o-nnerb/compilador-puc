from Lexer.LexerEnum import LexerEnum
from Lexer.LexerQueue import LexerQueue
from Lexer.LexerToken import LexerToken
from Lexer.LexerHash import LexerHash
from .ParserTree import ParserTree

from Interpreter.Variable.Variable import VariableConstantType, VariableDeclarationCast

from enum import Enum, unique


class ParserVariable(LexerToken):
    def __init__(self, value):
        super(ParserVariable, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isVariable(object):
        return compareToken(object, [LexerEnum.id, LexerEnum.integer, LexerEnum.float, LexerEnum.boolean])
    
    def isStoreVariable(self):
        return compareToken(self, LexerEnum.id)
    
class ParserOperator(LexerToken):
    def __init__(self, value):
        super(ParserOperator, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isOperator(object):
        return compareToken(object, [LexerEnum.operator, LexerEnum.logical, LexerEnum.logical_operator])

class ParserAssigment(ParserOperator):
    def __init__(self, value):
        super(ParserAssigment, self).__init__(value)
    
    @staticmethod
    def isAssigment(object):
        return compareToken(object, LexerEnum.assigment)

class ParserOperation:
    first = 0
    operator = 0
    second = 0

    def __init__(self, first, second, operator):
        self.first = first
        self.second = second
        self.operator = operator

class ParserOperationAssigment(ParserOperation):
    def __init__(self, first, second, operator):
        super(ParserOperationAssigment, self).__init__(first, second, operator)

class ParserLineBlock:
    def __init__(self):
        return

    @staticmethod
    def isLineBlock(object):
        return object.getValue() == '('

class ParserLineBlockUnstack:
    value = 0
    before = 0

    def __init__(self):
        self.value = 0

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
        return
    
    def getBefore(self):
        return self.before

    def setBefore(self, value):
        self.before = value

    @staticmethod
    def isLineBlockUnstack(object):
        return object.getValue() == ')'

class ParserKeyword:
    def __init__(self):
        return

class ParserBlock:
    block = 0
    
    def __init__(self):
        return
    
    def setBlock(self, block):
        self.block = block

    @staticmethod
    def isBlock(object):
        return object.getValue() == "{"
    
    @staticmethod
    def isCloseBlock(object):
        return object.getValue() == '}'

class ParserIf(ParserBlock):
    value = 0

    elseBlock = 0

    def __init__(self, value):
        self.value = value
        super(ParserIf, self).__init__()

    @staticmethod
    def isElseBlock(object):
        return object.getValue() == "else"

    @staticmethod
    def isIfBlock(object):
        return object.getValue() == "if"

class ParserElse(ParserBlock):
    ifBlock = 0
    block = 0

    def __init__(self):
        super(ParserElse, self).__init__()

class ParserDeclarationVariable:
    variable = 0
    type = 0
    varType = 0

    def __init__(self, variable, type, varType):
        self.variable = variable
        self.type = type
        self.varType = varType
    
    @staticmethod
    def isDeclarationVariable(object):
        return VariableConstantType.isConstantType(object.getValue())

class ParserDeclarationExplicit:
    def __init__(self):
        return
    
    @staticmethod
    def isExplicit(object):
        return object.getValue() == ":"

class ParserVariableType:
    type = 0

    def __init__(self, type):
        self.type = type
    
    @staticmethod
    def isVariableType(object):
        return object.getToken() == LexerEnum.primitive

class ParserEmpty:
    def __init__(self):
        return

class ParserError:
    def __init__(self):
        return

class ParserMerge:
    def merge(first, second):
        ParserMerge.printObject(first)
        ParserMerge.printObject(second)
        print()

        if type(second) == ParserError:
            return second

        if type(first) == ParserError:
            return first

        if type(second) == ParserEmpty:
            if type(first) == ParserOperator:
                return ParserError()
            return first

        if type(first) == ParserAssigment:
            if type(second) == ParserVariable:
                return ParserOperationAssigment(0, second, first)
            
            if type(second) == ParserOperation and second.first:
                return ParserOperationAssigment(0, second, first)
        
        if type(first) == ParserOperator:
            if type(second) == ParserVariable:
                return ParserOperation(0, second, first)
            
            if type(second) == ParserOperation and second.first:
                return ParserOperation(0, second, first)

        if type(first) == ParserVariable:
            if type(second) == ParserOperationAssigment:
                if not first.isStoreVariable():
                    return ParserError()
                second.first = first
                return second

            if type(second) == ParserOperation and not second.first:
                second.first = first
                return second
            
            if type(second) == ParserDeclarationVariable and type(second.variable) == ParserOperationAssigment:
                second.variable = ParserMerge.merge(first, second.variable)
                return second
        
        if type(first) == ParserLineBlock:
            if type(second) == ParserLineBlockUnstack:
                if second.getValue():
                    if type(second.getValue()) == ParserOperation and not second.getValue().first:
                        return ParserError()

                    if second.getBefore():
                        return ParserMerge.merge(second.getValue(), second.getBefore())
                    return second.getValue()
                return ParserEmpty()

        if type(second) == ParserLineBlockUnstack:
            if not second.getValue():
                second.setValue(first)
                return second
            
            second.setValue(ParserMerge.merge(first, second.getValue()))
            return second
        
        if type(first) == ParserLineBlockUnstack:
            if type(second) == ParserOperation and not second.first:
                first.setBefore(second)
                return first
        
        if type(first) == ParserOperation:
            if type(second) == ParserOperation and not second.first and first.first and first.second:
                second.first = first
                return second

        if type(first) == ParserIf:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

            if type(second) == ParserElse:
                first.elseBlock = second
                return first

        if type(first) == ParserElse:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first
            if type(second) == ParserIf:
                first.ifBlock = second
                return first

        if type(first) == ParserVariableType:
            if type(second) == ParserOperationAssigment:
                return ParserDeclarationVariable(second, first, 0)

        if type(first) == ParserDeclarationExplicit:
            if type(second) == ParserDeclarationVariable:
                if second.variable and second.type:
                    return second

        return ParserError()

    @staticmethod
    def printObject(object):
        if not object:
            print("_ParserMerge<" , end="")
            print(object, end="")
            print(">")
            return
        
        print("_ParserMerge" , end="")
        print(object)

class Parser:
    queue = 0

    def __init__(self, queue):
        self.queue = queue.copy()
        self.queue.needsPersist(True)

    @staticmethod
    def isEndline(object):
        return object.getToken() == LexerEnum.endline or object.getValue() == ';'
    
    @staticmethod
    def toParse(object, callback, types, notFound):
        for type in types:
            if type == ParserLineBlockUnstack and ParserLineBlockUnstack.isLineBlockUnstack(object):
                return ParserMerge.merge(ParserLineBlockUnstack(), callback())

            if type == ParserLineBlock and ParserLineBlock.isLineBlock(object):
                return ParserMerge.merge(ParserLineBlock(), callback())
            
            if type == ParserVariable and ParserVariable.isVariable(object):
                return ParserMerge.merge(ParserVariable(object), callback())
            
            if type == ParserOperator and ParserOperator.isOperator(object):
                return ParserMerge.merge(ParserOperator(object), callback())

            if type == ParserAssigment and ParserAssigment.isAssigment(object):
                return ParserMerge.merge(ParserAssigment(object), callback())
            
            if type == ParserKeyword and Parser.isKeyword(object):
                return ParserKeyword()
            
            if type == ParserBlock and ParserBlock.isBlock(object):
                return ParserEmpty()

            if type == ParserDeclarationExplicit and ParserDeclarationExplicit.isExplicit(object):
                return ParserMerge.merge(ParserDeclarationExplicit(), callback())

            if type == ParserVariableType and ParserVariableType.isVariableType(object):
                return ParserMerge.merge(ParserVariableType(object), callback())
            
        return notFound()

    def execute(self):
        if self.queue.isEmpty():
            return ParserEmpty()
    
        object = self.queue.getHead()
        self.queue.toRight()

        if Parser.isEndline(object):
            return ParserEmpty()

        parsed = Parser.toParse(object, self.execute, [
            ParserLineBlockUnstack,
            ParserLineBlock,
            ParserVariable,
            ParserOperator,
            ParserAssigment,
            ParserKeyword,
        ], ParserError)
        
        if type(parsed) == ParserKeyword:
            return Parser.keywordMerge(self.executeKeyword(object), self.execute)

        return parsed

    def executeKeyword(self, keyword):
        if ParserIf.isIfBlock(keyword):
            return self.isIfValid(Parser.isMergeValid(self.blockIf()))
        
        if ParserDeclarationVariable.isDeclarationVariable(keyword):
            return self.isDeclarationValid(keyword, Parser.isMergeValid(self.declarationLine()))

    # ParserDeclarationVariable
    # ParserOperationAssigment
    def isDeclarationValid(self, keyword, merged):
        print(merged)
        if type(merged) == ParserOperationAssigment:
            return ParserDeclarationVariable(merged, VariableDeclarationCast.auto, VariableConstantType.toConstantType(keyword))
        if type(merged) == ParserDeclarationVariable:
            merged.varType = VariableConstantType.toConstantType(keyword)
            return merged

        return ParserError()

    def isIfValid(self, merged):
        if type(merged) == ParserError:
            return merged
        
        if type(merged) == ParserEmpty:
            return ParserError()

        merged = ParserMerge.merge(ParserIf(merged), self.block())

        if type(merged) == ParserIf:
            if ParserIf.isElseBlock(self.queue.getHead()):
                self.queue.toRight()

                if ParserBlock.isBlock(self.queue.getHead()):
                    self.queue.toRight()
                    return ParserMerge.merge(merged, ParserMerge.merge(ParserElse(), self.block()))
                
                if ParserIf.isIfBlock(self.queue.getHead()):
                    self.queue.toRight()
                    return ParserMerge.merge(merged, ParserMerge.merge(ParserElse(), self.isIfValid(Parser.isMergeValid(self.blockIf()))))
                
                return ParserError()

        return merged

    def blockIf(self):
        if self.queue.isEmpty():
            return ParserError()
    
        object = self.queue.getHead()
        self.queue.toRight()

        return Parser.toParse(object, self.blockIf, [
            ParserBlock,
            ParserLineBlockUnstack,
            ParserLineBlock,
            ParserVariable,
            ParserOperator
        ], ParserError)

    def declarationLine(self):    
        if self.queue.isEmpty():
            return ParserEmpty()
    
        object = self.queue.getHead()
        self.queue.toRight()

        if Parser.isEndline(object):
            return ParserEmpty()

        return Parser.toParse(object, self.declarationLine, [
            ParserLineBlockUnstack,
            ParserLineBlock,
            ParserVariable,
            ParserDeclarationExplicit,
            ParserVariableType,
            ParserOperator,
            ParserAssigment
        ], ParserError)
        
    def block(self):
        object = self.queue.getHead()
        self.queue.toRight()
        
        instructions = LexerQueue()

        while object and not ParserBlock.isCloseBlock(object):
            line = Parser.isMergeValid(self.execute())
            if type(line) == ParserError:
                instructions = line
                break

            instructions.insert(line)
            object = self.queue.getHead()
            self.queue.toRight()

        return instructions        
        
    @staticmethod
    def isKeyword(object):
        return object.getToken() == LexerEnum.keyword

    @staticmethod
    def isMergeValid(merged):
        if type(merged) == ParserOperation and not merged.first:
            return ParserError()
        
        return merged
    
    @staticmethod
    def keywordMerge(merged, callback):
        if type(merged) == ParserDeclarationVariable:
            return merged

        return ParserMerge.merge(merged, callback())

    @staticmethod
    def run():
        parser = Parser(LexerQueue.shared())
        instructions = LexerQueue()

        while not parser.queue.isEmpty():
            line = Parser.isMergeValid(parser.execute())
            if type(line) == ParserError:
                print(line)
                quit()
                break

            instructions.insert(line)
        
        print("Lista de Instruções")
        instructions.verbose(showContent=False)
        quit()

"""
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

class ParserOperator:
    value = 0
    type = 0

    def __init__(self, object):
        self.value = object.getValue()
        self.type = object.getToken()
    
    def isLogical(self):
        return compareToken(self.type, [LexerEnum.logical, LexerEnum.logical_operator])
    
    def isNumerical(self):
        return compareToken(self.type, [LexerEnum.operator, LexerEnum.logical_operator])

class ParserOperation:
    right = 0
    left = 0
    operator = 0
    
    def __init__(self, right, left, operator):
        self.right = right
        self.left = left
        self.operator = operator
    
    def isAssigment(self):
        return self.operator.value == '='
    
class ParserVariable:
    value = 0
    type = 0

    def __init__(self, object):
        self.value = object.getValue()
        self.type = object.getToken()

    def isVariable(self):
        return self.type == LexerEnum.id
    
    def isCarry(self):
        return compareToken(object, [LexerEnum.integer, LexerEnum.float, LexerEnum.boolean])

    def valueCanChange(self):
        if not self.isVariable(self):
            return False
        
        # Pegar na Hash se é var ou let
        return True

    @staticmethod
    def create(object):
        self = ParserVariable(object)
        if self.isVariable() or self.isCarry():
            return self
        
        return False

class ParserLineBlockStack: # ( ou )
    def __init__(self):
        return

class ParserLineBlockUnstack:
    def __init__(self):
        return

class ParserMerge:
    def __init__(self, first, second):
        return

class ParserErrorType(Enum):
    variable=0
    empty=0
    assigment=0

class ParserError:
    token = 0
    typeError = 0

    def __init__(self, token, typeError):
        self.token = token
        self.typeError = typeError

class Parser:
    queue = 0
    context = []
    warning = []

    def __init__(self, queue):
        self.queue = queue.copy()
        self.queue.needsPersist(True)
    
    def isExpression(self, object, rightSide):
        variable = ParserVariable(object)

        if not variable:
            return ParserError(object, ParserErrorType.variable)

        if variable.isCarry() and not rightSide:
            return ParserError(object, ParserErrorType.assigment)      

        return ParserMerge(variable, self.shouldEnd(rightSide))

    def isContext(self, context):
        if not len(self.context):
            return False
        
        return self.context[-1] == context

    def shouldEnd(self, rightSide, variable=0):        
        object = self.queue.getHead()
        self.queue.toRight()

        if object.getValue() == ')' and self.isContext(ParserEnum.runtimeBlock):
            self.queue.toLeft()
            return ParserLineBlockUnstack()

        if compareToken(object, [LexerEnum.logical, LexerEnum.logical_operator]):
            return self.isOperator(object, rightSide)

        if self.isContext(ParserEnum.logical):
            return False

        if compareToken(object, [LexerEnum.operator, LexerEnum.logical_operator]):
            return self.isOperator(object, rightSide)
        
        if compareToken(object, LexerEnum.assigment):
            return self.isAssigment(rightSide)
        
        if compareToken(object, LexerEnum.endline):
            return True
        
        if object.getValue() == ';':
            return True
        
        return False

    def isOperator(self, object, rightSide):
        operator = ParserOperator(object)

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
            return ret and self.isOperator(object, True)
        
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

    def isVariable(self, value):
        object = self.queue.getHead()
        self.queue.toRight()

        self.isExpression(object, False)

        print(object.getValue())
        quit()

    def isKeyword(self, object):
        value = object.getValue()
        if value == "if":
            return self.isLogicalBlock()
        if value == "var":
            return self.isVariable(value)
        if value == "let":
            return self.isVariable(value)

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

"""
def compareToken(object, values):
    return LexerEnum.compare(object, values)
"""
def compareContext(object, values):
    return ParserEnum.compare(object, values)
    """