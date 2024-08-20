import json
from lexical_analysis import Token

current_dir = ""
for index in reversed(range(len(__file__))):
    if __file__[index] == '/':
        current_dir = __file__[:index]
        break

GRAMMAR_JSON_FILE = current_dir + "/definition_files/grammar.json"
with open(GRAMMAR_JSON_FILE, 'r') as f:
    GRAMMAR_RULES = json.load(f)["grammar"]

START_SYMBOL = "expression"

class AST_node():
    def __init__(self, left, operator:Token, right=None):
        if type(left) == AST_node or type(left) == Token:
            self.left = left
        else:
            raise Exception("AST_node.left must be AST_node or Token")
        self.operator = operator
        if type(right) == AST_node or type(right) == Token or right == None:
            self.right = right
        else:
            raise Exception("AST_node.right must be AST_node, Token or None")
    
    def __str__(self) -> str:
        output_string = str(self.operator)

        output_string = output_string + "\n" + str(self.left)
        output_string = output_string + "\n" + str(self.right)
        
        return output_string

class AST_generator():
    def __init__(self, tokens:list[Token], start_symbol:str=START_SYMBOL):
        self.tokens = tokens
        self.current_token_pointer = 0
        self.start_symbol = start_symbol

    def get_node(self, rule_name:str):
        rule_strings = GRAMMAR_RULES[rule_name]
        saved_token_pointer = self.current_token_pointer
        # foreach possible grammar string
        for rule in rule_strings:
            print(f"Trying rule {rule}:")
            ''' foreach rule segment:
                    if segment is token type, check for match w current token
                        if match, increment pointer
                            if token type is punctuation, ignore
                            else if it is the operator, return a node with left/right being func calls of the respective NTs
                            elif it is object, assign to left
                        if not match, throw error?
                    if segment is non token type, call func again to create a new node
                        if left is null, assign it to left, else assign it to right
                
                outside the foreach:
                    if you have left, op and right, create and return new node
                    if you have left and op, do the same
                    if you have only left, if rule consists of only <T> then you can return it as a str
                    else throw error
                
                think of a terminal as the operator of a node, and an NT as another func call to create a node
            '''
            self.current_token_pointer = saved_token_pointer
            try:
                rule_segments = str.split(rule)
                left_node, operator, right_node = None, None, None
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
                            if terminal in ["PLUS_MINUS", "MULT_DIVIDE", "MOD", "EXP", "LOGICAL"]:
                                print("terminal is operator")
                                operator = current_token
                            # if terminal type is object
                            elif terminal in ["ID", "CHAR", "BOOL"]:
                                print("terminal is object")
                                left_node = current_token
                        # if no match, raise error
                        else:
                            print(f"EXCEPTION: terminal {terminal} does not matches token {self.tokens[self.current_token_pointer]}")
                            raise Exception(f"Current token {self.tokens[self.current_token_pointer]} doesn't match terminal {terminal}.")
                    # if segment is non-terminal
                    else:
                        print(f"segment {rule_segment} is non-terminal")
                        print(f"calling get_node on {rule_segment}")
                        node = self.get_node(rule_segment)
                        if left_node == None:
                            left_node = node
                            print(f"assign to left node on call {rule}, segment {rule_segment}")
                        elif right_node == None:
                            right_node = node
                            print(f"assign to right node on call {rule}, segment {rule_segment}")
                        else:
                            print(f"EXCEPTION: On rule {rule}, there already exists two nodes: trying to add one with call {rule_segment}.")
                            raise Exception(f"On rule {rule}, there already exists two nodes: trying to add one with call {rule_segment}.")
                
                if left_node != None and operator != None:
                    print(f"has left and op, not none")
                    new_node = AST_node(left=left_node, operator=operator, right=right_node)
                    return new_node
                # if only left not none
                elif left_node != None and operator == None and right_node == None:
                    print(f"has only left")
                    # if rule only has 1 segment (excluding brackets)
                    count = 0
                    for segment in rule_segments:
                        if segment[0] == "<" and segment[-1] == ">":
                            if segment[1:-1] not in ["(", ")"]:
                                count += 1
                        else:
                            count += 1
                    if count == 1:
                        print(f"return left {left_node}")
                        return left_node
                    print(f"rule {rule} has len != 1")
                else:
                    print(f"EXCEPTION: Wrong states for left, op, right: {left_node}, {operator}, {right_node}.")
                    raise Exception(f"Wrong states for left, op, right: {left_node}, {operator}, {right_node}.")
            except:
                pass
                
        # if all rules are tried with no success, raise error
        print(f"EXCEPTION: No rules under {rule_name} matched.")
        raise Exception(f"No rules under {rule_name} matched.")
    
    def generate_abstract_syntax_tree(self) -> AST_node:
        return self.get_node(rule_name=self.start_symbol)

import lexical_analysis as la

line = "(a+b)*a^b+a"
tokens = la.convert_into_tokens(line)

ast_generator = AST_generator(tokens=tokens)
node = ast_generator.generate_abstract_syntax_tree()
print(str(node))