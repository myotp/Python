# -*- coding: utf-8 -*-
'''
主运行程序，主要步骤
1，根据起始的index页面地址，获取所有的Suite的链接地址

'''

URL_INDEX_PAGE="http://127.0.0.1:8000/index.html"

import urllib2
from bs4 import BeautifulSoup

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
'''
def parse_index_page(soup):
    SUITE_COLUMN_IN_RESULT_TABLE=0
    result_list = []
    test_results_table = soup.find('table')
    for row in test_results_table.tbody.findAll('tr'):
        e = row.findAll('td')[SUITE_COLUMN_IN_RESULT_TABLE]
        suite_name = str(e.text) ## unicode to str
        link = str(e.find('a').get('href'))
        result_tuple = (suite_name, link)
        result_list.append(result_tuple)
    return result_list

def run_main():
    ## 先根据起始的index页面，获取所有的SUITE链接
    index_soup = url_to_soup(URL_INDEX_PAGE)
    suites_link_list = parse_index_page(index_soup)
    print suites_link_list

if __name__ == '__main__':
    run_main()