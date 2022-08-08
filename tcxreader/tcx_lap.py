from tcxreader.tcx_track_point import TCXTrackPoint
from datetime import datetime
from typing import List


class TCXLap:
    def __init__(self, trackpoints: List[TCXTrackPoint] = None, calories: int = None,
                 hr_avg: float = None, hr_max: float = None, hr_min=None, max_speed: float = None,
                 avg_speed: float = None, start_time: datetime = None, end_time: datetime = None,
                 duration: float = None, cadence_avg: float = None, cadence_max: float = None, ascent: float = None,
                 descent: float = None, distance: float = None, altitude_avg: float = None, altitude_min: float = None,
                 altitude_max: float = None, lx_ext:dict = None, tpx_ext_stats: dict = None,
                 ):
        """
        Similar to TCXExercise, but is a container class for a lap.
        :param tpx_ext_stats: contains statistics (min, max, avg) of TPX extenstion data of trackpoints
        :param lx_ext: contains LX extension data
        :param trackpoints: List of TCXTrackPoint objects
        :param calories: total calories used in an exercise
        :param hr_avg: maxiumum heartrate achieved during the exercise
        :param hr_max: average heartrate during the exercise
        :param hr_min: minimum heartrate achieved during the exercise
        :param avg_speed: average speed during the exercise (km/h)
        :param start_time: datetime of exercise start
        :param end_time: datetime of exercise end
        :param duration: duration of exercise in seconds
        :param cadence_avg: average cadence during the exercise
        :param cadence_max: maximum cadence during the exercise
        :param ascent: total meters of ascent during the exercise
        :param descent: total meters of descent during the exercise
        :param distance: total distance of exercise in meters
        :param altitude_avg: average altitude in meters
        :param altitude_min: minimum altitude during the exercise
        :param altitude_max: maxiumum altitude during the exersice

        """

        self.trackpoints:List[TCXTrackPoint] = trackpoints
        self.calories:int = calories
        self.hr_avg:float = hr_avg
        self.hr_max:int = hr_max
        self.hr_min:int = hr_min
        self.duration = duration
        self.max_speed:float = max_speed
        self.avg_speed:float = avg_speed
        self.start_time = start_time
        self.end_time = end_time
        self.cadence_avg = cadence_avg
        self.cadence_max = cadence_max
        self.ascent = ascent
        self.descent = descent
        self.distance = distance
        self.altitude_avg = altitude_avg
        self.altitude_min = altitude_min
        self.altitude_max = altitude_max
        self.tpx_ext_stats:dict = tpx_ext_stats
        if self.tpx_ext_stats==None:
            self.tpx_ext_stats={}
        self.lx_ext:dict = lx_ext
        if self.lx_ext==None:
            self.lx_ext={}
