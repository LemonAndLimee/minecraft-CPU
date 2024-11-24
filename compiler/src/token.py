import re
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

TOKEN_TYPES_JSON_FILE = dir_path + "\\..\\definition_files\\token_types.json"

class Token:
    '''Class used to hold info about a lexical token. Contains a token type, and an optional value.'''
    def __init__(self, type:str, value:str=None) -> None:
        self.type = type
        self.value = value if value != None else None
    def __str__(self) -> str:
        if self.value != None:
            return (f"<{self.type}, '{self.value}'>")
        else:
            return (f"<{self.type}>")

with open(TOKEN_TYPES_JSON_FILE, 'r') as f:
    TOKEN_TYPES = json.load(f)

def get_token_type(string:str) -> str:
    '''Returns token type if string is valid token, None otherwise.'''
    for type in TOKEN_TYPES["regex_patterns"]:
        pattern = TOKEN_TYPES["regex_patterns"][type]
        
        if re.fullmatch(pattern=pattern, string=string) != None:
            return type
    return None

def create_token(string:str, token_type:str) ->Token:
    '''Takes a string and a token type, and returns an equivalent token. If store_value == 1, store that value.'''
    store_value = bool(TOKEN_TYPES["stores_value"][token_type])
    if store_value == 1:
        value_string = string.upper() if token_type == "TYPE" else string
        token = Token(type=token_type, value=value_string)
    else:
        token = Token(type=token_type)
    return token