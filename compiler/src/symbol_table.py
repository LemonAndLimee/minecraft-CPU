from src.syntax_analysis import AstNode, SCOPE_DEFINERS
from src.lexical_analysis import Token

class StEntry():
    '''Stores data for an entry in the symbol table dict.
    Attributes:
        memory_address (int):
        data_type (str): Data type of symbol for this entry
        entry_type (str): Entry type of symbol (e.g. variable, const)
    '''
    def __init__(self, memory_addr:int, data_type:str, entry_type:str) -> None:
        self.memory_address = memory_addr
        self.data_type = data_type
        self.entry_type = entry_type
    
    def __str__(self) -> str:
        output = f"m_addr={self.memory_address}, d_type={self.data_type}, e_type={self.entry_type}"
        return output
    
    def __eq__(self, entry: object) -> bool:
        if entry.memory_address == self.memory_address and entry.data_type == self.data_type and entry.entry_type == self.entry_type:
            return True
        else:
            return False

class StEntryVar(StEntry):
    '''Stores data for a variable entry in the symbol table dict.
    Attributes:
        memory_address (int):
        data_type (str): Data type of symbol for this entry
        entry_type (str): Automatically set to "VAR"
        is_accessed (bool): True if the symbol is accessed later in the code, False otherwise
    '''
    def __init__(self, memory_addr:int, data_type:str) -> None:
        super().__init__(memory_addr=memory_addr, data_type=data_type, entry_type="VAR")
        self.is_accessed = False
    
    def __str__(self) -> str:
        output = super().__str__() + f", is_accessed={self.is_accessed}"
        return output
    
    def __eq__(self, value: object) -> bool:
        if super().__eq__(value) == False:
            return False
        elif value.is_accessed != self.is_accessed:
            return False
        return True

class StEntryConst(StEntry):
    '''Stores data for a const entry in the symbol table dict.
    Attributes:
        memory_address (int):
        data_type (str): Data type of symbol for this entry
        entry_type (str): Automatically set to "CONST"
        const_value (any): The value held in the const variable
    '''
    def __init__(self, memory_addr:int, data_type:str, const_value) -> None:
        super().__init__(memory_addr=memory_addr, data_type=data_type, entry_type="CONST")
        self.const_value = const_value
    
    def __str__(self) -> str:
        output = super().__str__() + f", const_val={self.const_value}"
        return output
    
    def __eq__(self, value: object) -> bool:
        if super().__eq__(value) == False:
            return False
        elif value.const_value != self.const_value:
            return False
        return True

