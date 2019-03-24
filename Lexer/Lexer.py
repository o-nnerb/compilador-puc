import regex as re
import os
from .LexerEnum import LexerEnum
from .LexerToken import LexerToken
from .LexerQueue import LexerQueue

from Interpreter.Variable.VariableType import VariableType

# re.match("(?:if|else|while|func|return|for|in|var|let)", string
class LexerKeyword:
    keywords = ['if', 'else', 'while', 'func', 'return', 'for', 'var', 'let', 'break']
    @staticmethod
    def isKeyword(string):
        for keyword in LexerKeyword.keywords:
            if keyword == string:
                return True
                
        return False

class Lexer:
    file = 0
    output = 0
    write_out = False
    line = ""

    def __init__(self, fileURL, args):
        self.file = open(fileURL, "r")
        for arg in args:
            if arg == "-lx":
                self.write_out = True
                path = fileURL.split('.')
                path.pop()
                path = '.'.join(path) + '.lx'
                self.output = open(path, "w")

        if self.file == False or (self.write_out == True and self.output == False):
            print("Error: can't open file at \""+fileURL+"\"")
            exit()

    @staticmethod
    def isId(imin, line):
        i = imin
        while i < len(line):
            if bool(re.match("[a-zA-Z]", line[i])) == False:
                if i == imin or bool(re.match("[0-9]", line[i])) == False:
                    return (i - 1, LexerEnum.id)
            i += 1

        return (i - 1, LexerEnum.id)

    @staticmethod
    def isNum(imin, line):
        i = imin
        isFloat = False
        while i < len(line):
            if bool(re.match("[0-9]", line[i])) == False:
                if (i+1)==len(line) or line[i] != "." or bool(re.match("[0-9]",line[i+1])) == False:
                    if isFloat:
                        return (i-1, LexerEnum.float)
                    return (i-1, LexerEnum.integer)

                isFloat |= line[i] == "."
            i += 1
        
        if isFloat:
            return (i-1, LexerEnum.float)
        return (i-1, LexerEnum.integer)

    @staticmethod
    def isNeg(imin, line):
        if line[imin] != "!":
            return (imin-1, False)
            
        if line[imin+1] != "=":
            return (imin, LexerEnum.operator_prefix)

        return (imin+1, LexerEnum.logical)

    @staticmethod
    def isEqual(imin, line):
        if line[imin] != "=":
            return (imin-1, False)
            
        if line[imin+1] != "=":
            return (imin, LexerEnum.assigment)

        return (imin+1, LexerEnum.logical)

    @staticmethod
    def isGreater(imin, line):
        if line[imin] != ">":
            return (imin - 1, False)
        
        if line[imin+1] == "=":
            return (imin+1, LexerEnum.logical)
        
        if line[imin+1] == ".":
            if line[imin+2] == ".":
                return (imin+2, LexerEnum.operator_range)

        return (imin, LexerEnum.logical)

    @staticmethod 
    def isLess(imin, line):
        if line[imin] != "<":
            return (imin - 1, False)
        
        if line[imin+1] != "=":
            return (imin, LexerEnum.logical)

        return (imin+1, LexerEnum.logical)

    @staticmethod
    def isOperator(imin, line):
        if bool(re.match("(?:\+|\*|\%|\-|\/|\^)", line[imin])) == False:
            return (imin-1, False)

        return (imin, LexerEnum.operator)
    
    @staticmethod
    def isDelimitador(imin, line):
        if line[imin] == ".":
            if line[imin+1] == ".":
                if line[imin+2] == "<" or line[imin+2] == ".":
                    return (imin+2, LexerEnum.operator_range)

        if bool(re.match("(?:\(|\)|\;|\:|\,|\.|\{|\})", line[imin])) == False:
            return (imin-1, False)

        return (imin, LexerEnum.delimiter)

    @staticmethod
    def isKeyword(string):
        #string = string.lower()

        if bool(re.match("(?:true|false)", string)) == True:
            return (True, LexerEnum.boolean)

        if string == "not":
            return (True, LexerEnum.operator_prefix)
        
        if string == "or" or string == "and":
            return (True, LexerEnum.logical_operator)

        if VariableType.isPrimitive(string):
            return (True, LexerEnum.primitive)
        
        if string == "in":
            return (True, LexerEnum.operator_in)

        if not LexerKeyword.isKeyword(string):
            return (False, False)

        return (True, LexerEnum.keyword)

    @staticmethod
    def parseLine(imin, line):
        (imax, context) = Lexer.isId(imin, line)
        if imax >= imin:
            (isKeyword, keyContext) = Lexer.isKeyword(line[imin:imax+1])
            if isKeyword:
                return (imax, keyContext)
            return (imax, context)
        
        functions = [Lexer.isNum, Lexer.isNeg, Lexer.isEqual, Lexer.isGreater, Lexer.isLess, Lexer.isOperator, Lexer.isDelimitador]

        for func in functions:
            (imax, context) = func(imin, line)
            if imax >= imin:
                return (imax, context)

        return (imin-1, False)

    def parse(self):
        iline = 0
        queue = LexerQueue.shared()
        lineHasInstruction = False
        for line in self.file:
            iline += 1
            imin = 0
            lineHasInstruction = False
            while imin < len(line):
                (imax, token) = Lexer.parseLine(imin, line)
                if imax < imin:
                    if line[imin] != '\t' and line[imin] != '\n' and line[imin] != ' ' and line[imin] != '\r':
                        # Save line and imin
                        queue.insert(LexerToken(LexerEnum.lexer_error, line[imin]))
                        #if self.write_output:
                        print('Error: compiler couldn\'t compreend this caracter (' + str(line[imin]) + ') on line ' + str(iline))
                        print(line)
                    imin += 1
                else:
                    value = line[imin:imax+1]
                    object = LexerToken(token, value)
                    queue.insert(object)

                    if self.write_out:
                        self.output.write(token.value+'{'+value+'}')
                    
                    imin = imax+1
                    lineHasInstruction = True
            
            if lineHasInstruction and bool(re.match("(?:\;)", queue.lastElement().getValue())) == False:
                object = LexerToken(LexerEnum.endline, "end")
                queue.insert(object)
                if self.write_out:
                    self.output.write(object.getToken().value + "{"+object.getValue()+"}")

            if self.write_out:
                self.output.write('\n')

        return

    @staticmethod
    def run(args):
        del args[0]

        if len(args) == 0:
            print('Error: arquivo não encontrado')
            exit()
        
        path = args.pop(0)
        if path[0] == '/':
            return Lexer(path, args).parse()
            exit()

        path = os.getcwd() + '/' + path
        return Lexer(path, args).parse()