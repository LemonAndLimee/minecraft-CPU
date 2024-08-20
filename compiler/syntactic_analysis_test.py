import unittest

import lexical_analysis as la
import syntactic_analysis as sa

class TestPrintAST(unittest.TestCase):
    def test_print_single_ast_node(self):
        node = sa.AST_node(left="a", operator="+", right="b")
        node_string = str(node)
        expected_string = "+ a b"
        self.assertEqual(node_string, expected_string)
    
    def test_print_not_node(self):
        node = sa.AST_node(left="a", operator="!")
        node_string = str(node)
        expected_string = "! a"
        self.assertEqual(node_string, expected_string)
    
    def test_print_multiple_nodes(self):
        node1 = sa.AST_node(left="a", operator="*", right="b")
        exp_node = sa.AST_node(left="d", operator="^", right="2")
        node2 = sa.AST_node(left="c", operator="*", right=exp_node)
        root_node = sa.AST_node(left=node1, operator="+", right=node2)
        node_string = str(root_node)
        expected_string = "+ * a b * c ^ d 2"
        self.assertEqual(node_string, expected_string)

class TestGetAST(unittest.TestCase):
    def test_get_single_expression_node(self):
        tokens = [
            la.create_token(string="a", token_type="ID"),
            la.create_token(string="+", token_type="PLUS_MINUS"),
            la.create_token(string="b", token_type="ID")
        ]
        ast_generator = sa.AST_generator(tokens=tokens)
        node = ast_generator.generate_abstract_syntax_tree()
        node_string = str(node)

        expected_string = f"{str(tokens[1])}\n{str(tokens[0])}\n{str(tokens[2])}"

        self.assertEqual(node_string, expected_string)

    def test_get_complex_expression(self):
        '''test expression: (a+b)*a^b+a, expect in order ((a+b)*(a^b))+a'''
        line = "(a+b)*a^b+a"
        tokens = la.convert_into_tokens(line)

        ast_generator = sa.AST_generator(tokens=tokens)
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