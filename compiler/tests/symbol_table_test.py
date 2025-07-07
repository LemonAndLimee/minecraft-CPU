import unittest
from unittest.mock import MagicMock
from ..src.symbol_table import *

class TestEntryClasses(unittest.TestCase):
    def test_equality_var_entry(self):
        '''Test __eq__ method on StEntryVar class'''
        entry_1 = StEntryVar(memory_addr=0, data_type="CHAR")
        entry_2 = StEntryVar(memory_addr=0, data_type="CHAR")
        self.assertEqual(entry_1, entry_2)
        entry_1.is_accessed = True
        self.assertNotEqual(entry_1, entry_2)
    def test_equality_const_entry(self):
        '''Test __eq__ method on StEntryConst class'''
        entry_1 = StEntryConst(memory_addr=0, data_type="CHAR", const_value=2)
        entry_2 = StEntryConst(memory_addr=0, data_type="CHAR", const_value=2)
        self.assertEqual(entry_1, entry_2)
    def test_inequality_cross_entry_types(self):
        '''Test __eq__ method between different entry classes. It should be inequal but not result in error.'''
        entry_1 = StEntryVar(memory_addr=0, data_type="CHAR")
        entry_2 = StEntryConst(memory_addr=0, data_type="CHAR", const_value=2)
        try:
            self.assertNotEqual(entry_1, entry_2)
        except:
            self.fail("Inequality across entry types shouldn't result in an error.")
    def test_equality_with_none(self):
        '''Tests __eq__ when an entry is compared to None. It should not throw an error, but return False.'''
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        self.assertNotEqual(entry, None)
    def test_equality_with_other_datatype(self):
        '''Tests __eq__ when an entry is compared to other data type. It should raise an exception.'''
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        with self.assertRaises(TypeError):
            result = entry == 1
    
    def test_str_var_entry(self):
        '''Test __str__ method of StEntryVar class'''
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        expected_string = f"m_addr=0, d_type=CHAR, e_type=VAR, is_accessed=False"
        self.assertEqual(str(entry), expected_string)
    def test_str_const_entry(self):
        '''Test __str__ method of StEntryConst class'''
        entry = StEntryConst(memory_addr=0, data_type="CHAR", const_value=2)
        expected_string = f"m_addr=0, d_type=CHAR, e_type=CONST, const_val=2"
        self.assertEqual(str(entry), expected_string)
    
