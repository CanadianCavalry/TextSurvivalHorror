from distutils.core import setup
import py2exe

musicFiles = ['Music/Oblivion.mp3']
soundFiles = ['Sounds/RevolverShot.mp3']

setup (console=['__init__.py'],
data_files=[('sounds',soundFiles), ('music', musicFiles)])