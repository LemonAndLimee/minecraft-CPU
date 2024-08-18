import unittest

import lexical_analysis as la

class TestGetTokenType(unittest.TestCase):
    def test_get_token_type_type(self):
        token_type = la.get_token_type("char")
        self.assertEqual(token_type, "TYPE", "get_token_type() failed on input 'char'")
        token_type = la.get_token_type("bool")
        self.assertEqual(token_type, "TYPE", "get_token_type() failed on input 'bool'")

    def test_get_token_type_assign(self):
        token_type = la.get_token_type("=")
        self.assertEqual(token_type, "ASSIGN", "get_token_type() failed on input '='")
    
    def test_get_token_type_char(self):
        token_type = la.get_token_type("'a'")
        self.assertEqual(token_type, "CHAR", "get_token_type() failed on input ''a''")
        token_type = la.get_token_type("'\n'")
        self.assertEqual(token_type, "CHAR", "get_token_type() failed on input '\\n'")
        token_type = la.get_token_type("3")
        self.assertEqual(token_type, "CHAR", "get_token_type() failed on input '3'")
    
    def test_get_token_type_bool(self):
        token_type = la.get_token_type("True")
        self.assertEqual(token_type, "BOOL", "get_token_type() failed on input 'True'")
        token_type = la.get_token_type("False")
        self.assertEqual(token_type, "BOOL", "get_token_type() failed on input 'False'")

    def test_get_token_type_if(self):
        token_type = la.get_token_type("if")
        self.assertEqual(token_type, "IF", "get_token_type() failed on input 'if'")
    
    def test_get_token_type_else(self):
        token_type = la.get_token_type("else")
        self.assertEqual(token_type, "ELSE", "get_token_type() failed on input 'else'")
    
    def test_get_token_type_while(self):
        token_type = la.get_token_type("while")
        self.assertEqual(token_type, "WHILE", "get_token_type() failed on input 'while'")
    
    def test_get_token_type_for(self):
        token_type = la.get_token_type("for")
        self.assertEqual(token_type, "FOR", "get_token_type() failed on input 'for'")

    def test_get_token_type_id(self):
        token_type = la.get_token_type("x")
        self.assertEqual(token_type, "ID", "get_token_type() failed on input 'x'")
        token_type = la.get_token_type("variable_1")
        self.assertEqual(token_type, "ID", "get_token_type() failed on input 'variable_1'")
    
    def test_get_token_type_arithmetic(self):
        token_type = la.get_token_type("+")
        self.assertEqual(token_type, "ARITHMETIC", "get_token_type() failed on input '+'")
        token_type = la.get_token_type("-")
        self.assertEqual(token_type, "ARITHMETIC", "get_token_type() failed on input '-'")
        token_type = la.get_token_type("*")
        self.assertEqual(token_type, "ARITHMETIC", "get_token_type() failed on input '*'")
        token_type = la.get_token_type("/")
        self.assertEqual(token_type, "ARITHMETIC", "get_token_type() failed on input '/'")
        token_type = la.get_token_type("^")
        self.assertEqual(token_type, "ARITHMETIC", "get_token_type() failed on input '^'")
        token_type = la.get_token_type("%")
        self.assertEqual(token_type, "ARITHMETIC", "get_token_type() failed on input '%'")
    
    def test_get_token_type_logical(self):
        token_type = la.get_token_type("==")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '=='")
        token_type = la.get_token_type("!=")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '!='")
        token_type = la.get_token_type("<=")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '<='")
        token_type = la.get_token_type(">=")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '>='")
        token_type = la.get_token_type("<")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '<'")
        token_type = la.get_token_type(">")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '>'")
        token_type = la.get_token_type("!")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '!'")
        token_type = la.get_token_type("||")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '||'")
        token_type = la.get_token_type("&&")
        self.assertEqual(token_type, "LOGICAL", "get_token_type() failed on input '&&'")

    def test_get_token_type_parentheses(self):
        token_type = la.get_token_type("(")
        self.assertEqual(token_type, "(", "get_token_type() failed on input '('")
        token_type = la.get_token_type(")")
        self.assertEqual(token_type, ")", "get_token_type() failed on input ')'")

    def test_get_token_type_curly_brackets(self):
        token_type = la.get_token_type("{")
        self.assertEqual(token_type, "{", "get_token_type() failed on input '{'")
        token_type = la.get_token_type("}")
        self.assertEqual(token_type, "}", "get_token_type() failed on input '}'")
    
    def test_get_token_type_semicolon(self):
        token_type = la.get_token_type(";")
        self.assertEqual(token_type, ";", "get_token_type() failed on input ';'")
    
    def test_get_token_type_whitespace(self):
        token_type = la.get_token_type(" ")
        self.assertEqual(token_type, "WHITESPACE", "get_token_type() failed on input ' '")
        token_type = la.get_token_type("\n")
        self.assertEqual(token_type, "WHITESPACE", "get_token_type() failed on input '\\n'")
        token_type = la.get_token_type("\t")
        self.assertEqual(token_type, "WHITESPACE", "get_token_type() failed on input '\\t'")

