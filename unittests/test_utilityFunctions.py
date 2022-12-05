import unittest

# test imports
import utilityFunctions

class TestUtilityFunctions(unittest.TestCase):
    
    def test_TimeIntToStr_unitless(self):
        seconds = [42, 155, 4897, 94518]
        expected = ['0:00:00:42','0:00:02:35','0:01:21:37','1:02:15:18']
        results = []
        for s in seconds:
            results.append(utilityFunctions.TimeIntToStr(s, False))
            
        self.assertEqual(results[0], expected[0])
        self.assertEqual(results[1], expected[1])
        self.assertEqual(results[2], expected[2])
        self.assertEqual(results[3], expected[3])
        
    def test_TimeIntToStr_units(self):
        seconds = [1, 42, 117, 4897, 93678, 195273]
        expected = \
            [
                '1 second',
                '42 seconds',
                '1 minute, 57 seconds',
                '1 hour, 21 minutes, 37 seconds',
                '1 day, 2 hours, 1 minute, 18 seconds',
                '2 days, 6 hours, 14 minutes, 33 seconds'
            ]
        results = []
        for s in seconds:
            results.append(utilityFunctions.TimeIntToStr(s)) # using the default value
            
        self.assertEqual(results[0], expected[0])
        self.assertEqual(results[1], expected[1])
        self.assertEqual(results[2], expected[2])
        self.assertEqual(results[3], expected[3])
        self.assertEqual(results[4], expected[4])
        self.assertEqual(results[5], expected[5])
        
if __name__ == '__main__':
    unittest.main()