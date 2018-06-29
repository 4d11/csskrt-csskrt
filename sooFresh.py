from bs4 import BeautifulSoup, Tag

bulmaCDN = "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css"

f = open("test/test1.html")
f_data = f.read()

soup = BeautifulSoup(f_data, 'html.parser')

def get_bulma_starter():
    # hack since name is reserved
    meta = Tag(builder=soup.builder,
        name='meta',
        attrs={'name':"viewport", 'content': 'width=device-width, initial-scale=1'})

    stylesheet = soup.new_tag(
        'link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
    )
    return meta, stylesheet


for btn in soup.find_all('button'):
    print(btn.get('class'))

meta, stylesheet = get_bulma_starter()

soup.head.append(meta)
soup.head.append(stylesheet)

print(soup.head)







def import_framework(name):
    if (name == 'bulma'):
        meta, stylesheet = get_bulma_starter()




# print(btn.get('class', []))


# soup = BeautifulSoup("<b></b>")
# original_tag = soup.b
#
# new_tag = soup.new_tag("a", href="http://www.example.com")
# original_tag.append(new_tag)
