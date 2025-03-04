<p align="center">
    <img width="200" style="margin-bottom:-8px" src="https://raw.githubusercontent.com/alenrajsp/tcxreader/main/.github/logo/logo-white-background.png">
</p>

<h2 align="center">
    Reader for Garmin's TCX file format
</h2>

<p align="center">
    <a href="https://pypi.python.org/pypi/tcxreader">
        <img alt="PyPI Version" src="https://img.shields.io/pypi/v/tcxreader.svg" />
    </a>
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/tcxreader.svg" />
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/tcxreader.svg" />
    <a href="https://pepy.tech/project/tcxreader">
        <img alt="Downloads" src="https://pepy.tech/badge/tcxreader" />
    </a>
    <a href="https://github.com/alenrajsp/tcxreader/actions/workflows/test.yml">
        <img alt="tcxreader" src="https://github.com/alenrajsp/tcxreader/actions/workflows/test.yml/badge.svg">
    </a>
</p>

<p align="center">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/alenrajsp/tcxreader" />
    <a href="https://github.com/alenrajsp/tcxreader/blob/master/LICENSE">
        <img alt="GitHub license" src="https://img.shields.io/github/license/alenrajsp/tcxreader.svg" />
    </a>
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/alenrajsp/tcxreader.svg" />
    <a href='http://isitmaintained.com/project/alenrajsp/tcxreader "Average time to resolve an issue"'>
        <img alt="Average time to resolve an issue" src="http://isitmaintained.com/badge/resolution/alenrajsp/tcxreader.svg" />
    </a>
    <a href='http://isitmaintained.com/project/alenrajsp/tcxreader "Percentage of issues still open"'>
        <img alt="Percentage of issues still open" src="http://isitmaintained.com/badge/open/alenrajsp/tcxreader.svg" />
    </a>
    <a href="#-contributors">
        <img alt="All Contributors" src="https://img.shields.io/github/all-contributors/alenrajsp/tcxreader?color=ee8449" />
    </a>
</p>

<p align="center">
    <a href="https://zenodo.org/doi/10.5281/zenodo.10940281">
        <img alt="DOI" src="https://zenodo.org/badge/317671425.svg" />
    </a>
</p>

<p align="center">
    <a href="#-objective">🎯 Objective</a> •
    <a href="#-features">✨ Features</a> •
    <a href="#-installation">📦 Installation</a> •
    <a href="#-usage">🚀 Usage</a> •
    <a href="#-classes-explanation">🔍 Classes explanation</a> •
    <a href="#-missing-data-handling">🚨 Missing data handling</a> •
    <a href="#-datasets">💾 Datasets</a> •
    <a href="#-related-packagesframeworks">🔗 Related packages/frameworks</a> •
    <a href="#-license">🔑 License</a> •
    <a href="#-contributors">🫂 Contributors</a>
</p>

## 🎯 Objective

This is a simple TCX reader which can read Garmin TCX file extension files.  The following data is currently parsed: longitude,
latitude, elevation, time, distance, hr_value, cadence, watts, TPX_speed (extension). The following statistics are
calculated for each exercise: calories, hr_avg, hr_max, hr_min, avg_speed, start_time, end_time, duration, cadence_avg,
cadence_max, ascent, descent, distance, altitude_max, altitude_min, altitude_avg, steps and **author data**.

