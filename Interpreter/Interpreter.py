from .Element import Element, Runnable
from Interpreter.Variable.Variable import Variable, VariableType
from Lexer.LexerEnum import LexerEnum
from Lexer.LexerQueue import LexerQueue

from .InterpreterMap import map

class InterpreterStack:
    value = 0
    def __init__(self, value):
        if type(value) == InterpreterStack:
            self.value = value.value
            return

        self.value = value

class InterpreterUnstack:
    def __init(self):
        return

class InterpreterOperator:
    value = 0
    def __init__(self, value):
        self.value = value

class InterpreterId:
    value = 0
    def __init__(self, value):
        self.value = value
    
class InterpreterEmpty:
    def __init(self):
        return

class Interpreter:
    runnable = 0

    def __init__(self, value):
        if type(value) == Runnable:
            self.runnable = value
            return

        if type(value) == InterpreterEmpty:
            self.runnable = Runnable()
        
    @staticmethod
    def merge(left, right):
        #print("left ", end="")
        #print(left)
        #print("right ", end="")
        #print(right)
        if type(right) == InterpreterEmpty:
            return left
        
        if type(left) == InterpreterOperator:
            if type(right) == InterpreterId:
                return InterpreterOperator(Runnable.element(Element.both(0, left.value, Runnable.element(Element.single(right.value)))))
            
            if type(right) == Runnable:
                return InterpreterOperator(Runnable.element(Element.both(0, left.value, right)))
            
            if type(right) == InterpreterStack:
                return Interpreter.merge(left, right.value)
        
        if type(left) == InterpreterId:
            if type(right) == InterpreterOperator:
                right.value.getElement().setLeft(Runnable.element(Element.single(left.value)))
                return right.value
            
            if  type(right) == InterpreterUnstack:
                return left
        
        if type(left) == Runnable:
            if type(right) == InterpreterOperator:
                right.value.getElement().setLeft(left)
                return right.value
            
            if  type(right) == InterpreterUnstack:
                return left

        if type(left) == InterpreterStack:
            return Interpreter.merge(left.value, right)

    @staticmethod
    def operator(queue):
        if queue.isEmpty():
            return InterpreterEmpty()
            
        object = queue.getHead()
        queue.toRight()

        if compareToken(object, LexerEnum.endline) or object.getValue() == ';':
            return InterpreterEmpty()

        if object.getValue() == ')':
            return InterpreterUnstack()

        return Interpreter.merge(InterpreterOperator(object), Interpreter.first(queue))

    @staticmethod
    def first(queue):
        if queue.isEmpty():
            return InterpreterEmpty()

        object = queue.getHead()
        queue.toRight()

        map(object)

        #if compareToken(object, LexerEnum.endline) or object.getValue() == ';':
        #    return InterpreterEmpty()

        #if object.getValue() == '(':
        #    return Interpreter.merge(InterpreterStack(Interpreter.first(queue)), Interpreter.operator(queue))

        #if object.getValue() == ')':
        #    return InterpreterUnstack()

        #if compareToken(object, [LexerEnum.id, LexerEnum.integer, LexerEnum.float, LexerEnum.boolean]):
        #    return Interpreter.merge(InterpreterId(object), Interpreter.operator(queue))

        # keyword
        #return Runnable()

    @staticmethod
    def mount(queue):
        if queue.isEmpty():
            return Interpreter()

        return Interpreter(Interpreter.first(queue)) #Empty

    def execute(self):
        if not self.runnable:
            return
        
        self.runnable.run()
        return

    @staticmethod
    def run(queue):
        queue = queue.copy()
        queue.needsPersist(True)
        queue.toFirst()

        while not queue.isEmpty():
            Interpreter.mount(queue).execute()
            #queue.verbose(showContent=False)
            

def compareToken(object, values):
    return LexerEnum.compare(object, values)