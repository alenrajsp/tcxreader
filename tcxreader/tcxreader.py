import os
import xml.etree.ElementTree as ET
import maya
from tcxreader.tcx_track_point import TCXTrackPoint
from pathlib import Path

GARMIN_XML_SCHEMA = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
GARMIN_XML_EXTENSIONS = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}'


class TCXReader:
    def __init__(self):
        self = self

    def read(self, fileLocation: str) -> [TCXTrackPoint]:
        """
        :param fileLocation: location of the tcx file
        :return: A list of TCXTrackPoint objects.
        """

        tree = ET.parse(fileLocation)
        root = tree.getroot()
        trackpoints = []
        for activities in root:
            if activities.tag == GARMIN_XML_SCHEMA + 'Activities':
                for activity in activities:
                    if activity.tag == GARMIN_XML_SCHEMA + 'Activity':
                        for lap in activity:
                            if lap.tag == GARMIN_XML_SCHEMA + 'Lap':
                                for track in lap:
                                    if track.tag == GARMIN_XML_SCHEMA + 'Track':
                                        for trackpoint in track:
                                            tcx_point = TCXTrackPoint()
                                            if trackpoint.tag == GARMIN_XML_SCHEMA + 'Trackpoint':
                                                for trackpoint_data in trackpoint:
                                                    if trackpoint_data.tag == GARMIN_XML_SCHEMA + 'Time':
                                                        tcx_point.time = maya.parse(trackpoint_data.text,
                                                                                    '%Y-%m-%d %H:%M:%S.%f').datetime()
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
                                            trackpoints.append(tcx_point)
        # remove_data_at_start_and_end_without_gps
        removalList = []
        for index in range(len(trackpoints)):
            if trackpoints[index].longitude is None:
                removalList.append(index)

        for removal in sorted(removalList, reverse=True):
            del trackpoints[removal]
        return trackpoints
