from bs4 import BeautifulSoup, Tag
import os

file_path = 'test/test1.html'

f = open(file_path)
f_data = f.read()

soup = BeautifulSoup(f_data, 'html.parser')


class SooFresh():
    def __init__(self, html, framework):
        self.html = html
        self.framework = framework




def get_bulma_starter():
    # hack since name is reserved
    meta = Tag(builder=soup.builder,
        name='meta',
        attrs={'name':"viewport", 'content': 'width=device-width, initial-scale=1'})

    stylesheet = soup.new_tag(
        'link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
    )
    return meta, stylesheet


def initialize_framework(head: Tag):
    meta, stylesheet = get_bulma_starter()

    head.append(meta)
    head.append(stylesheet)



initialize_framework(soup.head)


for btn in soup.find_all('button'):
    print(btn.get('class'))

# meta, stylesheet = get_bulma_starter()

# soup.head.append(meta)
# soup.head.append(stylesheet)

# print(soup.head)







def import_framework(name):
    if (name == 'bulma'):
        meta, stylesheet = get_bulma_starter()



folder = os.path.dirname(file_path)
file = os.path.basename(file_path)
file_name, ext = os.path.splitext(file)

new_file_name = os.path.join(folder, file_name+'-fresh'+ext)
with open(new_file_name, 'w') as out_file:
    out_file.write(soup.prettify())



# print(btn.get('class', []))


# soup = BeautifulSoup("<b></b>")
# original_tag = soup.b
#
# new_tag = soup.new_tag("a", href="http://www.example.com")
# original_tag.append(new_tag)
