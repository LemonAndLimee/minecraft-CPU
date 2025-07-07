from lexical_token import Token
from grammar import *
from abstract_syntax_tree import AstNode

class AstGenerator():
    '''Used to generate an Abstract Syntax Tree. Stores a list of tokens and a pointer used to traverse the list.'''
    def __init__(self, tokens:list[Token], start_symbol:str=START_SYMBOL):
        self.tokens = tokens
        self.current_token_pointer = 0
        self.start_symbol = start_symbol
    
    def get_rule_length(self, rule:str) -> int:
        '''Returns number of symbols in rule, excluding any token types marked to be excluded from AST.'''
        rule_segments = str.split(rule)
        count = 0
        for segment in rule_segments:
            if segment[0] == "<" and segment[-1] == ">":
                if segment[1:-1] not in EXCLUDE_FROM_AST:
                    count += 1
            else:
                count += 1
        return count

    def get_return_object(self, operator, children:list, rule:str):
        '''Determines what to return given an operator and list of child nodes.
        If there is at least 1 child:
            If operator is not None, return a new AstNode.
            Else if operator is None:
                If the no. child nodes matches the no. rule elements:
                    If this number is 1, return the child.
                    If the number > 1, it is a grammar rule without an operator.
                    Therefore, make a new AstNode with operator being the name of the rule segment.
                Else if
        Else raise exception.'''
        if len(children) > 0:
            if operator != None:
                print(f"has at least one child and op, not none")
                new_node = AstNode(operator=operator, children=children)
                return new_node
            else:
                print(f"has no op")
                number_of_rule_elements = self.get_rule_length(rule)
                if len(children) == number_of_rule_elements:
                    print(f"child nodes matches rule segments length")
                    if number_of_rule_elements == 1:
                        print(f"returning child {str(children[0])} on rule {rule}")
                        return children[0]
                    elif number_of_rule_elements > 1:
                        rule_name = get_grammar_rule_name(rule)
                        print(f"return new node with str operator {rule_name}")
                        new_node = AstNode(operator=rule_name, children=children)
                        return new_node
                print(f"child nodes {len(children)} does not match rule segments length {number_of_rule_elements}")

        print(f"EXCEPTION on rule {rule}: Wrong states for op, children: {operator}, {children}.")
        raise Exception(f"Wrong states for op, children: {operator}, {children}.")

    def get_node(self, rule_name:str, is_root_node:bool=False):
        '''Traverses through tokens starting from the current pointer until the given rule has been met.
        Produces an AST node to represent this rule. Throws an exception if the rule cannot be met.
        If is_root_node is set to True, all tokens must be consumed for the rule to be accepted.'''
        rule_strings = GRAMMAR_RULES[rule_name]
        saved_token_pointer = self.current_token_pointer
        # foreach possible grammar string
        for rule in rule_strings:
            print(f"Trying rule {rule}:")
            self.current_token_pointer = saved_token_pointer
            try:
                rule_segments = str.split(rule)
                operator = None
                children = []

                for index in range(len(rule_segments)):
                    rule_segment = rule_segments[index]
                    print(f"on segment {rule_segment}:")
                    # if segment is terminal
                    if rule_segment[0] == "<" and rule_segment[-1] == ">":
                        print(f"segment is terminal")
                        terminal = rule_segment[1:-1]
                        current_token = self.tokens[self.current_token_pointer]
                        # if terminal symbol matches current token
                        if terminal == current_token.type:
                            print(f"terminal {terminal} matches token {current_token}")
                            self.current_token_pointer += 1
                            # if terminal type is operator (aka not punctuation)
                            if terminal in OPERATOR_TYPES:
                                print("terminal is operator")
                                operator = current_token
                            # if terminal type is object
                            elif terminal in OBJECT_TYPES:
                                print("terminal is object")
                                children.append(current_token)
                        # if no match, raise error
                        else:
                            print(f"EXCEPTION: terminal {terminal} does not matches token {self.tokens[self.current_token_pointer]}")
                            raise Exception(f"Current token {self.tokens[self.current_token_pointer]} doesn't match terminal {terminal}.")
                    # if segment is non-terminal
                    else:
                        print(f"segment {rule_segment} is non-terminal")
                        print(f"calling get_node on {rule_segment}")
                        node = self.get_node(rule_segment)
                        print(f"assign to child node on call {rule}, segment [{index}] {rule_segment}")
                        children.append(node)
                
                if is_root_node == True and self.current_token_pointer != len(self.tokens):
                    print(f"EXCEPTION: Extra leftover tokens on rule {rule}")
                    raise Exception(f"Extra leftover tokens on rule {rule}")
                
                return self.get_return_object(operator=operator, children=children, rule=rule)
            except:
                pass
                
        # if all rules are tried with no success, raise error
        print(f"EXCEPTION: No rules under {rule_name} matched.")
        raise Exception(f"No rules under {rule_name} matched.")
    
    def generate_abstract_syntax_tree(self) -> AstNode:
        return self.get_node(rule_name=self.start_symbol, is_root_node=True)
