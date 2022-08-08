from tcxreader.tcx_track_point import TCXTrackPoint
from datetime import datetime


class TCXAuthor:
    def __init__(self, name: str = None, version_major: int = None, version_minor: int = None, build_major: int = None,
                 build_minor: int = None):
        """
        :param name: usually name of the device used for recording
        :param version_major: major (XX) version of the device software (e.g. v XX.12)
        :param version_minor: minor (XX) version of the device software (e.g. v 12.XX)
        :param build_major: major version of the build of the device software
        :param build_minor: minor version of the build of the device software
        """
        self.name:str = name
        self.version_major:int = version_major
        self.version_minor:int = version_minor
        self.build_major:int = build_major
        self.build_minor:int = build_minor
