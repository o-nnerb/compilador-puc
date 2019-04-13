from .Lexer.ALexer import ALexer
from .Parser.AParser import AParser
from .VirtualMachine.VM import VM
import sys
import os

class ACompiler:
    @staticmethod
    def readFile(args):        
        args = [args[i] for i in range(0, len(args))]
        del args[0]

        if len(args) == 0:
            print('Error: arquivo não encontrado')
            exit()

        path = args.pop(0)
        if path[0] == '/':
            exit()

        path = os.getcwd() + '/' + path

        path = path.split("/")
        file = path.pop().split(".").pop(0)

        path = "/".join(path)

        file = open(path+"/"+file+".a", "r")
        string = ""
        for line in file:
            string += line
        
        return string

    @staticmethod
    def compile():
        
        VM.mount(AParser.run(ALexer.run(ACompiler.readFile(sys.argv)))).run()
        
