import sys
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Interpreter.Interpreter import Interpreter
from Lexer.LexerHash import LexerHash
from Lexer.LexerQueue import LexerQueue

Lexer.run(sys.argv)
Parser.run()
Interpreter.run()

for arg in sys.argv:
    if arg == "-v":
        print("Tabela de variáveis")
        LexerHash.shared().verbose()
        print("\nLista de instruções")
        LexerQueue.shared().verbose()
