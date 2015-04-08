# -*- coding: utf-8 -*-

'''
一个简单的演示用Python操作Excel表的例子
前提：已经存在一个Excel文件，名为~/Documents/simple-workbook.xls
并且有两页的sheet分别为Sheet1和Sheet2
此测试，就是想往Sheet2页面上写入一些简单数据即可

要演示的CT结果的页面存在~/Documents/ct_result.html
'''

__author__ = 'jia.wang'

import os.path
DEMO_EXCEL_FILE_PATH=os.path.expanduser("~/Documents/simple-workbook.xls")

import xlrd
import xlutils.copy
import os.path
import sys

'''
这里，演示基本的Excel简单读取文件，读出行，列数值，进行修改并修改保存
'''
def run_excel_demo(file_path):
    workbook = xlrd.open_workbook(file_path, formatting_info=True)
    print workbook
    print workbook.sheet_names()  ## [u'Sheet1', u'Sheet2']
    sheet = workbook.sheet_by_name("Sheet2")

    print sheet.nrows     ## 4行
    print sheet.ncols     ## 3列
    print sheet.cell_value(2, 2)

    for row in range(0, sheet.nrows):
        for col in range(0, sheet.ncols):
            sys.stdout.write(str(sheet.cell_value(row, col)) + '\t')
        print ''

    writable_workbook = xlutils.copy.copy(workbook)
    writable_sheet = writable_workbook.get_sheet(1)
    writable_sheet.write(1, 1, 55555)
    writable_sheet.write(1, 2, "Hello")
    writable_workbook.save(file_path)

def get_ct_url_result():  ## FIXME, now only use local file to simulate
    None     ## FIXME, 怎么写空函数预留个地方那个来着？

def get_ct_file_result():
    return open(os.path.expanduser("~/Documents/ct_result.html"))

from bs4 import BeautifulSoup
def run_ct_result_demo():
    html = get_ct_file_result()
    soup = BeautifulSoup(html)
    result_table = soup.find('table')
    for row in result_table.tbody.findAll('tr'):
        print row.findAll('td')[4]['title']  ## 目前，主报告页面的第四列正好是所有的SUITE名字列表

if __name__ == '__main__':
    run_excel_demo(DEMO_EXCEL_FILE_PATH)
    run_ct_result_demo()

