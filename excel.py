import xlrd
import xlwt
import xlutils.copy
import os
import time
def a_in_b(a, b):
    for i in b:
        if a in i:
            return 0
    return 1
def setOutCell(out_sheet, col, row, value):
    def _getOutCell(out_sheet_, colIndex, rowIndex):
        row = out_sheet_._Worksheet__rows.get(rowIndex)
        if not row: return None
        cell = row._Row__cells.get(colIndex)
        return cell
    previousCell = _getOutCell(out_sheet, col, row)
    out_sheet.write(row, col, value)
    if previousCell:
        newCell = _getOutCell(out_sheet, col, row)
        newCell.xf_idx = previousCell.xf_idx
while 1:
    colour = 2
    continue_ = str(input(
        "如需设置填充颜色请按数字代号（默认红色）:\n1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow, 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray\n"))
    try:
        if 1 <= int(continue_) <= 23:
            colour = int(continue_)
    except:
        pass
    count1 = 0
    count2 = 0
    filename1 = str(input("请输入文件1名（只支持.xls文件）：\n"))
    filename2 = str(input("请输入文件2名（只支持.xls文件）：\n"))
    writebook1 = xlwt.Workbook()
    writebook2 = xlwt.Workbook()
    name1 = filename1 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xls"
    name2 = filename2 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xls"
    os.system("copy " + filename1 + ".xls " + name1)
    os.system("copy " + filename2 + ".xls " + name2)
    workbook1 = xlrd.open_workbook(name1, formatting_info=True)
    workbook2 = xlrd.open_workbook(name2, formatting_info=True)
    worksheets1 = workbook1.sheet_names()
    worksheets2 = workbook2.sheet_names()
    workcontent1 = []
    workcontent2 = []
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = colour
    style = xlwt.XFStyle()
    style.pattern = pattern
    # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    for worksheet_name1 in range(len(worksheets1)):
        workcontent1.append([])
        worksheet1 = workbook1.sheet_by_name(worksheets1[worksheet_name1])
        num_rows1 = worksheet1.nrows
        for curr_row in range(num_rows1):
            row1 = worksheet1.row_values(curr_row)
            workcontent1[worksheet_name1].append(row1)
    for worksheet_name2 in range(len(worksheets2)):
        workcontent2.append([])
        worksheet2 = workbook2.sheet_by_name(worksheets2[worksheet_name2])
        num_rows2 = worksheet2.nrows
        for curr_row in range(num_rows2):
            row2 = worksheet2.row_values(curr_row)
            workcontent2[worksheet_name2].append(row2)
    workbook1 = xlutils.copy.copy(workbook1)
    workbook2 = xlutils.copy.copy(workbook2)
    sheets1 = []
    sheets2 = []
    for i in range(len(workcontent1)):
        sheets1.append(workbook1.get_sheet(i))
        for j in range(len(workcontent1[i])):
            if a_in_b(workcontent1[i][j], workcontent2):
                count1 += 1
                for k in range(len(workcontent1[i][j])):
                    sheets1[i].write(j, k, workcontent1[i][j][k], style)
            else:
                for k in range(len(workcontent1[i][j])):
                    setOutCell(sheets1[i], k, j, workcontent1[i][j][k])
    for i in range(len(workcontent2)):
        sheets2.append(workbook2.get_sheet(i))
        for j in range(len(workcontent2[i])):
            if a_in_b(workcontent2[i][j], workcontent1):
                count2 += 1
                for k in range(len(workcontent2[i][j])):
                    sheets2[i].write(j, k, workcontent2[i][j][k], style)
            else:
                for k in range(len(workcontent2[i][j])):
                    setOutCell(sheets2[i], k, j, workcontent2[i][j][k])
    workbook1.save(name1)
    workbook2.save(name2)
    print(filename1 + ".xls中有%d行存在差异；" % count1)
    print(filename2 + ".xls中有%d行存在差异。" % count2)
    os.system("start " + name1)
    os.system("start " + name2)
    continue_ = str(input("还需要继续吗？[y|n]"))
    if continue_ == "n":
        break
