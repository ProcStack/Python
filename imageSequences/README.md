**These scripts are good for creating, editing, and converting image sequences**

**They are mostly wrappers for linux commands, but with added logic**

--------------------

Script - **cropSequence.py**

Used to crop an image sequence within the folder the script is ran.

Prepends a given variable, 'crop' by default

Command - **python *Path*/cropSequence.py [0,0,500,250]**

--------------------


Script - **slimSeq.py**

Slim image/file sequences down by copying every N frame to the same folder as the image sequence with 'slim' prepended.


For movies, having a lot of frames is great for smooth video

But when it comes to generating gifs, without using a color pallette map, every frame counts in its file size

Ending up with a 20 meg gif to display on the web is never fun for cell phone users not on wifi


Supports any sequence with a number in a shared position - *name.#.ext / name_#.ext / name#.ext*

Command - **python *Path*/slimSeq.py [-v -s #] sequenceName.#.ext**
