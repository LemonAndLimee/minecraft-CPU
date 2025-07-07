from lexical_token import Token

class AstNode():
    '''Abstract Syntax Tree node. Contains operator and child nodes.
    Attributes:
        children (list): list of pointers to child nodes, or Tokens.
        parent (AstNode): parent node
        operator: a Token or string that is the 'label' of the node, describing the relationship/operation the node represents.'''
    def __init__(self, operator, parent:"AstNode"=None, children:list=[]):
        self.parent = parent
        if type(operator) == Token or type(operator) == str:
            self.operator = operator
        else:
            raise Exception("Operator must be of type Token or str.")
        self.children = []
        for node in children:
            if type(node) == AstNode or type(node) == Token:
                self.children.append(node)
                if type(node) == AstNode:
                    node.parent = self
            else:
                raise Exception("Child node must be of type AstNode or Token.")
    
    def __str__(self) -> str:
        output_string = str(self.operator)

        for node in self.children:
            output_string = output_string + "\n" + str(node)
        
        return output_string