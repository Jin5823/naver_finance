import time
import pandas
import requests
from bs4 import BeautifulSoup


def naver_sise_time_url(item_code):
    """
    :param item_code: string 형태의 종목 코드를 입력하면 자동으로 6자리까지 0을 채움
    :return: 네이버 당일 시간별 시세 url
    """
    item_code = item_code.zfill(6)
    naver_url = 'https://finance.naver.com/item/sise_time.nhn?code='+item_code
    return naver_url


def naver_sise_day_url(item_code):
    """
    :param item_code: string 형태의 종목 코드를 입력하면 자동으로 6자리까지 0을 채움
    :return: 네이버 일별 시세 url
    """
    item_code = item_code.zfill(6)
    naver_url = 'http://finance.naver.com/item/sise_day.nhn?code='+item_code
    return naver_url


def naver_board_url(item_code):
    """
    :param item_code: string 형태의 종목 코드를 입력하면 자동으로 6자리까지 0을 채움
    :return: 네이버 종목토론실 url
    """
    item_code = item_code.zfill(6)
    naver_url = 'http://finance.naver.com/item/board.nhn?code='+item_code
    return naver_url


def get_naver_sise_time(url, date):
    """
    :param url: naver_sise_time_url 으로 생성한 네이버 url
    :param date: datetime 라이브러리로 생성한 변수 (예 datetime.datetime(2020, 3, 10))
    :return: 지정한 날짜의 시간별 시세 정보
    """
    page = 0
    is_item = ''
    date = str(date.date()).replace('-', '')
    while_loop = True
    naver_item = pandas.DataFrame()
    req_head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    while while_loop:
        time.sleep(0.1)
        page += 1
        pg_url = url + '&thistime=%s190000&page=%d' % (date, page)
        temp = pandas.read_html(requests.get(pg_url, headers=req_head).text, header=0)[0]
        naver_item = naver_item.append(temp, ignore_index=True)

        for last_item in naver_item.dropna().tail(1)['체결시각']:
            if is_item == last_item:
                while_loop = False
            is_item = last_item

        if not is_item:
            while_loop = False

    naver_item = naver_item.dropna().reset_index(drop=True)
    return naver_item


def get_naver_sise_day(url, last_date):
    """
    :param url: naver_sise_day_url 으로 생성한 네이버 url
    :param last_date: datetime 라이브러리로 생성한 변수 (예 datetime.datetime(2020, 3, 10))
    :return: 지정한 날짜까지의 시세 정보
    """
    page = 0
    is_item = ''
    last_date = str(last_date.date()).replace('-', '.')
    while_loop = True
    naver_item = pandas.DataFrame()
    req_head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    while while_loop:
        time.sleep(0.1)
        page += 1
        pg_url = url + '&page=%d' % page
        temp = pandas.read_html(requests.get(pg_url, headers=req_head).text, header=0)[0]
        naver_item = naver_item.append(temp, ignore_index=True)

        for last_item in naver_item.dropna().tail(1)['날짜']:
            if is_item == last_item:
                while_loop = False
            is_item = last_item
            if last_item < last_date:
                while_loop = False

        if not is_item:
            while_loop = False

    naver_item = naver_item.dropna().reset_index(drop=True)
    naver_item = naver_item.drop(naver_item[naver_item['날짜'] < last_date].index)
    return naver_item


def get_naver_board(url, last_date):
    """
    :param url: naver_board_url 으로 생성한 네이버 url
    :param last_date: datetime 라이브러리로 생성한 변수 (예 datetime.datetime(2020, 3, 10))
    :return: 지정한 날짜까지의 종목토론실 정보
    """
    page = 0
    is_item = ''
    last_date = str(last_date.date()).replace('-', '.')
    while_loop = True
    naver_item = pandas.DataFrame()
    req_head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    while while_loop:
        time.sleep(0.1)
        page += 1
        pg_url = url + '&page=%d' % page

        temp = pandas.read_html(requests.get(pg_url, headers=req_head).text, header=0)[1]
        del temp[temp.columns[-1]]
        naver_item = naver_item.append(temp, ignore_index=True)

        for last_item in naver_item.dropna().tail(1)['날짜']:
            if is_item == last_item:
                while_loop = False
            is_item = last_item
            if last_item.split(' ')[0] < last_date:
                while_loop = False

        if not is_item:
            while_loop = False

    naver_item = naver_item.dropna().reset_index(drop=True)
    naver_item['날짜'] = naver_item['날짜'].apply(lambda x: x.split(' ')[0])
    naver_item = naver_item.drop(naver_item[naver_item['날짜'] < last_date].index)
    return naver_item


def get_naver_sise_high_down(market=0):
    """
    :param market: 코스피 0, 코스닥 1
    :return: 급락 종목 정보
    """
    naver_item = pandas.DataFrame()
    req_head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    pg_url = "https://finance.naver.com/sise/sise_high_down.nhn" + '?sosok=%d' % market
    req_page = requests.get(pg_url, headers=req_head).text

    temp = pandas.read_html(req_page, header=0)[1]
    temp.drop(['N', 'PER', 'ROE'], axis='columns', inplace=True)
    naver_item = naver_item.append(temp, ignore_index=True)
    naver_item = naver_item.dropna().reset_index(drop=True)

    soup = BeautifulSoup(req_page, 'html.parser')
    table = soup.findAll('table')[1]
    codes = []
    for each in table.findAll("a"):
        link = each['href']
        codes.append(link.split("=")[-1])

    if len(codes) != len(naver_item):
        print("err")

    naver_item.insert(2, '종목코드', codes)
    return naver_item
