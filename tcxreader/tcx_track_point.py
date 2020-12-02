class TCXTrackPoint(object):
    def __init__(self, longitude: float = None, latitude: float = None, elevation: float = None, time=None,
                 distance=None, hr_value: int = None, cadence=None, TPX_speed: float = None, watts: float = None):
        '''
        :param longitude: Longitude of the trackpoint
        :param latitude: Latitude of the trackpoint
        :param elevation: Elevation of the trackpoint
        :param time: Datetime of the trackpoint
        :param distance: Total distance traveled at the current trackpoint
        :param hr_value: Heart rate value at the trackpoint
        :param cadence: Cadence at the trackpoint
        :param TPX_speed: Current speed (extension), not necessarily OK!
        :param watts: Watts usage at the trackpoint
        '''
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation
        self.time = time
        self.distance = distance
        self.hr_value = hr_value
        self.cadence = cadence
        self.watts = watts
        self.TPX_speed = TPX_speed

    def __str__(self):
        (longitude, latitude, elevation) = (self.longitude, self.latitude, self.elevation)
        time = self.time
        distance = self.distance
        (hr_value, cadence, watts) = (self.hr_value, self.cadence, self.watts)
        TPX_speed = self.TPX_speed

        return f'{time} | lat:{latitude}, lon:{longitude} elev:{elevation} | m:{distance} | ' \
               f'hr:{hr_value}, cadence:{cadence}, watt:{watts}, TPX_speed:{TPX_speed}'

    def __unicode__(self):
        return self.__str__()
