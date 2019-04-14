from .Lexer.ALexer import ALexer
from .Parser.AParser import AParser
from .VirtualMachine.VM import VM
import sys
import os

class ACompiler:
    @staticmethod
    def isAsm(args):
        for arg in args:
            if arg == "-asm":
                return True
        
        return False
    
    @staticmethod
    def openFile(fromPath):
        args = [fromPath[i] for i in range(0, len(fromPath))]
        if ACompiler.isAsm(args):
            args.pop(0)
            return ACompiler.openFile(args)
        
        if len(args) == 0:
            print("Error: No such file or directory")
            exit()

        if fromPath[0] == '/':
            exit()

        fromPath = args.pop(0)
        fromPath = os.getcwd() + '/' + fromPath

        fromPath = fromPath.split("/")
        file = fromPath.pop().split(".").pop(0)

        fromPath = "/".join(fromPath)

        file = open(fromPath+"/"+file+".a", "r")
        string = ""
        for line in file:
            string += line
        
        if ACompiler.isAsm(args):
            args.pop(0)
            string += ACompiler.openFile(args)
        return string

    @staticmethod
    def readFile(args):        
        args = [args[i] for i in range(0, len(args))]
        del args[0]

        if len(args) == 0:
            print('Error: arquivo não encontrado')
            exit()
        
        return ACompiler.openFile(args)


    @staticmethod
    def compile():

        VM.mount(AParser.run(ALexer.run(ACompiler.readFile(sys.argv)))).run()
        
