from enum import Enum, unique
import os
from Lexer.LexerQueue import LexerQueue
from .AssemblerMap import Mapper, Operation, AssemblerAction, Element, DynamicJump, If

import traceback
class AssemblerVariable:
    pointer = 0
    name = 0

    def __init__(self, name, pointer):
        self.name = name
        self.pointer = pointer
    
class AssemblerVariables:
    allVariables = []
    assemblerInstruction = 0
    
    def __init__(self):
        self.allVariables = []

    def context(self, assemblerInstruction):
        self.assemblerInstruction = assemblerInstruction
        return self

    def save(self, variable, register):
        variable = AssemblerVariable(variable.name, len(self.allVariables))
        self.assemblerInstruction.store(variable.pointer, register)
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

    def fromString(string):
        all = [
            (1, AssemblerRegister.r1),
            (2, AssemblerRegister.r2),
            (3, AssemblerRegister.r3),
            (4, AssemblerRegister.r4),
            (5, AssemblerRegister.r5),
            (6, AssemblerRegister.r6),
            (7, AssemblerRegister.r7),
            (8, AssemblerRegister.r8),
        ]

        for (index, reg) in all:
            if string == "R" + str(index):
                return reg
        
        return 0

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

class InstructionsContext:
    assembler = 0

    def __init__(self, assembler):
        self.assembler = assembler

class AssemblerValueConstant:
    value = 0

    def __init__(self, value):
        self.value = value

class AssemblerInstruction:
    register = AssemblerRegisters()
    counter = 0
    instruction = []

    __shared = 0

    def __init__(self):
        self.counter = 0
        self.instruction = []


    def toFile(self, args):
        args = [args[i] for i in range(0, len(args))]
        del args[0]
        path = args.pop(0)
        if path[0] == '/':
            exit()
        else:
            path = os.getcwd() + '/' + path

        path = path.split("/")
        fileName = path.pop().split(".").pop(0)
        path = "/".join(path) + "/"+fileName+".a"
        file = open(path, "w")
        file.write(self.asLines())
        file.close()

    @staticmethod
    def shared():
        if not AssemblerInstruction.__shared:
            AssemblerInstruction.__shared = AssemblerInstruction()

        return AssemblerInstruction.__shared

    def save(self, string):
        self.instruction.append(string)
        self.counter += 1
        return self.counter

    def asLines(self):
        if len(self.instruction) == 0:
            return "\n"
        isEnd = self.instruction[len(self.instruction)-1] == "\n"
        if isEnd:
            isEnd = ""
        else:
            isEnd = "\n"
        return ("\n".join([line for line in self.instruction])) + isEnd

    @staticmethod
    def temporary():
        return AssemblerInstruction()
        
    def load(self, pointer, register=0):
        if not register:
            register = self.register.firstAvailable()
            register.lock()
        
        pointer = "["+str(pointer)+"]"

        traceback.print_stack()
        return AssemblerContext(register, self.save("load " + register.name() + ", " + str(pointer)))

    def store(self, pointer, register):
        register.unlock()
        pointer = "["+str(pointer)+"]"

        return AssemblerContext(register, self.save("store " + str(pointer) + ", " + register.name()))

    def mov(self, first, second):
        first.lock()
        second = AssemblerInstruction.asSomething(second)

        return AssemblerContext(first, self.save("mov " + first.name() + ", " + second))
    
    @staticmethod
    def asSomething(register):
        if type(register) == AssemblerValueConstant:
            return str(register.value)

        return register.name()

    def binary(self, first, second, third, operation):
        first.lock()
        
        second = AssemblerInstruction.asSomething(second)
        third = AssemblerInstruction.asSomething(third)
        
        return AssemblerContext(first, self.save(operation + " " + first.name() + ", " + second + ", " + third))
    
    def unary(self, first, second, operation):
        first.lock()
        
        second = AssemblerInstruction.asSomething(second)

        return AssemblerContext(first, self.save(operation + " " + first.name() + ", " + second))

    def add(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "add")
    
    def sub(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "sub")
    
    def mul(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "mul")
    
    def div(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "div")
    
    def mod(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "mod")
    
    def pot(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "pot")
    
    def cmpAnd(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "and")
    
    def cmpOr(self, first, second, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, second, "or")
    
    def cmpNot(self, first, register=0):
        if not register:
            register = self.register.firstAvailable()

        return self.binary(register, first, "or")
    
    def jump(self, pointer):
        return self.binary(0, self.save("jump " + str(pointer)))

    def jumps(self, first, second, pointer, operation):        
        first = AssemblerInstruction.asSomething(first)
        second = AssemblerInstruction.asSomething(second)

        return AssemblerContext(0, self.save(operation + " " + first + ", " + second + ", " + str(pointer)))
    
    def beq(self, first, second, pointer):
        return self.jumps(first, second, pointer, "beq")

    def bne(self, first, second, pointer):
        return self.jumps(first, second, pointer, "bne")

    def blt(self, first, second, pointer):
        return self.jumps(first, second, pointer, "blt")

    def ble(self, first, second, pointer):
        return self.jumps(first, second, pointer, "ble")

    def bgt(self, first, second, pointer):
        return self.jumps(first, second, pointer, "bgt")

    def bge(self, first, second, pointer):
        return self.jumps(first, second, pointer, "bge")

    def push(self, first):
        return AssemblerContext(first, self.save("push " + first.name()))

    def pop(self, first):
        return AssemblerContext(first, self.save("pop " + first.name()))

    def read(self, first):
        return AssemblerContext(first, self.save("read " + first.name()))

    def write(self, first):
        return AssemblerContext(first, self.save("write " + first.name()))

