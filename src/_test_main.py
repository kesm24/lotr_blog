import unittest

from main import main

class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main("Hello World"), "Hello World")