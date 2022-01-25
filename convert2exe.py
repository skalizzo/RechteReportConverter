"""
dieses Skript wandelt den rr_converter.py in eine ausführbare .exe Datei um
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    'rr_converter.py',
    '--onefile',
    #'--windowed'
])
