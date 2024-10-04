import unittest
from src.symbol_table import *

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
    def test_get_entry(self):
        '''Test SymbolTable get_entry() method'''
        table = SymbolTable()
        entry = StEntryVar(memory_addr=0, data_type="CHAR")
        table.table["test1"] = entry
        
        self.assertEqual(table.get_entry("test1"), entry)
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