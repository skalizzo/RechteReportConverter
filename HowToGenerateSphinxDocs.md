# Sphinx Autodoc - HowTo 

## Dokumentation generieren

1. ein Verzeichnis erstellen (z.B. "docs"), in dem die Dokumentation abgelegt werden soll
2. per Terminal in das Verzeichnis wechseln
3. über ```sphinx-quickstart``` werden die initialen Dateien generiert
4. in der conf.py folgende Lines auskommentieren und den Pfad des initialen Moduls referenzieren 
(hier 2 Verzeichnisse über dem Verzeichnis, in dem conf.py liegt) 
: ```sys.path.insert(0, os.path.abspath('../..'))```

    Außerdem muss das autodoc Modul geladen werden: 
    ```
    extensions = ['sphinx.ext.autodoc']
    ```
7. über ```sphinx-autodoc -f -o docs/source ..``` können die nötigen rst-Files automatisch generiert werden.
Diese Files steuern, welcher Inhalt in die Dokumentation übernommen wird. 
Es wird u.a. ein File 'modules.rst' generiert.
8. in der 'index.rst' kann dann modules (oder auch andere Daten) wie folgt hinzugefügt werden:
    ```
    .. toctree::
       :maxdepth: 2
       :caption: Contents:
    
       modules
    ```
   Diese Daten tauchen dann als extra Menüpunkt auf.
9. über ```make html``` können dann die html-Files erzeugt werden
   Falls Fehler auftauchen können die erzeugten Files über ```make clean``` 
   wieder entfernt werden

## Styling
in der ```conf.py``` kann der Output auch gestylt werden:
Ein schönes HTML-Thema ist zum Beispiel folgendes:
```
html_theme = 'sphinx_rtd_theme' 
```