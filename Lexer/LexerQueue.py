class LexerQueueNode:
    node = 0
    next = 0
    prev = 0

    def __init__(self, node):
        self.node = node

    @staticmethod
    def create(node, prev):
        node = LexerQueueNode(node)
        node.prev = prev
        return node
    
    def delete(self):
        self.node = 0
        self.next = 0
        self.prev = 0

    def getNode(self):
        return self.node

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev
    
    def setNext(self, next):
        self.next = next
    
    def setPrev(self, prev):
        self.prev = prev

class LexerQueue:
    first = 0
    last = 0
    head = 0
    save = 0
    
    __shared = 0

    def __init__(self):
        return

    @staticmethod
    def shared():
        if not LexerQueue.__shared:
            LexerQueue.__shared = LexerQueue()

        return LexerQueue.__shared

    def toFirst(self):
        self.head = self.first
    
    def insert(self, token):
        node = LexerQueueNode.create(token, self.last)
        if self.last:
            self.last.setNext(node)
        
        self.last = node

        if not self.first:
            self.first = node
            self.head = node
        
    def popFirst(self):
        if self.save:
            print("Calling popFirst when you are persisting data")
            print("Nothing will happen")
            return False

        if not self.first:
            return False
        
        object = self.first.getNode()
        toDelete = self.first

        if not self.last.getPrev():
            self.last = 0
            self.first = 0
            self.head = 0
        
        if self.first and self.first.getNext():
            self.first = self.first.getNext()
            self.first.setPrev(0)
        
        toDelete.delete()
        return object
    
    def lastElement(self):
        if not self.last:
            return 0
        return self.last.getNode()

    def firstElement(self):
        if not self.first:
            return 0
        return self.first.getNode()
        
    def isEmpty(self):
        return not self.first or (self.save and not self.head)

    def needsPersist(self, boolean):
        self.save = boolean
    
    def toRight(self):
        if not self.head:
            return False
        
        last = self.head.getNode()
        self.head = self.head.getNext()
        
        return last
    
    def toLeft(self):
        if not self.head:
            return False

        left = self.head.getPrev()
        if not left:
            return False

        self.head = left
        return self.head.getNode()
    
    def getHead(self):
        if not self.head:
            return False
        return self.head.getNode()

    def copy(self):
        queue = LexerQueue()
        node = self.first
        while node:
            queue.insert(node.getNode())
            node = node.getNext()
        return queue

    def verbose(self):
        if self.save:
            head = self.head
            self.toFirst()
            while self.head:
                last = self.getHead()
                self.toRight()

                print(last.getToken() + "<" + last.getValue() + ">")

            self.head = head
            return
        
        while not self.isEmpty():
            last = self.popFirst()
            print(last.getToken() + "<" + last.getValue() + ">")




