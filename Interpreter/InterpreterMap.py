from Parser.Parser import ParserBreak, ParserFunction, ParserFunctionVariable, ParserFor, ParserForInRange, VariableDeclarationCast, ParserWhile, ParserIf, ParserStringBlock, ParserStringQueue, ParserOperationAssigment, ParserVariableType, ParserDeclarationVariable, ParserVariable, ParserOperation, ParserFunction, ParserIf, ParserEmpty
from Interpreter.Variable.Variable import VariableType, Variable, VariableConstantType
from Lexer.LexerHash import LexerHash
import sys
import readline

def executeOperation(operation):
    if type(operation) == ParserOperation:
        if type(operation.second) == ParserOperation:
            operation.second = executeOperation(operation.second)
            operation.first = executeOperation(operation.first)
            return Variable.withOperator(operation.operator.getValue(), operation.first, operation.second)

        if type(operation.second) == ParserVariable:
            second = executeOperation(operation.second)
            first = executeOperation(operation.first)
            
            print(operation.operator.getValue(), first)
            return Variable.withOperator(operation.operator.getValue(), first, second)

    elif type(operation) == ParserVariable:
        if operation.isStoreVariable():
            variable = LexerHash.shared().getObject(operation.getValue())
            if not variable:
                print("Error: referenciando a uma varíavel não existente")
                quit()
            return variable
        else:
            return Variable("ans", operation.getValue(), VariableType.cast(operation.getToken()), VariableConstantType.var)

def processBlock(queue):
    arrayVar = []
    def nVar(variable):
        print("appending")
        arrayVar.append(variable)

    if not queue:
        return

    while not queue.isEmpty():
        head = queue.getHead()
        if not head:
            break
        if type(head) == ParserBreak:
            break
        map(head, __newVariable=nVar)
        queue.toRight()

    for var in arrayVar:
        LexerHash.shared().remove(var.name)

def processIfBlock(parserObject):
    queue = parserObject.block
    variable = Variable("ans", executeOperation(parserObject.value).value, VariableType.boolean, VariableConstantType.let)
    variable.toBoolean()
    if variable.value:
        processBlock(queue)
        parserObject.block.toFirst()
    elif parserObject.elseBlock:
        print(parserObject.elseBlock)
        if parserObject.elseBlock.ifBlock:
            processIfBlock(parserObject.elseBlock.ifBlock)
        else:
            processBlock(parserObject.elseBlock.block)

def processForRange(range, block):
    variable = executeOperation(range.variable)
    fromV = executeOperation(range.range.first)
    toV = executeOperation(range.range.last)
    operator = range.range.operator.operator.getValue()
    variable.assigment(fromV)
    
    def increaseTilTop():
        if variable.value < toV.value:
            processBlock(block)
            block.toFirst()
            toAss = variable.copy()
            toAss.value += 1
            variable.assigment(toAss)
            increaseTilTop()
    
    def decreaseTilFloor():
        if variable.value > toV.value:
            processBlock(block)
            block.toFirst()
            toAss = variable.copy()
            toAss.value -= 1
            variable.assigment(toAss)
            decreaseTilFloor()
    
    def change(evolution):
        processBlock(block)
        block.toFirst()
        toAss = variable.copy()
        toAss.value += evolution
        variable.assigment(toAss)
        if evolution == 1:
            if variable.value <= toV.value:
                change(evolution)
        else:
            if variable.value >= toV.value:
                change(evolution)
    
    if operator == "..<":
        if fromV.value == toV.value:
            print("Warning: for nâo está executando")
            return
        if fromV.value > toV.value:
            print("Error: indice de início maior que o de fim")
            quit()
        increaseTilTop()
    
    if operator == "...":
        if fromV.value > toV.value:
            change(-1)
        else:
            change(1)

    if operator == ">..":
        if fromV.value == toV.value:
            print("Warning: for nâo está executando")
            return
        if fromV.value < toV.value:
            print("Error: indice de início menor que o de fim")
            quit()
        decreaseTilFloor()

def processFor(parserObject):
    if type(parserObject.value) == ParserForInRange:
        processForRange(parserObject.value, parserObject.block)

def processWhile(parserObject):
    queue = parserObject.block
    variable = Variable("ans", executeOperation(parserObject.value).value, VariableType.boolean, VariableConstantType.let)
    variable.toBoolean()
    if variable.value:
        processBlock(queue)
        queue.toFirst()
        processWhile(parserObject)

