# Set up Video Capture
0. Make sure you don't install the 64-bit version of Raspberry PI -- libmmal isn't supported on 64-bit
1. Connect camera using ribbon cable
2. `sudo raspi-config` > `3 - Interface Options` > `I1 - Legacy Camera` > `Enable`
3. Reboot
4. Run `raspistill -o image.jpg` to get an image.
5. ????
6. Profit!

# TODO
* Figure out why openCV doesn't run. Getting an error with numpy, shown below
```
ImportError: numpy.core.multiarray failed to import
```
* Image compression scheme
* Figure out what kind of processing we want to do to calculate visiblility. Do we need another peripheral? A laser?!?!?!?!