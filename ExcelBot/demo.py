# -*- coding: utf-8 -*-

'''
一个简单的演示用Python操作Excel表的例子
前提：已经存在一个Excel文件，名为~/Documents/simple-workbook.xls
并且有两页的sheet分别为Sheet1和Sheet2
此测试，就是想往Sheet2页面上写入一些简单数据即可

要演示的CT结果的页面存在~/Documents/ct_result.html

本机测试网页URL路径：
http://127.0.0.1:8000/index.html
http://127.0.0.1:8000/xxx_SUITE.html

'''

URL_INDEX_PAGE="http://127.0.0.1:8000/index.html"

import os.path
DEMO_EXCEL_FILE_PATH=os.path.expanduser("~/Documents/simple-workbook.xls")

import xlrd
import xlutils.copy
import os.path
import sys

'''
这里，演示基本的Excel简单读取文件，读出行，列数值，进行修改并修改保存
'''
def demo_excel_basics(file_path):
    workbook = xlrd.open_workbook(file_path)
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
def demo_ct_result_basics():
    html = get_ct_file_result()
    soup = BeautifulSoup(html)
    result_table = soup.find('table')
    for row in result_table.tbody.findAll('tr'):
        print row.findAll('td')[4]['title']  ## 目前，主报告页面的第四列正好是所有的SUITE名字列表

import urllib2
def open_page(url):
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    return html

'''
获取CT测试结果的root folder
url = http://127.0.0.1:8000/index.html
====> http://127.0.0.1:8000/
'''
import os.path
def ct_result_root_folder_from_index_url(url):
    return os.path.dirname(url)

'''
url to soup
'''
def url_to_soup(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    response.close()
    return soup

def demo_ct_html():
    print 'URL: ', URL_INDEX_PAGE
    root_path = ct_result_root_folder_from_index_url(URL_INDEX_PAGE)
    print '测试结果所在根目录：', root_path
    print '模拟SUITE路径就是', os.path.join(root_path, "xxx_SUITE.html")
    html = open_page(URL_INDEX_PAGE)
    print 'HTML:', html
    soup = url_to_soup(URL_INDEX_PAGE)
    result_table = soup.find('table')
    for row in result_table.tbody.findAll('tr'):
        print row.findAll('td')[0].find('a').get('href')
        print row.findAll('td')[0].text

def demo_ct_index_page():
    soup = url_to_soup(URL_INDEX_PAGE)
    list = parse_index_page(soup)
    print 'List: ', list

'''
分析index页面，得到SUITE与对应的Link
Suite在列表第一列，有对应的suite的名字与实际的链接地址
'''
SUITE_COLUMN_IN_RESULT_TABLE=0
def parse_index_page(soup):
    result_list = []
    test_results_table = soup.find('table')
    for row in test_results_table.tbody.findAll('tr'):
        e = row.findAll('td')[SUITE_COLUMN_IN_RESULT_TABLE]
        suite_name = str(e.text) ## unicode to str
        link = str(e.find('a').get('href'))
        result_tuple = (suite_name, link)
        result_list.append(result_tuple)
    return result_list

if __name__ == '__main__':
    demo_excel_basics(DEMO_EXCEL_FILE_PATH)
    demo_ct_result_basics()

    ## 演示基本的CT结果页面的基本操作
    demo_ct_html()
    demo_ct_index_page()
