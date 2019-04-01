class ParserTreeNode:
    node = 0
    prefix = 0
    operator = 0
    right = 0

    def __init__(self, node):
        self.node = node

    @staticmethod
    def create(node):
        return ParserTreeNode(node)
    
    def delete(self):
        self.node = 0
        self.prefix = 0
        self.right = 0

    def getNode(self):
        return self.node

    def getRight(self):
        return self.right

    def getPrefix(self):
        return self.prefix
    
    def setRight(self, right):
        self.right = right
    
    def setPrefix(self, prefix):
        self.prefix = prefix
    
    def setOperator(self, operator):
        self.operator = operator
    
    def getOperator(self):
        return self.operator
    
    @staticmethod
    def delete(node):
        if not node:
            return 
        
        if node.getRight():
            ParserTreeNode.delete(node.getRight())

        node.right = 0
        node.prefix = 0
        node.operator = 0
        node.node = 0

class ParserTree:
    root = 0

    def __init__(self):
        root = 0
    
    @staticmethod
    def searchNode(root):
        if not root:
            return 0

        if root.getRight():
            return ParserTree.searchNode(root.getRight())
        
        return root


    def insertID(self, element):
        if not self.root:
            self.root = ParserTreeNode.create(element)
            return True
        
        root = ParserTree.searchNode(self.root)
        if not root.getNode():
            if root.getPrefix():
                root.setNode(element) 
                return True
            print("Erro sequencia de caracteres")
            return False

        if not root.getOperator():
            print("Erro sequencia de caracteres")
            return False
        
        root.setRight(ParserTreeNode.create(element))
        return True
    
    def insertOperator(self, element):
        if not self.root:
            print("Erro sequencia de caracteres")
            return
        
        root = ParserTree.searchNode(self.root)
        if not root.getNode():
            print("Erro sequencia de caracteres")
            return False

        if not root.getOperator():
            root.setOperator(element)
            return True

        print("Erro sequencia de caracteres")
        return False
    
    def insertPrefix(self, element):
        if not self.root:
            self.root = ParserTreeNode.create(0)
            self.root.setPrefix(element)
            return True
        
        root = ParserTree.searchNode(self.root)
        if not root.getNode():
            print("Erro sequencia de caracteres")
            return False

        if not root.getOperator():
            print("Erro sequencia de caracteres")
            return False
        
        root.setPrefix(element)
        return True
    
    def lastInserted(self):
        object = ParserTree.searchNode(self.root)
        if not object:
            return
        
        return object.getNode()
    
    def lastInsertedOperator(self):
        object = ParserTree.searchNode(self.root)
        if not object:
            return
        
        return object.getOperator()
    
    def isEmpty(self):
        return self.root == 0

    def deleteAll(self):
        ParserTreeNode.delete(self.root)
        self.root = 0
    
    @staticmethod
    def printRecursivo(node):
        if not node:
            return
        
        string = ""
        if node.getPrefix():
            string += node.getPrefix().getValue()

        string += node.getNode().getValue()
        if node.getOperator():
            string += " " + node.getOperator().getValue()
        #print(string)

        ParserTree.printRecursivo(node.getRight())

    def print(self):
        ParserTree.printRecursivo(self.root)
            

        
        



