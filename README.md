## Objective

This is a simple TCX parser / reader which can read Garmin TCX file extension files. The package currently does not
support laps and merges the whole exercise into one exercise object. The following data is currently parsed: longitude,
latitude, elevation, time, distance, hr_value, cadence, watts, TPX_speed (extension). The following statistics are
calculated for each exercise: calories, hr_avg, hr_max, hr_min, avg_speed, start_time, end_time, duration, cadence_avg,
cadence_max, ascent, descent, distance, altitude_max, altitude_min, altitude_avg

GitHub requests appreciated.
[pypi](https://pypi.org/project/tcxreader/)
[github](https://github.com/alenrajsp/tcxreader)

## Installation

    pip install tcxreader

## Dependencies

This package uses [maya](https://pypi.org/project/maya/) for parsing / reading datetimes from TCX files.

## Example

An example on how to use the package is shown below.

```python
from tcxreader.tcxreader import TCXReader, TCXTrackPoint

tcx_reader = TCXReader()
file_location = 'example_data/15.tcx'

data: TCXTrackPoint = tcx_reader.read(file_location)
""" Example output:
data = {TCXExercise}
 activity_type = {str} 'Biking'
 ascent = {float} 1404.400026500225
 avg_speed = {float} 24.285282782608693
 cadence_avg = {NoneType} None
 cadence_max = {NoneType} None
 calories = {int} 2010
 descent = {float} 1422.000026166439
 distance = {float} 116366.98
 duration = {float} 17250.0
 end_time = {datetime} 2015-02-19 14:18:59+00:00
 hr_avg = {float} 140.59545804464972
 hr_max = {int} 200
 hr_min = {int} 94
 altitude_max = {float}
 altitude_min = {float}
 altitude_avg = {float}
 max_speed = {float} 18.95800018310547
 start_time = {datetime} 2015-02-19 09:31:29+00:00
 trackpoints = {list: 7799} [TCXTrackPoint]
 
    {TCXTrackPoint}
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
```

## Features

Allows parsing / reading of TCX files.

## Datasets

Datasets are available on the following links: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip)
, [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip)

## Licence

This package is distributed under the MIT License. This license can be found online
at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it
at your own risk!