class TestSymbolTableClass(unittest.TestCase):
    def test_init(self):
        '''Test the __init__ method of the SymbolTable class'''
        table = SymbolTable()
        self.assertIsNone(table.parent)
        self.assertEqual(len(table.children), 0)
        self.assertEqual(len(table.table), 0)
    def test_equal(self):
        '''Test __eq__ method of the SymbolTable class. It only compares the table attribute.'''
        table_1 = SymbolTable()
        entry_1 = StEntryVar(memory_addr=0, data_type="CHAR")
        table_1.table["test"] = entry_1
        
        table_2 = SymbolTable()
        entry_2 = StEntryVar(memory_addr=0, data_type="CHAR")
        table_2.table["test"] = entry_2
        
        self.assertEqual(table_1, table_2)
    def test_not_equal(self):
        '''Test __eq__ method on non-equivalent tables.'''
        table_1 = SymbolTable()
        entry_1 = StEntryVar(memory_addr=0, data_type="CHAR")
        table_1.table["test"] = entry_1
        
        table_2 = SymbolTable()
        entry_2 = StEntryVar(memory_addr=3, data_type="CHAR")
        table_2.table["test"] = entry_2
        
        self.assertNotEqual(table_1, table_2)
    def test_str(self):
        '''Test __str__ method on SymbolTable class'''
        table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        table.table["test1"] = entry
        table.table["test2"] = entry
        
        expected_string = f"test1:[{str(entry)}],\ntest2:[{str(entry)}]"
        self.assertEqual(str(table), expected_string)
    def test_get_entry_in_current_table(self):
        '''Test SymbolTable get_entry() method. It should return an entry if it exists in current table or higher in tree.'''
        table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        table.table["test1"] = entry
        
        self.assertEqual(table.get_entry("test1"), entry)
    def test_get_entry_in_higher_table(self):
        '''Test SymbolTable get_entry() method. It should return an entry if it exists in current table or higher in tree.'''
        table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        table.table["test1"] = entry
        child_table = SymbolTable(parent=table)
        
        self.assertEqual(child_table.get_entry("test1"), entry)
    def test_get_const_entry_in_current_table(self):
        '''Test SymbolTable get_const_entry() method. It should return an entry if it exists in the root node table.'''
        table = SymbolTable()
        entry = StEntryConst(memory_addr=0, data_type="CHAR", const_value=3)
        table.table["test1"] = entry
        self.assertEqual(table.get_const_entry(3), entry)
    def test_get_const_entry_in_higher_table(self):
        '''Test SymbolTable get_const_entry() method. It should return an entry if it exists the root node table.'''
        table = SymbolTable()
        entry = StEntryConst(memory_addr=0, data_type="CHAR", const_value=3)
        table.table["test1"] = entry
        child_table = SymbolTable(parent=table)
        self.assertEqual(child_table.get_const_entry(3), entry)
    def test_get_nonexistent_entry(self):
        '''Test get_entry() method on non-existent entry. Should return None.'''
        table = SymbolTable()
        self.assertIsNone(table.get_entry("test1"))
    def test_add_entry(self):
        '''Test add_entry() method'''
        table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        table.add_entry("test1", entry)
        self.assertEqual(table.get_entry("test1"), entry)
    def test_add_existing_entry(self):
        '''Test add_entry() method on already existing entry. Should raise exception.'''
        table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        table.add_entry("test1", entry)
        self.assertRaises(Exception, table.add_entry, "test1", entry)
    def test_assign_child(self):
        '''Test assign_child() method'''
        table = SymbolTable()
        child_table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        child_table.add_entry("test1", entry)
        token = Token(type="IF")
        
        table.assign_child(token, child_table)
        self.assertEqual(table.children[token], child_table)
    def test_get_child(self):
        '''Test get_child() method'''
        table = SymbolTable()
        child_table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        child_table.add_entry("test1", entry)
        token = Token(type="IF")
        
        table.assign_child(token, child_table)
        self.assertEqual(table.get_child(token=token), child_table)
    def test_get_non_existent_child(self):
        '''Test get_child() method for a non existent child. Should return None.'''
        table = SymbolTable()
        token = Token(type="IF")
        
        self.assertEqual(table.get_child(token=token), None)
    def test_get_root_node(self):
        '''Test get_root_node() method'''
        table = SymbolTable()
        child_table = SymbolTable(parent=table)
        grandchild_table = SymbolTable(parent=child_table)
        
        self.assertEqual(grandchild_table.get_root_node(), table)

