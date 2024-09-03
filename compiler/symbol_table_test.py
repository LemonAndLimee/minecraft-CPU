import unittest

import symbol_table as st

class TestSymbolTableClasses(unittest.TestCase):
    def test_create_var_entry(self):
        entry = st.SymbolTableEntryVariable(memory_addr=0, data_type=st.DATA_TYPES["CHAR"])
        self.assertEqual(entry.entry_type, st.ENTRY_TYPES["VAR"])
        self.assertEqual(entry.is_accessed, False)
    def test_create_const_entry(self):
        entry = st.SymbolTableEntryConst(memory_addr=0, data_type=st.DATA_TYPES["CHAR"], const_value=1)
        self.assertEqual(entry.entry_type, st.ENTRY_TYPES["CONST"])
        self.assertEqual(entry.const_value, 1)
    def test_get_set_entry_to_table(self):
        entry = st.SymbolTableEntryVariable(memory_addr=0, data_type=st.DATA_TYPES["CHAR"])
        table = st.SymbolTable()
        table.add_symbol_table_entry(identifier="x", entry=entry)
        self.assertEqual(table.get_entry_from_id("x"), entry)
    def test_get_set_entry_to_node(self):
        entry = st.SymbolTableEntryVariable(memory_addr=0, data_type=st.DATA_TYPES["CHAR"])
        node = st.SymbolTableTreeNode()
        node.add_symbol_table_entry(identifier="x", entry=entry)
        self.assertEqual(node.get_entry_from_id("x"), entry)
    def test_create_child_node(self):
        node = st.SymbolTableTreeNode()
        token = st.Token(type="FOR")
        child = node.create_child(token=token)
        self.assertEqual(child.parent_node, node)
        self.assertEqual(child, node.child_nodes[token])