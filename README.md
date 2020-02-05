# ACM-IEEE-arXiv Info Spider

The project is part of my graduation design which aims to crawl structured information of papers in ACM, IEEE and arXiv digital library.

**Keywords**: Python, Scrapy, MySQL, Papers

# Dependency

- Python 3.6
- MySQL 8.0.17
- scrapy
- logging
- re
- pymysql
- twisted
- json
- fake_useragent

## The Data Structure of Database
- MYSQL_DBNAME = 'papers'
- TABLE_NAME = {'ACM_Data', 'IEEE_Data', 'arXiv_Data'}



attribute | data_type | length | not NULL 
---|---|---|---
p_id | int | 0 | :white_check_mark:(key) | 
title | varchar | 255
authors | varchar | 255
year | varchar | 255
type | varchar | 255
subjects | varchar | 255
url | varchar | 255
abstract | varchar | 255
citation | int | 0


# Features
1. A Script runs automatically to get free proxies (HTTP only) and will be integrated to scrapy-based main program soon.
2. For every request, it will generate a random proxy and user-agent.
3. TXT file, raw json (not exact json) and MySQL are provided to store data.
4. Level-based optional log is given.  
5. Asynchronous mode is used as data storage mechanism for MySQL pipeline, thus the program is more efficient and reliable when encounts data flood from spider.

# Install & Run

In terminal

```
scrapy crawl ACM_Spider
```
```
scrapy crawl IEEE_Spider
```
...

# Developing in Process

- IEEE Spider (The HTML is JS-dynamic.)
- arXix (easy)
- Proxy downloader integration
- MongoDB Storage
- Robuster Xpath rules
- UUID for database

# Some pics
![](https://github.com/xyjigsaw/ACM-IEEE-arXiv-Spider/blob/master/MySQL-Spider.png)