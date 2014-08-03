# Koopuzzle Tileset Generator
(1.3)

----------------------------------------------------------------

Support:   http://rvlution.net/forums/  
On GitHub: https://github.com/RoadrunnerWMC/Koopuzzle-Tileset-Generator  

----------------------------------------------------------------

Koopuzzle Tileset Generator is a small program which can view and save RGB4A3 and RGBA8 Koopuzzle tilesets.  

----------------------------------------------------------------

### Getting Started

If you're on Windows and don't care about having the bleeding-edge latest features, you can use the official installer. This is by far the easiest setup method. The installer will take care of everything for you.

If you are not on Windows or you want the very latest features, you'll need to run Koopuzzle Tileset Generator from source.


### How to Run Koopuzzle Tileset Generator from Source

Download and install the following:
 * Python 3.4 (or newer) - http://www.python.org
 * PyQt 5.3 (or newer) - http://www.riverbankcomputing.co.uk/software/pyqt/intro
 * cx_Freeze 4.3 (or newer) (optional) - http://cx-freeze.sourceforge.net

Run the following in a command prompt:  
`python3 koopuzzle_tileset_generator.py`  
You can replace `python3` with the path to python.exe (including "python.exe" at the end) and `koopuzzle_tileset_generator.py` with the path to koopuzzle_tileset_generator.py (including "koopuzzle_tileset_generator.py" at the end)


### Koopuzzle Tileset Generator Team

Developers:
 * RoadrunnerWMC - Developer
 * Tempus - TPL decoding functions from BRFNTify

### Dependencies/Libraries/Resources

Python 3 - Python Software Foundation (https://www.python.org)  
Qt 5 - Nokia (http://qt.nokia.com)  
PyQt5 - Riverbank Computing (http://www.riverbankcomputing.co.uk/software/pyqt/intro)  
Interface Icons - FlatIcons (http://flaticons.net)  
cx_Freeze - Anthony Tuininga (http://cx-freeze.sourceforge.net)


### License

Koopuzzle Tileset Generator is released under the GNU General Public License v3.
See the license file in the distribution for information.

----------------------------------------------------------------

## Changelog

Release 1.3: (August 2, 2014)
 * New icon set
 * Added license.txt and license headers to the source files
 * New readme
 * Dropped Python 2 support
 * Added PyQt5 support
 * Switched from py2exe to cx_Freeze

 Release 1.2: (September 29, 2013)
 * Fixed bug in which Windows EXEs don't close when
   File->Exit is clicked
 * Fixed bug in which RGB4A3 tilesets don't save correctly
 * Added keyboard shortcuts

Release 1.1: (July 16, 2013)
 * Renamed "RGB5A3" to "RGB4A3"
 * Optimized RGB4A3 encoding/decoding
 * Other minor improvements

Release 1.0: (July 10, 2013)
 * Initial release