GitHub requests appreciated.
[pypi](https://pypi.org/project/tcxreader/)
[github](https://github.com/alenrajsp/tcxreader)

## ✨ Features

Allows parsing / reading of TCX files.

## 📦 Installation

```
pip install tcxreader
```

## 🚀 Usage

An example on how to use the package is shown below.

```python
from tcxreader.tcxreader import TCXReader, TCXExercise

tcx_reader = TCXReader()
file_location = 'example_data/cross-country-skiing_activity_1.tcx'

"""
Minor warning, the read method also has a default parameter of only_gps (tcx_readerread(self, fileLocation: str, only_gps: bool = True)) set to true. If set to True erases any Trackpoints at the start and end of the exercise without GPS data.
"""

data: TCXExercise = tcx_reader.read(file_location)
""" Example output:
data = {TCXExercise}
 activity_type = {str} 'Other'
altitude_avg = {float} 2285.6744874553915
altitude_max = {float} 2337.60009765625
altitude_min = {float} 1257.5999755859375
ascent = {float} 1117.9996337890625
author = {TCXAuthor} [TCXAuthor]
avg_speed = {float} 8.534458975426906
cadence_avg = {NoneType} None
cadence_max = {NoneType} None
calories = {int} 532
descent = {float} 118.19970703125
distance = {float} 5692.01
duration = {float} 2401.0
end_time = {datetime} 2020-12-26 15:54:22
hr_avg = {float} 141.1954732510288
hr_max = {int} 172
hr_min = {int} 83
laps = {list: 2} [TCXLap]
lx_ext = {dict: 0} {}
max_speed = {float} 23.50810546875
start_time = {datetime} 2020-12-26 15:14:21
tpx_ext_stats = {dict: 2} {'Speed': {'min': 0.0, 'max': 6.1579999923706055, 'avg': 2.2930514418784482}, 'RunCadence': {'min': 0, 'max': 95, 'avg': 40.81069958847737}}
trackpoints = {list: 486} [TCXTrackpoint]
 
    {TCXTrackPoint} 
     cadence = {NoneType} None
     distance = {float} 7.329999923706055
     elevation = {float} 2250.60009765625
     hr_value = {int} 87
     latitude = {float} 46.49582446552813
     longitude = {float} 15.50408081151545
     time = {datetime} 2020-12-26 15:14:28
     tpx_ext = {dict: 2} {'Speed': 0.7459999918937683, 'RunCadence': 58}
"""
```
## 🔍 Classes explanation

Below figure explains the classes of **tcxreader** and the data they contain.

### TCXReader()
User initializes the tcxreader by creating a **TCXReader** class instance. To read the data of a **TCX activity** the user must use
**TCXReader.read(*filename*)** method. 
The output of **read()** is an instance of **TCXExercise** class.

### TCXExercise
Primary class that holds cumulative data of an exercise. TCXExercise contains **all** the **trackpoints** of an activity
(e.g. from all the laps merged).

### TCXLap
One TCX activity may contain multiple laps. In the TCX file they are visible by the **Lap** tag.
```xml
<Lap StartTime="2020-12-26T15:50:22.000Z">
...
</Lap>
```
TCXLap contains all the trackpoints of a lap.

### TCXTrackpoint
A point in an exercise. Almost always has **latitude, longitude, time**. Can also have *cadence, distance, elevation, hr_value, tpx_ext*.
The tpx_ext refers to individual extensions contained inside the trackpoint. An example of the Trackpoint (pre-parsing) 
in the TCX file is shown below.

```xml
<Trackpoint>
    <Time>2020-12-26T15:50:21.000Z</Time>
    <Position>
        <LatitudeDegrees>46.49732105433941</LatitudeDegrees>
        <LongitudeDegrees>15.496849408373237</LongitudeDegrees>
    </Position>
    <AltitudeMeters>2277.39990234375</AltitudeMeters>
    <DistanceMeters>5001.52978515625</DistanceMeters>
    <HeartRateBpm>
        <Value>148</Value>
    </HeartRateBpm>
    <Extensions>
        <ns3:TPX>
            <ns3:Speed>3.3589999675750732</ns3:Speed>
            <ns3:RunCadence>61</ns3:RunCadence>
        </ns3:TPX>
    </Extensions>
</Trackpoint>
```

### tpx_ext
The data parsed from the **trackpoint TPX Extensions**. Example of data (pre-parsing) is shown below.
```xml
<Extensions>
    <ns3:TPX>
        <ns3:Speed>3.3589999675750732</ns3:Speed>
        <ns3:RunCadence>61</ns3:RunCadence>
    </ns3:TPX>
</Extensions>
```
Can occur **once (1x)** in every **trackpoint**.
### tpx_ext_stats
Contains **minimum**, **maximum** and **average** values of the recorded **tpx_ext** key.

### lx_ext
The data parsed from the **lap LX Extensions**. Example of data (pre-parsing) is shown below.
```xml
<Extensions>
    <ns3:LX>
        <ns3:AvgSpeed>1.0820000171661377</ns3:AvgSpeed>
        <ns3:Steps>65</ns3:Steps>
    </ns3:LX>
</Extensions>
```
Can occur **once (1x)** in every **lap**. 

The tags which do not contain **Avg, Min, Max** in their name (e.g. steps) are
summed in the **TCXExercise** **lx_ext** dictionary. 

All tags are recorded in the **TCXLap** **lx_ext** dictionary


### Schema of the data
<div width="100%" style="background-color: white; width: 100%">
 <img width="100%" style="margin-bottom:-8px" src="https://raw.githubusercontent.com/alenrajsp/tcxreader/7c9af6dc88f9d83a8c6751b454f118220ecfd9a1/.github/images/data-explanation.svg">
</div>

## 🚨 Missing data handling
Due to the nature of the TCX file format, some data may be missing. The **tcxreader** can handle this in two ways:
1) If data is missing at a TCX point it is set to **None**. (*default*)
    - tcx_reader.read(file_location) (*default*)
    - tcx_reader.read(file_location, null_value_handling=1) (*default*)
    - tcx_reader.read(file_location, null_value_handling=NullValueHandling.NONE) (*default*)
2) If data is missing at one or more TCX points it is linearly interpolated.
   - tcx_reader.read(file_location, null_value_handling=2)
   - tcx_reader.read(file_location, null_value_handling=NullValueHandling.LINEAR_INTERPOLATION)
   
