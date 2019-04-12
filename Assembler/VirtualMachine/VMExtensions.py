from .Parser.AParser import AParserOperation, AParserJumpcccc, AParserJumpCMP, AParserMov AParserStore, AParserLoad

class VMOperation(AParserOperation):
    # code = 0
    # first = 0
    # second = 0
    # third = 0
    registers = 0

    @staticmethod
    def fromSuper(sup):
        return VMOperation(sup.code, sup.first, sup.second, sup.third)

    def setRegisters(self, registers):
        self.registers = registers
        return self
    
    def execute(self):
        print("Execute Operation")
        self.registers = 0

        quit()

class VMJump(AParserJump):
    # code = 0
    # first = 0
    instructions = 0

    @staticmethod
    def fromSuper(sup):
        return VMJump(sup.code, sup.first)
    
    def setInstructions(self, instructions):
        self.instructions = instructions
        return

    def execute(self):
        print("Execute Jump")
        self.instructions = 0

        quit()

class VMJumpCMP(AParserJumpCMP):
    # code = 0
    # first = 0
    # second = 0
    # third = 0
    registers = 0

    @staticmethod
    def fromSuper(sup):
        return VMJumpCMP(sup.code, sup.first, sup.second, sup.third)
    
    def setRegisters(self, registers):
        self.registers = registers
        return

    def execute(self):
        print("Execute JumpCMP")
        self.registers = 0

        quit()

class VMMov(AParserMov):
    # code = 0
    # first = 0
    # second = 0
    registers = 0
    memory = 0

    @staticmethod
    def fromSuper(sup):
        return VMMov(sup.code, sup.first, sup.second)
    
    def setRegisters(self, registers):
        self.registers = registers
        return
    
    def setMemory(self, memory):
        self.memory = memory
        return self

    def execute(self):
        print("Execute Mov")
        self.registers = 0
        self.memory = 0

        quit()

class VMStore(AParserStore):
    # code = 0
    # first = 0
    # second = 0
    registers = 0
    memory = 0

    @staticmethod
    def fromSuper(sup):
        return VMStore(sup.code, sup.first, sup.second)
    
    def setRegisters(self, registers):
        self.registers = registers
        return
    
    def setMemory(self, memory):
        self.memory = memory
        return self

    def execute(self):
        print("Execute Store")
        self.registers = 0
        self.memory = 0
        
        quit()

class VMLoad(AParserLoad):
    # code = 0
    # first = 0
    # second = 0
    registers = 0
    memory = 0

    @staticmethod
    def fromSuper(sup):
        return VMStore(sup.code, sup.first, sup.second)
    
    def setRegisters(self, registers):
        self.registers = registers
        return
    
    def setMemory(self, memory):
        self.memory = memory
        return self

    def execute(self):
        print("Execute Load")
        self.registers = 0
        self.memory = 0
        
        quit()