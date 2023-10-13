# Python网络爬虫学习笔记

## 初见网络爬虫

当你创建一个BeautifulSoup对象时，需要传入两个参数

`bs = BeautifulSoup(html.read(), 'html.parser')`

第一个参数是HTML文本，第二个参数是解析器。html.parser是Python3自带的一个解析器。

常见的解析器：

+ html.parser
+ lxml（需要单独安装）
+ html5lib（需要单独安装）

### 异常处理

```python
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print(e)
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        title = bs.body.h1
    except AttributeError as e:
        print(e)
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title:
    print(title)
```



