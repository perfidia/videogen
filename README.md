VideoGen
========

Description
-----------

Videogen is a tool for creating video files from XML configuration files. It allows to connect videos, sounds and images into a single video file.
The tool can use effects as VideoRepeat or can cut media from and to a specific time.

Installation
------------

### Simple

    python setup.py install

### Using eggs

    python setup.py bdist_egg
    cd dist
    easy_install <package_name>

Getting started
---------------

To see videogen options type videogen --help. If you want to create a video from the data/config1.xml file, with output called video1.avi
using /home/user/tmp as a catalogue for temporary files and use an external ffmpeg binary, type:

videogen -c data/config1.xml -o video1.avi -t /home/user/tmp/ -e /path/to/external/ffmpeg.

The XML file can load video files (load type="VideoFile" or load type="AudioVideoFile" depending if we need audio from the original video),
audio files (load type="AudioFile") and images (load type="ImageFile"). There is also a possibility to generate
a solid background - generate type="BackgroundGenerate" and a similiar option for audio silence (generate type="SilenceGenerate").
For XML examples, see the data catalogue.

Authors
-------

See AUTHORS file.

License
-------

VideoGen is released under The MIT License. See LICENSE file.
