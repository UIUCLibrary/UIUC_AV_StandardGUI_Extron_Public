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

## -----------------------------------------------------------------------------

class Class_TestClass(unittest.TestCase): # rename for module to be tested
    def setUp(self) -> None:
        self.TestClass = someClass
        return super().setUp()
    
    def test_Class_Properties(self): 
        # Property
        with self.subTest(param='Property'):
            self.assertIsInstance(self.TestClass.Property, PropertyClass)
            
    def test_Class_PRIV_Properties(self):
        # __PrivProp
        with self.subTest(param='__PrivProp'):
            self.assertIsInstance(self.TestClass._someClass__PrivProp, PrivPropClass)
            
    def test_Class_EventHandler_TestHandler(self):
        btnList = []
        actList = []
        
        for btn in btnList:
            for act in actList:
                with self.subTest(button=btn.Name, action=act):
                    try:
                        self.TestClass._someClass__TestHandler(btn, act)
                    except Exception as inst:
                        self.fail('__TestHandler raised {} unexpectedly!'.format(type(inst)))
    
    def test_Class_PRIV_Method(self):
        try:
            self.TestClass._someClass__Method()
        except Exception as inst:
            self.fail('__Method raised {} unexpectedly!'.format(type(inst)))
    
    def test_Class_Method(self):
        try:
            self.TestClass.Method()
        except Exception as inst:
            self.fail('Method raised {} unexpectedly!'.format(type(inst)))
    
if __name__ == '__main__':
    unittest.main()