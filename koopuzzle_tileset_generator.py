#!/usr/bin/python
# -*- coding: latin-1 -*-

# Koopuzzle Tileset Generator - Edits Koopuzzle Tileset BINs
# Version 1.3
# Copyright (C) 2013-2014 RoadrunnerWMC
# Started 7/10/13

# This file is part of Koopuzzle Tileset Generator.

# Koopuzzle Tileset Generator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Koopuzzle Tileset Generator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Koopuzzle Tileset Generator.  If not, see <http://www.gnu.org/licenses/>.



# koopuzzle_tileset_generator.py
# This is the main executable for Koopuzzle Tileset Generator


################################################################
################################################################

version = '1.3'



# Imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets



############################################
############################################
############# Tileset Viewer ###############


class TilesetViewer(QtWidgets.QLabel):
    """Widget that opens/renders/saves/exports/imports Koopuzzle tilesets"""
    XTiles, YTiles = 32, 15 # size of a KP tileset

    def __init__(self):
        """Initialises the TilesetViewer"""
        global FilePath
        QtWidgets.QLabel.__init__(self)
        self.colorformat = 'RGB4A3'

        # Add a light BG to make it look nicer
        self.setBackgroundRole(QtGui.QPalette.Light)
        self.setAutoFillBackground(True)

    def updateView(self):
        """Updates the label to reflect changes to self.img"""
        self.setPixmap(QtGui.QPixmap.fromImage(self.img))

    def load(self, path):
        """Loads/renders a tileset"""
        # Load the file
        file = open(path, 'rb')
        data = file.read()
        file.close()

        # Render the data
        if len(data) < 800000: # sizes vary somewhat
            self.img = self.RGB4A3Decode(data)
            self.colorformat = 'RGB4A3'
        else:
            self.img = self.RGBA8Decode(data)
            self.colorformat = 'RGBA8'
        self.updateView()

    def loadFromImage(self, path):
        """Creates self.pixmap from a file"""
        image = QtGui.QImage(path)
        if (image.width(), image.height()) != (896, 420):
            QtGui.QMessageBox.warning(self, 'Invalid Dimensions', 'This is not an 896x420 image!')
            return

        self.img = image
        self.colorformat = 'RGB4A3'
        self.updateView()

    def save(self, path):
        """Saves a tileset from self.pixmap"""
        if self.colorformat == 'RGB4A3': data = self.RGB4A3Encode(self.img)
        else: data = self.RGBA8Encode(self.img)
        F = open(path, 'wb')
        F.write(data)
        F.close()
        del F

    def export(self, path):
        """Exports to path"""
        self.img.save(path)




    # Decoding/Encoding (RGB4A3)
    # From Puzzle (heavily modified)
    def RGB4A3Decode(self, tex):
        """Decodes a RGB4A3-encoded image and returns it"""
        progress = QtWidgets.QProgressDialog()
        progress.setLabelText('Rendering (RGB4A3 format)...')
        progress.show()

        dest = QtGui.QImage(896,420,QtGui.QImage.Format_ARGB32)
        dest.fill(QtCore.Qt.transparent)

        i = 0
        for ytile in range(0, 420, 4):
            for xtile in range(0, 896, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):

                        try: newpixel = (tex[i] << 8) | tex[i+1]
                        except IndexError: continue
                        except TypeError: # Python 2 opens binary files as strings
                            newpixel = (ord(tex[i]) << 8) | ord(tex[i+1])

                        if (newpixel >= 0x8000): # Check if it's RGB555
                            red = ((newpixel >> 10) & 0x1F) * 255 / 0x1F
                            green = ((newpixel >> 5) & 0x1F) * 255 / 0x1F
                            blue = (newpixel & 0x1F) * 255 / 0x1F
                            alpha = 0xFF
                        else: # If not, it's RGB4A3
                            alpha = ((newpixel & 0x7000) >> 12) * 255 / 0x7
                            blue = ((newpixel & 0xF00) >> 8) * 255 / 0xF
                            green = ((newpixel & 0xF0) >> 4) * 255 / 0xF
                            red = (newpixel & 0xF) * 255 / 0xF

                        alpha, red, green, blue = int(alpha), int(red), int(green), int(blue)

                        argb = (red) | (green << 8) | (blue << 16) | (alpha << 24)
                        i += 2
                        dest.setPixel(xpixel, ypixel, argb)
            progress.setValue(ytile/self.YTiles*28)

        progress.close()
        del progress
        return dest

    def RGB4A3Encode(self, image):
        """Encodes a RGB4A3-encoded image and returns it"""
        progress = QtWidgets.QProgressDialog()
        progress.setLabelText('Encoding (RGB4A3)...')
        progress.show()

        dest = []
        blankPixels = 0 # to cut off the end of the file to save space
        for ytile in range(0, 420, 4):
            if blankPixels == None: blankPixels = 0
            
            for xtile in range(0, 896, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):

                        pixel = image.pixel(xpixel, ypixel)

                        a = int(pixel >> 24)
                        r = int((pixel >> 16) & 0xFF)
                        g = int((pixel >> 8) & 0xFF)
                        b = int(pixel & 0xFF)

                        # Use RGB4A3 because RGB555 isn't used in any Newer tilesets
                        alpha = int(a/32)
                        red = int(r/16)
                        green = int(g/16)
                        blue = int(b/16)
                        rgbDAT = (blue) | (green << 4) | (red << 8) | (alpha << 12)

                        dest.append(rgbDAT >> 8)
                        dest.append(rgbDAT & 0xFF)

                        # Keep track of blank pixels
                        if (a == 0) and (blankPixels != None): blankPixels += 2
                        else: blankPixels = None

            # Update progress
            progress.setValue(ytile/self.YTiles*28)

        # Cut off the end of the file if it has a lot of blank pixels
        if blankPixels != None: dest = dest[:len(dest)-blankPixels]

        progress.close()
        del progress
        if sys.version[0] == '2':
            # Py2 saves binary files as strings
            string = ''
            for i in dest: string += chr(i)
            return string
        else: # Py3 uses bytes()
            return bytes(dest)


    # Decoding/Encoding (RGBA8)
    # Not from Puzzle
    def RGBA8Decode(self, tex):
        """Decodes a RGBA8-encoded image and returns it"""
        progress = QtWidgets.QProgressDialog()
        progress.setLabelText('Rendering (RGBA8 Format)...')
        progress.show()

        dest = QtGui.QImage(896, 420, QtGui.QImage.Format_ARGB32)
        dest.fill(QtCore.Qt.transparent)
        P = QtGui.QPainter(dest)

        i = 0
        for ytile in range(0, 420, 4):
            for xtile in range(0, 896, 4):
                A = []
                R = []
                G = []
                B = []
                try:
                    for AR in range(16):
                        A.append(tex[i])
                        R.append(tex[i+1])
                        i += 2
                    for GB in range(16):
                        G.append(tex[i])
                        B.append(tex[i+1])
                        i += 2
                except IndexError: continue

                j = 0
                for ypixel in range(ytile, ytile+4):
                    for xpixel in range(xtile, xtile+4):
                        try: P.setPen(QtGui.QPen(QtGui.QColor.fromRgb(R[j], G[j], B[j], A[j])))
                        except TypeError: # Python 2 opens binary files as strings
                            P.setPen(QtGui.QPen(QtGui.QColor.fromRgb(ord(R[j]), ord(G[j]), ord(B[j]), ord(A[j]))))
                        P.drawPoint(xpixel, ypixel)
                        j += 1
            progress.setValue(ytile/self.YTiles*28)

        progress.close()
        del progress
        del P
        return dest


    def RGBA8Encode(self, image):
        """Encodes a RGBA8-encoded image and returns it"""
        progress = QtWidgets.QProgressDialog()
        progress.setLabelText('Encoding (RGBA8)...')
        progress.show()

        dest = []

        i = 0
        for ytile in range(0, 420, 4):
            for xtile in range(0, 896, 4):
                A = []
                R = []
                G = []
                B = []
                for ypixel in range(ytile, ytile+4):
                    for xpixel in range(xtile, xtile+4):
                        pixel = image.pixel(xpixel, ypixel)
                        A.append(int(pixel >> 24))
                        R.append(int((pixel >> 16) & 0xFF))
                        G.append(int((pixel >> 8) & 0xFF))
                        B.append(int(pixel & 0xFF))

                for color in range(16):
                    dest.append(A[color])
                    dest.append(R[color])
                for color in range(16):
                    dest.append(G[color])
                    dest.append(B[color])
            progress.setValue(ytile/self.YTiles*28)

        progress.close()
        del progress
        if sys.version[0] == '2':
            # Py2 saves binary files as strings
            string = ''
            for i in dest: string += chr(i)
            return string
        else: # Py3 uses bytes()
            return bytes(dest)



