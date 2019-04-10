from enum import Enum, unique
from Lexer.LexerQueue import LexerQueue
from .AssemblerMap import Mapper, Operation, AssemblerAction, Element

class AssemblerVariable:
    pointer = 0
    name = 0

    def __init__(self, name, pointer):
        self.name = name
        self.pointer = pointer
    
class AssemblerVariables:
    allVariables = []

    def __init__(self):
        self.allVariables = []

    def save(self, variable, register):
        variable = AssemblerVariable(variable.name, len(self.allVariables))
        AssemblerInstruction.store(variable.pointer, register)
        self.allVariables.append(variable)

    def findPointer(self, variable):
        for _variable in self.allVariables:
            if _variable.name == variable.name:
                return _variable.pointer
            
        return -1


class AssemblerInstructionNode:
    globalCounter = 0

    string = 0
    next = 0
    pointer = 0

    def __init__(self, string):
        self.string = string

        AssemblerInstructionNode.globalCounter += 1
        self.pointer = AssemblerInstructionNode.globalCounter

    def setNext(self, next):
        self.next = next

@unique
class AssemblerRegister(Enum):
    r1 = "R1"
    r2 = "R2"
    r3 = "R3"
    r4 = "R4"
    r5 = "R5"
    r6 = "R6"
    r7 = "R7"
    r8 = "R8"

class AssemblerRegisterControl:
    register = 0
    isEnable = True

    def __init__(self, register):
        self.register = register

    def lock(self):
        self.isEnable = False

    def unlock(self):
        self.isEnable = True

    def name(self):
        return self.register.value

class AssemblerRegisters:
    allRegisters = []

    def __init__(self):
        self.allRegisters = [
            AssemblerRegisterControl(AssemblerRegister.r1),
            AssemblerRegisterControl(AssemblerRegister.r2),
            AssemblerRegisterControl(AssemblerRegister.r3),
            AssemblerRegisterControl(AssemblerRegister.r4),
            AssemblerRegisterControl(AssemblerRegister.r5),
            AssemblerRegisterControl(AssemblerRegister.r6),
            AssemblerRegisterControl(AssemblerRegister.r7),
            AssemblerRegisterControl(AssemblerRegister.r8),
        ]

    def firstAvailable(self):
        for register in self.allRegisters:
            if register.isEnable:
                return register
        
        print("Assembler Error: can't find a one register not in use")
        print("Please, verify your code")
        quit()
    
    def isAllBusy(self):
        for register in self.allRegisters:
            if register.isEnable:
                return False
        
        return True

    def getRegister(self, register):
        for _register in self.allRegisters:
            if _register.register == register:
                return _register

        return False

    def unlockAll():
        for register in self.allRegisters:
            register.unlock()
        

class AssemblerContext:
    register = 0
    line = 0

    def __init__(self, register, line):
        self.register = register
        self.line = line

class AssemblerValueConstant:
    value = 0

    def __init__(self, value):
        self.value = value

class AssemblerInstruction:
    register = AssemblerRegisters()
    counter = 0
    instruction = ""

    __shared = 0

    def __init__(self):
        return

    @staticmethod
    def shared():
        if not AssemblerInstruction.__shared:
            AssemblerInstruction.__shared = AssemblerInstruction()

        return AssemblerInstruction.__shared

    def save(self, string):
        self.instruction += string + "\n"
        self.counter += 1
        return self.counter

    @staticmethod
    def load(pointer, register=0, isMemory=True):
        self = AssemblerInstruction.shared()

        if not register:
            register = self.register.firstAvailable()
            register.lock()
        
        if isMemory:
            pointer = "["+str(pointer)+"]"
        
        return AssemblerContext(register, self.save("load " + register.name() + ", " + str(pointer)))

    @staticmethod
    def store(pointer, register, isMemory=True):
        self = AssemblerInstruction.shared()
        register.unlock()
        if isMemory:
            pointer = "["+str(pointer)+"]"

        return AssemblerContext(register, self.save("store " + str(pointer) + ", " + register.name()))
    
    @staticmethod
    def asSomething(register):
        if type(register) == AssemblerValueConstant:
            return str(register.value)

        return register.name()


    @staticmethod
    def binary(first, second, third, operation):
        self = AssemblerInstruction.shared()
        first.lock()
        
        second = self.asSomething(second)
        third = self.asSomething(third)
        
        return AssemblerContext(first, self.save(operation + " " + first.name() + ", " + second + ", " + third))
    
    @staticmethod
    def unary(first, second, operation):
        self = AssemblerInstruction.shared()
        first.lock()
        
        second = self.asSomething(second)

        return AssemblerContext(first, self.save(operation + " " + first.name() + ", " + second))

    @staticmethod
    def add(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "add")
    
    @staticmethod
    def sub(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "sub")
    
    @staticmethod
    def mul(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "mul")
    
    @staticmethod
    def div(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "div")
    
    @staticmethod
    def mod(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "mod")
    
    @staticmethod
    def pot(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "pot")
    
    @staticmethod
    def cmpAnd(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "and")
    
    @staticmethod
    def cmpOr(first, second, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, second, "or")
    
    @staticmethod
    def cmpNot(first, register=0):
        if not register:
            register = AssemblerInstruction.shared().register.firstAvailable()

        return AssemblerInstruction.binary(register, first, "or")
    
    @staticmethod
    def jump(pointer):
        self = AssemblerInstruction.shared()
        return AssemblerInstruction.binary(0, self.save("jump " + str(pointer)))

    @staticmethod
    def jumps(first, second, pointer, operation):
        self = AssemblerInstruction.shared()
        
        first = self.asSomething(first)
        second = self.asSomething(second)

        return AssemblerContext(0, self.save(operation + " " + first + ", " + second + ", " + str(pointer)))
    
    @staticmethod
    def beq(first, second, pointer):
        return AssemblerInstruction.jumps(first, second, pointer, "beq")

    @staticmethod
    def bne(first, second, pointer):
        return AssemblerInstruction.jumps(first, second, pointer, "bne")

    @staticmethod
    def blt(first, second, pointer):
        return AssemblerInstruction.jumps(first, second, pointer, "blt")

    @staticmethod
    def ble(first, second, pointer):
        return AssemblerInstruction.jumps(first, second, pointer, "ble")

    @staticmethod
    def bgt(first, second, pointer):
        return AssemblerInstruction.jumps(first, second, pointer, "bgt")

    @staticmethod
    def bge(first, second, pointer):
        return AssemblerInstruction.jumps(first, second, pointer, "bge")

    @staticmethod
    def push(first):
        return AssemblerContext(first, self.save("push " + first.name()))

    @staticmethod
    def pop(first):
        return AssemblerContext(first, self.save("pop " + first.name()))

    @staticmethod
    def read(first):
        return AssemblerContext(first, self.save("read " + first.name()))

    @staticmethod
    def write(first):
        return AssemblerContext(first, self.save("write " + first.name()))

