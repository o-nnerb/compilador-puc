from .Runnable import Runnable
from Lexer.LexerEnum import LexerEnum
from Lexer.LexerHash import LexerHash as Hash
from .Variable.Variable import Variable
from .Variable.Variable import VariableType

class Element:
    right = 0 #runnable
    operator = 0
    left = 0 #runnable

    value = 0 #Runnable ou ParserToken

    def __init__(self):
        return

    @staticmethod
    def single(value):
        self = Element()
        self.value = value
        return self
    
    @staticmethod
    def both(left, operator, right):
        self = Element()
        self.right = right
        self.operator = operator
        self.left = left
        return self
    
    def setRight(self, right):
        self.right = right
    
    def setLeft(self, left):
        self.left = left
    
    def setOperator(self, operator):
        self.operator = operator
    
    @staticmethod
    def operation(operator, left, right):
        operator = operator.getValue()
        
        if operator == "+":
            return left + right
        
        if operator == "-":
            return left - right
        
        if operator == "/":
            return left / right
        
        if operator == "%":
            return left % right
        
        if operator == "*":
            return left * right
        
        if operator == "^":
            return left ** right

        #boolean

        if operator == "<":
            return left < right
        
        if operator == ">":
            return left > right
        
        if operator == "<=":
            return left <= right
        
        if operator == ">=":
            return left >= right
        
        if operator == "!=":
            return left != right
        
        if operator == "==":
            return left == right

        if operator == "and":
            return left and right
        
        if operator == "or":
            return left or right

        return False

    def run(self):
        if not self.value:
            left = self.left.run()
            right = self.right.run()

            if compareToken(self.operator, LexerEnum.assigment):
                left.assigment(right)
                return left

            return Element.operation(self.operator, left, right)
        
        if type(self.value) == Runnable:
            return self.value.run()

        if compareToken(self.value, LexerEnum.id):
            return Hash.shared().getObject(self.value.getValue()) # valor, tipo

        if compareToken(self.value, LexerEnum.boolean):
            return Variable("carry", self.value.getValue() == "true", VariableType.boolean).primitiveCast()
        
        # Vai ser um inteiro ou um float
        if compareToken(self.value, LexerEnum.integer):
            return Variable("carry", self.value.getValue(), VariableType.integer).primitiveCast()
        if compareToken(self.value, LexerEnum.float):
            return Variable("carry", self.value.getValue(), VariableType.float).primitiveCast()

        return False

def compareToken(object, values):
    return LexerEnum.compare(object, values)