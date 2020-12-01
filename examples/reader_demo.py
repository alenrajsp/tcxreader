"""
Simple example of using the TCX reader!
"""
from tcxreader.tcxreader import TCXReader, TCXTrackPoint

tcx_reader = TCXReader()
file_location = '../example_data/15.tcx'

data: TCXTrackPoint = tcx_reader.read(file_location)

print("Output")
print(str(data[0]))

"""
Example output:
data[n] = {TCXTrackPoint}
	 TPX_speed = {float} 5.011000156402588
	 cadence = {float} 80
	 distance = {float} 514.0499877929688
	 elevation = {float} 46.79999923706055
	 hr_value = {int} 134
	 latitude = {float} 45.5244944896549
	 longitude = {float} 13.596355207264423
	 time = {datetime} 2015-02-19 09:34:17+00:00
	 watts = {float} 123
"""
