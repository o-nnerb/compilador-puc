from Lexer.LexerEnum import LexerEnum
from Lexer.LexerQueue import LexerQueue
from Lexer.LexerToken import LexerToken
from Lexer.LexerHash import LexerHash
from .ParserTree import ParserTree

from Interpreter.Variable.Variable import VariableConstantType, VariableDeclarationCast

from enum import Enum, unique
import traceback

class ParserVariable(LexerToken):
    def __init__(self, value):
        super(ParserVariable, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isVariable(object):
        return compareToken(object, [LexerEnum.id, LexerEnum.integer, LexerEnum.float, LexerEnum.boolean, LexerEnum.string])
    
    def isStoreVariable(self):
        return compareToken(self, LexerEnum.id)
    
class ParserStringOperatorAppendE:
    def __init__(self):
        return
    
    @staticmethod
    def isAppendE(object):
        return object.getToken() == LexerEnum.string_append_e

class ParserStringOperatorAppend:
    def __init__(self):
        return

    @staticmethod
    def isAppend(object):
        return object.getToken() == LexerEnum.string_append

class ParserStringAppend:
    first = 0
    second = 0

    def __init__(self):
        return

    def setFirst(self, object):
        if not self.first:
            if type(object) == ParserVariable:
                self.first = object
                return self
            if type(object) == ParserLineBlockCarry:
                self.first = object
                return self
            return ParserError()
        
        self.first = ParserMerge.merge(object, self.first)
        if type(self.first) == ParserError:
            return self.first

        return self

    @staticmethod
    def isAppend(object):
        return ParserStringOperatorAppend.isAppend(object) or ParserStringOperatorAppendE.isAppendE(object)

    @staticmethod
    def toParserClass(object):
        if ParserStringOperatorAppend.isAppend(object):
            return ParserStringOperatorAppend()
        
        if ParserStringOperatorAppendE.isAppendE(object):
            return ParserStringOperatorAppendE()
        
        return ParserError()

class ParserOperator(LexerToken):
    def __init__(self, value):
        super(ParserOperator, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isOperator(object):
        return compareToken(object, [LexerEnum.operator, LexerEnum.logical, LexerEnum.logical_operator])

class ParserPFixOperator(LexerToken):
    def __init__(self, value):
        super(ParserPFixOperator, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isPFixOperator(object):
        return compareToken(object, LexerEnum.operator_pfix)

@unique
class ParserFixType(Enum):
    none = 0
    prefix = 1
    posfix = 2

    @staticmethod
    def isPrefix(object):
        return ParserFixType.prefix
    
    @staticmethod
    def isPosfix(object):
        if object.getValue() != "!":
            return ParserFixType.posfix

        return ParserFixType.none

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
    
class ParserFixOperation:
    variable = 0
    operator = 0
    fixType = 0
    
    def __init__(self, variable, operator, fixType):
        self.variable = variable
        self.operator = operator
        self.fixType = fixType

class ParserOperationFixParcial:
    first = 0
    second = 0

    def __init__(self, first, second):
        self.first = first
        self.second = second

class ParserOperationAssigment(ParserOperation):
    def __init__(self, first, second, operator):
        super(ParserOperationAssigment, self).__init__(first, second, operator)

class ParserLineBlockAbstract:
    def __init__(self):
        return

class ParserLineBlock:
    value = 0
    def __init__(self, value):
        self.value = value

    @staticmethod
    def isLineBlock(object):
        return object.getToken() == LexerEnum.delimiter and object.getValue() == '('

    @staticmethod
    def merge(value):
        if type(value) == ParserStringAppend:
            value.first = ParserLineBlock.merge(value.first)
            return value

        if type(value) != ParserLineBlockCarry:
            return ParserError()
        
        return ParserMerge.merge(ParserLineBlockAbstract(), value)

    def isSomething(self):
        return self.value and type(self.value) != ParserEmpty

class ParserLineBlockCarry(ParserLineBlock):
    after = 0
    def __init__(self):
        super(ParserLineBlockCarry, self).__init__(0)

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def getAfter(self):
        return self.after

    def setAfter(self, value):
        self.after = value

    @staticmethod
    def isLineBlockUnstack(object):
        return object.getToken() == LexerEnum.delimiter and object.getValue() == ')'

    def superMerge(self):
        if self.value:
            return self.value
        return ParserEmpty()

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
        return object.getToken() == LexerEnum.delimiter and object.getValue() == "{"
    
    @staticmethod
    def isCloseBlock(object):
        return object.getToken() == LexerEnum.delimiter and object.getValue() == '}'

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

    def __init__(self):
        super(ParserElse, self).__init__()

class ParserWhile(ParserBlock):
    value = 0

    def __init__(self, value):
        self.value = value
        super(ParserWhile, self).__init__()
    
    @staticmethod
    def isWhileBlock(object):
        return object.getValue() == "while"

class ParserFor(ParserBlock):
    value = 0

    def __init__(self, value):
        self.value = value
        super(ParserFor, self).__init__()
    
    @staticmethod
    def isForBlock(object):
        return object.getValue() == "for"

class ParserOperatorForIn():
    value = 0

    def __init__(self, value):
        self.value = value
    
    @staticmethod
    def isInOperator(object):
        return object.getValue() == "in"

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
    
class ParserBreak:
    def __init__(self):
        return

    @staticmethod
    def isBreak(object):
        return object.getValue() == "break"

class ParserOperatorRange:
    operator = 0

    def __init__(self, operator):
        self.operator = operator

    @staticmethod
    def isForRange(object):
        return object.getToken() == LexerEnum.operator_range    

class ParserOperatorForRange:
    first = 0
    last = 0
    operator = 0

    def __init__(self, operator, first, last):
        self.operator = operator
        self.first = first
        self.last = last

    def isRangeMounted(self):
        return self.first and type(self.first) == ParserVariable and self.last and type(self.last) == ParserVariable and self.operator and type(self.operator) == ParserOperatorRange

class ParserForInRange:
    variable = 0
    operator = 0
    range = 0

    def __init__(self, variable, operator, range):
        self.variable = variable
        self.operator = operator
        self.range = range

class ParserFunc(ParserBlock):
    name = 0
    parameters = 0 # LexerQueue + returnType

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
        super(ParserFunc, self).__init__()
    
    @staticmethod
    def isFuncBlock(object):
        return object.getValue() == "func"

class ParserFunction:
    name = 0
    parameters = 0

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class ParserFutureFunction:
    first = 0
    second = 0

    def __init__(self, first, second):
        self.first = first
        self.second = second

class ParserFunctionVariable:
    name = 0
    value = 0

    def __init__(self, value):
        self.value = value

class ParserFuncVariable(ParserVariable):
    def __init__(self, value):
        super(ParserFuncVariable, self).__init__(value)

class ParserFuncVariableDeclarationExplicit(ParserDeclarationExplicit):
    def __init__(self):
        return super(ParserFuncVariableDeclarationExplicit, self).__init__()

class ParserFuncVariableDeclaration(ParserDeclarationVariable):
    def __init__(self, variable, type):
        super(ParserFuncVariableDeclaration, self).__init__(variable, type, VariableConstantType.let)

class ParserFuncComma(ParserLineBlockCarry):
    after = 0
    
    def __init__(self):
        return super(ParserFuncComma, self).__init__()
    
    @staticmethod
    def isComma(object):
        return object.getValue() == ","

class ParserFunctionComma:
    def __init__(self):
        return

class ParserFunctionCommaTree:
    first = 0
    second = 0

    holder = 0

    def __init__(self):
        return
    
    def insert(self, value):
        if self.holder:
            print("Can't insert while there is a holder")
            quit()

        if not self.second:
            self.second = value
            return self

        if not self.first:
            self.first = value
            return self
        
        new = ParserFunctionCommaTree()
        new.first = value
        new.second = self
        
        return new

    def getHolder(self):
        if not self.holder:
            return ParserEmpty()
        return self.holder    

class ParserFuncOperatorReturn:
    def __init__(self):
        return
    
    @staticmethod
    def isOperatorReturn(object):
        return object.getValue() == "->"

class ParserFuncReturnType(ParserVariableType):
    def __init__(self, type):
        super(ParserFuncReturnType, self).__init__(type)

class ParserFuncParameter:
    declaration = 0
    next = 0

    def __init__(self, declaration):
        self.declaration = declaration
    
    def setNext(self, next):
        self.next = next

class ParserFuncParameterQueue:
    head = 0
    returnType = 0

    def __init__(self, head, returnType):
        self.head = head
        self.returnType = returnType

class ParserEmpty:
    def __init__(self):
        return

class ParserError:
    def __init__(self):
        traceback.print_stack()
        quit()
        return
@unique
class ParserContext(Enum):
    function = 0

    def types(self):
        if self == ParserContext.function:
            return (ParserFuncVariable, ParserFuncVariableDeclarationExplicit, ParserFuncOperatorReturn, ParserFuncComma)
        return ()

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

            if type(second) == ParserFixOperation:
                return ParserOperationAssigment(0, second, first)
            
            if type(second) == ParserLineBlock and second.isSomething():
                return ParserOperationAssigment(0, second, first)
            
            if type(second) == ParserFunction:
                return ParserOperationAssigment(0, second, first)
        
        if type(first) == ParserOperator:
            if type(second) == ParserVariable:
                return ParserOperation(0, second, first)
                
            if type(second) == ParserFixOperation:
                return ParserOperation(0, second, first)
            
            if type(second) == ParserOperation and second.first:
                return ParserOperation(0, second, first)
            
            if type(second) == ParserLineBlock and second.isSomething():
                return ParserOperation(0, second, first)
            
            if type(second) == ParserFunction:
                return ParserOperation(0, second, first)
            
            if type(second) == ParserFunctionCommaTree:
                if second.getHolder():
                    second.holder = ParserMerge.merge(first, second.getHolder())
                    return second
            
            if type(second) == ParserFutureFunction:
                return ParserMerge.merge(first, ParserMerge.merge(second.first.value, second.second))

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
                if not first.isStoreVariable():
                    return ParserError()
                second.variable = ParserMerge.merge(first, second.variable)
                return second

            if type(second) == ParserOperatorForRange and not second.first:
                second.first = first
                return second
            
            if type(second) == ParserForInRange and not second.variable:
                if not first.isStoreVariable():
                    return ParserError()

                second.variable = first
                return second
            
            if type(second) == ParserPFixOperator:
                fixType = ParserFixType.isPosfix(second)
                if fixType != ParserFixType.none:
                    return ParserFixOperation(first, second, fixType)

            if type(second) == ParserOperationFixParcial:
                if type(second.first) == ParserPFixOperator and type(second.second) == ParserOperation and not second.second.first:
                    second.second.first = ParserMerge.merge(first, second.first)
                    return second.second
            
            if type(second) == ParserLineBlock and first.isStoreVariable():
                if type(second.value) == ParserEmpty:
                    return ParserFunction(first, second.value)
                if type(second.value) == ParserFunctionVariable:
                    return ParserFunction(first, second.value)
                if type(second.value) == ParserFunctionCommaTree and not second.value.holder:
                    return ParserFunction(first, second.value)

                return ParserError()
            
            if type(second) == ParserFutureFunction:
                return ParserMerge.merge(ParserMerge.merge(first, second.first), second.second)
            
            if type(second) == ParserFunctionVariable and not second.name:
                second.name = first
                return second

            if type(second) == ParserFunctionCommaTree:
                print(second.first)
                if not second.first:
                    second.holder = ParserMerge.merge(first, second.getHolder())
                    return second
                if type(second.first) == ParserFunctionVariable:
                    second.holder = ParserMerge.merge(first, second.getHolder())
                    return second
                    
        if type(first) == ParserFunction:
            if type(second) == ParserOperation and not second.first:
                second.first = first
                return second

        if type(first) == ParserLineBlockAbstract:
            if type(second) == ParserVariable:
                return ParserLineBlock(second)

            if type(second) == ParserLineBlock:
                return ParserLineBlock(second)
            
            if type(second) == ParserOperation and second.first and second.second and second.operator:
                return ParserLineBlock(second)
            
            if type(second) == ParserFuncParameter:
                return ParserFuncParameterQueue(second, 0)

            if type(second) == ParserFunctionVariable:
                return ParserLineBlock(second)
            
            if type(second) == ParserFunctionCommaTree:
                if type(second.holder) == ParserFunctionVariable and second.holder.name:
                    toAppend = second.holder
                    second.holder = 0
                    return ParserLineBlock(second.insert(toAppend))
            
            if type(second) == ParserFunction:
                return ParserLineBlock(second)
            
            if type(second) == ParserFixOperation:
                return ParserLineBlock(second)

        if type(first) == ParserStringOperatorAppendE:
            if type(second) == ParserVariable and second.getToken() == LexerEnum.string:
                operation = ParserStringAppend()
                operation.second = second
                return operation
            
        if type(first) == ParserStringOperatorAppend:
            if type(second) == ParserStringAppend and second.first:
                operation = ParserStringAppend()
                operation.second = second
                return operation

        if type(second) == ParserLineBlockCarry:
            if not second.getValue():
                if type(first) == ParserLineBlockAbstract:
                    if second.getAfter():
                        return ParserMerge.merge(ParserLineBlock(ParserEmpty()), second.getAfter())
                    return ParserLineBlock(ParserEmpty())
                second.setValue(first)
                return second
                
            if type(second.getValue()) == ParserLineBlockCarry:
                second.setValue(ParserMerge.merge(first, second.getValue()))
                return second

            second.setValue(ParserMerge.merge(first, second.getValue()))
            if type(second.getValue()) == ParserLineBlock:
                if second.getAfter():
                    return ParserMerge.merge(second.getValue(), second.getAfter())
                return second.getValue()
            
            if type(second.getValue()) == ParserFuncParameterQueue:
                if second.getAfter():
                    if type(second.getAfter()) != ParserFuncReturnType:
                        return ParserError()
                    return ParserFuncParameterQueue(second.getValue(), second.getAfter())
                return second.getValue()

            return second

        if type(first) == ParserLineBlockCarry and not first.after:
            if type(second) == ParserOperation and not second.first:
                first.setAfter(second)
                return first
            
            if type(second) == ParserFuncReturnType:
                first.setAfter(second)
                return first
            
            if type(second) == ParserFunctionCommaTree:
                first.setAfter(second)
                return first
            
        if type(first) == ParserLineBlock:
            if type(second) == ParserOperation and not second.first:
                return ParserFutureFunction(first, second)
            
            #print(second)
            if type(second) == ParserFunctionCommaTree and second.getHolder():
                second.holder = ParserMerge.merge(first, second.getHolder())
                return second
        
        if type(first) == ParserOperation:
            if type(second) == ParserOperation and not second.first and first.first and first.second:
                second.first = first
                return second
            
        if type(first) == ParserPFixOperator:
            if type(second) == ParserVariable and second.isStoreVariable():
                fixType = ParserFixType.isPrefix(first)
                if fixType != ParserFixType.none:
                    return ParserFixOperation(first, second, fixType)
                
            if type(second) == ParserOperation and not second.first:
                return ParserOperationFixParcial(first, second)

        if type(first) == ParserFixOperation:
            if type(second) == ParserOperation and not second.first and second.operator and second.second:
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
            
            if type(second) == ParserVariable:
                return ParserFunctionVariable(second)

            if type(second) == ParserOperation and second.first:
                return ParserFunctionVariable(second)
            
            if type(second) == ParserFunctionCommaTree:
                if not second.first:
                    second.holder = ParserMerge.merge(first, second.getHolder())
                    return second
                if type(second.first) ==  ParserFunctionVariable:
                    second.holder = ParserMerge.merge(first, second.getHolder())
                    return second

            if type(second) == ParserFutureFunction:
                return ParserMerge.merge(first, ParserMerge.merge(second.first.value, second.second))

        if type(first) == ParserWhile:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

        if type(first) == ParserOperatorRange:
            if type(second) == ParserVariable:
                return ParserOperatorForRange(first, 0, second)

        if type(first) == ParserOperatorForIn:
            if type(second) == ParserOperatorForRange and second.isRangeMounted():
                return ParserForInRange(0, first, second)

        if type(first) == ParserFor:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

        if type(first) == ParserFuncVariableDeclarationExplicit:
            if type(second) == ParserVariableType:
                return ParserFuncVariableDeclaration(0, second)

        if type(first) == ParserFuncVariable and first.isStoreVariable():
            if type(second) == ParserFuncVariableDeclaration and not second.variable:
                second.variable = first
                return ParserFuncParameter(second)

            if type(second) == ParserFuncParameterQueue:
                return ParserFunc(first, second)

        if type(first) == ParserFuncComma:
            if type(second) == ParserFuncParameter:
                first.after = second
                return first
        
        if type(second) == ParserFuncComma:
            if not second.getValue():
                    second.setValue(first)
                    return second
            
            merged = ParserMerge.merge(first, second.getValue())
            if type(merged) == ParserFuncParameter:
                if not second.after or type(second.after) != ParserFuncParameter:
                    return ParserError()
                
                merged.setNext(second.after)
                return merged

            second.setValue(merged)
            return second

        if type(first) == ParserFunc:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

        if type(first) == ParserFuncOperatorReturn:
            if type(second) == ParserVariableType:
                return ParserFuncReturnType(second.type)

        if type(first) == ParserFunctionComma:
            if type(second) == ParserFunctionVariable and second.name:
                return ParserFunctionCommaTree().insert(second)
            
            if type(second) == ParserFunctionCommaTree:
                if second.holder and type(second.holder) == ParserFunctionVariable:
                    new = second.holder
                    second.holder = 0
                    return second.insert(new)

        if type(second) == ParserStringAppend:
            return second.setFirst(first)

                
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
    def toParseWithContext(object, callback, types, notFound, context):
        if context == ParserContext.function:
            for _type in context.types():
                if _type == ParserFuncVariable and ParserFuncVariable.isVariable(object):
                    return ParserMerge.merge(ParserFuncVariable(object), callback())

                if _type ==  ParserFuncVariableDeclarationExplicit and ParserFuncVariableDeclarationExplicit.isExplicit(object):
                    return ParserMerge.merge(ParserFuncVariableDeclarationExplicit(), callback())

                if _type == ParserFuncOperatorReturn and ParserFuncOperatorReturn.isOperatorReturn(object):
                    return ParserMerge.merge(ParserFuncOperatorReturn(), callback())
            
                if _type == ParserFuncComma and ParserFuncComma.isComma(object):
                    return ParserMerge.merge(ParserFuncComma(), callback())

        return Parser.toParse(object, callback, types, notFound)

    @staticmethod
    def toParse(object, callback, types, notFound):
        for type in types:            
            if type == ParserLineBlockCarry and ParserLineBlockCarry.isLineBlockUnstack(object):
                return ParserMerge.merge(ParserLineBlockCarry(), callback())

            if type == ParserLineBlock and ParserLineBlock.isLineBlock(object):
                return ParserLineBlock.merge(callback())
            
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

            if type == ParserOperatorRange and ParserOperatorRange.isForRange(object):
                return ParserMerge.merge(ParserOperatorRange(object), callback())

            if type == ParserOperatorForIn and ParserOperatorForIn.isInOperator(object):
                return ParserMerge.merge(ParserOperatorForIn(object), callback())
            
            if type == ParserPFixOperator and ParserPFixOperator.isPFixOperator(object):
                return ParserMerge.merge(ParserPFixOperator(object), callback())
            
            if type == ParserFunctionComma and ParserFuncComma.isComma(object):
                return ParserMerge.merge(ParserFunctionComma(), callback())
            
            if type == ParserStringAppend and ParserStringAppend.isAppend(object):
                return ParserMerge.merge(ParserStringAppend.toParserClass(object), callback())                
            
        return notFound()

    def execute(self):
        if self.queue.isEmpty():
            return ParserEmpty()
    
        object = self.queue.getHead()
        self.queue.toRight()
        
        if Parser.isEndline(object):
            return ParserEmpty()

        parsed = Parser.toParse(object, self.execute, [
            ParserLineBlockCarry,
            ParserLineBlock,
            ParserVariable,
            ParserOperator,
            ParserPFixOperator,
            ParserFunctionComma,
            ParserAssigment,
            ParserDeclarationExplicit,
            ParserStringAppend,
            ParserKeyword,
        ], ParserError)
        
        if type(parsed) == ParserKeyword:
            return Parser.keywordMerge(self.executeKeyword(object), self.execute)

        return parsed

    def executeKeyword(self, keyword):
        if ParserIf.isIfBlock(keyword):
            return self.isIfValid(Parser.isMergeValid(self.blockIf()))
        
        if ParserBreak.isBreak(keyword):
            return ParserBreak()

        if ParserWhile.isWhileBlock(keyword):
            return self.isWhileValid(Parser.isMergeValid(self.blockIf()))

        if ParserFor.isForBlock(keyword):
            return self.isForValid(Parser.isMergeValid(self.blockFor()))

        if ParserFunc.isFuncBlock(keyword):
            return self.isFuncValid(Parser.isMergeValid(self.blockFunc()))
        
        if ParserDeclarationVariable.isDeclarationVariable(keyword):
            return self.isDeclarationValid(keyword, Parser.isMergeValid(self.declarationLine()))

    # ParserDeclarationVariable
    # ParserOperationAssigment
    def isDeclarationValid(self, keyword, merged):
        if type(merged) == ParserOperationAssigment:
            return ParserDeclarationVariable(merged, VariableDeclarationCast.auto, VariableConstantType.toConstantType(keyword))

        if type(merged) == ParserDeclarationVariable:
            merged.varType = VariableConstantType.toConstantType(keyword)
            return merged

        return ParserError()

    def isWhileValid(self, merged):
        if type(merged) == ParserLineBlock:
            merged = merged.value

        if type(merged) == ParserError:
            return merged
        
        if type(merged) == ParserEmpty:
            return ParserError()

        return ParserMerge.merge(ParserWhile(merged), self.block())
    
    def isForValid(self, merged):
        if type(merged) == ParserError:
            return merged
        
        if type(merged) == ParserEmpty:
            return ParserError()

        if type(merged) != ParserForInRange:
            return ParserError()

        return ParserMerge.merge(ParserFor(merged), self.block())        
    
    def isFuncValid(self, merged):
        if type(merged) == ParserFuncVariable:
            return ParserMerge.merge(ParserFunc(merged, ParserFuncParameterQueue(0, 0)), self.block())

        if type(merged) != ParserFunc:
            return ParserError()

        return ParserMerge.merge(merged, self.block())

    def isIfValid(self, merged):
        if type(merged) == ParserLineBlock:
            merged = merged.value

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
            ParserLineBlockCarry,
            ParserLineBlock,
            ParserVariable,
            ParserOperator,
            ParserPFixOperator,
            ParserFunctionComma,
            ParserDeclarationExplicit,
        ], ParserError)

    def blockFor(self):
        if self.queue.isEmpty():
            return ParserError()
    
        object = self.queue.getHead()
        self.queue.toRight()

        return Parser.toParse(object, self.blockFor, [
            ParserBlock,
            ParserVariable,
            ParserOperatorRange,
            ParserOperatorForIn
        ], ParserError)
    
    def blockFunc(self):
        if self.queue.isEmpty():
            return ParserError()
    
        object = self.queue.getHead()
        self.queue.toRight()

        return Parser.toParseWithContext(object, self.blockFunc, [
            ParserBlock,
            ParserLineBlockCarry,
            ParserLineBlock,
            ParserVariableType
        ], ParserError, ParserContext.function)


    def declarationLine(self):    
        if self.queue.isEmpty():
            return ParserEmpty()
    
        object = self.queue.getHead()
        self.queue.toRight()

        if Parser.isEndline(object):
            return ParserEmpty()

        return Parser.toParse(object, self.declarationLine, [
            ParserLineBlockCarry,
            ParserLineBlock,
            ParserVariable,
            ParserDeclarationExplicit,
            ParserVariableType,
            ParserOperator,
            ParserPFixOperator,
            ParserAssigment
        ], ParserError)
        
    def block(self):
        object = self.queue.getHead()
        instructions = LexerQueue()

        while object and not ParserBlock.isCloseBlock(object):
            line = Parser.isMergeValid(self.execute())
            
            if type(line) == ParserError:
                instructions = line
                break

            if type(line) != ParserEmpty:
                instructions.insert(line)

            object = self.queue.getHead()

        if not object:
            return ParserError()

        self.queue.toRight()
        return instructions        
        
    @staticmethod
    def isKeyword(object):
        return object.getToken() == LexerEnum.keyword

    @staticmethod
    def notAccepted(merged, types):
        for _type in types:
            if type(merged) == _type:
                return ParserError()
            
        return ParserEmpty()

    @staticmethod
    def isMergeValid(merged):
        if type(merged) == ParserFutureFunction:
            merged = ParserMerge.merge(merged.first.value, merged.second)

        if type(merged) == ParserOperation and not merged.first:
            return ParserError()

        if type(merged) == ParserOperationAssigment and not merged.first:
            return ParserError()

        if type(merged) == ParserStringAppend and not merged.first:
            return ParserError()
        
        if type(merged) == ParserLineBlock:
            if type(merged.value) == ParserEmpty:
                return ParserError()

            notAccepted = Parser.isMergeValid(merged.value)

        else:
            notAccepted = Parser.notAccepted(merged, [
                ParserOperationFixParcial,
                ParserPFixOperator,
                ParserLineBlockCarry,
                ParserFunctionVariable,
                ParserFunctionComma,
                ParserFunctionCommaTree
            ])
        
        if type(notAccepted) == ParserError:
            return notAccepted

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

def compareToken(object, values):
    return LexerEnum.compare(object, values)