import schedule
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time


def get_my_stock():
    client = MongoClient("localhost", 27017)
    db = client.dbsparta
    x = db.stocks
    codes = []
    for a in x.find({}, {"_id": 0, "code": 1}):
        codes.append(a["code"])

    ### option 적용 ###
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )

    driver = webdriver.Chrome("chromedriver", options=options)
    ##################
    update = []
    for code in codes:
        # 네이버 주식페이지 url을 입력합니다.
        url = "https://m.stock.naver.com/item/main.nhn#/stocks/" + code + "/total"

        # 크롬을 통해 네이버 주식페이지에 접속합니다.
        driver.get(url)

        # 정보를 받아오기까지 2초를 잠시 기다립니다.
        time.sleep(2)

        # 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공합니다.
        soup = BeautifulSoup(driver.page_source, "html.parser")

        current_price = soup.select_one(
            "#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > strong"
        ).text

        variance = soup.select_one(
            "#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > div > span.gap_price > span.price"
        ).text

        rate = soup.select_one(
            "#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > div > span.gap_rate > span.rate"
        ).text
        update.append([code, current_price, variance, rate])
    print("-------")
    # 크롬을 종료합니다.
    driver.quit()
    # db에 값들을 업데이트해줍니다.
    for i in range(20):
        x.update_one({"code": update[i][0]}, {"$set": {"share": update[i][1]}})
        x.update_one({"code": update[i][0]}, {"$set": {"variance": update[i][2]}})
        x.update_one({"code": update[i][0]}, {"$set": {"variance_rate": update[i][3]}})


def job():
    get_my_stock()


def run():
    schedule.every(60).seconds.do(job)  # 60초에 한번씩 실행
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    run()
