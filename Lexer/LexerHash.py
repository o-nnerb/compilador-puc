from Interpreter.Variable.Variable import Variable, VariableType

class LexerHashNode:
    variable = 0

    def __init__(self, key):
        self.variable = Variable(key, 0, VariableType.nil)
    
    @staticmethod
    def create(key, value, type):
        node = LexerHashNode(key)
        node.variable.value = value
        node.variable.type = type
        return node

    def getVariable(self):
        return self.variable

class LexerHash:
    tabela = []

    __shared = 0

    def __init__(self):
        return

    @staticmethod
    def shared():
        if not LexerHash.__shared:
            LexerHash.__shared = LexerHash()

        return LexerHash.__shared

    @staticmethod
    def hashKey(string):
        key = 0
        for char in string:
            key += ord(char)

        return key%100

    def insert(self, lexerToken):
        key = LexerHash.hashKey(lexerToken.getValue())
        node = LexerHashNode(lexerToken.getValue())
        while len(self.tabela) <= key:
            self.tabela.append(0)
        
        if not self.tabela[key]:
            self.tabela[key] = node
            return
        
        if type(self.tabela[key]) == list:
            for element in self.tabela[key]:
                if element.variable.getName() == node.variable.getName():
                    return
            self.tabela[key].append(node)
            return

        if self.tabela[key].variable.getName() == node.variable.getName():
            return
            
        self.tabela[key] = [self.tabela[key], node]
    
    def getObject(self, value):
        key = int(LexerHash.hashKey(value))
        if len(self.tabela) <= key:
            return False
        
        if not self.tabela[key]:
            return False

        if type(self.tabela[key]) == list:
            for node in self.tabela[key]:
                if node.variable.getName() == value:
                    return node.variable

            return False
        
        return self.tabela[key].variable
    
    def verbose(self):
        for node in self.tabela:
            if node:
                if type(node) == list:
                    for element in node:
                        print(element.variable.verbose())
                else:
                    print(node.variable.verbose())
    

print("Alloc")