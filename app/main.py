import sys
import requests
from bs4 import BeautifulSoup

da_link = sys.argv[-1]
print("WE ARE READY TO GOOOOOOOO:\n{}".format(da_link))
r = requests.get(da_link)
data = r.text
body = r.content
soup = BeautifulSoup(data)
for link in soup.find_all("a"):
    print(link.get("href"))

# print(body)