class TestCreateToken(unittest.TestCase):
    def test_create_type(self):
        created_token = la.create_token(string="char", token_type="TYPE")
        self.assertEqual(created_token.type, "TYPE", "create_token() type failed on input 'char'")
        self.assertEqual(created_token.value, "char", "create_token() value failed on input 'char'")
    def test_create_assign(self):
        created_token = la.create_token(string="=", token_type="ASSIGN")
        self.assertEqual(created_token.type, "ASSIGN", "create_token() type failed on input '='")
        self.assertIsNone(created_token.value, "create_token() value failed on input '='")
    def test_create_char(self):
        created_token = la.create_token(string="'a'", token_type="CHAR")
        self.assertEqual(created_token.type, "CHAR", "create_token() type failed on input ''a''")
        self.assertEqual(created_token.value, "'a'", "create_token() value failed on input ''a''")
        created_token = la.create_token(string="1", token_type="CHAR")
        self.assertEqual(created_token.type, "CHAR", "create_token() type failed on input '1'")
        self.assertEqual(created_token.value, "1", "create_token() value failed on input '1'")
    def test_create_bool(self):
        created_token = la.create_token(string="True", token_type="BOOL")
        self.assertEqual(created_token.type, "BOOL", "create_token() type failed on input 'True'")
        self.assertEqual(created_token.value, "True", "create_token() value failed on input 'True'")
    def test_create_if(self):
        created_token = la.create_token(string="if", token_type="IF")
        self.assertEqual(created_token.type, "IF", "create_token() type failed on input 'if'")
        self.assertIsNone(created_token.value, "create_token() value failed on input 'if'")
    def test_create_else(self):
        created_token = la.create_token(string="else", token_type="ELSE")
        self.assertEqual(created_token.type, "ELSE", "create_token() type failed on input 'else'")
        self.assertIsNone(created_token.value, "create_token() value failed on input 'else'")
    def test_create_while(self):
        created_token = la.create_token(string="while", token_type="WHILE")
        self.assertEqual(created_token.type, "WHILE", "create_token() type failed on input 'while'")
        self.assertIsNone(created_token.value, "create_token() value failed on input 'while'")
    def test_create_for(self):
        created_token = la.create_token(string="for", token_type="FOR")
        self.assertEqual(created_token.type, "FOR", "create_token() type failed on input 'for'")
        self.assertIsNone(created_token.value, "create_token() value failed on input 'for'")
    def test_create_id(self):
        created_token = la.create_token(string="var1", token_type="ID")
        self.assertEqual(created_token.type, "ID", "create_token() type failed on input 'var1'")
        self.assertEqual(created_token.value, "var1", "create_token() value failed on input 'var1'")
    def test_create_arithmetic(self):
        created_token = la.create_token(string="+", token_type="ARITHMETIC")
        self.assertEqual(created_token.type, "ARITHMETIC", "create_token() type failed on input '+'")
        self.assertEqual(created_token.value, "+", "create_token() value failed on input '+'")
    def test_create_logical(self):
        created_token = la.create_token(string="==", token_type="LOGICAL")
        self.assertEqual(created_token.type, "LOGICAL", "create_token() type failed on input '=='")
        self.assertEqual(created_token.value, "==", "create_token() value failed on input '=='")
    def test_create_left_parens(self):
        created_token = la.create_token(string="(", token_type="(")
        self.assertEqual(created_token.type, "(", "create_token() type failed on input '('")
        self.assertIsNone(created_token.value, "create_token() value failed on input '('")
    def test_create_right_parens(self):
        created_token = la.create_token(string=")", token_type=")")
        self.assertEqual(created_token.type, ")", "create_token() type failed on input ')'")
        self.assertIsNone(created_token.value, "create_token() value failed on input ')'")
    def test_create_left_brace(self):
        created_token = la.create_token(string="{", token_type="{")
        self.assertEqual(created_token.type, "{", "create_token() type failed on input '{'")
        self.assertIsNone(created_token.value, "create_token() value failed on input '{'")
    def test_create_right_brace(self):
        created_token = la.create_token(string="}", token_type="}")
        self.assertEqual(created_token.type, "}", "create_token() type failed on input '}'")
        self.assertIsNone(created_token.value, "create_token() value failed on input '}'")
    def test_create_semicolon(self):
        created_token = la.create_token(string=";", token_type=";")
        self.assertEqual(created_token.type, ";", "create_token() type failed on input ';'")
        self.assertIsNone(created_token.value, "create_token() value failed on input ';'")
    def test_create_whitespace(self):
        created_token = la.create_token(string=" ", token_type="WHITESPACE")
        self.assertEqual(created_token.type, "WHITESPACE", "create_token() type failed on input ' '")
        self.assertIsNone(created_token.value, "create_token() value failed on input ' '")

