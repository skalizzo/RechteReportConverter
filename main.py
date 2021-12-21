import os
import traceback
from collections import defaultdict
import xlwings as xw
import pandas as pd
pd.set_option('display.max_columns', None)
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_latest_rechte_report(directory: str):
    # get list of xlsx files in current directory
    files = {
        f: os.path.getmtime(f) for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
           and str(os.path.splitext(f)[1]).lower() == ".xlsx"
    }
    print(files)
    latest_file = ""
    if len(files) == 0:
        print('keine Dateien gefunden.')
        return
    elif len(files) == 1:
        latest_file = list(files.keys())[0]
    # if multiple files determine latest file
    elif len(files) > 1:
        latest_file = max(files, key=files.get)
    print(latest_file)
    return latest_file


def get_rights_data(df: pd.DataFrame):
    print(df.columns)
    wb = xw.Book.caller()
    wks_tp = wb.sheets['TP']
    wks_rr = wb.sheets['RR_NEU']
    # if wks_tp["AK8"].value == "Hello xlwings!":
    #     wks_tp["AK8"].value = "Bye xlwings!"
    # else:
    #     wks_tp["AK8"].value = "Hello xlwings!"
    last_row_tp = wks_tp.range('A' + str(wks_tp.cells.last_cell.row)).end('up').row
    last_row_rr = wks_rr.range('B' + str(wks_rr.cells.last_cell.row)).end('up').row
    print(last_row_tp)
    print(last_row_rr)
    # rights_dict = defaultdict(set)
    # end_dates_tvod = dict()
    # end_dates_est = dict()
    # for row_rr in range(2, last_row_rr):
    #     print(int((row_rr/last_row_rr)*100), '%')
    #     tnr = wks_rr.range('D' + str(row_rr)).value
    #     end_date = wks_rr.range('M' + str(row_rr)).value
    #     # add transaction types (T-VoD or EST)
    #     rights_dict[tnr].add(wks_rr.range('H' + str(row_rr)).value)
    #     # add country rights
    #     rights_dict[tnr].add(wks_rr.range('J' + str(row_rr)).value)
    #     for transaction_type, end_dates in {
    #         'T-VoD': end_dates_tvod,
    #         'EST': end_dates_est
    #     }.items():
    #         if wks_rr.range('H' + str(row_rr)).value == transaction_type:
    #             if end_date:
    #                 if not end_dates.get(tnr) or end_dates.get(tnr) < end_date:
    #                     end_dates[tnr] = end_date
    #
    # print(rights_dict)

    end_dates = dict()

    df['Lizenzende'] = df['Lizenzende'].astype('datetime64', errors='ignore')

    for row_tp in range(8, last_row_tp):
        rights = []
        countries = []
        print(f"{int((row_tp/last_row_tp)*100)}%")
        tnr = wks_tp.range('C' + str(row_tp)).value
        so_nr = set()
        if tnr:
            try:
                end_date = df[(df['Titel-Nr.'] == tnr) & (df['Lizenzende'].notna())]['Lizenzende'].max()
                rights = set(df[(df['Titel-Nr.'] == tnr)]['Recht'].unique().tolist())
                countries = set(df[(df['Titel-Nr.'] == tnr)]['Territorium'].unique().tolist())
                so_nr = set(df[(df['Titel-Nr.'] == tnr)]['SO-Nr.'].unique().tolist())
                licensor = set(df[(df['Titel-Nr.'] == tnr)]['Vertragspartner'].unique().tolist())
            except:
                print(df[df['Titel-Nr.'] == tnr]['Lizenzende'])
                print(traceback.format_exc())
                end_date = None
            if end_date:
                end_dates[tnr] = end_date
                wks_tp["AK" + str(row_tp)].value = end_date
            if 'T-VoD' in rights:
                wks_tp["AL" + str(row_tp)].value = 'T-VoD'
            if 'EST' in rights:
                wks_tp["AM" + str(row_tp)].value = 'EST'
            if 'DEU' in countries or 'Deutschland' in countries:
                wks_tp["AN" + str(row_tp)].value = 'DE'
            if so_nr:
                # use so_nr[0]
                pass

    print(end_dates)











def main():
    filepath_rights_report = get_latest_rechte_report(os.curdir)
    if not filepath_rights_report:
        return
    print('reading rights report')
    df = pd.read_excel(filepath_rights_report)
    #print(df.head())
    print('converting rights')
    get_rights_data(df)




if __name__ == "__main__":
    xw.Book("tp/TPDD aktuell.xlsm").set_mock_caller()
    main()
