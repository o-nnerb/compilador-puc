from .Lexer.ALexer import ALexer
from .Parser.AParser import AParser
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
            print(path)
            exit()

        path = os.getcwd() + '/' + path
        print(path)

        path = path.split("/")
        file = path.pop().split(".").pop(0)

        path = "/".join(path)
        print(path)
        print(file)

        file = open(path+"/"+file+".a", "r")
        string = ""
        for line in file:
            string += line
        
        return string

    @staticmethod
    def compile():
        
        print(AParser.run(ALexer.run(ACompiler.readFile(sys.argv))))
