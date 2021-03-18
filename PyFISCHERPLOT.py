# -*- coding:utf-8 -*-

'''
Name of Code: PyFISCHERPLOT. Developer: Zongyang Chen, Daming Yang. E-mail: damingyang@sohu.com. Software Require: Python 3.0 language pack, Python library Xlrd, Python library Xlsxwriter.Program Language: Python 3.0. Program Size: 4.48 KB. Purpose: constructing Fischer plots using geological data.
'''

import xlrd
import xlsxwriter
import os


class WorkBook(object):

    def get_data(self, path):
        data_1 = []
        orign_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], path)
        book = xlrd.open_workbook(orign_path)
        Data_sheet = book.sheets()[0]
        cols_0 = Data_sheet.col_values(0)
        del cols_0[0]
        cols_1 = Data_sheet.col_values(1)
        del cols_1[0]
        return cols_0, cols_1

    def process_data(self, *data):
        cols_0 = data[0][0]
        del cols_0[0]
        del cols_0[0]
        cols_1 = data[0][1]
        cols_2 = [1 if cols_1[i + 1] > cols_1[i]
                  else 0 for i in range(0, len(cols_1) - 1)]
        cols_3 = [cols_2[i + 1] - cols_2[i] for i in range(0, len(cols_2) - 1)]
        cols_4 = [round(cols_0[i], 20)
                  for i in range(0, len(cols_3)) if cols_3[i] == 1]
        cols_5 = [round(cols_4[i + 1] - cols_4[i], 20)
                  for i in range(0, len(cols_4) - 1)]
        cols_5.reverse()
        deep_ave = round(sum(cols_5) / len(cols_5), 20)
        cols_6 = [round(cols_5[i] - deep_ave, 20)
                  for i in range(0, len(cols_5))]
        cols_7 = []
        for i in range(0, len(cols_6)):
            if i == 0:
                cols_7.append(cols_6[0])
            else:
                a = round(cols_7[i - 1] + cols_6[i], 20)
                cols_7.append(a)
        cols_7.reverse()
        del cols_4[0]
        cols_8 = [i for i in range(1, len(cols_7) + 1)]
        return cols_4, cols_7, cols_8

    def write_draw_charts(self, path, *data):
        path_new = os.path.join(os.path.split(os.path.realpath(__file__))[
                        0], "processed_" + path)
        cols_4 = data[0][0]
        cols_7 = data[0][1]
        cols_8 = data[0][2]
        workbook_new = xlsxwriter.Workbook(path_new)
        worksheet = workbook_new.add_worksheet()
        bold = workbook_new.add_format({'bold': 1})
        headings_1 = ["Depth", "CDMT"]
        data_all = [cols_4, cols_7, cols_8]
        # 写入表头
        worksheet.write_row("A1", headings_1, bold)
        # 写入数据
        worksheet.write_column("A2", data_all[0])
        worksheet.write_column("B2", data_all[1])
        headings_2 = ["Cycle Number", "CDMT"]
        # 写入表头
        worksheet.write_row("C1", headings_2, bold)
        # 写入数据
        worksheet.write_column("C2", data_all[2])
        worksheet.write_column("D2", data_all[1])

        chart_col = workbook_new.add_chart({"type": "line"})
        chart_col.add_series({
            'name': '=Sheet1!$B$1',
            'categories': '=Sheet1!$A$2:$A${}'.format(len(cols_7) + 1),
            'values':   '=Sheet1!$B$2:$B${}'.format(len(cols_7) + 1),
            'line': {'color': 'red'},
        })
        chart_col.set_title({"name": "Fischer Plot"})
        chart_col.set_x_axis({'name': 'Depth(m)'})
        chart_col.set_y_axis({'name': 'CDMT'})
        chart_col.set_style(1)

        worksheet.insert_chart(
            'E3', chart_col, {'x_offset': 0, 'y_offset': 0})

        chart_col = workbook_new.add_chart({"type": "line"})
        chart_col.add_series({
            'name': '=Sheet1!$B$1',
            'categories': '=Sheet1!$C$2:$C${}'.format(len(cols_7) + 1),
            'values':   '=Sheet1!$D$2:$D${}'.format(len(cols_7) + 1),
            'line': {'color': 'red'},
        })
        chart_col.set_title({"name": "Fischer Plot"})
        chart_col.set_x_axis({'name': 'Cycle Number'})
        chart_col.set_y_axis({'name': 'CDMT'})
        chart_col.set_style(1)

        worksheet.insert_chart(
            'E20', chart_col, {'x_offset': 0, 'y_offset': 0})
        workbook_new.close()
        print("**********", path_new, "--Done--", "**************")
        return None


if __name__ == '__main__':
    workbook = WorkBook()
    subDirNameList = os.path.split(os.path.realpath(__file__))[0]
    file_paths = os.listdir(subDirNameList)
    for i in file_paths:
        if ".xls" in i:
            try:
                get_data = workbook.get_data(i)
                process_data = workbook.process_data(get_data)
                write_draw_chart = workbook.write_draw_charts(i, process_data)
            except Exception as e:
                print('!!!!!', i, "--The catched exception is {}--".format(e), '!!!!')
