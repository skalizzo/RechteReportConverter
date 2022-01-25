import logging
import os
import sys
from datetime import datetime, date
LOG_DIR = os.path.join(os.curdir, 'Logfiles')
LOG_FILE = os.path.join(LOG_DIR, f'rr_converter_log_{datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}.log')
print("logging status to ", LOG_FILE)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s')
from tqdm import trange
import os
import traceback
from typing import List
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)


class RR_Converter:
    """
    Ein Command Line Tool mit dem man die Rechtedaten aus der LDB LizenzLea (neue Rechteverwaltung)
    in einen Rechtereport umwandeln kann, der dem Format des alten RechteReports entspricht.
    Enthält nur EST und TVOD-Rechte, keine Holdbacks.
    """
    def __init__(self):
        print('starting RechteReport-Converter')
        logging.info(f'RechteReportConverter gestartet von {os.getlogin()}')
        for folder in ["./export", "./import"]:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def convert_rights_report_to_old_version(self):
        """
        liest neueste xlsx Datei
        :return:
        """

        filepath_rights_report = self.get_latest_rechte_report(
            os.path.join(application_path, 'import')
        )
        if not filepath_rights_report:
            logging.error(
                """ERROR: Kein XLSX File im 'import'-Ordner gefunden. 
Bitte lege den Export der LizenzLEA als xlsx File im import-Ordner ab und starte das Tool erneut."""
            )
            return
        logging.info(f'Verwende jüngste Datei: {filepath_rights_report}')
        print('reading rights report')
        try:
            df = pd.read_excel(filepath_rights_report)
        except:
            logging.error(
                """ERROR: Konnte Daten vom Excel File nicht lesen. Eventuell ist es in einem anderen Programm geöffnet?"""
            )
            return
        # print(df.head())
        print('converting rights')
        try:
            title_data = self.get_rights_data(df)
        except:
            logging.error(
                f"""ERROR: Fehler beim konvertieren der Daten aus der LizenzLEA in das alte RR-Report-Format
                {traceback.format_exc()}"""
            )
            return

        try:
            self.export_excel_report(title_data)
        except:
            logging.error(
                f"""ERROR: Fehler beim Export der Daten.
                {traceback.format_exc()}"""
            )
            return
        logging.info(f'SUCCESS: Export der Daten ins alte RR-Format erfolgreich. Der exportierte Report liegt im "export"-Ordner ')
        print('Export erfolgreich abgeschlossen. Die Datei liegt im export-Ordner ab.')

    def export_excel_report(self, title_data:List[dict], filename="export/rechtereport.xlsx"):
        """
        exportiert den Rechtereport als XLSX-Datei
        die erste Zeile wird freigelassen, danach kommt der Header (um dem Format des alten Reports zu entsprechen)
        :param title_data: eine Liste, die für jeden Titel bzw. jede Tnr ein Dictionary mit Rechtedaten enthält
        :param [OPTIONAL] filename: der relative Pfad und Dateiname unter dem der Report abgespeichert werden soll
        (sollte eine .xlsx-Datei sein)
        :return:
        """
        print('exporting file to "export" folder')
        df = pd.DataFrame(title_data, columns=title_data[0].keys())
        columns = [
            # 'TNR',
            'LG',
            'LG-Nr.',  # leer
            'V_Name',
            'V_NR',
            'Titelname',
            'TNR',
            'Lizenzende',
            'T-ungültig',
            'Label',
            'Brands',
            'kino1',
            'kino2',
            'kino3',
            'video1',
            'video2',
            'video3',
            'video4',
            'video5',
            'tv1',
            'tv2',
            'tv3',
            'tv4',
            'tv5',
            'tv6',
            'tv7',
            'anc1',
            'anc2',
            'anc3',
            'anc4',
            'anc5',
            'land1',
            'land2',
            'land3',
            'klammerrecht',
            'dd1',
            'dd2',
            'dd3',
            'dd4',
            'dd5',
            'TVOD',
            'dd6',
            'EST',
            'dd7',
            'dd8',
            'DE',
            'CH',
            'AT',
            'LUX',
            'LIE',
            'dd9',
            'AA',
            'SO_ID',
        ]
        for col in columns:
            if not col in df.columns:
                df[col] = ''
        df = df[columns]
        filename = f"export/RechteReportOldFormat_{date.today().strftime('%Y-%m-%d')}.xlsx"
        df.to_excel(filename, sheet_name='RR', index=False, startrow=1)

    def get_latest_rechte_report(self, directory: str) ->os.PathLike:
        """
        sucht die zuletzt erstellte/modifizierte Datei in einem gegebenen Verzeichnis
        :param directory: der Ordner in dem gesucht werden soll als String
        :return:
        """
        # get list of xlsx files in current directory
        print('searching for latest Report within the "import"-directory')
        try:
            files = {
                f: os.path.getmtime(os.path.join(directory, f)) for f in os.listdir(str(directory))
                if os.path.isfile(os.path.join(directory, f))
                   and str(os.path.splitext(f)[1]).lower() == ".xlsx"
            }
            latest_file = ""
            if len(files) == 0:
                print('keine Dateien gefunden.')
                return
            elif len(files) == 1:
                latest_file = list(files.keys())[0]
            # if multiple files determine latest file
            elif len(files) > 1:
                latest_file = max(files, key=files.get)
            print('neuester gefundener Report: ',latest_file)
            return os.path.join(directory, latest_file)
        except:
            print(traceback.format_exc())
            logging.error(
                """ERROR: Kein XLSX File im 'import'-Ordner gefunden. 
Bitte lege den Export der LizenzLEA als xlsx File im import-Ordner ab und starte das Tool erneut."""
            )
            return



    def get_rights_data(self, df: pd.DataFrame) ->List[dict]:
        """
        konvertiert Rechtedaten aus LizenzLEA Format (zeilenbasiert) in altes RechteReport-Format (spaltenbasiert)
        :param df: DataFrame mit eingelesenem LizenzLEA-Export
        :return: Liste mit 1 Dictionary je Titelnummer
        """
        # get unique tnr values from LizenzLEA report
        titelnummern = df['Titel-Nr.'].unique().tolist()

        end_dates = dict()
        df['Lizenzende'] = df['Lizenzende'].astype('datetime64', errors='ignore')

        title_data = []

        i = 0
        nr_of_titles = len(titelnummern)

        for i in trange(nr_of_titles):
            tnr = titelnummern[i]
            #print(int((i / nr_of_titles) * 100))
            #i += 1
            est = ''
            tvod = ''
            de = ''
            at = ''
            ch = ''
            lu = ''
            li = ''
            aa = ''
            licensor = ''
            so_nr = ''
            vertragsnummer = ''
            vertragsname = ''
            titelname = ''

            rights = set()
            countries = set()
            so_nrs = set()
            licensors = set()
            vertragsnummern = set()
            vertragsnamen = set()
            titelnamen = set()
            try:
                rights = set(df[(df['Titel-Nr.'] == tnr)]['Recht'].unique().tolist())
                countries = set(df[(df['Titel-Nr.'] == tnr)]['Territorium'].unique().tolist())
                so_nrs = set(df[(df['Titel-Nr.'] == tnr)]['SO-Nr.'].unique().tolist())
                licensors = set(df[(df['Titel-Nr.'] == tnr)]['Vertragspartner'].unique().tolist())
                vertragsnummern = set(df[(df['Titel-Nr.'] == tnr)]['Zugehörige Paketvertrags-ID'].unique().tolist())
                vertragsnamen = set(df[(df['Titel-Nr.'] == tnr)]['Zugehöriger Paketvertragsname'].unique().tolist())
                titelnamen = set(df[(df['Titel-Nr.'] == tnr)]['Titelname'].unique().tolist())
                end_date = df[(df['Titel-Nr.'] == tnr) & (df['Lizenzende'].notna())]['Lizenzende'].max()
                if not type(end_date) in (float, np.nan, np.NAN):
                    end_date = end_date.strftime('%d.%m.%Y')

            except:
                print(df[df['Titel-Nr.'] == tnr]['Lizenzende'])
                print(traceback.format_exc())
                print(end_date)
                end_date = ''

            if 'T-VoD' in rights:
                tvod = 'X'
            if 'EST' in rights:
                est = 'X'
            if 'DEU' in countries or 'Deutschland' in countries:
                de = 'X'
            if 'AUT' in countries or 'Österreich' in countries:
                at = 'X'
            if 'CHD' in countries or 'Dt. Schweiz' in countries:
                ch = 'X'
            if 'LUX' in countries or 'Luxemburg' in countries:
                lu = 'X'
            if 'LIE' in countries or 'Liechtenstein' in countries:
                li = 'X'
            if 'AA' in countries or 'Südtirol' in countries:
                aa = 'X'
            if licensors:
                licensor = licensors.pop()
            if so_nrs:
                so_nr = so_nrs.pop()
            if vertragsnummern:
                vertragsnummer = vertragsnummern.pop()
            if vertragsnamen:
                vertragsname = vertragsnamen.pop()
            if titelnamen:
                titelname = titelnamen.pop()

            title_data.append(
                {
                    'TNR': tnr,
                    'SO_ID': so_nr,
                    'Titelname': titelname,
                    'LG': licensor,
                    'V_NR': vertragsnummer,
                    'V_Name': vertragsname,
                    'Lizenzende': end_date,
                    'EST': est,
                    'TVOD': tvod,
                    'DE': de,
                    'AT': at,
                    'CH': ch,
                    'LUX': lu,
                    'LIE': li,
                    'AA': aa,
                }
            )
        return title_data



if __name__ == '__main__':
    RR_Converter().convert_rights_report_to_old_version()