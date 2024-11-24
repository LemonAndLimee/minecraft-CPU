import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
GRAMMAR_JSON_FILE = dir_path + "\\..\\definition_files\\grammar.json"

with open(GRAMMAR_JSON_FILE, 'r') as f:
    grammar_data = json.load(f)
    GRAMMAR_RULES = grammar_data["grammar"]
    OPERATOR_TYPES = grammar_data["operators"]
    EXCLUDE_FROM_AST = grammar_data["exclude_from_AST"]
    OBJECT_TYPES = grammar_data["objects"]
    SCOPE_DEFINERS = grammar_data["scope_definers"]
    CONST_TYPES = grammar_data["const_types"]
    VALID_CONDITION_DATA_TYPES = grammar_data["valid_condition_types"]

START_SYMBOL = "statement"

def get_grammar_rule_name(rule:str):
    '''Given a rule, return its name from the json file.'''
    for key in GRAMMAR_RULES:
        for grammar_rule in GRAMMAR_RULES[key]:
            if rule == grammar_rule:
                return key
    raise Exception("No matching grammar rule.")