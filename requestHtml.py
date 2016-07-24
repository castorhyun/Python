#coding: utf-8

import urllib.request
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("Hello World")
    req = urllib.request.Request("http://www.clien.net/cs2/bbs/board.php?bo_table=park");
    data = urllib.request.urlopen(req).read()

    print(data)

    f = open("./response_clien.html", "wb")
    f.write(data)
    f.close()
