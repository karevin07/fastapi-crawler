import time

import requests
from bs4 import BeautifulSoup

from mongo import insert_item, delete_item, get_client, get_item_info

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
}

db_name = "591"
list_collection_name = "item_list"
detail_collection_name = "item_detail"

client = get_client()
db = client[db_name]


def get_house_detail(house_id, h):
    s = requests.Session()
    url = f'https://rent.591.com.tw/home/{house_id}'
    resp = s.get(url, headers=h)
    soup = BeautifulSoup(resp.text, "lxml")
    title = soup.select_one("title").text
    if title == "591房屋交易網--對不起，您訪問的頁面不存在":
        return "delete"
    else:
        item_token = soup.select_one('meta[name="csrf-token"]')["content"]
        headers = h
        headers["X-CSRF-TOKEN"] = item_token
        headers["deviceid"] = s.cookies.get_dict()["T591_TOKEN"]
        headers["device"] = "pc"

        url = f'https://bff.591.com.tw/v1/house/rent/detail?id={house_id}'
        r = s.get(url, headers=headers)
        house_detail = r.json()['data']
        return house_detail


def parse_detail(post_id, json_data):
    item_detail = {}
    item_detail["post_id"] = post_id
    item_detail["title"] = json_data["title"]
    for breadcrumb in json_data["breadcrumb"]:
        item_detail[breadcrumb["query"]] = breadcrumb["name"]
    for info in json_data["info"]:
        item_detail[info["key"]] = info["value"]
    item_detail["address"] = json_data["positionRound"]["address"]
    item_detail["role_name"] = json_data["linkInfo"]["roleName"]
    item_detail["role"] = json_data["linkInfo"]["role"]
    item_detail["name"] = json_data["linkInfo"]["name"].replace(item_detail["role_name"], "").replace(": ", "").strip()
    item_detail["mobile"] = json_data["linkInfo"]["mobile"].replace("-", "")
    item_detail["price"] = int(json_data["price"].replace(",", ""))
    if item_detail["name"].endswith("先生"):
        item_detail["owner"] = "1"
    elif item_detail["name"].endswith("小姐"):
        item_detail["owner"] = "2"
    else:
        item_detail["owner"] = "0"

    try:
        house_rule = json_data["service"]["rule"]
    except:
        house_rule = ""
    if "此房屋男女皆可租住" in house_rule:  ##0: other, 1: male ,2: female, 3: male and female
        item_detail["allow_gender"] = 3
    elif "此房屋限女生租住" in house_rule:
        item_detail["allow_gender"] = 2
    elif "此房屋限男生租住" in house_rule:
        item_detail["allow_gender"] = 1
    else:
        item_detail["allow_gender"] = 0
    return item_detail


def need_update(item, item_old):
    if item["post_id"] not in item_old:
        return True
    else:
        if item["price"] != item_old[item["post_id"]]:
            return True
    return False


def main():
    collection_list = db[list_collection_name]
    collection_detail = db[detail_collection_name]

    item_info = get_item_info(collection_detail)

    item_list = collection_list.find()
    for item in item_list:
        if need_update(item, item_info):
            jd = get_house_detail(item["post_id"], headers)
            if jd == "delete":
                print("item list delete {}".format(item["post_id"]))
                delete_item(item["post_id"], db_name, list_collection_name)
                continue
            item_detail = parse_detail(item["post_id"], jd)
            insert_item(item_detail, db_name, detail_collection_name)
            print("item detail insert {}".format(item["post_id"]))
            time.sleep(0.1)
        else:
            print("already exist {}".format(item["post_id"]))


if __name__ == '__main__':
    main()
