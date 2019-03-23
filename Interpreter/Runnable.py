class Runnable:
    _runnable = 0
    _element = 0 # Element

    def __init__(self):
        return
    
    @staticmethod
    def runnable(runnable):
        self = Runnable()
        self._runnable = runnable
        return self
    
    @staticmethod
    def element(element):
        self = Runnable()
        self._element = element
        return self

    def getElement(self):
        return self._element
    
    def run(self):
        if not self._runnable:
            if not self._element:
                return
            return self._element.run()
        
        return self._runnable.run()