def processFunction(parserObject):
    name = parserObject.name.getValue()
    if name == "console":
        if type(parserObject.parameters) == ParserFunctionVariable:
            if parserObject.parameters.name.getValue() == "print":
                if type(parserObject.parameters.value) == ParserStringQueue:
                    value = intepreterString(parserObject.parameters.value)
                else:
                    value = executeOperation(parserObject.parameters.value)
                    if value.type == VariableType.string:
                        value = normalizeString(value)

                print(value.value)
                return
            if parserObject.parameters.name.getValue() == "read":
                message = 0
                if type(parserObject.parameters.value) == ParserStringQueue:
                    value = intepreterString(parserObject.parameters.value)
                    message = value.value
                elif type(parserObject.parameters.value) == ParserVariable:
                    value = executeOperation(parserObject.parameters.value)
                    if value.type == VariableType.string:
                        message = normalizeString(value).value
                
                if message:
                    s = input(message)
                    return Variable("ans", s, VariableType.string, VariableConstantType.var).toAuto()

        quit()

    print("Error: função não declarada")
    quit()

def normalizeString(variable):
    if variable.name == "ans" and variable.type == VariableType.string:
        variable.value = variable.value[1:len(variable.value)-1]
    else:
        variable.value = str(variable.value)
    return variable

def intepreterString(queue):
    print(queue.node)

    if type(queue.node) == ParserStringBlock:
        variable = executeOperation(queue.node.block)
    else:
        variable = executeOperation(queue.node)
    
    variable = normalizeString(variable)

    if queue.next:
        value = intepreterString(queue.next)

        variable.value = variable.value + value.value
        return variable

    return variable

def map(parserObject, __newVariable=0):
    if type(parserObject) == ParserEmpty:
        return 
    
    if type(parserObject) == ParserVariable:
        print("Warning: valor não atribuido " + str(parserObject.getValue()))

    if type(parserObject) == ParserOperation:
        variable = executeOperation(parserObject)
        print("Warning: valor não utilizado " + str(variable.value))

    if type(parserObject) == ParserOperationAssigment:
        variable = executeOperation(parserObject.first)
        print(variable)
        if type(parserObject.second) == ParserStringQueue:
            value = intepreterString(parserObject.second)
        else:
            value = executeOperation(parserObject.second)
        print(value)
        variable.assigment(value)
        LexerHash.shared().verbose()
    
    if type(parserObject) == ParserIf:
        processIfBlock(parserObject)
    if type(parserObject) == ParserWhile:
        processWhile(parserObject)
    if type(parserObject) == ParserFor:
        processFor(parserObject)
    if type(parserObject) == ParserFunction:
        processFunction(parserObject)
    if type(parserObject) == ParserDeclarationVariable:
        (assigment, primitiveType, varType) = parserObject.map()
        
        name = assigment.first.getValue()
        if LexerHash.shared().getObject(name):
            print("Error: Can't create the same variable")
            quit()


        if type(assigment.second) == ParserVariable:
            value = assigment.second.getValue()
            if type(primitiveType) == ParserVariableType:
                primitiveType = VariableType.isPrimitive(primitiveType.type.getValue())
                if primitiveType != VariableType.cast(assigment.second.getToken()):
                    print("Error: Can't assigment diferent types in declaration")
                    quit()

            if type(primitiveType) == VariableDeclarationCast and primitiveType == VariableDeclarationCast.auto:
                print("do stuff")
                primitiveType = VariableType.cast(assigment.second.getToken())

        else:
            if type(assigment.second) == ParserFunction:
                value = processFunction(assigment.second)
                print(primitiveType, value.type)
                if type(primitiveType) == VariableDeclarationCast and primitiveType == VariableDeclarationCast.auto:
                    primitiveType = value.type
                elif primitiveType != value.type:
                    print("Error: Can't assigment diferent types in declaration")
                    quit()
                value = value.value
            if type(assigment.second) == ParserOperation:
                value = executeOperation(assigment.second)
                print(primitiveType, value.type)
                if type(primitiveType) == VariableDeclarationCast and primitiveType == VariableDeclarationCast.auto:
                    primitiveType = value.type
                elif primitiveType != value.type:
                    print("Error: Can't assigment diferent types in declaration")
                    quit()
                
                value = value.value
            if type(assigment.second) == ParserStringQueue:
                value = intepreterString(assigment.second)
                if type(primitiveType) == VariableDeclarationCast and primitiveType == VariableDeclarationCast.auto:
                    primitiveType = value.type
                elif primitiveType != value.type:
                    print("Error: Can't assigment diferent types in declaration")
                    quit()
                value = value.value
        
        if type(primitiveType) == ParserVariableType:
            primitiveType = VariableType.isPrimitive(primitiveType.type.getValue())        

        variable = Variable(name, value, primitiveType, varType)
        LexerHash.shared().insert(variable)
        LexerHash.shared().verbose()
        print("Creating")
        if __newVariable:
            print("Creating")
            __newVariable(variable)
    print(parserObject) 
