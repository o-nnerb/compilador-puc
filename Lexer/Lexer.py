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
    def charAt(index):
        if len(Lexer.line) <= index:
            return ""
        
        return Lexer.line[index]
    
    @staticmethod
    def charRange(fromIndex, toIndex):
        if fromIndex == toIndex:
            return ""

        if len(Lexer.line) <= fromIndex:
            return ""
        
        return Lexer.charAt(fromIndex) + Lexer.charRange(fromIndex+1, toIndex)

    @staticmethod
    def isId(imin):
        i = imin
        while i < len(Lexer.line):
            if bool(re.match("[a-zA-Z]", Lexer.charAt(i))) == False:
                if i == imin or bool(re.match("[0-9]", Lexer.charAt(i))) == False:
                    return (i - 1, LexerEnum.id)
            i += 1

        return (i - 1, LexerEnum.id)

    @staticmethod
    def isNum(imin):
        i = imin
        isFloat = False
        while i < len(Lexer.line):
            if bool(re.match("[0-9]", Lexer.charAt(i))) == False:
                if (i+1)==len(Lexer.line) or Lexer.charAt(i) != "." or bool(re.match("[0-9]", Lexer.charAt(i+1))) == False:
                    if isFloat:
                        return (i-1, LexerEnum.float)
                    return (i-1, LexerEnum.integer)

                isFloat |= Lexer.charAt(i) == "."
            i += 1
        
        if isFloat:
            return (i-1, LexerEnum.float)
        return (i-1, LexerEnum.integer)

    @staticmethod
    def isNeg(imin):
        if Lexer.charAt(imin) != "!":
            return (imin-1, False)
            
        if Lexer.charAt(imin+1) != "=":
            return (imin, LexerEnum.operator_pfix)

        return (imin+1, LexerEnum.logical)

    @staticmethod
    def isEqual(imin):
        if Lexer.charAt(imin) != "=":
            return (imin-1, False)
            
        if Lexer.charAt(imin+1) != "=":
            return (imin, LexerEnum.assigment)

        return (imin+1, LexerEnum.logical)

    @staticmethod
    def isGreater(imin):
        if Lexer.charAt(imin) != ">":
            return (imin - 1, False)
        
        if Lexer.charAt(imin+1) == "=":
            return (imin+1, LexerEnum.logical)
        
        if Lexer.charAt(imin+1) == ".":
            if Lexer.charAt(imin+2) == ".":
                return (imin+2, LexerEnum.operator_range)

        return (imin, LexerEnum.logical)

    @staticmethod 
    def isLess(imin):
        if Lexer.charAt(imin) != "<":
            return (imin - 1, False)
        
        if Lexer.charAt(imin+1) != "=":
            return (imin, LexerEnum.logical)

        return (imin+1, LexerEnum.logical)

    @staticmethod
    def isOperator(imin):
        if Lexer.charAt(imin) == "+":
            if Lexer.charAt(imin+1) == "+":
                return (imin+1, LexerEnum.operator_pfix)
            return (imin, LexerEnum.operator)

        if Lexer.charAt(imin) == "-":
            if Lexer.charAt(imin+1) == "-":
                return (imin+1, LexerEnum.operator_pfix)
            if Lexer.charAt(imin+1) == ">":
                return (imin+1, LexerEnum.operator_return)
            return (imin, LexerEnum.operator)
        
        if Lexer.charAt(imin) == "*":
            if Lexer.charAt(imin+1) == "/":
                return (imin+1, LexerEnum.comment_multiple)
            return (imin, LexerEnum.operator)
        
        if Lexer.charAt(imin) == "/":
            if Lexer.charAt(imin+1) == "/":
                return (imin+1, LexerEnum.comment_line)
            if Lexer.charAt(imin+1) == "*":
                return (imin+1, LexerEnum.comment_multiple)
            return (imin, LexerEnum.operator)

        if bool(re.match("(?:\%|\^)", Lexer.charAt(imin))) == False:
            return (imin-1, False)

        return (imin, LexerEnum.operator)
    
    @staticmethod
    def isDelimitador(imin):
        if Lexer.charAt(imin) == ".":
            if Lexer.charAt(imin+1) == ".":
                if Lexer.charAt(imin+2) == "<" or Lexer.charAt(imin+2) == ".":
                    return (imin+2, LexerEnum.operator_range)

        if bool(re.match("(?:\(|\)|\;|\:|\,|\.|\{|\})", Lexer.charAt(imin))) == False:
            return (imin-1, False)

        return (imin, LexerEnum.delimiter)
    
    @staticmethod
    def isKeyword(string):
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
    def findLimit(imin):
        countP = 1

        while Lexer.charAt(imin) != "":
            if Lexer.charAt(imin) == "(":
                countP = countP + 1
            elif Lexer.charAt(imin) == ")":
                countP = countP - 1
            
            if not countP:
                break

            imin += 1

        return imin

    @staticmethod
    def isString(imin, forced=False, asp=0):
        oimin = imin
        if not forced and Lexer.charAt(imin) != "\"" and Lexer.charAt(imin) != "\'":
            return imin-1

        if not forced:
            asp = Lexer.charAt(imin)

        if forced:
            if Lexer.charAt(imin) == asp:
                return imin
            if Lexer.charAt(imin) == "\\":
                if Lexer.charAt(imin+1) == "(":
                    return imin+1

        imin += 1
        while Lexer.charAt(imin) != "":
            if Lexer.charAt(imin) == "\\":
                if Lexer.charAt(imin+1) == "(":
                    return imin+1
                
            if Lexer.charAt(imin) == asp:
                break
            
            imin += 1
        
        if Lexer.charAt(imin) == "":
            return oimin-1

        return imin

    @staticmethod
    def append(string, asp):
        if len(string) == 0:
            string = "\"\""
            
        if string[0] != asp:
            string = asp + string
        
        if string[len(string)-1] != asp:
            string += asp

        if len(string) == 1:
            string += asp
            
        LexerQueue.shared().insert(LexerToken(LexerEnum.string, string))
    
    @staticmethod
    def createAppend():
        LexerQueue.shared().insert(LexerToken(LexerEnum.string_append, "\("))
    
    @staticmethod
    def createAppendE():
        LexerQueue.shared().insert(LexerToken(LexerEnum.string_append_e, ")"))

    @staticmethod
    def mayBeAppend(imin, imax, asp, oimin):
        if imax >= imin:
            if Lexer.charAt(imax) == "(" and Lexer.charAt(imax-1) == "\\":
                ibound = Lexer.findLimit(imax+1)
                if Lexer.charAt(ibound) == ")":
                    Lexer.append(Lexer.charRange(imin, imax-1), asp)
                    Lexer.createAppend()

                    toParse = Lexer.charRange(imax+1, ibound)

                    if len(toParse) > 0:
                        Lexer.processLine(toParse, True)

                    Lexer.createAppendE()

                    iafter = Lexer.isString(ibound+1, True, asp)

                    return Lexer.mayBeAppend(ibound+1, iafter, asp, oimin)

            else:
                string = Lexer.charRange(imin, imax+1)
                Lexer.append(string, asp)
                return (imax, LexerEnum.string)

        return (oimin-1, False)

    @staticmethod
    def canBeString(imin):
        imax = Lexer.isString(imin)
        return Lexer.mayBeAppend(imin, imax, Lexer.charAt(imin), imin)

    @staticmethod
    def parseLine(imin):
        (imax, context) = Lexer.isId(imin)
        if imax >= imin:
            (isKeyword, keyContext) = Lexer.isKeyword(Lexer.charRange(imin, imax+1))
            if isKeyword:
                return (imax, keyContext)
            return (imax, context)
        
        functions = [Lexer.isNum, Lexer.isNeg, Lexer.isEqual, Lexer.isGreater, Lexer.isLess, Lexer.isOperator, Lexer.isDelimitador, Lexer.canBeString]
        
        for func in functions:
            (imax, context) = func(imin)
            if imax >= imin:
                return (imax, context)

        return (imin-1, False)

    @staticmethod
    def parserFrom(imin):
        queue = LexerQueue.shared()

        (imax, token) = Lexer.parseLine(imin)
        #print(token)
        
        if imax < imin:
            if Lexer.charAt(imin) != '\t' and Lexer.charAt(imin) != '\n' and Lexer.charAt(imin) != ' ' and Lexer.charAt(imin) != '\r':
                # Save line and imin
                #queue.insert(LexerToken(LexerEnum.lexer_error, Lexer.charAt(imin)))
                #if self.write_output:
                if not queue.isLock():
                    print('Error: compiler couldn\'t compreend this caracter (' + str(Lexer.charAt(imin)) + ') on line ' + str(0))
            imin += 1
            return (True, imin)
        else:
            if token and token != LexerEnum.string:
                value = Lexer.charRange(imin, imax+1)
                object = LexerToken(token, value)
                queue.insert(object)
            
            imin = imax+1
            return (True, imin)

    @staticmethod
    def processLine(line, forced=False):
        if forced:
            oldLine = Lexer.line
        
        Lexer.line = line
        imin = 0

        lineHasInstruction = False
        
        while imin < len(Lexer.line):
            (lineHasInstruction, imin) = Lexer.parserFrom(imin)
            Lexer.line = line

        if not forced and (Lexer.charAt(imin) != '\n' or lineHasInstruction and LexerQueue.shared().lastElement() and bool(re.match("(?:\;)", LexerQueue.shared().lastElement().getValue())) == False):
            object = LexerToken.endline()
            LexerQueue.shared().insert(object)
        
        if forced:
            Lexer.line = oldLine
    
    def parse(self):
        queue = LexerQueue.shared()
        lineHasInstruction = False
        for line in self.file:
            Lexer.processLine(line)

        if self.write_out:
            queue.write_out(self.toOutput)
        return

    def toOutput(self, object):
        self.output.write(object.getToken().value + "{"+object.getValue()+"}")

    @staticmethod
    def run(args):
        args = [args[i] for i in range(0, len(args))]
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