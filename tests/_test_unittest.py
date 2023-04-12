################################################################################
# Copyright © 2023 The Board of Trustees of the University of Illinois
#
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import unittest

## test imports ----------------------------------------------------------------
from extronlib.system import Wait
## -----------------------------------------------------------------------------

class Unittest_TestClass(unittest.TestCase): # rename for module to be tested
    
    def test_Success(self):
        self.assertEqual(1, 1)
        
    def test_Failure(self): 
        self.assertEqual(1, 2)
        
    def test_Wait_Decorator(self):
        @Wait(1)
        def WaitHandler():
            self.assertEqual(1, 2)
    
    def wait_callable(self):
        self.assertEqual(1, 1)
        
    def test_Wait_Callable(self):
        Wait(1, self.wait_callable)
    
if __name__ == '__main__':
    unittest.main()