import datetime
import xml.etree.ElementTree as ET

from tcxreader.tcx_author import TCXAuthor
from tcxreader.tcx_exercise import TCXExercise
from tcxreader.tcx_lap import TCXLap
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

        tcx_exercise = TCXExercise(calories=0, distance=0, tpx_ext_stats={}, lx_ext={}, laps=[])

        tree = ET.parse(fileLocation)
        root = tree.getroot()
        trackpoints = []
        for node in root:
            if node.tag == GARMIN_XML_SCHEMA + 'Activities':
                for activity in node:
                    if activity.tag == GARMIN_XML_SCHEMA + 'Activity':
                        tcx_exercise.activity_type = activity.attrib['Sport']
                        for lap in activity:
                            tcx_lap = TCXLap(calories=0, distance=0, trackpoints=[], tpx_ext_stats={}, lx_ext={})
                            if lap.tag == GARMIN_XML_SCHEMA + 'Lap':
                                for lap_child in lap:
                                    if lap_child.tag == GARMIN_XML_SCHEMA + 'Calories':
                                        calories = int(round(float(lap_child.text)))
                                        tcx_exercise.calories += calories
                                        tcx_lap.calories += calories
                                    if lap_child.tag == GARMIN_XML_SCHEMA + 'DistanceMeters':
                                        tcx_exercise.distance += float(lap_child.text)
                                        tcx_lap.distance += float(lap_child.text)
                                    if lap_child.tag == GARMIN_XML_SCHEMA + 'Track':
                                        for trackpoint in lap_child:
                                            tcx_point = TCXTrackPoint(tpx_ext={})
                                            if trackpoint.tag == GARMIN_XML_SCHEMA + 'Trackpoint':
                                                self.trackpoint_parser(tcx_point, trackpoint)
                                            trackpoints.append(tcx_point)
                                            tcx_lap.trackpoints.append(tcx_point)
                                if lap_child.tag == GARMIN_XML_SCHEMA + 'Extensions':
                                    extensions = lap_child
                                    for extension in extensions:
                                        if extension.tag == GARMIN_XML_EXTENSIONS+'LX':
                                            for lx_extension in extension:

                                                tag_name = lx_extension.tag.replace(GARMIN_XML_EXTENSIONS, "")
                                                tag_value = lx_extension.text
                                                if '.' in tag_value:
                                                    tag_value = float(tag_value)
                                                else:
                                                    tag_value = int(tag_value)

                                                if "Avg" in tag_name or "Average" in tag_name or "Max" in tag_name or "Min" in tag_name:
                                                    pass
                                                else:
                                                    if tag_name in tcx_exercise.lx_ext:
                                                        tcx_exercise.lx_ext[tag_name] += tag_value
                                                    else:
                                                        tcx_exercise.lx_ext[tag_name] = tag_value

                                                tcx_lap.lx_ext[tag_name] = tag_value
                            if len(tcx_lap.trackpoints)>0:
                                tcx_exercise.laps.append(tcx_lap)
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

        tcx_exercise = self.__find_hi_lo_avg(tcx_exercise, only_gps)
        for lap in tcx_exercise.laps:
            self.__find_hi_lo_avg(lap, only_gps)
        return tcx_exercise

    def trackpoint_parser(self, tcx_point:TCXTrackPoint, trackpoint):
        index = 0
        for trackpoint_data in trackpoint:
            if trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Time':
                for pat in (
                    "%Y-%m-%dT%H:%M:%S.%fZ",  # Zulu time, fractional seconds.
                    "%Y-%m-%dT%H:%M:%S.%f%z",  # Zulu time via explicit HH:MM offset, fractional seconds.
                    "%Y-%m-%dT%H:%M:%SZ",  # Zulu time, integer seconds
                    "%Y-%m-%dT%H:%M:%S%z"  # Zulu time via explicit HH:MM offset, integer seconds.
                ):
                    try:
                        tcx_point.time = datetime.datetime.strptime(
                            trackpoint_data.text, pat
                        )
                        break
                    except ValueError:
                        continue

                if not tcx_point.time:
                    raise ValueError(f'Cannot parse time {trackpoint_data.text!r}')

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
                    tcx_point.hr_value = int(float(heart_rate.text))
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Cadence':
                tcx_point.cadence = int(trackpoint_data.text)
            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Extensions':
                for extension in trackpoint_data:
                    if extension.tag == GARMIN_XML_EXTENSIONS + 'TPX':
                        # New extensions value parser!
                        for tpx_extension in extension:
                            tag_name = tpx_extension.tag.replace(GARMIN_XML_EXTENSIONS, "")
                            tag_value = tpx_extension.text
                            if '.' in tag_value:
                                tag_value=float(tag_value)
                            else:
                                tag_value=int(tag_value)
                            tcx_point.tpx_ext[tag_name]=tag_value

    def __find_hi_lo_avg(self, tcx: TCXExercise, only_gps:bool) -> TCXExercise:
        trackpoints = tcx.trackpoints

        if only_gps == True:
            removalList = []
            for index in range(len(trackpoints)):
                if trackpoints[index].longitude == None:
                    removalList.append(index)

            for removal in sorted(removalList, reverse=True):
                del trackpoints[removal]

        tcx.trackpoints = trackpoints


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

        tcx_extensions_data = {}

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

        values = {}
        for trackpoint in tcx.trackpoints:
            for extension in trackpoint.tpx_ext:
                if trackpoint.tpx_ext[extension] != None and \
                        (isinstance(trackpoint.tpx_ext[extension], int) or \
                         isinstance(trackpoint.tpx_ext[extension], float)):
                    if extension in values:
                        values[extension].append(trackpoint.tpx_ext[extension])
                    else:
                        values[extension] = []
                        values[extension].append(trackpoint.tpx_ext[extension])

        for key in values:
            tcx.tpx_ext_stats[key]={}
            tcx.tpx_ext_stats[key]["min"] = min(values[key])
            tcx.tpx_ext_stats[key]["max"] = max(values[key])
            tcx.tpx_ext_stats[key]["avg"] = sum(values[key])/len(values[key])




        if len(trackpoints) > 2:
            tcx.start_time = trackpoints[0].time
            tcx.end_time = trackpoints[-1].time
            tcx.duration = abs((tcx.start_time - tcx.end_time).total_seconds())
            tcx.avg_speed = tcx.distance / tcx.duration * 3.6

            skip = True
            max_speed = 0.0
            for index in range(len(tcx.trackpoints)):
                if skip!=True:
                    try:
                        time = abs((tcx.trackpoints[index-1].time - tcx.trackpoints[index].time).total_seconds())
                        distance = abs(tcx.trackpoints[index-1].distance - tcx.trackpoints[index].distance)
                        speed = distance/time*3.6
                        if speed>max_speed:
                            max_speed=speed
                    except Exception:
                        a=100
                skip=False
            tcx.max_speed=max_speed

        return tcx
