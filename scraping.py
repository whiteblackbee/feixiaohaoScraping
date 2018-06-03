# -*- coding: UTF-8 -*-
import requests
import os
from bs4 import BeautifulSoup


# url 请求网页数据
def getHtmlText(url, code):
    print('open:', url)
    try:
        r = requests.get(url)
        r.encoding = code
        r.raise_for_status()
        return r.text
    except Exception:
        return ''


# 解析网页，返回所需数据
def getSymbols(symbols, url):
    html = getHtmlText(url, 'utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.findAll('tbody')
    tab = tables[0]
    trs = tab.findAll('tr')
    for tr in trs:
        symbols.append(tr.attrs['id'])


def storeDetails(dir, urlBase, tokenSymbol):
    detail = ''
    html = getHtmlText(urlBase + 'coindetails/' + tokenSymbol, 'utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    baseInfoList = soup.find("ul", class_="baseInfoList")
    spens = baseInfoList.findAll('span')

    artBox = soup.find("div", class_="artBox")

    for p in artBox.findAll('p'):
        detail += p.get_text().strip()  # 简介, 需要拼接所有的 p text
    try:
        # 模式记得要加上 b，使文件以 2 进制模式打开，
        # 否则会报错 TypeError: write() argument must be str, not bytes
        with open(dir + '/' + tokenSymbol + '_detail.txt', 'w') as f:
            f.writelines([
                spens[0].get_text() + spens[1].get_text() + '\n',  # 英文名
                spens[2].get_text() + spens[3].get_text() + '\n',  # 中文名
                spens[8].get_text() + spens[9].get_text() + '\n',  # 白皮书
                '简介：' + detail + '\n'  # 简介
            ])
            f.close()
            print(tokenSymbol + '详情保存成功')
    except Exception:
        print(tokenSymbol + '详情保存失败')


def storeImage(dir, tokenSymbol, imagesUrl):
    path = dir + tokenSymbol + '.png'
    try:
        r = requests.get('http:' + imagesUrl)
        r.encoding = 'utf-8'
        # 模式记得要加上 b，使文件以 2 进制模式打开,
        # 否则会报错 TypeError: write() argument must be str, not bytes
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print(tokenSymbol + '图片保存成功')
    except Exception:
        print(tokenSymbol + '图片保存失败')


def storeData(dir, urlBase, tokenSymbol):
    html = getHtmlText(urlBase + 'currencies/' + tokenSymbol, 'utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    storeImage(dir, tokenSymbol, soup.find('h1').img.attrs['src'])
    storeDetails(dir, urlBase, tokenSymbol)


def getToknInfo(dir, url, symbol):
    path = dir + symbol + '/'
    if not os.path.exists(path):
        os.mkdir(path)  # 文件夹不存在则创建一个文件夹
    storeData(path, url, symbol)


def main():
    url = '''https://www.feixiaohao.com/'''
    newUrl = url
    symbols = []
    root = './coininfo/'
    if not os.path.exists(root):
        os.mkdir(root)  # 文件夹不存在则创建一个文件夹

    for index in range(21):
        if index != 0:
            newUrl = 'https://www.feixiaohao.com/' + 'list_' + str(index +
                                                                   1) + '.html'
        symbols = []
        getSymbols(symbols, newUrl)
        for symbol in symbols:
            getToknInfo(root, url, symbol)
    print(len(symbols))


if __name__ == '__main__':
    main()