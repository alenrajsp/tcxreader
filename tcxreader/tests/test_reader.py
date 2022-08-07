import os
from unittest import TestCase
from tcxreader.tcxreader import TCXTrackPoint, TCXExercise
from tcxreader.tcxreader import TCXReader


class TestTCXReader(TestCase):
    def setUp(self):
        filename_1 = os.path.join(os.path.dirname(__file__), "data", '15.tcx')
        filename_2 = os.path.join(os.path.dirname(__file__), "data", 'sup_activity_1.tcx')
        self.tcx:TCXExercise = TCXReader().read(filename_1)
        self.tcx_sup:TCXExercise = TCXReader().read(filename_2)

    def test_distance(self):
        self.assertEqual(self.tcx.distance, 116366.98)

    def test_duration(self):
        self.assertEqual(self.tcx.duration, 17250.0)

    def test_calories(self):
        self.assertEqual(self.tcx.calories, 2010)

    def test_hr_avg(self):
        self.assertEqual(int(self.tcx.hr_avg), 140)

    def test_hr_max(self):
        self.assertEqual(self.tcx.hr_max, 200)

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

    def test_author(self):
        self.assertEqual(self.tcx_sup.author.name, "Connect Api")
        self.assertEqual(self.tcx.author.version_major, 17)
        self.assertEqual(self.tcx.author.version_minor, 20)
        self.assertEqual(self.tcx.author.build_major, 0)
        self.assertEqual(self.tcx.author.build_minor, 0)

    def test_tpx_ext_stats(self):
        self.assertAlmostEqual(self.tcx.tpx_ext_stats['Speed']['max'], 18.95800018310547, places=10)