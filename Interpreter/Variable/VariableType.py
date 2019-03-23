from enum import Enum, unique

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
            return "Nil"
        if self == VariableType.string:
            return "String"
        if self == VariableType.integer:
            return "Integer"
        if self == VariableType.float:
            return "Float"
        if self == VariableType.boolean:
            return "Boolean"
        if self == VariableType.number:
            return "Number"
        return ""