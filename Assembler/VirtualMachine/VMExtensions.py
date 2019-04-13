from Assembler.Parser.AParser import AParserOperation, AParserJump, AParserJumpCMP, AParserMov, AParserStore, AParserLoad, AParserPop, AParserPush
from .VMMemoryController import VMMemoryController
from .VMRegisterController import VMRegisterControl

class VMOperation(AParserOperation):
    # code = 0
    # first = 0
    # second = 0
    # third = 0

    @staticmethod
    def fromSuper(sup):
        return VMOperation(sup.code, sup.first, sup.second, sup.third)
    
    @staticmethod
    def asValue(object):
        if type(object) == VMRegisterControl:
            return object.value
        
        return object

    def execute(self):
        if self.code == "add":
            self.first.value = VMOperation.asValue(self.second) + VMOperation.asValue(self.third)
            return
        
        if self.code == "sub":
            self.first.value = VMOperation.asValue(self.second) - VMOperation.asValue(self.third)
            return
        
        if self.code == "mul":
            self.first.value = VMOperation.asValue(self.second) * VMOperation.asValue(self.third)
            return
        
        if self.code == "pot":
            self.first.value = VMOperation.asValue(self.second) ** VMOperation.asValue(self.third)
            return
        
        if self.code == "div":
            vt = VMOperation.asValue(self.third)
            if vt == 0:
                print("VM Aritmetic Error: dividindo por 0")
                quit()
            self.first.value = VMOperation.asValue(self.second) / vt
            return
        
        if self.code == "mod":
            vt = VMOperation.asValue(self.third)
            if vt == 0:
                print("VM Aritmetic Error: resto por 0")
                quit()
            self.first.value = VMOperation.asValue(self.second) % vt
            return
        
        if self.code == "and":
            self.first.value = VMOperation.asValue(self.second) and VMOperation.asValue(self.third)
            return
        
        if self.code == "or":
            self.first.value = VMOperation.asValue(self.second) or VMOperation.asValue(self.third)
            return

        print("Execute Operation Error: type " + str(self.code))
        quit()

class VMJump(AParserJump):
    # code = 0
    # first = 0

    @staticmethod
    def fromSuper(sup):
        return VMJump(sup.code, sup.first)

    def execute(self):
        VMMemoryController.shared().movePC(self.first)

class VMJumpCMP(AParserJumpCMP):
    # code = 0
    # first = 0
    # second = 0
    # third = 0

    @staticmethod
    def fromSuper(sup):
        return VMJumpCMP(sup.code, sup.first, sup.second, sup.third)
        
    @staticmethod
    def asValue(object):
        if type(object) == VMRegisterControl:
            return object.value
        
        return object

    def execute(self):
        shouldJump = False
        
        if self.code == "beq":
            shouldJump = VMOperation.asValue(self.first) == VMOperation.asValue(self.second)
        
        elif self.code == "bne":
            shouldJump = VMOperation.asValue(self.first) != VMOperation.asValue(self.second)
        
        elif self.code == "blt":
            shouldJump = VMOperation.asValue(self.first) < VMOperation.asValue(self.second)
        
        elif self.code == "ble":
            shouldJump = VMOperation.asValue(self.first) <= VMOperation.asValue(self.second)
        
        elif self.code == "bgt":
            shouldJump = VMOperation.asValue(self.first) > VMOperation.asValue(self.second)
        
        elif self.code == "bge":
            shouldJump = VMOperation.asValue(self.first) >= VMOperation.asValue(self.second)

        if shouldJump:
            VMMemoryController.shared().movePC(self.third)

class VMMov(AParserMov):
    # code = 0
    # first = 0
    # second = 0

    @staticmethod
    def fromSuper(sup):
        return VMMov(sup.code, sup.first, sup.second)

    def execute(self):
        if type(self.second) == VMRegisterControl:
            self.first.value = self.second.value
            return
        
        self.first.value = self.second

class VMStore(AParserStore):
    # code = 0
    # first = 0
    # second = 0

    @staticmethod
    def fromSuper(sup):
        return VMStore(sup.code, sup.first, sup.second)

    def execute(self):
        VMMemoryController.shared().store(self.first, self.second.value)     

class VMLoad(AParserLoad):
    # code = 0
    # first = 0 always register
    # second = 0 always memory

    @staticmethod
    def fromSuper(sup):
        return VMLoad(sup.code, sup.first, sup.second)

    def execute(self):
        self.first.value = VMMemoryController.shared().read(self.second)

class VMPush(AParserPush):
    # code = 0
    # first = 0

    @staticmethod
    def fromSuper(sup):
        return VMPush(sup.code, sup.first, sup.second)

    def execute(self):
        VMMemoryController.shared().push(self.first.value)

class VMPop(AParserPop):
    # code = 0
    # first = 0

    @staticmethod
    def fromSuper(sup):
        return VMPop(sup.code, sup.first, sup.second)

    def execute(self):
        self.first.value = VMMemoryController.shared().pop()
