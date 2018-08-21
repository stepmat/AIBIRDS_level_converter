# AIBIRDS_level_convertor
This converter will allow levels to be converted between the Science Birds .xml format, and the official Angry Birds .json format.

Run the converter with two parameters, the level file to be converted and the file to convert it into.
e.g. python converter.py level-04.xml level1-1.json

Please note that the converter program cannot currently convert scaled objects.
If using the Iratus Aves generator, the "add_slopes" parameter must be set to false to generate levels that can be successfully converted.
