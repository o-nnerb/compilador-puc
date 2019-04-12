from enum import Enum, unique

@unique
class VMMemoryState(Enum):
    create = 0
    read = 1

class VMMemory:
    memory = []

    def __init__(self):
        return

    @staticmethod
    def allocate(array, at, index, status):
        if status == VMMemoryState.create:
            #array.append(0)
            if at == len(array):
                array.insert(at, VMMemoryCell(0, index))
                return array[at]

            if array[at].index > index:
                array.insert(at-1, VMMemoryCell(0, index))
                return array[at]
            
            if array[at].index < index:
                array.insert(at, VMMemoryCell(0, index))
                return array[at]
        
        return False

    @staticmethod
    def find(array, min, max, index, status=0):
        if len(array) == 0:
            return VMMemory.allocate(array, min, index, status)

        if len(array[min:max]) == 1:
            if array[min].index != index:
                return VMMemory.allocate(array, min, index, status)
            if status == VMMemoryState.create:
                array[min] = VMMemoryCell(0, index)            
            return array[min]

        mid = int((max+min)/2)
        
        if array[mid].index > index:
            return VMMemory.find(array, min, mid, index, status)
        
        if array[mid].index < index:
            return VMMemory.find(array, mid, max, index, status)
        
        return VMMemory.find(array, mid, mid+1, index, status)

    def search(self, index, status):
        return VMMemory.find(VMMemory.memory, 0, len(VMMemory.memory), index, status)
            
    def store(self, value, index):
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