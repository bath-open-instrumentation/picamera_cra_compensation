# PiCamera CRA compensation calibration jig

This folder holds the OpenSCAD designs for a simple mechanical assembly that allows you to illuminate a Raspberry Pi camera module with light of different colours, from a variable angle.  By taking measurememts with the sensor at different angles, it should be possible to figure out the optimal angle of incidence at each point on the sensor.  It should also be a convenient way to calibrate the sensor to take flat-field images, by generating a lens shading table and/or post-processing correction matrix.

The jig consists of two parts: a tube (into which the LED is mounted) and a holder for the Raspberry Pi camera module.  You may recognise quite a few of the OpenSCAD functions from the [OpenFlexure microscope](https://github.com/rwb27/openflexure_microscope/).
