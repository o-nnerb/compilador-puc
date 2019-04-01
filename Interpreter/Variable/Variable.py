from .VariableType import VariableType
import traceback
from enum import Enum, unique

class VariableDeclarationCast(Enum):
    auto = "AUTO"
    primitive = "PRIT"

class VariableConstantType(Enum):
    var = 0
    let = 1

    @staticmethod
    def toConstantType(string):
        if string == "let":
            return VariableConstantType.let
        if string == "var":
            return VariableConstantType.var
        
        return 0

    @staticmethod
    def isConstantType(string):
        return string == "let" or string == "var"
    
    def toString(self):
        if self == VariableConstantType.let:
            return "let"
        
        return "var"

class Variable:
    name = 0
    value = 0
    type = 0
    varType = 0

    def __init__(self, name, value, type, varType):
        self.name = name
        self.value = value
        self.type = type
        self.varType = varType
        self.cast(type)

    def getName(self):
        return self.name

    def setFinalValue(self, variable):
        self.value = variable.value
        self.type = variable.type

    def setPrimiteValue(self, value):
        variable = self.copy()
        variable.value = value
        self.setValue(variable)
    
    def copy(self):
        variable = Variable(self.name, self.value, self.type)
        return variable

    def setValue(self, variable):
        # variable (ans, value, type)
        if VariableType.compare(self.type, VariableType.nil):
            #first set
            if not VariableNil(variable):
                return False

            self.setFinalValue(variable)
            return True
        # casting
        # porque o tipo da variável é fixo
        variableTypes = [
            (VariableType.string,   VariableString),
            (VariableType.integer,  VariableInteger),
            (VariableType.float,    VariableFloat),
            (VariableType.boolean,  VariableBoolean),
            (VariableType.number,   VariableNumber)
        ]

        for (type, clss) in variableTypes:
            if VariableType.compare(self.type, type):
                if not clss(self, variable):
                    return False
            
            self.setFinalValue(variable)
            return True

        return False
    
    def copy(self):
        return Variable(self.name, self.value, self.type, self.varType)

    def toString(self):
        if self.type != VariableType.string:
            print("Error: operação com string nâo suportado")
            quit()
        self.type = VariableType.string
        return
    
    def toInteger(self):
        self.value = int(self.value)
        self.type = VariableType.integer
        return
    
    def toFloat(self):
        self.value = float(self.value)
        self.type = VariableType.float
        return
    
    def toBoolean(self):
        if self.value == "true":
            self.value = 1
        elif self.value == "false":
            self.value = 0
        else:
            if not self.value:
                self.value = 0
            else:
                self.value = 1
        self.type = VariableType.boolean
        return
    
    def toNumber(self):
        return
    
    def read(self):
        if self.type == VariableType.nil:
            print("Runtime error: reading a nil variable")
            quit()

    def cast(self, variableType, reading=True):
        if reading:
            self.read()

        if variableType == VariableType.nil:
            if reading:
                print("Runtime error: reading a nil variable")
                quit()
            
            return True

        if variableType == VariableType.string:
            self.toString()
            return True

        if variableType == VariableType.integer:
            self.toInteger()
            return True

        if variableType == VariableType.float:
            self.toFloat()
            return True

        if variableType == VariableType.boolean:
            self.toBoolean()
            return True

        if variableType == VariableType.number:
            self.toNumber()
            return True

        return False

    @staticmethod
    def defaultPriority():
        return [VariableType.string, VariableType.float, VariableType.number, VariableType.integer, VariableType.boolean]
    #operators
    @staticmethod
    def castWithPriorityType(self, other, reading=True, types=0):
        ans = self.copy()
        other = other.copy()
        ans.name = "ans"

        if not types:
            types = Variable.defaultPriority()

        for type in types:
            if ans.type == type:
                if not other.cast(ans.type, reading):
                    return (0, 0)
                return (ans, other)

            if other.type == type:
                if not ans.cast(other.type, reading):
                    return (0, 0)
                return (ans, other)
        return (0, 0)

    def __add__(self, other):
        # Addition
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value + other.value)
        return ans
    
    def __mul__(self, other):
        # Multiplication
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value * other.value)

        return ans
     
    def __sub__(self, other):
        # Subtraction
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value - other.value)
        return ans
     
    def __mod__(self, other):
        # Remainder
        ans = VariableNumber(self.copy()).asSuper()
        other = VariableNumber(other.copy()).asSuper()
        
        ans.toInteger()
        other.toInteger()

        print("first " + str(ans.value))
        print("second " + str(other.value))
        ans.setPrimiteValue(ans.value % other.value)
        print("result " + str(ans.value))
        return ans
     
    def __truediv__(self, other):
        # Division
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value / other.value)
        return ans

    def __pow__(self, other):
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value ** other.value)
        return ans
     
    def __lt__(self, other):
        # Less than
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value < other.value)
        return ans
     
    def __le__(self, other):
        # Less than or equal to
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value <= other.value)
        return ans
     
    def __eq__(self, other):
        # Equal to
        (ans, other) = Variable.castWithPriorityType(self, other)  
        print("Bf " + str(ans.value))      
        print("Bf " + str(other.value)) 
        ans.setPrimiteValue(ans.value == other.value)
        ans.toBoolean()  
        print("Rf " + str(ans.value))   
        return ans
     
    def __ne__(self, other):
        # Not equal to
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value != other.value)
        ans.toBoolean()
        return ans
     
    def __gt__(self, other):
        # Greater than
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value > other.value)
        ans.toBoolean()
        return ans
     
    def __ge__(self, other):
        # Greater than or equal to
        (ans, other) = Variable.castWithPriorityType(self, other)        
        ans.setPrimiteValue(ans.value >= other.value)
        ans.toBoolean()
        return ans
        
    def __and2__(self, other):
        (ans, other) = Variable.castWithPriorityType(self, other)   
        ans.setPrimiteValue(ans.value and other.value)
        ans.toBoolean()
        return ans

    def __or2__(self, other):
        (ans, other) = Variable.castWithPriorityType(self, other)   
        ans.setPrimiteValue(ans.value or other.value)
        ans.toBoolean()
        return ans

    def assigment(self, other):
        if self.varType == VariableConstantType.let:
            print("Error: variavel " + self.name + " é constante.")
            quit()
        other.read()
        other = other.copy()
        
        ans = self.copy()
        ans.name = "ans"
        
        if not ans.type == VariableType.nil:
            if not other.cast(ans.type, False):
                print("Runtime error: can't parse variable")
                quit()

            if ans.type != other.type:
                print("Runtime error: (assigment) type not equal")
                quit()
                return False
    
        self.value = other.value
        self.type = other.type
        return True

    def primitiveCast(self):
        if self.type == VariableType.boolean:
            self.toBoolean()
            return self
        
        if self.type == VariableType.integer:
            self.toInteger()
            return self
        
        if self.type == VariableType.float:
            self.toFloat()
            return self
                    
        return self

    def toAuto(self):
        point = 0
        self.value = str(self.value)
        for char in self.value:
            if char < '0' or char > '9':
                if char == ".":
                    point += 1
                if point == 2 or char != ".":
                    self.toString()
                    return self
                    
        if point:
            if self.value[len(self.value)-1] != ".":
                self.toFloat()
                return self
        
        self.toInteger()
        return self

    def verbose(self):
        typeName = self.type.name()
        return self.varType.toString()+"_"+typeName+"("+self.name+", "+str(self.value)+")"

    @staticmethod
    def withOperator(operator, first, second):
        print(operator)
        if operator == "+":
            print((first + second).value)
            return first + second
        
        if operator == "-":
            return first - second
        
        if operator == "/":
            return first / second
        
        if operator == "%":
            return first % second
        
        if operator == "*":
            return first * second
        
        if operator == "^":
            return first ** second

        #boolean

        if operator == "<":
            return first < second
        
        if operator == ">":
            return first > second
        
        if operator == "<=":
            return first <= second
        
        if operator == ">=":
            return first >= second
        
        if operator == "!=":
            return first != second
        
        if operator == "==":
            return first == second

        if operator == "and":
            return first and second
        
        if operator == "or":
            return first or second

        return False

class VariableNil(Variable):
    @staticmethod
    def cast(variable):
        return True

class VariableString(Variable):
    @staticmethod
    def cast(variable):        
        return variable.cast(VariableType.string)

class VariableInteger(Variable):
    @staticmethod
    def cast(variable):
        return variable.cast(VariableType.integer)

class VariableFloat(Variable):
    @staticmethod
    def cast(variable):
        return variable.cast(VariableType.float)

class VariableBoolean(Variable):
    @staticmethod
    def cast(variable):
        return variable.cast(VariableType.boolean)

class VariableNumber(Variable):
    
    def __init__(self, variable):
        super(VariableNumber, self).__init__(variable.name, variable.value, variable.type, variable.varType)

        if not self.isNumber:
            print("(Runtime error): can't parse variable to number format")
            quit()
    
    def isNumber(self):
        self.read()

        return VariableType.compare(self.type, [Variable.integer, Variable.float, Variable.boolean])

    def asSuper(self):
        return Variable(self.name, self.value, self.type, self.varType)

    @staticmethod
    def cast(variable):
        return variable.cast(VariableType.number)