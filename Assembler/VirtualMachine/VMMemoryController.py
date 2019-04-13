from .VMMemory import VMMemory, VMMemoryCellValue, VMMemoryCellEmpty
from enum import Enum, unique
import traceback

@unique
class VMMemoryArea(Enum):
    instruction = 0
    data = 1
    stack = 2

class VMMemoryContext(VMMemory):
    area = 0
    def __init__(self, area):
        super(VMMemoryContext, self).__init__()

        self.area = area
        if area == VMMemoryArea.instruction:
            self.asSequencial()
            self.asReadWrite()
            return
        
        if area == VMMemoryArea.data:
            self.asAleatory()
            self.asReadWrite()
            return
        
        if area == VMMemoryArea.stack:
            self.asAleatory()
            self.asReadWrite()
            return

class VMMemoryController:
    instruction = VMMemoryContext(VMMemoryArea.instruction)
    data = VMMemoryContext(VMMemoryArea.data)
    stack = VMMemoryContext(VMMemoryArea.stack)

    programCounter = 0

    def __init__(self):
        self.instruction = VMMemoryContext(VMMemoryArea.instruction)
        self.data = VMMemoryContext(VMMemoryArea.data)
        self.stack = VMMemoryContext(VMMemoryArea.stack)
    
    def saveInstructions(self, instructions):
        for i in range(0, len(instructions)):
            self.instruction.store(i, instructions[i])
        
        self.instruction.asReadOnly()
    
    def nextInstruction(self):
        inst = self.instruction.read(self.programCounter)
        if type(inst) == VMMemoryCellEmpty:
            traceback.print_stack()
            print("Program ended!")
            quit()
        
        self.programCounter += 1
        return inst.value
    
    def didEndInstructions(self):
        return self.programCounter >= self.instruction.nextIndex()
    
    def movePC(self, pointer):
        if pointer >= self.instruction.nextIndex() or pointer < 0:
            traceback.print_stack()
            print("Bad access! Can't move to instruction at " + str(pointer))
            quit()
        
        self.programCounter = pointer

    def push(self, value):
        self.stack.store(value, self.stack.nextIndex())

    def pop(self):
        poped = self.stack.delete(self.stack.nextIndex()-1)
        if type(poped) == VMMemoryCellEmpty:
            traceback.print_stack()
            print("Can't create memory cell for " + str(data))
            quit()
        return poped.value

    def store(self, index, data):
        data = self.data.store(index, data)
        if type(data) == VMMemoryCellEmpty:
            traceback.print_stack()
            print("Can't create memory cell for " + str(data))
            quit()
        
    def read(self, index):
        data = self.data.read(index)
        if type(data) == VMMemoryCellEmpty:
            traceback.print_stack()
            print("Can't create memory cell for " + str(data))
            quit()

        return data.value

    __shared = 0
    @staticmethod
    def shared():
        if not VMMemoryController.__shared:
            VMMemoryController.__shared = VMMemoryController()
            
        return VMMemoryController.__shared

    def verbose(self):
        print("Instructions Memory")
        for reg in self.instruction.memory:
            print(reg.index, reg.value.code)

        print("\nData Memory")
        if len(self.data.memory) == 0:
            print("Empty")
        else:
            for reg in self.data.memory:
                print(reg.index, reg.value)

        print("\nStack Memory")
        if len(self.stack.memory) == 0:
            print("Empty")
        else:
            for reg in self.stack.memory:
                print(reg.index, reg.value)
        print()