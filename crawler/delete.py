from mongo import delete_item, get_client, get_item_info

db_name = "591"
list_collection_name = "item_list"
detail_collection_name = "item_detail"

client = get_client()
db = client[db_name]


def main():
    collection_list = db["item_list"]
    collection_detail = db["item_detail"]

    item_list_info = get_item_info(collection_list)
    item_detail_info = get_item_info(collection_detail)

    for item_detail in item_detail_info:
        if item_detail not in item_list_info:
            delete_item(item_detail["post_id"], db_name, detail_collection_name)
            print("item detail delete {}".format(item_detail["post_id"]))
        else:
            pass


if __name__ == '__main__':
    main()
