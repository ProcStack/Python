Comments to come, my apologies

This is a dump for a pixel processing test using pygame.

** Pygame is very slow for full screen pixel processing, this was made with the intention of running on a RaspberryPi, but it seems OpenGL is the better option in this situation**


Here is the kind of effects you'll see with this script-

https://www.youtube.com/watch?v=NvqFOaD-OWo

https://www.youtube.com/watch?v=-U6eKRmdEyo

-----------------

What you'll find in this python script-

Pixel processing on a per pixel level using an array of [R1,G1,B1, R2,G2,B2, ... R#,G#,B#]

RGB to HSV;  HSV to RGB (I'm still working out a bug when Hue rolls over past 1.  0-1 should be the same Hue, but is not

Rotating values around a given postion in the screen

Transitions between modes


-----------------

Command to run- ** Hit Escape to quit **

python visualizer.py (verbosePrint) (Visual#; 0-6) (Resolution#) (ScreenShots/Windowed mode)

Resolution of 20--

python visualizer.py 20

Mode 4; resoltion of 10--

python visualizer.py 4 10

Verbose printing on screen, resolution 10--

python visualizer.py v 10

Windowed resolution of 20--

python visualizer.py 20 w

-----------------

!! Important Python Modules & Linux apt-get commands ~~

** I'll update this list with the windows module documentation pages in time, you will need to install these modules for python manually for Windows/Mac**

GTK-

sudo apt-get install python-gtk2


CTypes-

sudo apt-get install python-ctypeslib



Pygame-

sudo apt-get install python-pygame


Xlib-

sudo apt-get install libx11-dev



Muliprocessing- (Not used as much as I'd like to be using it in this script)

sudo apt-get install python-multiprocessing



Numpy-

Just a heads up, I ran into some issues with running Numpy, finding out that I'd need to uninstall it and reinstall it, you 
might not need to do this

- From - http://stackoverflow.com/questions/9449309/how-to-correctly-install-python-numpy-in-ubuntu-11-10-oneiric

sudo apt-get remove python-numpy

sudo rm -r /usr/local/lib/pythonX.X/dist-packages/numpy

sudo apt-get install python-numpy
