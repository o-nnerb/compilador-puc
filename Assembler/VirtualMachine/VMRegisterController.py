from Assembler.Assembler import AssemblerRegister, AssemblerRegisterControl, AssemblerRegisters

class VMRegisterControl(AssemblerRegisterControl):
    #register = 0
    #isEnable = True
    value = 0
    
    def __init__(self, register, value):
        self.register = register
        self.value = value

class VMRegisterController(AssemblerRegisters):
    __shared = 0

    def __init__(self):
        self.allRegisters = [
            VMRegisterControl(AssemblerRegister.r1, 0),
            VMRegisterControl(AssemblerRegister.r2, 0),
            VMRegisterControl(AssemblerRegister.r3, 0),
            VMRegisterControl(AssemblerRegister.r4, 0),
            VMRegisterControl(AssemblerRegister.r5, 0),
            VMRegisterControl(AssemblerRegister.r6, 0),
            VMRegisterControl(AssemblerRegister.r7, 0),
            VMRegisterControl(AssemblerRegister.r8, 0),
        ]

    #def getRegister(self, register):
    #    for _register in self.allRegisters:
    #        if _register.register == register:
    #            return _register

    #    return False

    @staticmethod
    def shared():
        if not VMRegisterController.__shared:
            VMRegisterController.__shared = VMRegisterController()
        
        return VMRegisterController.__shared

    def verbose(self):
        print("\nRegister Table\n")
        for reg in self.allRegisters:
            print(reg.name(), reg.value)
        print()

        