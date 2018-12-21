"""
Measuring the colour response of a Raspberry Pi camera

This script uses an RGB LED (via an Arduino) to find the response
of the Raspberry Pi camera to red, green, and blue light.  This
goes further than the lens shading correction, as it measures the
off-diagonal terms (i.e. crosstalk between colour channels).  NB
the assumption that we can produce a valid correction based on raw
images isn't necessarily correct; in general it is probably 
necessary to use some sort of closed-loop process to get something
that works reliably with processed images.

(c) Richard Bowman 2018, released under GPL v3

"""
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from set_colour import SingleNeoPixel
from contextlib import closing
import time
import yaml

def rgb_image(camera, resize=None, **kwargs):
    """Capture an image and return an RGB numpy array"""
    with PiRGBArray(camera, size=resize) as output:
        camera.capture(output, format='rgb', resize=resize, **kwargs)
        return output.array

if __name__ == "__main__":
    print("Checking for lens shading support...", end="")
    if not hasattr(PiCamera, "lens_shading_table"):
        print("not present.")
        raise ImportError("This program requires the forked picamera library with lens shading support")
    else:
        print("present")

    print("Generating a flat lens shading table")
    with PiCamera() as cam:
        lens_shading_table = np.zeros(cam._lens_shading_table_shape(), dtype=np.uint8) + 32

    with PiCamera(lens_shading_table=lens_shading_table, resolution=(640,480)) as camera, \
         SingleNeoPixel() as led:
        print("Turning on the LED and letting the camera auto-expose", end="")
        led.set_rgb(255,255,255)
        camera.start_preview()
        for i in range(6):
            print(".", end="")
            time.sleep(0.5)
        print("done")

        print("Freezing the camera settings...")
        camera.shutter_speed = camera.exposure_speed
        print("Shutter speed = {}".format(camera.shutter_speed))
        camera.exposure_mode = "off"
        print("Auto exposure disabled")
        g = camera.awb_gains
        camera.awb_mode = "off"
        camera.awb_gains = g
        print("Auto white balance disabled, gains are {}".format(g))
        print("Analogue gain: {}, Digital gain: {}".format(camera.analog_gain, camera.digital_gain))

        print("Adjusting shutter speed to avoid saturation", end="")
        for i in range(3):
            print(".", end="")
            camera.shutter_speed = int(camera.shutter_speed * 230.0 / np.max(rgb_image(camera)))
            time.sleep(1)
        print("done")

        camera_settings = {k: getattr(camera, k) for k in ['analog_gain', 'digital_gain', 'shutter_speed', 'awb_gains', 'awb_mode', 'exposure_mode', 'lens_shading_table']}
        with open("output/camera_settings.yaml", "w") as outfile:
            yaml.dump(camera_settings, outfile)
        
        print("Taking measurement")
        fig, ax = plt.subplots(3, 4, figsize=(8,7))
        for i, rgb in enumerate([(255,255,255), (255,0,0), (0,255,0), (0,0,255)]):
            print("Setting illumination to {}".format(rgb))
            led.set_rgb(*rgb)
            time.sleep(1)
            print("Capturing raw image")
            camera.capture("output/capture_r{}_g{}_b{}.jpg".format(*rgb), bayer=True)
            rgb = rgb_image(camera)
            channels = ["red", "green", "blue"]
            for j, channel in enumerate(channels):
                cm = LinearSegmentedColormap(channel+"map",
                        {c: [(0,0,0),(1,1,1)] if c==channel 
                            else [(0,0,0),(0.95,0,1),(1,1,1)] 
                            for c in channels})
                ax[j,i].imshow(rgb[:,:,j], vmin=0, vmax=255, cmap=cm)

        plt.savefig("output/preview.pdf")
    plt.show()