class TestConvertIntoTokens(unittest.TestCase):
    def test_convert_line(self):
        line = "char x = a + (2*b - 3);"
        tokens = la.convert_into_tokens(line)
        types = []
        for token in tokens:
            types.append(token.type)
        expected_types = ["TYPE", "ID", "ASSIGN", "ID", "ARITHMETIC", "(", "CHAR",
                          "ARITHMETIC", "ID", "ARITHMETIC", "CHAR", ")", ";"]
        self.assertListEqual(types, expected_types)

    def test_convert_single_token_line(self):
        line = "}"
        tokens = la.convert_into_tokens(line)
        types = []
        for token in tokens:
            types.append(token.type)
        expected_types = ["}"]
        self.assertListEqual(types, expected_types)
    
    def test_convert_space_char(self):
        line = "' '"
        tokens = la.convert_into_tokens(line)
        types = []
        for token in tokens:
            types.append(token.type)
        expected_types = ["CHAR"]
        self.assertListEqual(types, expected_types)
    
    def test_convert_for_loop_line(self):
        line = "for (char i = 0; i < 3; i = i+1) {"
        tokens = la.convert_into_tokens(line)
        types = []
        for token in tokens:
            types.append(token.type)
        expected_types = [
            "FOR", "(", "TYPE", "ID", "ASSIGN", "CHAR", ";", "ID", "LOGICAL",
            "CHAR", ";", "ID", "ASSIGN", "ID", "ARITHMETIC", "CHAR", ")", "{"
            ]
        self.assertListEqual(types, expected_types)

    def test_convert_multiline(self):
        lines = [
            "char x = 0;",
            "for (char i = 0; i < 3; i = i+1) {",
            "if (i % 2 == 0) {",
            "x = x + i;",
            "}",
            "}"
        ]
        tokens = la.convert_into_tokens(lines)
        types = []
        for token in tokens:
            types.append(token.type)
        expected_types = [
            "TYPE", "ID", "ASSIGN", "CHAR", ";",
            "FOR", "(", "TYPE", "ID", "ASSIGN", "CHAR", ";", "ID", "LOGICAL",
            "CHAR", ";", "ID", "ASSIGN", "ID", "ARITHMETIC", "CHAR", ")", "{",
            "IF", "(", "ID", "ARITHMETIC", "CHAR", "LOGICAL", "CHAR", ")", "{",
            "ID", "ASSIGN", "ID", "ARITHMETIC", "ID", ";",
            "}", "}"
        ]
        self.assertListEqual(types, expected_types)

if __name__ == "main":
    unittest.main()