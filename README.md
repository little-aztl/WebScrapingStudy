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

## 复杂HTML解析

通过`bs.findAll(tagName, tagAttributes)`可以获取页面中所有指定的标签，不再只是第一个。

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(), 'html.parser')

namelist = bs.findAll('span', {'class' : 'green'})
for name in namelist:
    print(name.get_text())
```

> `get_text`会清除掉你正在处理的HTML文档中的所有标签，然后返回一个只包含文字的字符串。一般情况下，你应该尽可能地保留HTML文档的标签结构，最后才使用`.get_text()`。

### `find()`与`find_all()`

`find_all(tag, attributes, recursive, text, limit, keywords)`

`find(tag, attributes, recursive, text, keywords)`

+ tag：可以传递一个标签，也可以传递一个标签列表

    `.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])`

+ attributes：传递一个Python字典

    `.find_all('span', {'class': {'green', 'red'}})`

+ recursive：bool参数，是否递归向下查询（默认为True）

+ text：用标签的文本内容去匹配

    `.find_all(text = 'the prince')`

+ limit：获取网页中的前几项。find就是limit为1的find_all

### BeautifulSoup的其他对象

+ NavigableString对象

    用来表示标签里的文字，而不是标签本身

+ Comment对象

    用来查找HTML文档的注释。

### 子标签

注意子标签和后代标签的区别

```python
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'lxml')

for child in bs.find('table', attrs={'id' : 'giftList'}).children:
    print(child)
```

子标签：`.children`

后代标签：`.descendants`

### 兄弟标签

```python
for sibling in bs.find('table', {'id':'giftList'}).tr.next_siblings:
    print(sibling)
```

`next_siblings`使得从表格中收集数据变得简单。

类似地还有`previous_siblings`

### 父标签

```python
print(bs.find('img', {'src' : '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
```

`.parent`

### 正则表达式

例子：`aa*bbbbb(cc)*(d|e)`

+ `aa*`a后面跟着的叫a星，表示重复任意次a，包括0次
+ `bbbbb`5个b
+ `(cc)*`任意偶数个c
+ `(d|e)`d或e

| 符号     | 含义                                       |
| -------- | ------------------------------------------ |
| ...*     | 任意次（可以0次）                          |
| ...+     | 任意次（至少1次）                          |
| [...]    | 匹配括号里的任意一个字符（相当于任选一个） |
| (...)    | 编组                                       |
| {m, n}   | 匹配前面的表达式m到n次（闭区间）           |
| [^...]   | 匹配不在括号中的字符                       |
| ...\|... | 或                                         |
| .        | 任意单个字符                               |
| ^...     | 从字符串开始匹配                           |
| \\...    | 转义字符（\\.、\\|、\\\\、\\/)             |
| ...$     | 从字符串末端开始匹配                       |
| ?!...    | 不包含                                     |

例子：邮箱地址

`[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)`

应用

```python
import re
images = bs.find_all('img', {'src' : re.compile('\.\.\/img.*\.jpg')})
for image in images:
    print(image['src'])
```

### 获取属性

获取全部属性：`myTag.attrs`

获取某个属性：`myTag.attrs['src']`

### Lambda表达式

BeautifulSoup允许我们将一个函数作为参数传入find_all函数，该函数将一个标签对象作为参数，返回一个bool值。BeautifulSoup把值为真的标签保留。

```python
for tag in bs.find_all(lambda tag : len(tag.attrs) == 2):
    print(tag)
```

## 编写网络爬虫

urlparse的用法

```python
from url.parse import urlparse

includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme, urlparse(includeUrl).netloc)
```

