from enum import Enum, unique

@unique
class LexerEnum(Enum):
    id = "ID"
    integer = "INT"
    float = "FLT"

    boolean = "BOOL"
    
    operator = "OPR"
    logical_operator = "LOG_OPR"
    operator_prefix = "OPR_PRE"
    operator_posfix = "OPR_POS"

    delimiter = "DEL"
    logical = "LOG"

    assigment = "ASS"
    keyword = "KEY"
    endline = "END"

    forloop = "FOR" # {..., ...<} (não implementado)

    error = "ERR"
    expression = "EXP"

    @staticmethod
    def compare(object, values):
        token = object.getToken()
        if type(values) != list:
            return token == values
        
        for value in values:
            if token == value:
                return True
        
        return False