class TestSymbolTableGenerator(unittest.TestCase):
    def test_add_entry_var(self):
        '''Test SymbolTableGenerator add_var_entry() method.'''
        current_st = SymbolTable()
        generator = SymbolTableGenerator()
        data_type = "CHAR"
        name = "test1"
        generator.add_var_entry(table=current_st, data_type=data_type, name=name)
        
        entry = current_st.get_entry(name=name)
        expected_entry = StEntryVar(memory_addr=0, data_type=data_type)
        
        # check the entry was created and added to symbol table
        self.assertEqual(entry, expected_entry)
        # check the next memory address pointer was incremented
        self.assertEqual(generator.next_mem_addr, 1)
    
    def test_add_const_var(self):
        '''Test SymbolTableGenerator add_const_entry() method.'''
        current_st = SymbolTable()
        generator = SymbolTableGenerator()
        data_type = "CHAR"
        value = 3
        generator.add_const_entry(table=current_st, data_type=data_type, const_value=value)
        
        expected_entry = StEntryConst(memory_addr=0, data_type=data_type, const_value=value)
        expected_name = "const_0"
        entry = current_st.get_entry(name=expected_name)
        
        # check the entry was created and added to symbol table
        self.assertEqual(entry, expected_entry)
        # check the next memory address pointer was incremented
        self.assertEqual(generator.next_mem_addr, 1)
        # check the next const name pointer was incremented
        self.assertEqual(generator.next_const_name_ptr, 1)
    
    def test_memory_address_pointer(self):
        '''Tests an entry is assigned to the correct memory address, and that it is incremented after.'''
        current_st = SymbolTable()
        generator = SymbolTableGenerator(next_mem_addr=5)
        data_type = "CHAR"
        name = "test1"
        generator.add_var_entry(table=current_st, data_type=data_type, name=name)
        
        entry = current_st.get_entry(name=name)
        expected_entry = StEntryVar(memory_addr=5, data_type=data_type)
        
        # check the entry was created and added to symbol table, with a matching memory address
        self.assertEqual(entry, expected_entry)
        # check the next memory address pointer was incremented
        self.assertEqual(generator.next_mem_addr, 6)
    
    def test_process_token_new_const(self):
        '''Test the process_token() method with a const that has no existing entry. Checks the entry is added to the root table.'''
        root_st = SymbolTable()
        child_st = SymbolTable(parent=root_st)
        data_type = "CHAR"
        value = 3
        const_token = Token(type=data_type, value=value)

        generator = SymbolTableGenerator()
        generator.process_token(token=const_token, parent_node=None, current_st=child_st)
        
        expected_entry = StEntryConst(memory_addr=0, data_type=data_type, const_value=value)
        entry = root_st.get_const_entry(value=value)
        
        # check the entry was created and added to symbol table
        self.assertEqual(entry, expected_entry)
        # check the next memory address pointer was incremented
        self.assertEqual(generator.next_mem_addr, 1)
        # check the next const name pointer was incremented
        self.assertEqual(generator.next_const_name_ptr, 1)
    
    def test_process_token_new_var(self):
        '''Test the process_token() method with a var that has no existing entry. Checks the entry is added to the table.'''
        table = SymbolTable()
        data_type = "CHAR"
        name = "test1"
        id_token = Token(type="ID", value=name)
        parent_token = Token(type="TYPE", value=data_type)
        parent_node = AstNode(operator=parent_token, children=[id_token])

        generator = SymbolTableGenerator()
        original_mem_addr = generator.next_mem_addr
        original_const_ptr = generator.next_const_name_ptr
        generator.process_token(token=id_token, parent_node=parent_node, current_st=table)
        
        expected_entry = StEntryVar(memory_addr=0, data_type=data_type)
        entry = table.get_entry(name=name)
        
        # check the entry was created and added to symbol table
        self.assertEqual(entry, expected_entry, f"\nexpected = {str(expected_entry)}\nreceived = {str(entry)}")
        # check the next memory address pointer was incremented
        self.assertEqual(generator.next_mem_addr, original_mem_addr+1)
        # check the next const name pointer was not incremented
        self.assertEqual(generator.next_const_name_ptr, original_const_ptr)
    
    def test_process_token_new_var_no_decl(self):
        '''Test the process_token() method with a var that has no existing entry, and is not a declaration. Should raise exception.'''
        table = SymbolTable()
        name = "test1"
        id_token = Token(type="ID", value=name)
        parent_token = Token(type="ID", value="test2") # parent token not of type TYPE - not a declaration
        parent_node = AstNode(operator=parent_token, children=[id_token])

        generator = SymbolTableGenerator()
        with self.assertRaises(Exception):
            generator.process_token(token=id_token, parent_node=parent_node, current_st=table)
    
    def test_process_token_existing_var(self):
        '''Test the process_token() method with a var that has an existing entry. Assert that method assigns is_accessed to true.'''
        table = SymbolTable()
        name = "test1"
        data_type = "CHAR"
        id_token = Token(type="ID", value=name)
        entry = StEntryVar(memory_addr=0, data_type=data_type)
        table.add_entry(name=name, entry=entry)
        
        # assert that is_accessed is false before process_token() is method
        self.assertEqual(entry.is_accessed, False)
        
        parent_token = Token(type="=")
        parent_node = AstNode(operator=parent_token, children=[id_token])

        generator = SymbolTableGenerator()
        generator.process_token(token=id_token, parent_node=parent_node, current_st=table)
        # assert that is_accessed has now been changed to true
        retrieved_entry = table.get_entry(name=name)
        self.assertEqual(retrieved_entry.is_accessed, True, f"Retrieved entry: {str(retrieved_entry)}")
        
    
    def test_process_token_existing_var_invalid_etype(self):
        '''Test the process_token() method with a var whose name is already taken by a const entry. Assert error is raised.'''
        table = SymbolTable()
        name = "const_0" # this name will be already taken but the first const entry added
        data_type = "CHAR"
        id_token = Token(type="ID", value=name)
        
        const_entry = StEntryConst(memory_addr=0, data_type=data_type, const_value=0)
        table.add_entry(name=name, entry=const_entry)
        
        parent_token = Token(type="=")
        parent_node = AstNode(operator=parent_token, children=[id_token])

        generator = SymbolTableGenerator()
        with self.assertRaises(Exception):
            generator.process_token(token=id_token, parent_node=parent_node, current_st=table)
    
    def test_process_token_existing_var_decl(self):
        '''Test the process_token() method with a var that has an existing entry, in a declaration statement. Assert error is raised.'''
        table = SymbolTable()
        name = "test1"
        data_type = "CHAR"
        id_token = Token(type="ID", value=name)
        
        # create and add existing entry
        entry = StEntryVar(memory_addr=0, data_type=data_type)
        table.add_entry(name=name, entry=entry)
        
        # parent node is a declaration type
        parent_token = Token(type="TYPE", value=data_type)
        parent_node = AstNode(operator=parent_token, children=[id_token])

        generator = SymbolTableGenerator()
        with self.assertRaises(Exception):
            generator.process_token(token=id_token, parent_node=parent_node, current_st=table)
    
    def test_process_ast_node_scope_definer(self):
        '''Assert that process_ast_node() will create a child symbol table if given node is scope defining.'''
        scope_token = Token(type="IF")
        ast_node = AstNode(operator=scope_token)
        
        table = SymbolTable()
        generator = SymbolTableGenerator()
        
        # assert that table has no children
        self.assertEqual(len(table.children), 0)
        generator.process_ast_node(node=ast_node, current_st=table)
        
        # assert that table has 1 child
        self.assertEqual(len(table.children), 1)
        # assert that the child table has been added with the correct corresponding token
        # variable "table" is an empty table, thus the expected child table should be equal to it
        self.assertEqual(table.get_child(token=scope_token), table)
    
    def test_process_ast_node_misc_with_children(self):
        '''Assert that process_ast_node() will call traverse_ast() if given node is non scope defining, and has at least 1 child.'''
        child_token = Token(type="+")

        misc_token = Token(type="=")
        ast_node = AstNode(operator=misc_token, children=[child_token])
        
        table = SymbolTable()
        generator = SymbolTableGenerator()
        generator.traverse_ast = MagicMock()
        generator.process_ast_node(node=ast_node, current_st=table)
        # assert that traverse_ast is called
        generator.traverse_ast.assert_called_once_with(ast_parent_node=ast_node, current_st=table)
    
    def test_process_ast_node_misc_no_children(self):
        '''Assert that process_ast_node() will not call traverse_ast() if given node is non scope defining but has no children.'''
        misc_token = Token(type="=")
        ast_node = AstNode(operator=misc_token)
        
        table = SymbolTable()
        generator = SymbolTableGenerator()
        generator.traverse_ast = MagicMock()
        generator.process_ast_node(node=ast_node, current_st=table)
        # assert that traverse_ast is not called
        generator.traverse_ast.assert_not_called()
    
    def test_process_ast_node_call(self):
        '''Assert that a call to process_ast_object() with an ast node will result in a call to process_ast_node()'''
        token = Token(type="=")
        ast_node = AstNode(operator=token)
        
        table = SymbolTable()
        generator = SymbolTableGenerator()
        generator.process_ast_node = MagicMock()
        generator.process_ast_object(node=ast_node, parent_node=None, current_st=table)
        
        generator.process_ast_node.assert_called_once_with(node=ast_node, current_st=table)
    
    def test_process_token_call(self):
        '''Assert that a call to process_ast_object() with a token will result in a call to process_token()'''
        token = Token(type="=")
        
        table = SymbolTable()
        generator = SymbolTableGenerator()
        generator.process_token = MagicMock()
        generator.process_ast_object(node=token, parent_node=None, current_st=table)
        
        generator.process_token.assert_called_once_with(token=token, parent_node=None, current_st=table)