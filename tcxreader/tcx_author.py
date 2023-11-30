class TCXAuthor:
    def __init__(self, name: str = None, version_major: int = None, version_minor: int = None, build_major: int = None,
                 build_minor: int = None):
        """
        Class for storing the author of the TCX file. This is usually the device used for recording.
        :param name: Name of the device used for recording (usually).
        :param version_major: Major (XX) version of the device software (e.g. v XX.12).
        :param version_minor: Minor (YY) version of the device software (e.g. v 12.YY).
        :param build_major: Major version of the build of the device software.
        :param build_minor: Minor version of the build of the device software.
        """
        self.name: str = name
        self.version_major: int = version_major
        self.version_minor: int = version_minor
        self.build_major: int = build_major
        self.build_minor: int = build_minor
