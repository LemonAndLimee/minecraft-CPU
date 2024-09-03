from syntax_analysis import AstNode
from lexical_analysis import Token

DATA_TYPES = {
    "CHAR": 0,
    "BOOL": 1
}
ENTRY_TYPES = {
    "VAR": 0,
    "CONST": 1
}

'''
A symbol table stores identifiers, and is a dict in the form: identifier:entry, where entry has the following attributes:
    - memory address
    - data type
    - entry type (variable, const)
        - const value
        - is accessed? bool
    
Symbol tables exist in a tree structure, where the root node represents the global scope, and any children represent nested scopes.
Thus, a variable can be accessed if it exists in the current symbol table or any parent tables.
Variables can exist separately in multiple scopes - when searching, return a match for the closest table when travelling up through parents.
Const entries can be accessed anywhere: they should exist in the root table.

A tree node has attributes:
    - its symbol table
    - parent node
    - child nodes (exists as a dict in the form token:node, with token being the instance of e.g. IF, FOR)

To create symbol table tree, do a depth-first traversal of the AST:
(Note: this is just to create the symbol tree. Type checking etc. will be done as part of the semantic analysis stage)

When traversing the AST, if an ID is read:
    If it is preceeded by a TYPE token, this is a declaration:
        Create an entry in the symbol table (if there is already one, throw error)
    Else:
        If there is not an entry in this table or any parent table, throw error
    
    Else not assignment and not declaration:
        If is accessed bool is false, set it to true

If a const value is read (e.g. CHAR, BOOL):
    Check entries in root table for a matching const_value - if none exists, create entry

If a scope type token is read (e.g. IF, FOR):
    Create new child symbol table

'''

class SymbolTableEntry():
    def __init__(self, memory_addr:int, data_type, entry_type) -> None:
        self.memory_address = memory_addr
        self.data_type = data_type
        self.entry_type = entry_type

class SymbolTableEntryVariable(SymbolTableEntry):
    def __init__(self, memory_addr:int, data_type) -> None:
        super().__init__(memory_addr=memory_addr, data_type=data_type, entry_type=ENTRY_TYPES["VAR"])
        self.is_accessed = False

class SymbolTableEntryConst(SymbolTableEntry):
    def __init__(self, memory_addr:int, data_type, const_value) -> None:
        super().__init__(memory_addr=memory_addr, data_type=data_type, entry_type=ENTRY_TYPES["CONST"])
        self.const_value = const_value

class SymbolTable():
    def __init__(self) -> None:
        self.table = {}
    
    def add_symbol_table_entry(self, identifier:str, entry:SymbolTableEntry):
        self.table[identifier] = entry
    
    def get_entry_from_id(self, identifier:str):
        return self.table[identifier]

class SymbolTableTreeNode():
    def __init__(self, parent_node=None) -> None:
        self.symbol_table = SymbolTable()
        if parent_node == None or type(parent_node) == SymbolTableTreeNode:
            self.parent_node = parent_node
        else:
            raise Exception("Symbol Table Tree Node creation: parent node must be of type SymbolTableTreeNode or None")
        self.child_nodes = {}
    
    def add_symbol_table_entry(self, identifier:str, entry:SymbolTableEntry):
        self.symbol_table.add_symbol_table_entry(identifier=identifier, entry=entry)
    
    def get_entry_from_id(self, identifier:str):
        return self.symbol_table.get_entry_from_id(identifier=identifier)
    
    def create_child(self, token:Token):
        '''Create child node and add to child_nodes list. Return said child node.'''
        child_node = SymbolTableTreeNode(parent_node=self)
        self.child_nodes[token] = child_node
        return child_node


