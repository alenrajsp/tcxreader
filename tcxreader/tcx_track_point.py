class TCXTrackPoint(object):
    def __init__(self, longitude: float = None, latitude: float = None, elevation: float = None, time=None,
                 distance=None, hr_value: int = None, cadence=None, tpx_ext:dict= {}):
        '''
        :param longitude: Longitude of the trackpoint
        :param latitude: Latitude of the trackpoint
        :param elevation: Elevation of the trackpoint
        :param time: Datetime of the trackpoint
        :param distance: Total distance traveled at the current trackpoint
        :param hr_value: Heart rate value at the trackpoint
        :param cadence: Cadence at the trackpoint
        :param tpx_ext: Dictionary of all additional data types! e,g, speed, cadence, runcadence
        '''
        self.longitude:float = longitude
        self.latitude:float = latitude
        self.elevation:int = elevation
        self.time = time
        self.distance:float = distance
        self.hr_value:int = hr_value
        self.cadence:int = cadence
        self.tpx_ext:dict = tpx_ext

    def __str__(self):
        (longitude, latitude, elevation) = (self.longitude, self.latitude, self.elevation)
        time = self.time
        distance = self.distance
        (hr_value, cadence) = (self.hr_value, self.cadence)

        tpx_str = ""
        for key in self.tpx_ext:
            tpx_str+=f'\n\t{key}:{self.tpx_ext[key]}'

        return f'Time:{time}\nLatitude:\t{latitude}\nLongitude:\t{longitude}\nElevation:\t{elevation}\nDistance:\t{distance}\n' \
               f'Heartrate:\t{hr_value}\nCadence:\t{cadence} \nTPX Extensions: {tpx_str}\n#############################'

    def __unicode__(self):
        return self.__str__()
