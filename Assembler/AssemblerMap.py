from Parser.Parser import ParserBreak, ParserFunction, ParserFunctionVariable, ParserFor, ParserLineBlock, ParserForInRange, VariableDeclarationCast, ParserWhile, ParserIf, ParserStringBlock, ParserStringQueue, ParserOperationAssigment, ParserVariableType, ParserDeclarationVariable, ParserVariable, ParserOperation, ParserFunction, ParserIf, ParserEmpty
from enum import Enum, unique

@unique
class AssemblerAction(Enum):
    none = 0
    load = 1
    constant = 2
    create = 3
    store = 4

class Element:
    name = 0
    value = 0
    action = 0

    def __init__(self, name, value, action):
        self.name = name
        self.value = value
        self.action = action

    @staticmethod
    def fromVariable(variable):
        if variable.isStoreVariable():
            return Element(variable.getValue(), 0, AssemblerAction.load)
        
        return Element(0, variable.getValue(), AssemblerAction.constant)

class Operation:
    first = 0
    second = 0
    operator = 0

    def __init__(self, first, second, operator):
        self.first = first
        self.second = second
        self.operator = operator

class DynamicJump:
    rule = 0
    block = 0

    def __init__(self, rule, block):
        self.rule = rule
        self.block = block

class If(DynamicJump):
    elseBlock = 0

    def __init__(self, rule, block, elseBlock):
        self.elseBlock = elseBlock
        super(If, self).__init__(rule, block)



class Mapper:

    @staticmethod
    def toOperation(object):
        if type(object) == ParserOperation:
            return Operation(Mapper.toOperation(object.first), Mapper.toOperation(object.second), object.operator.getValue())
    
        if type(object) == ParserVariable:
            return Element.fromVariable(object)

        if type(object) == ParserLineBlock:
            return Mapper.toOperation(object.value)

        print("Error: can't recognize " + str(object))
        return

    @staticmethod
    def _map(object):
        #print(object)

        if type(object) == ParserEmpty:
            return []

        if type(object) == ParserOperation:
            return Mapper.toOperation(object)

        if type(object) == ParserOperationAssigment:
            variable = Element.fromVariable(object.first)
            variable.action = AssemblerAction.store
            
            if type(object.second) == ParserStringQueue:
                print("Assembler error: type not supported")
                quit()
            else:
                value = Mapper.toOperation(object.second)
            
            return [value, variable]
        
        if type(object) == ParserDeclarationVariable:
            (assigment, primitiveType, varType) = object.map()
            
            variable = Element.fromVariable(assigment.first)
            variable.action = AssemblerAction.create

            if type(assigment.second) == ParserVariable:
                value = Element.fromVariable(assigment.second)

            elif type(assigment.second) == ParserFunction:
                print("Assembler error: functions are not supported")
                quit()

            elif type(assigment.second) == ParserOperation:
                value = Mapper.toOperation(assigment.second)
                    
            elif type(assigment.second) == ParserStringQueue:
                print("Assembler error: type not supported")
                quit()
            else:
                print("Assembler error: instruction undefined " + str(assigment.second))
                quit()
            
            return [value, variable]
        
        if type(object) == ParserIf:
            if not object.block:
                object.block = []
            else:
                object.block = object.block.asArray()

            if not object.elseBlock:
                return If(Mapper.toOperation(object.value), object.block, 0)
            return If(Mapper.toOperation(object.value), object.block, Mapper.map(object.elseBlock))

    @staticmethod
    def map(object):
        ret = Mapper._map(object)
        if type(ret) != list:
            return [ret]
        return ret
