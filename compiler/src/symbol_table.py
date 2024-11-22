from src.syntax_analysis import AstNode, Token, SCOPE_DEFINERS, CONST_TYPES

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
        if entry == None:
            return False
        elif isinstance(entry, StEntry) or issubclass(entry, StEntry):
            if entry.memory_address == self.memory_address and entry.data_type == self.data_type and entry.entry_type == self.entry_type:
                return True
            else:
                return False
        else:
            raise TypeError("Entry must be of type StEntry or a derived data type.")

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

class SymbolTable():
    '''Stores symbols and entries in a dict, as well as references to parent and child symbol tables.
    Attributes:
        parent (SymbolTable):
        children (dict): in the form Token:SymbolTable
        table (dict): contains symbol table entries in the form name:Entry
    Methods:
        get_entry(name)
        add_entry(name, entry)
        assign_child(token, child)
    '''
    def __init__(self, parent:"SymbolTable"=None) -> None:
        self.parent = parent
        self.children = {}
        self.table = {}
    
    def __eq__(self, value:"SymbolTable") -> bool:
        '''Compares 2 symbol table classes. Only considers table entries; children/parent are not compared.'''
        if len(self.table) != len(value.table):
            return False
        else:
            for name in self.table.keys():
                if name not in value.table.keys():
                    return False
                if self.get_entry(name) != value.get_entry(name):
                    return False
        return True
    
    def __str__(self) -> str:
        output_string = ""
        for name in self.table.keys():
            output_string = output_string + f"{name}:[{str(self.get_entry(name))}],\n"
        output_string = output_string[:-2]
        return output_string
    
    def get_entry(self, name:str) -> StEntry:
        '''Returns entry if it exists in current or higher scope. Otherwise returns None.'''
        if name in self.table.keys():
            return self.table[name]
        elif not self.parent is None:
            return self.parent.get_entry(name)
        else:
            return None
    
    def add_entry(self, name:str, entry:StEntry):
        if name in self.table.keys():
            raise Exception("Entry already exists.")
        else:
            self.table[name] = entry
    
    def get_const_entry(self, value) -> StEntryConst:
        '''Returns const entry if it exists in current or higher scope. Otherwise returns None. Searches by value'''
        root_node = self.get_root_node()
        for key in root_node.table.keys():
            entry = root_node.get_entry(key)
            if type(entry) == StEntryConst and entry.const_value == value:
                return entry
        return None
    
    def assign_child(self, token:Token, child:"SymbolTable"):
        self.children[token] = child
    
    def get_child(self, token:Token) -> "SymbolTable" :
        '''Returns child table associated with a given token. If there is no associated child, return None.'''
        if token in self.children.keys():
            return self.children[token]
        else:
            return None
    
    def get_root_node(self) -> "SymbolTable":
        '''Returns root node of symbol table tree. Returns self if has no parent.'''
        if self.parent is None:
            return self
        else:
            return self.parent.get_root_node()

