from enum import Enum, unique
from Lexer.LexerEnum import LexerEnum

class VariableType(Enum):
    nil = 0
    string = 1
    integer = 2
    float = 3
    boolean = 4

    number = 5 # mix Int e Float

    @staticmethod
    def compare(object, values):
        if type(values) != list:
            return object == values.value
        
        for val in values:
            if object == val.value:
                return True
        
        return False

    def name(self):
        if self == VariableType.nil:
            return "nil"
        if self == VariableType.string:
            return "string"
        if self == VariableType.integer:
            return "integer"
        if self == VariableType.float:
            return "float"
        if self == VariableType.boolean:
            return "boolean"
        if self == VariableType.number:
            return "number"
        return ""

    @staticmethod
    def isPrimitive(string):
        if string == "string":
            return VariableType.string
        if string == "integer":
            return VariableType.integer
        if string == "float":
            return VariableType.float
        if string == "boolean":
            return VariableType.boolean

        return 0

    @staticmethod
    def cast(value):
        if value == LexerEnum.string:
            return VariableType.string
        
        if value == LexerEnum.integer:
            return VariableType.integer
        
        if value == LexerEnum.float:
            return VariableType.float
        
        if value == LexerEnum.boolean:
            return VariableType.boolean
        
        return 0