import re
import json

TOKEN_TYPES_JSON_FILE = "compiler/token_types.json"

class Token:
    '''Class used to hold info about a lexical token. Contains a token type, and an optional value.'''
    def __init__(self, type:int, value:str=None) -> None:
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
    for type in TOKEN_TYPES["token_regex_patterns"]:
        pattern = TOKEN_TYPES["token_regex_patterns"][type]
        if re.fullmatch(pattern=pattern, string=string) != None:
            return type
    return None

def create_token(string:str, token_type:str):
    '''Takes a string and a token type, and returns an equivalent token.'''
    store_value = bool(TOKEN_TYPES["stores_value"][token_type])
    if store_value:
        token = Token(type=token_type, value=string)
    else:
        token = Token(type=token_type)
    return token

def convert_line_into_tokens(line:str) -> list:
    '''Converts a single line of code into a list of tokens.'''
    tokens = []
    if len(line) == 0:
        return tokens

    start_pointer = 0 # start of substring, inclusive
    end_pointer = 1 # end of substring, exclusive

    last_successful_pointer = None

    while end_pointer < len(line)+1:
        substring = line[start_pointer:end_pointer]
        token_type = get_token_type(substring)
        if token_type != None:
            last_successful_pointer = end_pointer
        else:
            # if there was a previously successful token, convert that then continue from current character
            if last_successful_pointer != None:
                token_string = line[start_pointer:last_successful_pointer]
                token_type = get_token_type(token_string)
                token = create_token(string=token_string, token_type=token_type)
                tokens.append(token)
                # reset pointers
                start_pointer = last_successful_pointer
                end_pointer = start_pointer
                last_successful_pointer = None

        end_pointer += 1
    
    # after scanning, there should be one token left at the end
    # if the remaining string is not a valid token, throw an exception
    remaining_string = line[start_pointer:end_pointer]
    token_type = get_token_type(remaining_string)
    print(f"remaining str= '{remaining_string}', type = {token_type}\n\tstart end= {start_pointer} {end_pointer}")
    if token_type != None:
        token = create_token(string=remaining_string, token_type=token_type)
        print(f"\tcreate token: '{token_string}', type: {token_type}")
        tokens.append(token)
    else:
        raise Exception(f"Invalid token(s) on following line:\n\t{line}")

    return tokens

def convert_lines_of_code_into_tokens(lines:list) -> list:
    '''Takes a list of lines of code, returns list of tokens.'''
    tokens = []
    for line in lines:
        line_tokens = convert_line_into_tokens(line)
        tokens.extend(line_tokens)
    
    return tokens