class SymbolTableGenerator():
    '''Used to generate symbol tables from an AST.
    Attributes:
        next_mem_addr (int): Next available memory address to be assigned to symbol.
    '''
    def __init__(self, next_mem_addr:int=0) -> None:
        self.next_mem_addr = next_mem_addr
        self.next_const_name_ptr = 0
    
    def create_st_from_ast(self, ast_node:AstNode, parent_st:SymbolTable=None) -> SymbolTable:
        '''Creates symbol tree from an AST representing a given scope.
        Attributes:
            ast_node (AstNode):
            parent_st (SymbolTable): optional parent symbol table
        '''
        # Create symbol table, then call traverse_ast on ast_node
        symbol_table = SymbolTable(parent=parent_st)
        self.traverse_ast(ast_parent_node=ast_node, current_st=symbol_table)
        return symbol_table
    
    def traverse_ast(self, ast_parent_node:AstNode, current_st:SymbolTable=None):
        '''Traverses an AST, adding entries or children to the given symbol table.
        Attributes:
            ast_parent_node (AstNode): The root of the AST (can be a Token if the tree is one object)
            current_st (SymbolTable): The table to add new entries to (if None, will create new one)
        '''
        for node in ast_parent_node.children:
            self.process_ast_object(node=node, parent_node=ast_parent_node, current_st=current_st)
    
    def process_ast_object(self, node:AstNode, parent_node:AstNode, current_st:SymbolTable):
        '''Represents a single step in the traversal of an AST.
        An AST object is considered, and depending on if it is of type AstNode or Token, a function call is made to take further action.'''
        if type(node) == AstNode:
            self.process_ast_node(node=node, current_st=current_st)
        elif type(node) == Token:
            self.process_token(token=node, parent_node=parent_node, current_st=current_st)
    
    def process_ast_node(self, node:AstNode, current_st:SymbolTable):
        '''Represents a single step in the traversal of an AST.
        Consider ast node: either create a new child table or continue traversing the tree via children.
        '''
        # if node has a scope-defining operator, create new child table
        if type(node.operator) == Token and node.operator.type in SCOPE_DEFINERS:
            child_table = self.create_st_from_ast(ast_node=node, parent_st=current_st)
            current_st.assign_child(token=node.operator, child=child_table)
        # else if node has children, recursively call to continue traversing tree
        elif len(node.children) > 0:
            self.traverse_ast(ast_parent_node=node, current_st=current_st)
    
    def process_token(self, token:Token, parent_node:AstNode, current_st:SymbolTable):
        '''Represents a single step in the traversal of an AST.
        Consider token in ast: check type, check if declaration, create/edit entry as appropriate.
        A token should always have a parent node, since it represents a leaf of the tree.
        '''
        if token.type == "ID":
            name = token.value
            entry = current_st.get_entry(name)
            # if there is an existing entry for that name
            if entry != None:
                if type(entry) == StEntryVar:
                    entry.is_accessed = True
                else:
                    raise Exception(f"There is an existing entry {entry} for name {name}. Entry type invalid: must be var.")
                # if parent is <TYPE>, raise error, as it has already been declared somewhere else
                if parent_node.operator.type == "TYPE":
                    raise Exception(f"Entry already exists for {name}: cannot declare it.")
            # if there is no existing entry, create one
            else:
                # if declaration, create entry
                if parent_node.operator.type == "TYPE":
                    self.add_var_entry(table=current_st, data_type=parent_node.operator.value, name=name)
                # if it is not a declaration, raise error as there is no existing entry
                else:
                    raise Exception(f"Undefined reference to variable {name}")
        if token.type in CONST_TYPES:
            entry = current_st.get_const_entry(token.value)
            # if there is no existing const entry, create one
            if entry == None:
                root_table = current_st.get_root_node()
                self.add_const_entry(table=root_table, data_type=token.type, const_value=token.value)
    
    def add_const_entry(self, table:SymbolTable, data_type:str, const_value):
        '''Adds const entry to specified table, generating a name using const name pointer.'''
        entry = StEntryConst(memory_addr=self.next_mem_addr, data_type=data_type, const_value=const_value)
        name = "const_" + str(self.next_const_name_ptr)
        self.next_const_name_ptr = self.next_const_name_ptr + 1
        self.add_entry(table=table, name=name, entry=entry)
    
    def add_var_entry(self, table:SymbolTable, data_type:str, name:str):
        '''Adds var entry to specified table.'''
        entry = StEntryVar(memory_addr=self.next_mem_addr, data_type=data_type)
        self.add_entry(table=table, name=name, entry=entry)
    
    def add_entry(self, table:SymbolTable, entry:StEntry, name:str):
        '''Adds entry to specified table. Increments memory address pointer.'''
        table.add_entry(name=name, entry=entry)
        self.next_mem_addr = self.next_mem_addr + 1