# RechteReport-Converter

## Was macht dieses Tool?

Der RR-Converter konvertiert Rechtedaten aus dem LizenzLEA Format (zeilenbasiert) in das alte RechteReport-Format (spaltenbasiert)

## Usage

+ Aus der LDB kann in der Gesamt-LizenzLEA ein Report generiert werden 

> #### Vorfilter: 
> + Art= EK; 
> + Recht=T-VoD, EST; 
> + Land=Deutschland, Österreich, Dt. Schweiz, Liechtenstein, Luxemburg, Südtirol (Alto Adige); 
> + Mandant = Leonine Licensing, Leonine Distribution, Concorde; 
> + Archiv-Flag ankreuzen damit auch diese Titel mit reinkommen (WICHTIG!!!))
+ --> dann LizenzLEA generieren und in beliebiges Feld mit rechter Maustaste klicken und File als ".xlsx"-Datei
exportieren
+ --> diese Datei muss in den 'import'-Ordner gelegt werden und dann kann der Converter gestartet werden 
(Doppelklick auf 'rr_converter.exe')
+ --> die generierte Datei wird im 'export'-Ordner abgelegt. Sie kann in die Titelplanungen per 'import RR-Report' 
eingelesen werden, genau wie die alten Rechte-Reports