from fast_test import get_single_item, get_mode
import unittest
import os

class TestMain(unittest.TestCase):
    def test_get_single_item_test(self):
        print(get_single_item(0))
        self.assertEqual("string",get_single_item(0)["text"])
        self.assertEqual(True,get_single_item(0)["is_done"])
        self.assertEqual(1.7,get_single_item(0)["price"])

    def test_get_env(self):
        self.assertEqual(os.environ.get("MODE"),get_mode())

#commenting
         
if __name__ =="__main__":
    unittest.main()