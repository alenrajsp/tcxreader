import datetime
import xml.etree.ElementTree as ET

from tcxreader.tcx_author import TCXAuthor
from tcxreader.tcx_exercise import TCXExercise
from tcxreader.tcx_track_point import TCXTrackPoint

GARMIN_XML_SCHEMA = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
GARMIN_XML_EXTENSIONS = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}'


class TCXReader:
    def __init__(self):
        self = self

    def read(self, fileLocation: str, only_gps: bool = True) -> TCXExercise:
        """
        :param only_gps: If set to True erases any Trackpoints at the start and end of the exercise without GPS data.
        :param fileLocation: location of the tcx file
        :return: A list of TCXTrackPoint objects.
        """

        tcx_exercise = TCXExercise(calories=0, distance=0)

        tree = ET.parse(fileLocation)
        root = tree.getroot()
        trackpoints = []
        for node in root:
            if node.tag == GARMIN_XML_SCHEMA + 'Activities':
                for activity in node:
                    if activity.tag == GARMIN_XML_SCHEMA + 'Activity':
                        tcx_exercise.activity_type = activity.attrib['Sport']
                        for lap in activity:
                            if lap.tag == GARMIN_XML_SCHEMA + 'Lap':
                                for lap_child in lap:
                                    if lap_child.tag == GARMIN_XML_SCHEMA + 'Calories':
                                        tcx_exercise.calories += int(lap_child.text)
                                    if lap_child.tag == GARMIN_XML_SCHEMA + 'DistanceMeters':
                                        tcx_exercise.distance += float(lap_child.text)
                                    if lap_child.tag == GARMIN_XML_SCHEMA + 'Track':
                                        for trackpoint in lap_child:
                                            tcx_point = TCXTrackPoint()
                                            if trackpoint.tag == GARMIN_XML_SCHEMA + 'Trackpoint':
                                                self.trackpoint_parser(tcx_point, trackpoint)
                                            trackpoints.append(tcx_point)
                                if lap_child.tag == GARMIN_XML_SCHEMA + 'Extensions':
                                    extensions = lap_child
                                    for extension in extensions:
                                        if extension.tag == GARMIN_XML_EXTENSIONS+'LX':
                                            for lx_extension in extension:
                                                if lx_extension.tag == GARMIN_XML_EXTENSIONS+'Steps': #i.e. Steps in a run or strokes on a sup
                                                    if tcx_exercise.steps != None:
                                                        tcx_exercise.steps += int(lx_extension.text)
                                                    else:
                                                        tcx_exercise.steps = int(lx_extension.text)
            if node.tag == GARMIN_XML_SCHEMA+'Author':
                author = TCXAuthor()
                for author_node in node:
                    if author_node.tag == GARMIN_XML_SCHEMA+'Name':
                        author.name=author_node.text
                    elif author_node.tag == GARMIN_XML_SCHEMA+'Build':
                        for build_node in author_node:
                            if build_node.tag == GARMIN_XML_SCHEMA+'Version':
                                for version_node in build_node:
                                    if version_node.tag == GARMIN_XML_SCHEMA+'VersionMajor':
                                        author.version_major = int(version_node.text)
                                    elif version_node.tag == GARMIN_XML_SCHEMA+'VersionMinor':
                                        author.version_minor = int(version_node.text)
                                    elif version_node.tag == GARMIN_XML_SCHEMA+'BuildMajor':
                                        author.build_major = int(version_node.text)
                                    elif version_node.tag == GARMIN_XML_SCHEMA+'BuildMinor':
                                        author.build_minor = int(version_node.text)
                tcx_exercise.author = author


        # remove_data_at_start_and_end_without_gps. Those stats are not taken for distance and hr measurements!
        if only_gps == True:
            removalList = []
            for index in range(len(trackpoints)):
                if trackpoints[index].longitude == None:
                    removalList.append(index)

            for removal in sorted(removalList, reverse=True):
                del trackpoints[removal]

        tcx_exercise.trackpoints = trackpoints

        tcx_exercise = self.__find_hi_lo_avg(tcx_exercise)
        return tcx_exercise

    def trackpoint_parser(self, tcx_point, trackpoint):
        for trackpoint_data in trackpoint:
            if trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Time':
                tcx_point.time = datetime.datetime.strptime(
                    trackpoint_data.text, '%Y-%m-%dT%H:%M:%S.%fZ')
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Position':
                for position in trackpoint_data:
                    if position.tag == GARMIN_XML_SCHEMA + "LatitudeDegrees":
                        tcx_point.latitude = float(position.text)
                    elif position.tag == GARMIN_XML_SCHEMA + "LongitudeDegrees":
                        tcx_point.longitude = float(position.text)
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'AltitudeMeters':
                tcx_point.elevation = float(trackpoint_data.text)
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'DistanceMeters':
                tcx_point.distance = float(trackpoint_data.text)
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'HeartRateBpm':
                for heart_rate in trackpoint_data:
                    tcx_point.hr_value = int(heart_rate.text)
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Cadence':
                tcx_point.cadence = int(trackpoint_data.text)
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Extensions':
                for extension in trackpoint_data:
                    if extension.tag == GARMIN_XML_EXTENSIONS + 'TPX':
                        for tpx_extension in extension:
                            if tpx_extension.tag == GARMIN_XML_EXTENSIONS + 'Speed':
                                tcx_point.TPX_speed = float(tpx_extension.text)
                            elif tpx_extension.tag == GARMIN_XML_EXTENSIONS + 'Watts':
                                tcx_point.watts = float(tpx_extension.text)

    def __find_hi_lo_avg(self, tcx: TCXExercise) -> TCXExercise:
        trackpoints = tcx.trackpoints
        hr = []
        altitude = []
        cadence = []
        for trackpoint in tcx.trackpoints:
            if trackpoint.hr_value != None:
                hr.append(trackpoint.hr_value)
            if trackpoint.elevation != None:
                altitude.append(trackpoint.elevation)
            if trackpoint.cadence != None:
                cadence.append(trackpoint.cadence)

        if len(altitude) > 0:
            (tcx.altitude_max, tcx.altitude_min) = (max(altitude), min(altitude))
            tcx.altitude_avg = sum(altitude) / len(altitude)

        (ascent, descent) = (0, 0)
        previous_altitude = -100
        for alt in altitude:
            if isinstance(alt, float):
                if previous_altitude == -100:
                    pass
                elif alt > previous_altitude:
                    ascent += alt - previous_altitude
                elif alt < previous_altitude:
                    descent += previous_altitude - alt
                previous_altitude = alt

        (tcx.ascent, tcx.descent) = (ascent, descent)

        if len(hr) > 0:
            (tcx.hr_max, tcx.hr_min) = (max(hr), min(hr))
            tcx.hr_avg = sum(hr) / len(hr)

        if len(cadence) > 0:
            tcx.cadence_max = max(cadence)
            tcx.cadence_avg = sum(cadence) / len(cadence)

        if len(trackpoints) > 2:
            tcx.start_time = trackpoints[0].time
            tcx.end_time = trackpoints[-1].time
            tcx.duration = abs((tcx.start_time - tcx.end_time).total_seconds())
            tcx.avg_speed = tcx.distance / tcx.duration * 3.6

        return tcx
