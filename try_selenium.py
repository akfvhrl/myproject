from selenium import webdriver
from bs4 import BeautifulSoup

import time

# 셀레니움을 실행하는데 필요한 크롬드라이버 파일을 가져옵니다.
driver = webdriver.Chrome('./chromedriver')

# 네이버 주식페이지 url을 입력합니다.
url = 'https://m.stock.naver.com/item/main.nhn#/stocks/005930/total'

# 크롬을 통해 네이버 주식페이지에 접속합니다.
driver.get(url)

# 정보를 받아오기까지 2초를 잠시 기다립니다.
time.sleep(2)

# 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공합니다.
soup = BeautifulSoup(driver.page_source, 'html.parser')

name = soup.select_one(
    '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.item_wrp > div > h2').text

current_price = soup.select_one(
    '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > strong').text

rate = soup.select_one(
    '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > div > span.gap_rate > span.rate').text

print(name, current_price, rate)

# 크롬을 종료합니다.
driver.quit()
