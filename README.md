## Objective
This is a simple TCX parser / reader which can read Garmin TCX file extension files. The package currently does not support laps and merges the whole exercise into one exercise object. 
The following data is currently parsed: longitude, latitude, elevation, time, distance, hr_value, cadence, watts, TPX_speed (extension). GitHub requests appreciated to add missing Extensions.
[pypi](https://pypi.org/project/tcxreader/)

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
print("Output")
print(str(data[0]))
```

## Features
Allows parsing / reading of TCX files.

## Datasets

Datasets are available on the following links: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip), [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip)

## Licence

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!