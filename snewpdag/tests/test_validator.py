'''
Unit tests for Validator plugin
'''
from snewpdag.values.History import History
import unittest
import numpy as np
from snewpdag.dag import Node
from snewpdag.plugins import ValidateKey
from snewpdag.plugins import ValidateKeyType
from snewpdag.plugins import ValidateListType
from snewpdag.plugins import ValidateSort

class TestValidator(unittest.TestCase):
    
    def test_plugin0(self):
        h1 = ValidateKey(search_key = 'action', name = 'val0')
        h2 = ValidateKeyType(key_type = 'str', name = 'val1')
        data = [
            {'action': 'alert'},
            {'dt': 1.0},
        ]
        print('-----Test1-----')
        self.assertEqual(h1.check_key(data[0]), True)
        self.assertEqual(h1.check_key(data[1]), False)
        self.assertEqual(h1.alert(data[0]), True)
        self.assertEqual(h1.alert(data[1]), False)

        self.assertEqual(h2.check_type(data[0]['action']), True)
        self.assertEqual(h2.alert(data[0]['action']), True)
    
    def test_plugin1(self):
        h1 = ValidateKey(search_key = 'dt', name = 'val0')
        h2 = ValidateKeyType(key_type = 'float', name = 'va1')
        data = [
            {'action': 'alert'},
            {'dt': 1.0},
        ]
        print('\n-----Test2-----')
        self.assertEqual(h1.check_key(data[0]), False)
        self.assertEqual(h1.check_key(data[1]), True)
        self.assertEqual(h2.check_type(data[1]['dt']), True)
    
    def test_plugin2(self):
        h1 = History()
        h1.append('Input1')
        h2 = ValidateKeyType(key_type = 'History', name = 'val0')
        data = [
            {'history': h1},
        ]
        print('\n-----Test3-----')
        self.assertEqual(h2.check_type(data[0]['history']), True)
    
    def test_plugin3(self):
        h1 = ValidateListType(max_fraction = 0.1, key_type = 'float', name = 'val0')
        h2 = ValidateListType(max_fraction = 0.1, key_type = 'str', name = 'val1')
        data = [
            {'dt': [0.0, 1.0, 2.1, 'bug0', 'bug1', 4.0, 'bug2', 9.0, 2.4, 5.3]},
        ]
        print('\n-----Test4-----')
        self.assertEqual(h1.check_listtype(data[0]['dt']), False)
        self.assertEqual(h1.alert(data[0]['dt']), False)

        self.assertEqual(h2.check_listtype(data[0]['dt']), False)
        self.assertEqual(h2.alert(data[0]['dt']), False)
    
    def test_plugin4(self):
        h1 = ValidateListType(max_fraction = 0.1, key_type = 'float', name = 'val0')
        data = [
            {'dt': [0.0, 1.0, 2.1, 'bug0', 9.3, 4.0, 14.5, 9.0, 2.4, 5.3]},
            {'dt': [0.0, 1.0, 2.1, 'bug0', 'bug1', 9.3, 4.0, 14.5, 9.0, 2.4, 5.3, 18.0, 19.4, 20.3, 14.0, 9.3, 4.0, 14.5, 9.0, 2.4, 5.3]},
        ]
        print('\n-----Test5-----')
        self.assertEqual(h1.check_listtype(data[0]['dt']), [0.0, 1.0, 2.1, 9.3, 4.0, 14.5, 9.0, 2.4, 5.3])
        self.assertEqual(h1.check_listtype(data[1]['dt']), [0.0, 1.0, 2.1, 9.3, 4.0, 14.5, 9.0, 2.4, 5.3, 18.0, 19.4, 20.3, 14.0, 9.3, 4.0, 14.5, 9.0, 2.4, 5.3])
    
    def test_plugin5(self):
        h1 = ValidateSort(listorder = '', name = 'val0')
        data = [
            {'dt': [0.0, 0.5, 1.0, 3.2, 5.3]},
            {'dt': [5.3, 3.2, 1.0, 0.5, 0.0]},
            {'dt': [0.0, 1.0, 5.3, 3.2, 0.5]},
        ]
        print('\n-----Test6-----')
        self.assertEqual(h1.check_sorted(data[0]['dt']), 'ascending')
        self.assertEqual(h1.check_sorted(data[1]['dt']), 'descending')
        self.assertEqual(h1.check_sorted(data[2]['dt']), None)