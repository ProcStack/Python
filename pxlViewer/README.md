# **pxlViewer**  *v0.0.5*
-----------------------------------
### **A PyQt and WebView based image viewer.**


*(Currently only intended for linux)*


I was getting a little tired of the default options in linux; so I made this thing.

http://metal-asylum.net/github/pxlViewer.gif

______________________________

I've linked it to an alias for ease of use; in my *.bash_aliases* file I added-

**`alias v='python /your/path/to/pxlViewer.py '`**


It can be ran locally from any folder--

**`v imageFile.jpg`**

Use the **`-debug`** or **`-d`** flag to enter debug mode.  Allows for inspecting the WebView's page; the developer tools window.

**`Left click drag`** to move image around

**`Wheel up/down`** or **`right click drag`** to zoom

Hitting **`Spacebar`**, **`H`**, or **`Return`** will reset the zoom; fitting the image to your window.

**`R`** to refresh the current image

**`Escape`** will close pxlViewer
