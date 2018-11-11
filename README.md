# Webscraping Instagram
Instagram only loads a small number of images to keep website loading fast. Additional images are loaded when user scrolls to the bottom of the page. 

This application uses Selenium to login into user's profile (optional -- if target profile is a friend of user) and access target profile. Application then downloads all images and their captions.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

**Prerequisities**
```
Python 3
- requests
- selenium
- beautifulsoup
- xlsxwriter
```

**Steps**
Open run_instagram_scraper.py and run Instagram(target_username, [username], [password]).

## Authors
- **Chris Chua** - _Initial work_

## Acknowledgements
- Project inspired by [Web Scraping with Python: BeautifulSoup, Requests & Selenium](https://www.udemy.com/web-scraping-with-python-beautifulsoup/) on Udemy.