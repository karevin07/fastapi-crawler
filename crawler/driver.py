import sys
import time

import parse_list, parse_detail, delete

city = sys.argv[1]


def main(city_name):
    start_time = time.time()
    parse_list.main(city_name)
    parse_detail.main()
    delete.main()
    print("--- cost {} seconds ---".format(time.time() - start_time))


if __name__ == '__main__':
    main(city)
