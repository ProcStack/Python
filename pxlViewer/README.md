# **pxlViewer**
-----------------------------------
### **A PyQt and WebView based image viewer.**


*(ALPHA; Work in progress; will compile to PyInstaller shortly; currently intended for linux)*


I was getting a little tired of the default options in linux; so I made this.

______________________________

I've linked it to an alias for ease of use; in my *.bash_aliases* file I added-

**`alias v='python /your/path/to/pxlViewer/viewer.py '`**


It can be ran locally from any folder--

**`v imageFile.jpg`**

**`-debug`** , **`-d`**   ; flag to enter debug mode

**`Left click`** drag to move image around

**`Wheel up/down`** or **`right click drag`** to zoom *(Right click zoom is WIP)*

**`Double click any button`** or **`resize the window`** will reset the zoom; fits the image to your window.
*(Clicking seems buggy right now, click more than twice in a row)*

**`Escape`** to close pxlViewer
