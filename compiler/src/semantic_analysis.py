from src.symbol_table import *
from src.grammar import OBJECT_TYPES, VALID_CONDITION_DATA_TYPES, SCOPE_DEFINERS

'''This stage is responsible for any remaining checks:
- type checking: 
    - check that any assignment statements resolve to the relevant variable's data type
    - check that the condition in an if/while statement resolves to a boolean or numeric type
- for loop check:
    - check the for loop conditions are valid
'''

def check_ast(ast_root:AstNode, symbol_table:SymbolTable):
    '''Takes an AST and a symbol table and performs any remaining checks for errors.
    Attributes:
        ast_root (AstNode): The root of the AST being checked
        symbol_table (SymbolTable): The symbol table associated with this AST
    '''
    #TODO:
    # if node is assignment operator, do type check with the 2 sides
    # if node is if operator, evaluate condition (aka first child) - make sure it is of type bool or numeric
    # if node is while operator, evaluate condition (aka first child) - make sure it is of type bool or numeric
    # if node is for operator, evaluate the 3 children:
        # child 0 and 2 must be assignment statements with valid RHS args data types
    # else foreach child, call self with child - if child is scope definer, pass child symbol table as argument

def check_assignment_data_type(assignment_ast_node:AstNode, symbol_table:SymbolTable):
    '''Checks the evaluated data type of an assignment statement value matches the variable data type.
    Attributes:
        assignment_ast_node (AstNode): This node represents the assignment operator - it is the root of the current sub-tree representing the statement
        symbol_table (SymbolTable): The symbol table associated with this AST
    '''
    evaluate_node_data_type(assignment_ast_node, symbol_table)

def check_condition_data_type(condition_ast_node:AstNode, symbol_table:SymbolTable):
    '''Checks the evaluated data type of a condition is a boolean or numeric type.
    Attributes:
        assignment_ast_node (AstNode): This node represents the condition section's operator - it is the root of the current sub-tree representing the expression
        symbol_table (SymbolTable): The symbol table associated with this AST
    '''
    data_type = evaluate_node_data_type(condition_ast_node, symbol_table)
    if data_type not in VALID_CONDITION_DATA_TYPES:
        raise Exception(f"Condition must be of boolean or numeric type. AST node:\n{condition_ast_node}")

def evaluate_node_data_type(ast_node:AstNode, symbol_table:SymbolTable):
    '''Returns the evaluated data type of an AST. Raises exception if any of the children have different data types.
    Attributes:
        ast_node (AstNode): This node represents the root of the tree being evaluated
        symbol_table (SymbolTable): The symbol table associated with this AST
    '''
    # if ast node operator is a comparison or logical operator, the type of this ast is boolean
    if type(ast_node.operator) == Token:
        if ast_node.operator.type == "COMPARISON" or ast_node.operator.type == "LOGICAL":
            return "BOOL"
    
    current_data_type = ""
    for child in ast_node.children:
        # if child is a terminal
        if type(child) == Token:
            if child.type in OBJECT_TYPES:
                if child.type == "ID":
                    name = child.value
                    entry = symbol_table.get_entry(name)
                    id_data_type = entry.data_type
                    if current_data_type == "":
                        current_data_type = id_data_type
                    elif id_data_type != current_data_type:
                        raise Exception(f"Semantic analysis: identifier {name} is of incompatible data type {id_data_type} vs expected {current_data_type}.")
                else:
                    if current_data_type == "":
                        current_data_type = child.type
                    elif child.type != current_data_type:
                        raise Exception(f"Semantic analysis: value {child.value} is of incompatible data type {child.type} vs expected {current_data_type}.")
            
        elif type(child) == AstNode:
            current_symbol_table = symbol_table
            if type(child.operator) == Token and child.operator in SCOPE_DEFINERS:
                current_symbol_table = symbol_table.get_child(child)
                
            child_ast_data_type = evaluate_node_data_type(child, current_symbol_table)
            if current_data_type == "":
                current_data_type = child_ast_data_type
            elif child_ast_data_type != current_data_type:
                raise Exception(f"Semantic analysis: incompatible evaluated data type {child_ast_data_type} vs expected {current_data_type} of AST:\n{child}")
    
    if current_data_type == "":
        raise Exception(f"Error evaluating data type on following AST node, no data type found:\n{ast_node}")