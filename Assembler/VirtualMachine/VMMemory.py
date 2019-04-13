from enum import Enum, unique
import traceback

@unique
class VMMemoryState(Enum):
    create = 0
    read = 1
    delete = 2

@unique
class VMMemoryRead(Enum):
    aleatory = 0
    sequencial = 1

@unique
class VMMemoryWrite(Enum):
    read_only = 0
    read_write = 1

class VMMemory:
    memory = []
    typeRead = VMMemoryRead.aleatory
    typeWrite = VMMemoryWrite.read_write

    def __init__(self):
        self.memory = []
        self.typeRead = VMMemoryRead.aleatory
        self.typeWrite = VMMemoryWrite.read_write

    def asAleatory(self):
        self.typeRead = VMMemoryRead.aleatory
        return self
    
    def asSequencial(self):
        self.typeRead = VMMemoryRead.sequencial
        return self

    def asReadWrite(self):
        if self.typeRead == VMMemoryWrite.read_only:
            print("Program is trying to unlock memory. Cleaning up everything!")
            self = VMMemory()
            return self
        self.typeWrite = VMMemoryWrite.read_write
        return self
    
    def asReadOnly(self):
        self.typeWrite = VMMemoryWrite.read_only
        return self

    @staticmethod
    def allocate(array, at, index, status):
        if status == VMMemoryState.create:
            #array.append(0)
            if at == len(array):
                array.insert(at, VMMemoryCell(0, index))
                return array[at]

            if len(array) > at:
                if array[at].index > index:
                    array.insert(at, VMMemoryCell(0, index))
                    return array[at]
                
                if array[at].index < index:
                    array.insert(at+1, VMMemoryCell(0, index))
                    return array[at+1]

                if array[at].index == index:
                    array[at] = VMMemoryCell(0, index)
                    return array[at]
            
        if status == VMMemoryState.delete:
            if len(array) > at and array[at].index == index:
                return array.pop(at)
        
        if status == VMMemoryState.read:
            if len(array) > at and array[at].index == index:
                return array[at]

        traceback.print_stack()
        print("Bad access! Trying to read a sequencial space that doesn't exist")
        quit()

    @staticmethod
    def find(array, min, max, index, status=0):
        if len(array) == 0:
            return VMMemory.allocate(array, min, index, status)

        if (max - min) == 1:
            return VMMemory.allocate(array, min, index, status)

        mid = int((max+min)/2)
        
        if array[mid].index > index:
            return VMMemory.find(array, min, mid, index, status)
        
        if array[mid].index < index:
            return VMMemory.find(array, mid, max, index, status)
        
        return VMMemory.find(array, mid, mid+1, index, status)

    def search(self, index, status):
        if index <= -1:
            traceback.print_stack()
            print("Bad access! Address " + str(index))
            quit()
            
        if self.typeRead == VMMemoryRead.sequencial:
            return VMMemory.allocate(self.memory, index, index, status)

        if len(self.memory) > index and self.memory[index].index == index:
                return VMMemory.allocate(self.memory, index, index, status)

        return VMMemory.find(self.memory, 0, len(self.memory), index, status)
            
    def store(self, index, value):
        if self.typeWrite == VMMemoryWrite.read_only:
            traceback.print_stack()
            print("Can't write in this memory. VMMemory will die!")
            quit()
            return
        
        cell = self.search(index, VMMemoryState.create)
        if not cell:
            return VMMemoryCellEmpty()
        
        cell.value = value
        return VMMemoryCellValue(cell.value)

    def read(self, index):
        cell = self.search(index, VMMemoryState.read)
        if not cell:
            return VMMemoryCellEmpty()
        
        return VMMemoryCellValue(cell.value)

    def nextIndex(self):
        return len(self.memory)
    
    def delete(self, index):
        cell = self.search(index, VMMemoryState.delete)
        if not cell:
            traceback.print_stack()
            print("Trying to delete an object that doesn't exists")
            quit()
        return cell

class VMMemoryCellEmpty:
    def __init__(self):
        return

class VMMemoryCellValue:
    value = 0
    def __init__(self, value):
        self.value = value

class VMMemoryCell:
    value = 0
    index = 0

    def __init__(self, value, index):
        self.value = value
        self.index = index