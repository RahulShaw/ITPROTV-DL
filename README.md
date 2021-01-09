# Download videos from ITPROTV / ITPROTV-DL

###### Python script to download videos from your ITPROTV account for offline viewing

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)

![ITPROTV-DL](https://i.imgur.com/iW2ilOD.png)

### Requirements
- Python 3.6 and above
- BeautifulSoup - https://pypi.org/project/beautifulsoup4/
- requests - https://pypi.org/project/requests/
- html5lib - https://pypi.org/project/html5lib/
- Selenium - https://pypi.org/project/selenium/
- tqdm - https://pypi.org/project/tqdm/
- ChromeDriver - http://chromedriver.chromium.org/
- Get cookies.txt - https://bit.ly/GoogleChrome-GetCookiesTxt
- Active subscription on itpro.tv

### Usage

> Clone the repo

> Run `pip install -r requirements.txt`

> Login to itpro.tv and visit the course page e.g. https://app.itpro.tv/course/mta-security-fundamentals-98367-2018/ and with the `Get cookies.txt` extension installed, click on the icon of the extension and click on `Export`. 

![Get cookies.txt](https://i.imgur.com/6QkV9RC.png)

> Rename the downloaded `itpro.tv_cookies.txt` file to `cookies.txt` and copy it to root of the cloned repo. Make sure that the name of the file is ``cookies.txt``. Repeat when you encounter an exception while downloading the videos (assuming you have an active subscription).

> course_link e.g. https://app.itpro.tv/course/mta-security-fundamentals-98367-2018/

``` python
>>> python driver.py course_link
```

I'd be gratified to have your support - 

[<img src="https://i.imgur.com/ngduQd7.png">](https://www.buymeacoffee.com/RahulShaw)
 