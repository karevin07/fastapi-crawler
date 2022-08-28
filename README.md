# fastapi-crawler

`fastapi-crawler` is a Python fastapi application and web crawler server

- [crawler](./crawler)
    - A web crawler, scraping data from [591](https://rent.591.com.tw/)
- [fastapi](./app)
    - A RESTful api use to query house data from `MongoDB`

## Installation

- copy .env file

```bash
cp example_env .env
```

- getting started with docker-compose

```bash
docker-compose up -d
```

## Usage

- crawler

```bash
## get taipei/new_taipei house data to mongodb from 591
docker-compose exec crawler python crawler/driver.py {taipei/new_taipei}
```

[fastapi](http://0.0.0.0:8000/docs#)

![](https://i.imgur.com/eoeJZwG.png)


## Reference

[A perfect way to Dockerize your Pipenv Python application](https://sourcery.ai/blog/python-docker/)

[Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)

[house591_spider](https://blog.jiatool.com/posts/house591_spider/)

## License
[MIT](https://choosealicense.com/licenses/mit/)