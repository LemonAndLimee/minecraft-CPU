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