class AssemblerElementContext:
    @staticmethod
    def toAssembly(object):
        if type(object) != Element:
            return
        
        print(object.action)
        if object.action == AssemblerAction.constant:
            return AssemblerValueConstant(object.value)
        if object.action == AssemblerAction.load:
            pointer = Assembler.variables.findPointer(object)
            return  AssemblerInstruction.load(pointer).register

class AssemblerOperationContext:

    @staticmethod
    def doOperation(object):
        holder = 0
        unlock = 0
        if type(object.first) == AssemblerRegisterControl:
            holder = object.first
        
        if type(object.second) == AssemblerRegisterControl:
            if not holder:
                holder = object.second
            else:
                unlock = object.second

        if not holder:
            holder = AssemblerInstruction.shared().register.firstAvailable()
            AssemblerInstruction.load(0, holder, False)

        if object.operator == "+":
            holder = AssemblerInstruction.add(object.first, object.second, holder)

        if object.operator == "-":
            holder = AssemblerInstruction.sub(object.first, object.second, holder)

        if object.operator == "*":
            holder = AssemblerInstruction.mul(object.first, object.second, holder)

        if object.operator == "/":
            holder = AssemblerInstruction.div(object.first, object.second, holder)

        if object.operator == "%":
            holder = AssemblerInstruction.mod(object.first, object.second, holder)

        if object.operator == "^":
            holder = AssemblerInstruction.pot(object.first, object.second, holder)

        if object.operator == "and":
            holder = AssemblerInstruction.cmpAnd(object.first, object.second, holder)

        if object.operator == "or":
            holder = AssemblerInstruction.cmpOr(object.first, object.second, holder)

        if unlock:
            unlock.unlock()

        return holder

    @staticmethod
    def toAssembly(object):
        if type(object) == Operation:
            object.first = AssemblerOperationContext.toAssembly(object.first)
            object.second = AssemblerOperationContext.toAssembly(object.second)
            
            return AssemblerOperationContext.doOperation(object).register
        
        if type(object) == Element:
            return AssemblerElementContext.toAssembly(object)

        return 0 

class Assembler:
    variables = AssemblerVariables()
    holder = 0

    @staticmethod
    def isAssigment(assigment):
        print(assigment.operator)

    @staticmethod
    def isOperation(object):
        if type(object) != Operation:
            return False

        return AssemblerOperationContext.toAssembly(object)
        
    @staticmethod
    def run(queue):
        Assembler.queue = queue.copy()

        while not Assembler.queue.isEmpty():
            instructions = Mapper.map(Assembler.queue.popFirst())
            print(instructions)
            
            holder = 0
            for instruction in instructions:
                flag = 0
                if holder and type(holder) == AssemblerRegisterControl:
                    if type(instruction) == Element:
                        if instruction.action == AssemblerAction.create:
                            Assembler.variables.save(instruction, holder)
                            flag = True
                        if instruction.action == AssemblerAction.store:
                            pointer = Assembler.variables.findPointer(instruction)
                            AssemblerInstruction.store(pointer, holder).register
                            flag = True
                    
                else:
                    if type(instruction) == Element:
                        holder = AssemblerElementContext.toAssembly(instruction)
                        flag = True
                        if type(holder) == AssemblerValueConstant:
                            holder = AssemblerInstruction.load(holder.value, 0, False).register
            
                if not flag:
                    holder = Assembler.isOperation(instruction)
                    flag = True

            if holder:
                holder.unlock()
                holder = 0
                AssemblerInstruction.shared().instruction += "\n"
            
            print(AssemblerInstruction.shared().instruction)
