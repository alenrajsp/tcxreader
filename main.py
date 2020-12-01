from tcxreader.tcxreader import TCXReader, TCXTrackPoint

tcx_reader = TCXReader()
file_location = 'example_data/15.tcx'

data: TCXTrackPoint = tcx_reader.read(file_location)

print("Output")
print(str(data[0]))
