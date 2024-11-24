from src.token import *

def get_non_whitespace_tokens(tokens:list[Token]) ->list[Token]:
    '''Takes a list of tokens and returns it without any whitespace tokens.'''
    new_list = []
    for token in tokens:
        if token.type != "WHITESPACE":
            new_list.append(token)
    return new_list

def convert_into_tokens(input) -> list[Token]:
    '''Converts a line or list of lines of code into a list of tokens, ignoring whitespace.'''
    if type(input) == str:
        line = input
        tokens = []
        # if empty line or commented line, return no tokens
        if len(line) == 0 or line[:2] == "//":
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
        
        # after scanning, there should be one token left at the end, unless the string only had 1
        # if the remaining string is not a valid token, throw an exception
        remaining_string = line[start_pointer:end_pointer]
        if len(remaining_string) > 0:
            token_type = get_token_type(remaining_string)
            if token_type != None:
                token = create_token(string=remaining_string, token_type=token_type)
                tokens.append(token)
            else:
                raise Exception(f"Invalid token(s) on following line:\n\t{line}")

        non_whitespace_list = get_non_whitespace_tokens(tokens)

        return non_whitespace_list
    
    elif type(input) == list:
        lines = input
        tokens = []
        for line in lines:
            line_tokens = convert_into_tokens(line)
            tokens.extend(line_tokens)
        
        return tokens
    
    else:
        raise Exception("Invalid input type: must be str or list")
