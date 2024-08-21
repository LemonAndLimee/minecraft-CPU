import json
from lexical_analysis import Token

current_dir = ""
for index in reversed(range(len(__file__))):
    if __file__[index] == '/':
        current_dir = __file__[:index]
        break

GRAMMAR_JSON_FILE = current_dir + "/definition_files/grammar.json"
with open(GRAMMAR_JSON_FILE, 'r') as f:
    grammar_data = json.load(f)
    GRAMMAR_RULES = grammar_data["grammar"]
    OPERATOR_TYPES = grammar_data["operators"]

START_SYMBOL = "logical"

class AST_node():
    '''Abstract Syntax Tree node. Contains operator and child nodes.
    Child nodes are pointers to nodes, or Tokens.
    Operator is a Token that is the 'label' of the node, describing the relationship/operation the node represents.'''
    def __init__(self, operator:Token, child_nodes:list):
        self.operator = operator
        self.child_nodes = []
        for node in child_nodes:
            if type(node) == AST_node or type(node) == Token:
                self.child_nodes.append(node)
            else:
                raise Exception("Child node must be of type AST_node or Token.")
    
    def __str__(self) -> str:
        output_string = str(self.operator)

        for node in self.child_nodes:
            output_string = output_string + "\n" + str(node)
        
        return output_string

class AST_generator():
    '''Used to generate an Abstract Syntax Tree. Stores a list of tokens and a pointer used to traverse the list.'''
    def __init__(self, tokens:list[Token]):
        self.tokens = tokens
        self.current_token_pointer = 0

    def get_node(self, rule_name:str):
        '''Traverses through tokens starting from the current pointer until the given rule has been met.
        Produces an AST node to represent this rule. Throws an exception if the rule cannot be met.'''
        rule_strings = GRAMMAR_RULES[rule_name]
        saved_token_pointer = self.current_token_pointer
        # foreach possible grammar string
        for rule in rule_strings:
            print(f"Trying rule {rule}:")
            self.current_token_pointer = saved_token_pointer
            try:
                rule_segments = str.split(rule)
                operator = None
                child_nodes = []

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
                            elif terminal in ["ID", "CHAR", "BOOL"]:
                                print("terminal is object")
                                child_nodes.append(current_token)
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
                        child_nodes.append(node)
                
                if len(child_nodes) > 0 and operator != None:
                    print(f"has at least one child and op, not none")
                    new_node = AST_node(operator=operator, child_nodes=child_nodes)
                    return new_node
                # if only 1 child not none
                elif len(child_nodes) == 1 and operator == None:
                    print(f"has only 1 child, no operator")
                    # if rule only has 1 segment (excluding brackets)
                    count = 0
                    for segment in rule_segments:
                        if segment[0] == "<" and segment[-1] == ">":
                            if segment[1:-1] not in ["(", ")"]:
                                count += 1
                        else:
                            count += 1
                    if count == 1:
                        print(f"return child {child_nodes[0]} from call {rule}")
                        return child_nodes[0]
                    print(f"rule {rule} has len != 1")
                else:
                    print(f"EXCEPTION: Wrong states for op, children: {operator}, {child_nodes}.")
                    raise Exception(f"Wrong states for op, children: {operator}, {child_nodes}.")
            except:
                pass
                
        # if all rules are tried with no success, raise error
        print(f"EXCEPTION: No rules under {rule_name} matched.")
        raise Exception(f"No rules under {rule_name} matched.")
    
    def generate_abstract_syntax_tree(self) -> AST_node:
        return self.get_node(rule_name=START_SYMBOL)

import lexical_analysis as la

line = "! b"
tokens = la.convert_into_tokens(line)

ast_generator = AST_generator(tokens=tokens)
node = ast_generator.generate_abstract_syntax_tree()
print(f"\n{str(node)}")