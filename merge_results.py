import os
from xlwt import Workbook
from statistics import *
import pandas as pd

def mergeResults(path=''): 
    sheets_generated = False
    sheets = []
    WB = Workbook()  # Excel Sheet
    output_path = path + "/summary.xls"
    # folders = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]
    # for folder in folders: 
    #     print(folder)
    #     summary_path = path + "/" + folder + "/summary.xls"
    #     xls = pd.ExcelFile(summary_path)
    #     if not sheets_generated: 
    #         sheets = createSheets(WB, summary_path)
    #         sheets_generated = True
    #     for index, sheet_name in enumerate(xls.sheet_names):
    #         sheet, row_index = sheets[index]
    #         sheets[index] = appendSheet(row_index, sheet, pd.read_excel(xls, sheet_name))
    # WB.save(output_path)

    generateResults(output_path, path)
def appendSheet(startIndex, sheet, data): 
    print("Appending to sheet "  + " at row " + str(startIndex) + " with data length = " + str(len(data)))
    for index in range(0, len(data)): 
        print(index)
        row = data.iloc[index]
        for i, val in enumerate(row): 
            sheet.write(startIndex, i, str(val))
        startIndex += 1
    return sheet,startIndex
def createSheets(excel_sheet, template_path): 
    xls = pd.ExcelFile(template_path)
    
    sheets = []
    for sheet_name in xls.sheet_names: 
        # TODO Insert new sheet into excel sheet
        template_sheet = pd.read_excel(xls, sheet_name)
        sheet = excel_sheet.add_sheet(sheet_name)
        i = 0 
        for column in template_sheet[:0]: 
            sheet.write(0, i, column)
            i+=1
        
        sheets.append([sheet, 1])
        
        
    return sheets


mergeResults('/Users/mostafa/python/filter_trajectory/results/report/fuzzy_fixed_fuzzy-fixed_original')