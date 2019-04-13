from .VMMemoryController import VMMemoryController
from .VMRegisterController import VMRegisterController
from .VMMapper import VMMapper
import sys

class VM:

    @staticmethod
    def run():
        while not VMMemoryController.shared().didEndInstructions():
            VMMemoryController.shared().nextInstruction().execute()

        print("\nProgram end with normal state")
        
        for arg in sys.argv:
            if arg == "-v":
                VMRegisterController.shared().verbose()
                VMMemoryController.shared().verbose()


    @staticmethod
    def mount(instructions):
        instructions = [VMMapper.map(instt) for instt in instructions]

        VMMemoryController.shared().saveInstructions(instructions)
        return VM