############################################
############################################
############# Other Dialogs ################



class ColorFormatDialog(QtWidgets.QDialog):
    """Dialog which asks for a color format"""
    formats = ('RGB4A3', 'RGBA8')
    def __init__(self, first):
        """Initialises the dialog"""
        QtWidgets.QDialog.__init__(self)

        # Create an info label
        info = """Pick a format to save the color data in. The default is RGB4A3.

- RGB4A3: Small files, good quality. Used for most tilesets.
- RGBA8: Much larger files, slightly higher quality. Not used often.
"""
        infoLabel = QtWidgets.QLabel(info)

        # Create the radiobuttons
        self.Btn5A3 = QtWidgets.QRadioButton('RGB4A3')
        self.Btn8   = QtWidgets.QRadioButton('RGBA8')
        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.Btn5A3)
        self.group.addButton(self.Btn8)
        self.group.setExclusive(True)
        if first == 'RGB4A3': self.Btn5A3.setChecked(True)
        else: self.Btn8.setChecked(True)

        # Create the radiobutton groupbox
        L = QtWidgets.QHBoxLayout()
        L.addWidget(self.Btn5A3)
        L.addWidget(self.Btn8)
        B = QtWidgets.QGroupBox('Color Format')
        B.setLayout(L)

        # Create the buttonbox
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # Create the layout
        L = QtWidgets.QVBoxLayout()
        L.addWidget(infoLabel)
        L.addWidget(B)
        L.addWidget(buttonBox)
        self.setLayout(L)

    def currentSetting(self):
        """Returns the current setting"""
        if self.Btn5A3.isChecked(): return 'RGB4A3'
        else: return 'RGBA8'