This behavior can be set in **TCXReader.read()** method by the **null_value_handling** parameter, where either **int** value or **NullValueHandling** enum can be passed.

## 💾 Datasets

Datasets available and used in the examples on the following links: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip), [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip), [DATASET3](https://github.com/firefly-cpp/tcx-test-files).

## 🔗 Related packages/frameworks

[1] [sport-activities-features: A minimalistic toolbox for extracting features from sports activity files written in Python](https://github.com/firefly-cpp/sport-activities-features)

[2] [AST-Monitor: A wearable Raspberry Pi computer for cyclists](https://github.com/firefly-cpp/AST-Monitor)

[3] [TCXReader.jl: Julia package designed for parsing TCX files](https://github.com/firefly-cpp/TCXReader.jl)

## 🔑 License

This package is distributed under the MIT License. This license can be found online
at [http://www.opensource.org/licenses/MIT](http://www.opensource.org/licenses/MIT).

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it
at your own risk!

## 🫂 Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alenrajsp"><img src="https://avatars.githubusercontent.com/u/27721714?v=4?s=100" width="100px;" alt="alenrajsp"/><br /><sub><b>alenrajsp</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/commits?author=alenrajsp" title="Code">💻</a> <a href="#maintenance-alenrajsp" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fortysix2ahead"><img src="https://avatars.githubusercontent.com/u/40423757?v=4?s=100" width="100px;" alt="fortysix2ahead"/><br /><sub><b>fortysix2ahead</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Afortysix2ahead" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.iztok-jr-fister.eu/"><img src="https://avatars.githubusercontent.com/u/1633361?v=4?s=100" width="100px;" alt="Iztok Fister Jr."/><br /><sub><b>Iztok Fister Jr.</b></sub></a><br /><a href="#data-firefly-cpp" title="Data">🔣</a> <a href="#mentoring-firefly-cpp" title="Mentoring">🧑‍🏫</a> <a href="#platform-firefly-cpp" title="Packaging/porting to new platform">📦</a> <a href="https://github.com/alenrajsp/tcxreader/commits?author=firefly-cpp" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/johnleeming"><img src="https://avatars.githubusercontent.com/u/13801070?v=4?s=100" width="100px;" alt="johnleeming"/><br /><sub><b>johnleeming</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Ajohnleeming" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rpstar"><img src="https://avatars.githubusercontent.com/u/10442282?v=4?s=100" width="100px;" alt="rpstar"/><br /><sub><b>rpstar</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Arpstar" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://relatable.dev/"><img src="https://avatars.githubusercontent.com/u/1128313?v=4?s=100" width="100px;" alt="James Robinson"/><br /><sub><b>James Robinson</b></sub></a><br /><a href="#maintenance-jlrobins" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/johwiebe"><img src="https://avatars.githubusercontent.com/u/33023818?v=4?s=100" width="100px;" alt="johwiebe"/><br /><sub><b>johwiebe</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Ajohwiebe" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://martin-ueding.de/"><img src="https://avatars.githubusercontent.com/u/976924?v=4?s=100" width="100px;" alt="Martin Ueding"/><br /><sub><b>Martin Ueding</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Amartin-ueding" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/simonpickering"><img src="https://avatars.githubusercontent.com/u/1830341?v=4?s=100" width="100px;" alt="Simon Pickering"/><br /><sub><b>Simon Pickering</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Asimonpickering" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rwinklerwilkes"><img src="https://avatars.githubusercontent.com/u/2768609?v=4?s=100" width="100px;" alt="Rich Winkler"/><br /><sub><b>Rich Winkler</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/issues?q=author%3Arwinklerwilkes" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ToonElewaut"><img src="https://avatars.githubusercontent.com/u/12350289?v=4?s=100" width="100px;" alt="Toon Elewaut"/><br /><sub><b>Toon Elewaut</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/commits?author=ToonElewaut" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lahovniktadej"><img src="https://avatars.githubusercontent.com/u/57890734?v=4?s=100" width="100px;" alt="Tadej Lahovnik"/><br /><sub><b>Tadej Lahovnik</b></sub></a><br /><a href="https://github.com/alenrajsp/tcxreader/commits?author=lahovniktadej" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
