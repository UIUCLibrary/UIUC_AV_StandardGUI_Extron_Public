import unittest

## test imports ----------------------------------------------------------------
import main
## -----------------------------------------------------------------------------

class Main_TestClass(unittest.TestCase):
    
    def test_Initilize(self):
        self.assertTrue(main.Initialize())
    
if __name__ == '__main__':
    unittest.main()