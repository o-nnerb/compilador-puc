from Assembler.Parser.AParser import AParserOperation, AParserJump, AParserJumpCMP, AParserMov, AParserStore, AParserLoad, AParserPop, AParserPush, AParserEmpty
from .VMExtensions import VMOperation, VMJump, VMJumpCMP, VMJumpCMP, VMMov, VMStore, VMLoad, VMPush, VMPop, VMEmpty
from Assembler.Assembler import AssemblerRegister, AssemblerValueConstant
from .VMRegisterController import VMRegisterController

class VMMapper:

    @staticmethod
    def toVMObject(object):
        if type(object) == AssemblerValueConstant:
            return int(object.value)
        
        if type(object) == AssemblerRegister:
            return VMRegisterController.shared().getRegister(object)
        
        print("Error at Mapper VM with " + str(object))
        quit()

    @staticmethod
    def asOperation(object):
        object.first = VMMapper.toVMObject(object.first)
        object.second = VMMapper.toVMObject(object.second)
        object.third = VMMapper.toVMObject(object.third)
        return VMOperation.fromSuper(object)

    @staticmethod
    def asJump(object):
        object.first = VMMapper.toVMObject(object.first)
        return VMJump.fromSuper(object)
        
    @staticmethod
    def asJumpCMP(object):
        object.first = VMMapper.toVMObject(object.first)
        object.second = VMMapper.toVMObject(object.second)
        object.third = VMMapper.toVMObject(object.third)
        return VMJumpCMP.fromSuper(object)

    @staticmethod
    def asMov(object):
        object.first = VMMapper.toVMObject(object.first)
        object.second = VMMapper.toVMObject(object.second)
        return VMMov.fromSuper(object)

    @staticmethod
    def asStore(object):
        object.first = VMMapper.toVMObject(object.first)
        object.second = VMMapper.toVMObject(object.second)
        return VMStore.fromSuper(object)

    @staticmethod
    def asLoad(object):
        object.first = VMMapper.toVMObject(object.first)
        object.second = VMMapper.toVMObject(object.second)
        return VMLoad.fromSuper(object)

    @staticmethod
    def asPop(object):
        object.first = VMMapper.toVMObject(object.first)
        return VMPop.fromSuper(object)

    @staticmethod
    def asPush(object):
        object.first = VMMapper.toVMObject(object.first)
        return VMPush.fromSuper(object)

    @staticmethod
    def asEmpty(object):
        return VMEmpty.fromSuper(object)        

    @staticmethod
    def map(object):
        if type(object) == AParserOperation:
            return VMMapper.asOperation(object)

        if type(object) == AParserJump:
            return VMMapper.asJump(object)

        if type(object) == AParserJumpCMP:
            return VMMapper.asJumpCMP(object)

        if type(object) == AParserMov:
            return VMMapper.asMov(object)

        if type(object) == AParserStore:
            return VMMapper.asStore(object)

        if type(object) == AParserLoad:
            return VMMapper.asLoad(object)

        if type(object) == AParserPop:
            return VMMapper.asPop(object)

        if type(object) == AParserPush:
            return VMMapper.asPush(object)

        if type(object) == AParserEmpty:
            return VMMapper.asEmpty(object)
