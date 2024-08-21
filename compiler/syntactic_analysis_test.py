import unittest

import lexical_analysis as la
import syntactic_analysis as sa

class TestPrintAST(unittest.TestCase):
    def test_print_single_ast_node(self):
        line = "a+b"
        tokens = la.convert_into_tokens(line)
        node = sa.AST_node(operator=tokens[1], child_nodes=[tokens[0], tokens[2]])
        node_string = str(node)
        expected_string = f"{str(tokens[1])}\n{str(tokens[0])}\n{str(tokens[2])}"
        self.assertEqual(node_string, expected_string)
    
    def test_print_not_node(self):
        line = "!a"
        tokens = la.convert_into_tokens(line)
        node = sa.AST_node(operator=tokens[0], child_nodes=[tokens[1]])
        node_string = str(node)
        expected_string = f"{str(tokens[0])}\n{str(tokens[1])}"
        self.assertEqual(node_string, expected_string)
    
    def test_print_multiple_nodes(self):
        token_a = la.create_token(string="a", token_type="ID")
        token_b = la.create_token(string="b", token_type="ID")
        token_plus = la.create_token(string="+", token_type="PLUS_MINUS")
        token_mult = la.create_token(string="*", token_type="MULT_DIVIDE")

        node1 = sa.AST_node(operator=token_mult, child_nodes=[token_a, token_b])
        node2 = sa.AST_node(operator=token_mult, child_nodes=[token_b, token_a])
        root_node = sa.AST_node(operator=token_plus, child_nodes=[node1, node2])
        node_string = str(root_node)

        expected_string = f"{str(token_plus)}\n{str(token_mult)}\n{str(token_a)}\n{str(token_b)}\n{str(token_mult)}\n{str(token_b)}\n{str(token_a)}"
        self.assertEqual(node_string, expected_string)

class TestGetAST(unittest.TestCase):
    def test_get_single_expression_node(self):
        tokens = [
            la.create_token(string="a", token_type="ID"),
            la.create_token(string="+", token_type="PLUS_MINUS"),
            la.create_token(string="b", token_type="ID")
        ]
        ast_generator = sa.AST_generator(tokens=tokens, start_symbol="logical")
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        expected_string = f"{str(tokens[1])}\n{str(tokens[0])}\n{str(tokens[2])}"

        self.assertEqual(node_string, expected_string)

    def test_get_complex_expression(self):
        '''test expression: (a+b)*a^b+a, expect in order ((a+b)*(a^b))+a'''
        line = "(a+b)*a^b+a"
        tokens = la.convert_into_tokens(line)

        ast_generator = sa.AST_generator(tokens=tokens, start_symbol="logical")
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        token_a = la.create_token(string="a", token_type="ID")
        token_b = la.create_token(string="b", token_type="ID")
        token_plus = la.create_token(string="+", token_type="PLUS_MINUS")
        token_mult = la.create_token(string="*", token_type="MULT_DIVIDE")
        token_exp = la.create_token(string="^", token_type="EXP")

        expected_string = f"{str(token_plus)}\n{str(token_mult)}\n{str(token_plus)}\n{str(token_a)}\n{str(token_b)}"
        expected_string = expected_string + f"\n{str(token_exp)}\n{str(token_a)}\n{str(token_b)}\n{str(token_a)}"

        self.assertEqual(node_string, expected_string)
    
    def test_get_comparison(self):
        line = "a >= a+b"
        tokens = la.convert_into_tokens(line)

        ast_generator = sa.AST_generator(tokens=tokens, start_symbol="logical")
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        token_a = la.create_token(string="a", token_type="ID")
        token_b = la.create_token(string="b", token_type="ID")
        token_plus = la.create_token(string="+", token_type="PLUS_MINUS")
        token_comp = la.create_token(string=">=", token_type="COMPARISON")

        expected_string = f"{str(token_comp)}\n{str(token_a)}\n{str(token_plus)}\n{str(token_a)}\n{str(token_b)}"

        self.assertEqual(node_string, expected_string)
    
    def test_get_logical(self):
        line = "a && a+b"
        tokens = la.convert_into_tokens(line)

        ast_generator = sa.AST_generator(tokens=tokens, start_symbol="logical")
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        token_a = la.create_token(string="a", token_type="ID")
        token_b = la.create_token(string="b", token_type="ID")
        token_plus = la.create_token(string="+", token_type="PLUS_MINUS")
        token_and = la.create_token(string="&&", token_type="LOGICAL_OP")

        expected_string = f"{str(token_and)}\n{str(token_a)}\n{str(token_plus)}\n{str(token_a)}\n{str(token_b)}"

        self.assertEqual(node_string, expected_string)
    
    def test_get_not(self):
        line = "!a"
        tokens = la.convert_into_tokens(line)

        ast_generator = sa.AST_generator(tokens=tokens, start_symbol="logical")
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        token_a = la.create_token(string="a", token_type="ID")
        token_not = la.create_token(string="!", token_type="NOT")

        expected_string = f"{str(token_not)}\n{str(token_a)}"

        self.assertEqual(node_string, expected_string)
    
    def test_get_statement(self):
        line = "char x = a*a;"
        tokens = la.convert_into_tokens(line)

        ast_generator = sa.AST_generator(tokens=tokens, start_symbol="statement")
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        token_a = la.create_token(string="a", token_type="ID")
        token_x = la.create_token(string="x", token_type="ID")
        token_assign = la.create_token(string="=", token_type="ASSIGN")
        token_mult = la.create_token(string="*", token_type="MULT_DIVIDE")
        token_type = la.create_token(string="char", token_type="TYPE")

        expected_string = f"{str(token_assign)}\n{str(token_type)}\n{str(token_x)}\n{str(token_mult)}\n{str(token_a)}\n{str(token_a)}"

        self.assertEqual(node_string, expected_string)