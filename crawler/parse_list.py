import time

import requests
from bs4 import BeautifulSoup

from mongo import insert_item, get_client, get_item_info, update_item

city_url = {
    "taipei": "https://rent.591.com.tw/?kind=0&region=1&",
    "new_taipei": "https://rent.591.com.tw/?kind=0&region=3"
}

city_api = {
    "taipei": "https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1&kind=0&region=1",
    "new_taipei": "https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1&kind=0&region=3"
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
}

db_name = "591"
list_collection_name = "item_list"
detail_collection_name = "item_detail"

client = get_client()
db = client[db_name]


def get_total_num(page_info):
    soup = BeautifulSoup(page_info, "lxml")
    total_num = soup.select_one("span.R").text.strip()
    return total_num


def get_item(json_data):
    item = {}
    item["post_id"] = json_data["post_id"]
    item["price"] = int(json_data["price"].replace(",", ""))
    return item


def get_item_list(city, h):
    rs = requests.session()
    resp = rs.get(city_url[city], headers=h)
    soup = BeautifulSoup(resp.text, "lxml")

    token = soup.select_one('meta[name="csrf-token"]')["content"]
    h["X-CSRF-TOKEN"] = token
    h["X-Requested-With"] = "XMLHttpRequest"

    res = rs.get(city_api[city], headers=h)
    jd = res.json()
    return jd


def main(city):
    collection_list = db[detail_collection_name]
    jd = get_item_list(city, headers)
    page_info = jd["data"]["page"]
    total_num = get_total_num(page_info)

    rs = requests.session()
    resp = rs.get(city_url[city], headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    token = soup.select_one('meta[name="csrf-token"]')["content"]
    headers["X-CSRF-TOKEN"] = token
    headers["X-Requested-With"] = "XMLHttpRequest"

    apiurl = city_api[city]

    item_info = get_item_info(collection_list)

    for row_num in range(0, int(total_num), 30):
        print(row_num, total_num)
        params = "&firstRow={}&totalRows={}".format(row_num, total_num)
        url_api = apiurl + params
        response = rs.get(url_api, headers=headers)
        json_data_list = response.json()["data"]["data"]
        for json_data in json_data_list:
            item = get_item(json_data)
            if item["post_id"] in item_info:
                update_item(item, db_name, list_collection_name)
                print("list update {}".format(item["post_id"]))
            else:
                insert_item(item, db_name, list_collection_name)
                print("list insert {}".format(item["post_id"]))
        time.sleep(1)


if __name__ == '__main__':
    main("taipei")
