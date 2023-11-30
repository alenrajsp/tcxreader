from tcxreader.tcx_track_point import TCXTrackPoint
from datetime import datetime
from typing import List


class TCXLap:
    def __init__(self, trackpoints: List[TCXTrackPoint] = None, calories: int = None,
                 hr_avg: float = None, hr_max: int = None, hr_min: int = None, max_speed: float = None,
                 avg_speed: float = None, start_time: datetime = None, end_time: datetime = None,
                 duration: float = None, cadence_avg: float = None, cadence_max: float = None, ascent: float = None,
                 descent: float = None, distance: float = None, altitude_avg: float = None, altitude_min: float = None,
                 altitude_max: float = None, lx_ext: dict = None, tpx_ext_stats: dict = None,
                 ):
        """
        Similar to TCXExercise, but is a container class for a lap.
        :param tpx_ext_stats: Contains statistics (min, max, avg) of TPX extension data of trackpoints.
        :param lx_ext: Contains LX extension data.
        :param trackpoints: List of TCXTrackPoint objects.
        :param calories: Total calories used in an exercise.
        :param hr_avg: Maximum heartrate achieved during the exercise.
        :param hr_max: Average heartrate during the exercise.
        :param hr_min: Minimum heartrate achieved during the exercise.
        :param avg_speed: Average speed during the exercise (km/h).
        :param start_time: Datetime of exercise start.
        :param end_time: Datetime of exercise end.
        :param duration: Duration of exercise in seconds.
        :param cadence_avg: Average cadence during the exercise.
        :param cadence_max: Maximum cadence during the exercise.
        :param ascent: Total meters of ascent during the exercise.
        :param descent: Total meters of descent during the exercise.
        :param distance: Total distance of exercise in meters.
        :param altitude_avg: Average altitude in meters.
        :param altitude_min: Minimum altitude during the exercise.
        :param altitude_max: Maximum altitude during the exercise.

        """

        self.trackpoints: List[TCXTrackPoint] = trackpoints
        self.calories: int = calories
        self.hr_avg: float = hr_avg
        self.hr_max: int = hr_max
        self.hr_min: int = hr_min
        self.duration = duration
        self.max_speed: float = max_speed
        self.avg_speed: float = avg_speed
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.cadence_avg: float = cadence_avg
        self.cadence_max: float = cadence_max
        self.ascent: float = ascent
        self.descent: float = descent
        self.distance: float = distance
        self.altitude_avg: float = altitude_avg
        self.altitude_min: float = altitude_min
        self.altitude_max: float = altitude_max
        self.tpx_ext_stats: dict = tpx_ext_stats
        if self.tpx_ext_stats == None:
            self.tpx_ext_stats: dict = {}
        self.lx_ext: dict = lx_ext
        if self.lx_ext == None:
            self.lx_ext: dict = {}
