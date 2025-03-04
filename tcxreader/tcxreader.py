import datetime
import xml.etree.ElementTree as ET
from enum import Enum
from typing import List, Union

from tcxreader.tcx_author import TCXAuthor
from tcxreader.tcx_exercise import TCXExercise
from tcxreader.tcx_lap import TCXLap
from tcxreader.tcx_track_point import TCXTrackPoint

GARMIN_XML_SCHEMA = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
GARMIN_XML_EXTENSIONS = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}'


class NullValueHandling(Enum):
    """
    Enum for handling null values in TCX file.
    """
    NONE = 1
    LINEAR_INTERPOLATION = 2


class TCXReader:
    def __init__(self):
        """
        Class for reading TCX files.
        """
        pass

    def read(self, fileLocation: str, only_gps: bool = True, null_value_handling: int = 1) -> TCXExercise:
        """
        Reads a TCX file and returns a TCXExercise object.

        :param fileLocation: Path to the TCX file.
        :param only_gps: If True, remove any Trackpoints at the start/end of the exercise without GPS data.
        :param null_value_handling: How to handle null values:
                                    1 = set to None
                                    2 = linear interpolation
        :return: A TCXExercise object.
        """
        # 1) Build an empty TCXExercise container
        tcx_exercise = TCXExercise(calories=0, distance=0, tpx_ext_stats={}, lx_ext={}, laps=[])

        # 2) Parse the file into a tree and extract the root
        tree, root = self.__parse_tcx_file(fileLocation)

        # 3) Read all activities and populate the `tcx_exercise` data
        trackpoints = self.__parse_activities(root, tcx_exercise)

        # 4) Read the file’s author (if present)
        self.__parse_author(root, tcx_exercise)

        # 5) Remove trackpoints that do not have GPS data if only_gps is True
        if only_gps:
            self.__remove_data_at_start_and_end_without_gps(trackpoints)

        # 6) Store the (possibly truncated) trackpoints in the top-level exercise
        tcx_exercise.trackpoints = trackpoints

        # 7) Interpolate missing values if requested
        if null_value_handling == 2 or null_value_handling == NullValueHandling.LINEAR_INTERPOLATION:
            tcx_exercise.trackpoints = self.__fill_none_with_averages(tcx_exercise.trackpoints)

        # 8) Calculate additional stats (min, max, avg, etc.) at the exercise level
        tcx_exercise = self.__find_hi_lo_avg(tcx_exercise, only_gps)

        # 9) Handle laps individually (fill missing data + calculate stats)
        for lap in tcx_exercise.laps:
            if null_value_handling == 2 or null_value_handling == NullValueHandling.LINEAR_INTERPOLATION:
                lap.trackpoints = self.__fill_none_with_averages(lap.trackpoints)
            self.__find_hi_lo_avg(lap, only_gps)

        return tcx_exercise

    # --------------------------------------------------------------------------
    #                             HELPER METHODS
    # --------------------------------------------------------------------------

    def __parse_tcx_file(self, fileLocation: str) -> Union[ET.ElementTree, ET.Element]:
        """
        Parses an XML file into an ElementTree and returns the tree + root.

        :param fileLocation: Path to the TCX file
        :return: (tree, root)
        """
        tree = ET.parse(fileLocation)
        root = tree.getroot()
        return tree, root

    def __parse_activities(self, root: ET.Element, tcx_exercise: TCXExercise) -> List[TCXTrackPoint]:
        """
        Reads <Activities> from the root and populates laps, trackpoints, and summary
        data (like total distance, total calories) in the `tcx_exercise` object.

        :param root: The root of the parsed TCX file
        :param tcx_exercise: The exercise container to fill
        :return: A flat list of all trackpoints found in the file
        """
        trackpoints = []

        for node in root:
            if node.tag == GARMIN_XML_SCHEMA + 'Activities':
                for activity in node:
                    if activity.tag == GARMIN_XML_SCHEMA + 'Activity':
                        # Sport Type
                        tcx_exercise.activity_type = activity.attrib['Sport']

                        # Parse <Lap> elements inside an Activity
                        for lap_node in activity:
                            if lap_node.tag == GARMIN_XML_SCHEMA + 'Lap':
                                tcx_lap = self.__parse_lap(lap_node, tcx_exercise)
                                if len(tcx_lap.trackpoints) > 0:
                                    tcx_exercise.laps.append(tcx_lap)
                                    trackpoints.extend(tcx_lap.trackpoints)
        return trackpoints

    def __parse_lap(self, lap_node: ET.Element, tcx_exercise: TCXExercise) -> TCXLap:
        """
        Parses a single <Lap> element, extracting Calories, DistanceMeters, trackpoints,
        and any lap-level LX extensions. The resulting data is stored in a new TCXLap,
        which is returned.

        :param lap_node: The <Lap> element
        :param tcx_exercise: The high-level TCXExercise container
        :return: A newly created TCXLap with the parsed data
        """
        tcx_lap = TCXLap(calories=0, distance=0, trackpoints=[], tpx_ext_stats={}, lx_ext={})

        for lap_child in lap_node:
            # Calories
            if lap_child.tag == GARMIN_XML_SCHEMA + 'Calories':
                calories = int(round(float(lap_child.text)))
                tcx_exercise.calories += calories
                tcx_lap.calories += calories

            # Distance
            elif lap_child.tag == GARMIN_XML_SCHEMA + 'DistanceMeters':
                distance_val = float(lap_child.text)
                tcx_exercise.distance += distance_val
                tcx_lap.distance += distance_val

            # Track (set of Trackpoint)
            elif lap_child.tag == GARMIN_XML_SCHEMA + 'Track':
                for trackpoint in lap_child:
                    if trackpoint.tag == GARMIN_XML_SCHEMA + 'Trackpoint':
                        tcx_point = TCXTrackPoint(tpx_ext={})
                        self.trackpoint_parser(tcx_point, trackpoint)
                        tcx_lap.trackpoints.append(tcx_point)

            # Lap-level <Extensions>
            elif lap_child.tag == GARMIN_XML_SCHEMA + 'Extensions':
                for extension in lap_child:
                    if extension.tag == GARMIN_XML_EXTENSIONS + 'LX':
                        # Example: <LX><AvgSpeed>...</AvgSpeed>...
                        for lx_extension in extension:
                            tag_name = lx_extension.tag.replace(GARMIN_XML_EXTENSIONS, "")
                            tag_value = lx_extension.text
                            # Convert to float or int
                            if '.' in tag_value:
                                tag_value = float(tag_value)
                            else:
                                tag_value = int(tag_value)

                            # Summation into the exercise-level dictionary
                            if "Avg" in tag_name or "Average" in tag_name or "Max" in tag_name or "Min" in tag_name:
                                # We skip adding these particular stats to a sum
                                pass
                            else:
                                if tag_name in tcx_exercise.lx_ext:
                                    tcx_exercise.lx_ext[tag_name] += tag_value
                                else:
                                    tcx_exercise.lx_ext[tag_name] = tag_value

                            # Also store in the lap-level dictionary
                            tcx_lap.lx_ext[tag_name] = tag_value

        return tcx_lap

    def __parse_author(self, root: ET.Element, tcx_exercise: TCXExercise) -> None:
        """
        Reads the <Author> element (if present) and populates an Author object
        in the `tcx_exercise`.

        :param root: The root of the parsed TCX file
        :param tcx_exercise: The exercise container to fill with author info
        :return: None
        """
        for node in root:
            if node.tag == GARMIN_XML_SCHEMA + 'Author':
                author = TCXAuthor()
                for author_node in node:
                    if author_node.tag == GARMIN_XML_SCHEMA + 'Name':
                        author.name = author_node.text
                    elif author_node.tag == GARMIN_XML_SCHEMA + 'Build':
                        for build_node in author_node:
                            if build_node.tag == GARMIN_XML_SCHEMA + 'Version':
                                for version_node in build_node:
                                    if version_node.tag == GARMIN_XML_SCHEMA + 'VersionMajor':
                                        author.version_major = int(version_node.text)
                                    elif version_node.tag == GARMIN_XML_SCHEMA + 'VersionMinor':
                                        author.version_minor = int(version_node.text)
                                    elif version_node.tag == GARMIN_XML_SCHEMA + 'BuildMajor':
                                        author.build_major = int(version_node.text)
                                    elif version_node.tag == GARMIN_XML_SCHEMA + 'BuildMinor':
                                        author.build_minor = int(version_node.text)
                tcx_exercise.author = author

    def __remove_data_at_start_and_end_without_gps(self, trackpoints: list) -> None:
        """
        Removes any TrackPoint that does not have longitude data. This effectively
        removes trackpoints that don't contain GPS info from the start/end.

        :param trackpoints: A list of all trackpoints
        :return: None (operates in-place)
        """
        removal_list = []
        for idx, tp in enumerate(trackpoints):
            if tp.longitude is None:
                removal_list.append(idx)

        # remove from the end to avoid shifting indexes
        for removal in sorted(removal_list, reverse=True):
            del trackpoints[removal]

    def trackpoint_parser(self, tcx_point: TCXTrackPoint, trackpoint: ET.Element) -> None:
        """
        Parses a <Trackpoint> XML element and fills the provided `tcx_point` object.

        :param tcx_point: TCXTrackPoint object to store parsed data
        :param trackpoint: <Trackpoint> element from the TCX
        :return: None
        """
        for trackpoint_data in trackpoint:
            if trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Time':
                # Attempt multiple time format patterns
                for pat in (
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S.%f%z",
                    "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%dT%H:%M:%S%z"
                ):
                    try:
                        tcx_point.time = datetime.datetime.strptime(trackpoint_data.text, pat)
                        break
                    except ValueError:
                        continue

                if not tcx_point.time:
                    raise ValueError(f'Cannot parse time {trackpoint_data.text!r}')

            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Position':
                for position in trackpoint_data:
                    if position.tag == GARMIN_XML_SCHEMA + "LatitudeDegrees":
                        try:
                            tcx_point.latitude = float(position.text)
                        except (ValueError, TypeError):
                            tcx_point.latitude = None
                    elif position.tag == GARMIN_XML_SCHEMA + "LongitudeDegrees":
                        try:
                            tcx_point.longitude = float(position.text)
                        except (ValueError, TypeError):
                            tcx_point.longitude = None

            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'AltitudeMeters':
                try:
                    tcx_point.elevation = float(trackpoint_data.text)
                except (ValueError, TypeError):
                    tcx_point.elevation = None

            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'DistanceMeters':
                try:
                    tcx_point.distance = float(trackpoint_data.text)
                except (ValueError, TypeError):
                    tcx_point.distance = None

            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'HeartRateBpm':
                for heart_rate in trackpoint_data:
                    try:
                        tcx_point.hr_value = int(float(heart_rate.text))
                    except (ValueError, TypeError):
                        tcx_point.hr_value = None

            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Cadence':
                try:
                    tcx_point.cadence = int(float(trackpoint_data.text))
                except (ValueError, TypeError):
                    tcx_point.cadence = None

            elif trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Extensions':
                for extension in trackpoint_data:
                    if extension.tag == GARMIN_XML_EXTENSIONS + 'TPX':
                        # e.g. <TPX><Speed>...</Speed><Watts>...</Watts>
                        for tpx_extension in extension:
                            tag_name = tpx_extension.tag.replace(GARMIN_XML_EXTENSIONS, "")
                            try:
                                tag_value = tpx_extension.text
                                if '.' in tag_value:
                                    tag_value = float(tag_value)
                                else:
                                    tag_value = int(tag_value)
                                tcx_point.tpx_ext[tag_name] = tag_value
                            except (ValueError, TypeError):
                                tcx_point.tpx_ext[tag_name] = None

    def __fill_none_with_averages(self, trackpoints: List[TCXTrackPoint]) -> List[TCXTrackPoint]:
        """
        Interpolates missing values in trackpoints with averages between the
        previous and next valid value.

        :param trackpoints: List of TCXTrackPoint objects
        :return: A new list of TCXTrackPoint with missing values linearly interpolated
        """
        def interpolate(start, end, length):
            """
            Interpolates between two values.
            :param start:
            :param end:
            :param length:
            :return:
            """
            step = (end - start) / (length + 1) if length + 1 != 0 else 0
            type_start = type(start)
            return [type_start(start + step * i) for i in range(1, length + 1)]

        def __fill_none_with_averages_for_data(data):
            """
            Interpolates missing values in data with averages between them.
            :param data:
            :return:
            """
            result = []
            i = 0
            while i < len(data):
                if data[i] is None:
                    start_i = i - 1
                    while i < len(data) and data[i] is None:
                        i += 1
                    end_i = i
                    start_val = data[start_i] if start_i >= 0 else 0
                    end_val = data[end_i] if end_i < len(data) else start_val
                    result.extend(interpolate(start_val, end_val, end_i - start_i))
                else:
                    result.append(data[i])
                    i += 1
            return result

        # Interpolate for simple numeric attributes
        def interpolate_attribute(attr):
            """
            Interpolates an attribute.
            :param attr:
            :return:
            """
            data = [getattr(tp, attr) for tp in trackpoints]
            return __fill_none_with_averages_for_data(data)

        # Interpolate for each known extension key
        def interpolate_tpx_ext(key):
            """
            Interpolates a TPX extension key.
            :param key:
            :return:
            """
            data = [tp.tpx_ext.get(key) for tp in trackpoints]
            return __fill_none_with_averages_for_data(data)

        attrs_to_interpolate = ['longitude', 'latitude', 'elevation', 'distance', 'hr_value', 'cadence']
        interpolated_attrs = {attr: interpolate_attribute(attr) for attr in attrs_to_interpolate}

        # Collect all extension keys
        tpx_keys = set()
        for tp in trackpoints:
            tpx_keys.update(tp.tpx_ext.keys())

        interpolated_tpx_ext = {key: interpolate_tpx_ext(key) for key in tpx_keys}

        # Build new trackpoints with interpolated data
        new_trackpoints = []
        for i in range(len(trackpoints)):
            new_tpx_ext = {key: interpolated_tpx_ext[key][i] for key in tpx_keys}
            new_trackpoint = TCXTrackPoint(
                longitude=interpolated_attrs['longitude'][i],
                latitude=interpolated_attrs['latitude'][i],
                elevation=interpolated_attrs['elevation'][i],
                distance=interpolated_attrs['distance'][i],
                hr_value=interpolated_attrs['hr_value'][i],
                cadence=interpolated_attrs['cadence'][i],
                tpx_ext=new_tpx_ext,
                time=trackpoints[i].time
            )
            new_trackpoints.append(new_trackpoint)

        return new_trackpoints

    def __find_hi_lo_avg(self, tcx: TCXExercise, only_gps: bool) -> TCXExercise:
        """
        Finds the highest, lowest, and average values for HR, altitude, cadence,
        speeds, etc. Also calculates total ascent/descent. Stores results in
        the given TCXExercise or TCXLap (both share the needed fields).

        :param tcx: A TCXExercise (or TCXLap) to modify
        :param only_gps: If True, remove any Trackpoints lacking GPS data
        :return: The modified tcx (for chaining)
        """
        trackpoints = tcx.trackpoints

        if only_gps:
            # remove trackpoints that lack longitude
            removal_list = []
            for index, tp in enumerate(trackpoints):
                if tp.longitude is None:
                    removal_list.append(index)
            for removal in sorted(removal_list, reverse=True):
                del trackpoints[removal]

        tcx.trackpoints = trackpoints

        hr = []
        altitude = []
        cadence = []

        for tp in tcx.trackpoints:
            if tp.hr_value is not None:
                hr.append(tp.hr_value)
            if tp.elevation is not None:
                altitude.append(tp.elevation)
            if tp.cadence is not None:
                cadence.append(tp.cadence)

        # Altitude stats
        if altitude:
            tcx.altitude_max = max(altitude)
            tcx.altitude_min = min(altitude)
            tcx.altitude_avg = sum(altitude) / len(altitude)
        else:
            tcx.altitude_max = None
            tcx.altitude_min = None
            tcx.altitude_avg = None

        # Ascent / Descent
        ascent, descent = 0.0, 0.0
        previous_altitude = None
        for alt in altitude:
            if previous_altitude is None:
                previous_altitude = alt
                continue
            if alt > previous_altitude:
                ascent += (alt - previous_altitude)
            elif alt < previous_altitude:
                descent += (previous_altitude - alt)
            previous_altitude = alt
        tcx.ascent = ascent
        tcx.descent = descent

        # Heart rate stats
        if hr:
            tcx.hr_max = max(hr)
            tcx.hr_min = min(hr)
            tcx.hr_avg = sum(hr) / len(hr)
        else:
            tcx.hr_max = None
            tcx.hr_min = None
            tcx.hr_avg = None

        # Cadence stats
        if cadence:
            tcx.cadence_max = max(cadence)
            tcx.cadence_avg = sum(cadence) / len(cadence)
        else:
            tcx.cadence_max = None
            tcx.cadence_avg = None

        # tpx_ext data min/max/avg
        values = {}
        for tp in tcx.trackpoints:
            for extension_key, extension_value in tp.tpx_ext.items():
                if extension_value is not None and (isinstance(extension_value, int) or isinstance(extension_value, float)):
                    if extension_key not in values:
                        values[extension_key] = []
                    values[extension_key].append(extension_value)

        for key, val_list in values.items():
            tcx.tpx_ext_stats[key] = {
                "min": min(val_list),
                "max": max(val_list),
                "avg": sum(val_list) / len(val_list),
            }

        # Time-based stats
        if len(tcx.trackpoints) > 2:
            tcx.start_time = tcx.trackpoints[0].time
            tcx.end_time = tcx.trackpoints[-1].time
            tcx.duration = abs((tcx.start_time - tcx.end_time).total_seconds())
            # Average speed in km/h
            if tcx.duration != 0:
                tcx.avg_speed = (tcx.distance / tcx.duration) * 3.6
            else:
                tcx.avg_speed = 0.0

            # Max speed: analyze consecutive trackpoints
            max_speed = 0.0
            for i in range(1, len(tcx.trackpoints)):
                prev_tp = tcx.trackpoints[i - 1]
                curr_tp = tcx.trackpoints[i]
                try:
                    dt = abs((prev_tp.time - curr_tp.time).total_seconds())
                    dist = abs(prev_tp.distance - curr_tp.distance) if (prev_tp.distance and curr_tp.distance) else 0.0
                    speed = (dist / dt) * 3.6 if dt != 0 else 0
                    if speed > max_speed:
                        max_speed = speed
                except ZeroDivisionError:
                    print(f"Zero division error at {i}")
                    pass
                except Exception as e:
                    print(f"Error at {i}: {e}")
                    pass
            tcx.max_speed = max_speed
        else:
            tcx.start_time = None
            tcx.end_time = None
            tcx.duration = 0
            tcx.avg_speed = 0.0
            tcx.max_speed = 0.0

        return tcx
