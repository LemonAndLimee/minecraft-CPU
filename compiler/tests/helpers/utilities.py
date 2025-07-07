import os
print(os.getcwd())

from src.abstract_syntax_tree import *

def create_ast_from_string(string:str) -> AstNode:
    '''Create AST from string, using the following format rules:
    Use <type,value> to represent a token. Optionally, use <type> for no value.
    Use prefix notation and parentheses to indicate the tree structure, for example:
        operator,(operator1,child1a,child1b),child2
    Attributes:
        string (str): A string representing the AST to be created, using the above format.
    '''
    comma_index = string.index(",")
    operator = string[:comma_index]
    print(operator)

create_ast_from_string("abcd,abcd")