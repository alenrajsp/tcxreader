from tcxreader.tcx_author import TCXAuthor
from tcxreader.tcx_lap import TCXLap
from tcxreader.tcx_track_point import TCXTrackPoint
from datetime import datetime
from typing import List


class TCXExercise:
    def __init__(self, trackpoints: List[TCXTrackPoint] = None, activity_type: str = None, calories: int = None,
                 hr_avg: float = None, hr_max: float = None, hr_min=None, max_speed: float = None,
                 avg_speed: float = None, start_time: datetime = None, end_time: datetime = None,
                 duration: float = None, cadence_avg: float = None, cadence_max: float = None, ascent: float = None,
                 descent: float = None, distance: float = None, altitude_avg: float = None, altitude_min: float = None,
                 altitude_max: float = None, author: TCXAuthor=None,
                 tpx_ext_stats: dict = None, lx_ext: dict = None, laps: List[TCXLap] = None):
        """
        Class for storing exercise data from a TCX file.
        :param trackpoints: List of TCXTrackPoint objects.
        :param activity_type: Sport string e.g. cycling.
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
        :param altitude_max: Maximum altitude during the exersice.
        :param author: Describes who recorded the data, e.g. which device.
        :param tpx_ext_stats: Contains statistics (min, max, avg) of TPX extension data of trackpoints.
        :param lx_ext: Contains sum of LX extension data for each key in LX extension tag.
        :param laps: Contains subset of data for each lap.

        """

        self.trackpoints: List[TCXTrackPoint] = trackpoints
        self.laps: List[TCXLap] = laps
        self.activity_type: str = activity_type
        self.calories: int = calories
        self.hr_avg: float = hr_avg
        self.hr_max: float = hr_max
        self.hr_min: float = hr_min
        self.duration: float = duration
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
        self.author: TCXAuthor = author
        self.tpx_ext_stats: dict = tpx_ext_stats
        self.lx_ext: dict = lx_ext
        
    def trackpoints_to_dict(self) -> list:
        """
        Convert trackpoints to a list of dictionaries.
        :return: list: A list of dictionaries containing trackpoint data.
        """
        trackpoint_dict = []
            
        for tp in self.trackpoints:
            trackpoint_dict.append(tp.to_dict())
                
            
        return trackpoint_dict
