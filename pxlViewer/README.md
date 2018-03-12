# **pxlViewer**  *v0.0.6*
-----------------------------------
### **A PyQt and WebView based image viewer.**


*(Currently only intended for linux)*


I was getting a little tired of the default options in linux; so I made this thing.

http://metal-asylum.net/github/pxlViewer06Updates.gif

______________________________

I've linked it to an alias for ease of use; in my *.bash_aliases* file I added-

**`alias v='python /your/path/to/pxlViewer.py '`**


It can be ran locally from any folder--

With no specified file to load, the first image found is displayed.

**`v`**

Or with a specific file given; currently only relative paths work. Sorry, absolute path support soon to come.

**`v imageFile.jpg`**
______________________________

**`Left click drag`** to move image around

**`Wheel up/down`** or **`right click drag`** to zoom

Hitting **`Spacebar`**, **`H`**, or **`Return`** will reset the zoom; fitting the image to your window.

**`R`** to refresh the current image

**`Escape`** will close pxlViewer

**`Left Key`** loads Previous image in directory.

**`Right Key`** loads Next image in directory.

**`F`** toggles full screen.

**`Alt key`** toggles menuBar; displays 'File' 'Image Info' and 'Help.
`Image Into` displays the file name, resolution, and file size of the image.
`Help` displays keyboard shortcuts.

Use the **`-debug`** or **`-d`** flag to enter debug mode.  Allows for inspecting the WebView's page; the developer tools window.

