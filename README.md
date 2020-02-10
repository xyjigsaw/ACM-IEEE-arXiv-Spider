# ACM-IEEE-arXiv Info Spider

![](https://github.com/xyjigsaw/ACM-IEEE-arXiv-Spider/blob/master/acemap.ico)
[Acemap](https://www.Acemap.info)

The project is part of my graduation design which aims to crawl structured information of papers from digital library.

### Supported Libraries
- ACM (Done)
- IEEE (Developing)
- arXiv (Done)
- AAAI (Done)

**Keywords**: Python, Scrapy, MySQL, Papers

# Dependencies and Requirements

- Python 3.6
- MySQL 8.0.17
- scrapy
- scrapy_proxies
- logging
- re
- pymysql
- twisted
- json
- fake_useragent

## Data Structure of Database
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
or
```
scrapy crawl IEEE_Spider
```
etc.

# Developing in Process

- IEEE Spider (The HTML is JS-dynamic.)
- arXix (easy)
- Proxy Downloader Integration
- MongoDB Storage
- Robuster Xpath Rules
- UUID for Database

# Some pics
![](https://github.com/xyjigsaw/ACM-IEEE-arXiv-Spider/blob/master/MySQL-Spider.png)