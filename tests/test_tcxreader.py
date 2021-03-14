import os
from unittest import TestCase
from tcxreader.tcxreader import TCXReader, TCXTrackPoint, TCXExercise


class TestTCXReader(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", '15.tcx')
        self.tcx = TCXReader().read(filename)

    def test_distance(self):
        self.assertEqual(self.tcx.distance, 116366.98)

    def test_duration(self):
        self.assertEqual(self.tcx.duration, 17250.0)
                
    def test_calories(self):
        self.assertEqual(self.tcx.calories, 2010)
        
    def test_hr_avg(self):
        self.assertEqual(int(self.tcx.hr_avg), 140)
        
    def test_hr_max(self):
        self.assertEqual(self.tcx.hr_max, None)        

    def test_hr_min(self):
        self.assertEqual(self.tcx.hr_min, 94)  
        
    def altitude_avg(self):
        self.assertEqual(self.tcx.altitude_avg, None)  

    def test_altitude_min(self):
        self.assertAlmostEqual(self.tcx.altitude_min, -5.4, places=1)  
        
    def test_ascent(self):
        self.assertAlmostEqual(self.tcx.ascent, 1404.4, places=1)          

    def test_descent(self):
        self.assertAlmostEqual(self.tcx.descent, 1422.0, places=1)
