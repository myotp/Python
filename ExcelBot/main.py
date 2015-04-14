# -*- coding: utf-8 -*-
'''
主运行程序，主要步骤
1，根据起始的index页面地址，获取所有的Suite的链接地址

'''

URL_INDEX_PAGE="http://127.0.0.1:8000/index.html"
TEMP_EXCEL_FILE_NAME="mytc.xls"

import urllib2
from bs4 import BeautifulSoup
import xlwt

'''
url to soup
'''
def url_to_soup(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    response.close()
    return soup

'''
分析index页面，得到SUITE与对应的Link
Suite在列表第一列，有对应的suite的名字与实际的链接地址
返回结果为[(suite_name::string, link::string)]
'''
def parse_index_page(soup):
    SUITE_COLUMN_IN_RESULT_TABLE=0
    result_list = []
    test_results_table = soup.find('table')
    for row in test_results_table.tbody.findAll('tr'):
        e = row.findAll('td')[SUITE_COLUMN_IN_RESULT_TABLE]
        suite_name = normalize_suite_name(str(e.text)) ## unicode to str
        link = str(e.find('a').get('href'))
        result_tuple = (suite_name, link)
        result_list.append(result_tuple)
    return result_list

'''
sbg_ft_cba_fm.src.sbg_ft_cba_fm_SUITE => sbg_ft_cba_fm_SUITE
'''
def normalize_suite_name(suite_name_in_index_page):
    return suite_name_in_index_page.split(".")[-1]

'''
Excel表单名字限制长度在31个字符，去掉_SUITE来尽可能满足Sheet名字的要求
abc_SUITE => abc
'''
def suite_name_to_sheet_name(suite_name):
    return suite_name[0:-6]

'''
分析具体的某个Suite的结果页面
返回结果为[(num::int, test_case_name::string, result::string)]
'''
TC_NUM_COLUMN = 0
TC_CASE_COLUMN = 3
TC_RESULT_COLUMN = 6
def parse_suite_page(soup):
    result_list = []
    suite_result_table = soup.find('table')
    for row in suite_result_table.tbody.findAll('tr'):
        tc_num = str(row.findAll('td')[TC_NUM_COLUMN].text)
        if tc_num: ## 对于init_per_suite等函数的时候，这里没有seq
            tc_num = int(tc_num)
            tc_case = str(row.findAll('td')[TC_CASE_COLUMN].text)
            tc_result = str(row.findAll('td')[TC_RESULT_COLUMN].text)
            result_tuple = (tc_num, tc_case, tc_result)
            result_list.append(result_tuple)
    return result_list

EXCEL_MAX_SHEET_NAME_LENGTH = 31
EXCEL_WIDTH_OF_ZERO_CHARACTER = 256

def run_main():
    result_list = []
    ## 先根据起始的index页面，获取所有的SUITE链接
    index_soup = url_to_soup(URL_INDEX_PAGE)
    suite_link_list = parse_index_page(index_soup)
    for (suite_name, link) in suite_link_list:
        print 'Running: ', suite_name
        suite_soup = url_to_soup(link)
        test_cases_result = parse_suite_page(suite_soup)
        suite_result_tuple = (suite_name, test_cases_result)
        result_list.append(suite_result_tuple)

    ## 保存结果到一个新的Excel表里
    workbook = xlwt.Workbook()
    for (suite_name, test_cases_result) in result_list:
        sheet_name = suite_name_to_sheet_name(suite_name)
        if (len(sheet_name) > EXCEL_MAX_SHEET_NAME_LENGTH):
            print 'HELP ME!!!! Too long sheet name', sheet_name
            continue

        sheet = workbook.add_sheet(sheet_name)
        sheet.write(0, 0, "TC")
        for (tc_num, tc_name, tc_result) in test_cases_result:
            sheet.write(tc_num, 0, tc_name)
            sheet.write(tc_num, 1, tc_result)
        max_tc_length = max([len(t[1]) for t in test_cases_result])
        sheet.col(0).width = max_tc_length * EXCEL_WIDTH_OF_ZERO_CHARACTER
    workbook.save(TEMP_EXCEL_FILE_NAME)

if __name__ == '__main__':
    run_main()