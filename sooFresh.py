from bs4 import BeautifulSoup


f = open("test/test1.html")
f_data = f.read()

soup = BeautifulSoup(f_data, 'html.parser')

print(soup.prettify())


for link in soup.find_all('a'):
    print(link.get('hretof'))