class AssemblerElementContext(InstructionsContext):
    def __init__(self, assembler):
        super(AssemblerElementContext, self).__init__(assembler)

    def toAssembly(self, object):
        if type(object) != Element:
            return
        
        #print(object.action)
        if object.action == AssemblerAction.constant:
            return AssemblerValueConstant(object.value)
        if object.action == AssemblerAction.load:
            pointer = Assembler.variables.findPointer(object)
            return  self.assembler.load(pointer).register

class AssemblerOperationContext(InstructionsContext):
    def __init__(self, assembler):
        super(AssemblerOperationContext, self).__init__(assembler)

    def doOperation(self, object):
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
            holder = self.assembler.register.firstAvailable()
            self.assembler.mov(holder, AssemblerValueConstant(0))

        if object.operator == "+":
            holder = self.assembler.add(object.first, object.second, holder)

        if object.operator == "-":
            holder = self.assembler.sub(object.first, object.second, holder)

        if object.operator == "*":
            holder = self.assembler.mul(object.first, object.second, holder)

        if object.operator == "/":
            holder = self.assembler.div(object.first, object.second, holder)

        if object.operator == "%":
            holder = self.assembler.mod(object.first, object.second, holder)

        if object.operator == "^":
            holder = self.assembler.pot(object.first, object.second, holder)

        if object.operator == "and":
            holder = self.assembler.cmpAnd(object.first, object.second, holder)

        if object.operator == "or":
            holder = self.assembler.cmpOr(object.first, object.second, holder)

        if unlock:
            unlock.unlock()

        return holder

    def toAssembly(self, object):
        if type(object) == Operation:
            object.first = self.toAssembly(object.first)
            object.second = self.toAssembly(object.second)
            
            return self.doOperation(object).register
        
        if type(object) == Element:
            return AssemblerElementContext(self.assembler).toAssembly(object)

        return 0 

class Assembler:
    variables = AssemblerVariables()
    holder = 0

    reference = 0

    @staticmethod
    def isAssigment(assigment):
        print(assigment.operator)

    @staticmethod
    def isOperation(context, object):
        if type(object) != Operation:
            return False

        return AssemblerOperationContext(context).toAssembly(object)
    
    @staticmethod
    def toAssembly(assemblerInstruction, queue):
        for object in queue:
            instructions = Mapper.map(object)

            holder = 0
            for instruction in instructions:
                flag = 0
                if holder and type(holder) == AssemblerRegisterControl:
                    if type(instruction) == Element:
                        if instruction.action == AssemblerAction.create:
                            Assembler.variables.context(assemblerInstruction).save(instruction, holder)
                            flag = True
                        if instruction.action == AssemblerAction.store:
                            pointer = Assembler.variables.context(assemblerInstruction).findPointer(instruction)
                            assemblerInstruction.store(pointer, holder).register
                            flag = True
                    
                else:
                    if type(instruction) == Element:
                        holder = AssemblerElementContext(assemblerInstruction).toAssembly(instruction)
                        flag = True
                        if type(holder) == AssemblerValueConstant:
                            holder = assemblerInstruction.mov(assemblerInstruction.register.firstAvailable(), holder).register

                    if type(instruction) == If:
                        temporary = AssemblerInstruction.temporary()
                        print(temporary.instruction)
                        temp = Assembler.toAssembly(temporary, instruction.block)
                        print(temp.instruction)
                        print(AssemblerInstruction.shared().instruction)
                        #quit()
            
                if not flag:
                    holder = Assembler.isOperation(assemblerInstruction, instruction)
                    flag = True

            if holder:
                holder.unlock()
                holder = 0
                assemblerInstruction.instruction[len(assemblerInstruction.instruction)-1] += "\n"
            
        return assemblerInstruction

    @staticmethod
    def run(queue):
        return Assembler.toAssembly(AssemblerInstruction.shared(), queue.copy().asArray())