############################################
############################################
############## Main Window #################


class MainWindow(QtWidgets.QMainWindow):
    """Main window"""
    def __init__(self):
        """Initialises the window"""
        QtWidgets.QMainWindow.__init__(self)

        # Create the viewer
        self.view = TilesetViewer()
        self.setCentralWidget(self.view)

        # Create the menubar and a few actions
        self.CreateMenubar()

        # Set window title and show the window
        self.setWindowTitle('Koopuzzle Tileset Generator ' + version)
        self.show()

    def CreateMenubar(self):
        """Sets up the menubar"""
        m = self.menuBar()

        # File Menu
        f = m.addMenu('&File')

        newAct = f.addAction('New Tileset from Image...')
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(self.HandleNew)
        newAct.setIcon(self.GetIcon('new'))

        openAct = f.addAction('Open Tileset...')
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.HandleOpen)
        openAct.setIcon(self.GetIcon('open'))

        self.saveasAct = f.addAction('Save Tileset As...')
        self.saveasAct.setShortcut('Ctrl+S')
        self.saveasAct.triggered.connect(self.HandleSaveAs)
        self.saveasAct.setIcon(self.GetIcon('saveas'))
        self.saveasAct.setEnabled(False)

        self.exportAct = f.addAction('Export Image...')
        self.exportAct.setShortcut('Ctrl+E')
        self.exportAct.triggered.connect(self.HandleExport)
        self.exportAct.setIcon(self.GetIcon('export'))
        self.exportAct.setEnabled(False)

        f.addSeparator()

        exitAct = f.addAction('Exit')
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.HandleExit)
        exitAct.setIcon(self.GetIcon('exit'))

        # Settings Menu
        s = m.addMenu('&Settings')

        self.formatAct = s.addAction('Set Color Format...')
        self.formatAct.setShortcut('Ctrl+C')
        self.formatAct.triggered.connect(self.HandleColorFormat)
        self.formatAct.setIcon(self.GetIcon('colors'))
        self.formatAct.setEnabled(False)

        # Help Menu
        h = m.addMenu('&Help')
        aboutAct = h.addAction('About...')
        aboutAct.setShortcut('Ctrl+H')
        aboutAct.triggered.connect(self.HandleAbout)
        aboutAct.setIcon(self.GetIcon('about'))

    def GetIcon(self, name):
        try: return QtGui.QIcon(QtGui.QPixmap('data/icon-' + name + '.png'))
        except: return QtGui.QIcon() # fail silently


    def HandleNew(self):
        """Creates a new file from a base image"""
        fp = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose an Image', '', 'Portable Network Graphics (*.png);;All Files (*)')[0]
        if fp == '': return

        self.view.loadFromImage(fp)
        self.setWindowTitle('Koopuzzle Tileset Generator %s - Untitled' % version)
        self.saveasAct.setEnabled(True)
        self.exportAct.setEnabled(True)
        self.formatAct.setEnabled(True)

    def HandleOpen(self):
        """Opens a file"""
        fp = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Tileset', '', 'Koopuzzle Tilesets (*.bin);;All Files (*)')[0]
        if fp == '': return

        self.view.load(fp)
        self.setWindowTitle('Koopuzzle Tileset Generator %s - %s' % (version, fp.replace('\\', '/').split('/')[-1]))
        self.saveasAct.setEnabled(True)
        self.exportAct.setEnabled(True)
        self.formatAct.setEnabled(True)

    def HandleSaveAs(self):
        """Saves to a new file"""
        fp = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Tileset As', '', 'Koopuzzle Tilesets (*.bin);;All Files (*)')[0]
        if fp == '': return

        self.view.save(fp)
        self.setWindowTitle('Koopuzzle Tileset Generator %s - %s' % (version, fp.replace('\\', '/').split('/')[-1]))

    def HandleExport(self):
        """Exports the tileset to a PNG"""
        fp = QtWidgets.QFileDialog.getSaveFileName(self, 'Export Tileset', '', 'Portable Network Graphics (*.png);;All Files (*)')[0]
        if fp == '': return

        self.view.export(fp)

    def HandleExit(self):
        """Exits"""
        exit()

    def HandleColorFormat(self):
        """Changes the tileset encoding format"""
        dlg = ColorFormatDialog(self.view.colorformat)
        if dlg.exec_() != QtWidgets.QDialog.Accepted: return

        self.view.colorformat = dlg.currentSetting()

    def HandleAbout(self):
        """Shows the About dialog"""
        try: readme = open('readme.md', 'r').read()
        except: readme = 'Koopuzzle Tileset Generator %s by RoadrunnerWMC\n(No readme.txt found!)\nLicensed under the GPL 3' % version

        txtedit = QtWidgets.QPlainTextEdit(readme)
        txtedit.setReadOnly(True)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(txtedit)
        layout.addWidget(buttonBox)

        dlg = QtWidgets.QDialog()
        dlg.setLayout(layout)
        dlg.setModal(True)
        dlg.setMinimumWidth(384)
        buttonBox.accepted.connect(dlg.accept)
        dlg.exec_()




# Main function
def main():
    """Main startup function"""
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
main()
