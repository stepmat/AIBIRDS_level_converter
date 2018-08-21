# AIBIRDS_level_converter
This program can convert levels between the Science-Birds .xml format, and the official Angry Birds .json format.

Run the converter with two parameters, the level file to be converted and the file to convert it into.

e.g. python converter.py level-04.xml level1-1.json

This program can bidirectionally convert between the two formats.

Please note that the program cannot currently convert scaled Science-Birds objects.

Please note that due to the two games using different physics engines, there is no guarantee that levels will remain stable when converted.

If using the Iratus Aves level generator (https://github.com/stepmat/IratusAves), the "add_slopes" parameter must be set to false in order to generate levels that can then be successfully converted.

Science-Birds level             |  Angry Birds level
:-------------------------:|:-------------------------:
![](/example_converted_levels/sciencebirds1.PNG)  |  ![](/example_converted_levels/angrybirds1.PNG)
![](/example_converted_levels/sciencebirds2.PNG)  |  ![](/example_converted_levels/angrybirds2.PNG)
![](/example_converted_levels/sciencebirds3.PNG)  |  ![](/example_converted_levels/angrybirds3.PNG)
![](/example_converted_levels/sciencebirds4.PNG)  |  ![](/example_converted_levels/angrybirds4.PNG)
