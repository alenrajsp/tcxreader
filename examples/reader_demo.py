"""
Simple example of using the TCX reader!
"""
from tcxreader.tcxreader import TCXReader, TCXExercise

tcx_reader = TCXReader()
file_location = '../example_data/cross-country-skiing_activity_1.tcx'

data: TCXExercise = tcx_reader.read(file_location)


print("Output")
print(str(data.trackpoints[0]))

"""
Example output:

= {TCXTrackPoint}
    Time:2015-02-19 09:31:29
    Latitude:	45.524007584899664
    Longitude:	13.59806134365499
    Elevation:	19.399999618530273
    Distance:	0.009999999776482582
    Heartrate:	94
    Cadence:	None 
    TPX Extensions: 
        Speed:0.0
    #############################
"""
