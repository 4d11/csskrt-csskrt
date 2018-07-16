from bs4 import BeautifulSoup, Tag, NavigableString
import os

file_path = 'test/test1.html'

f = open(file_path)
f_data = f.read()

soup = BeautifulSoup(f_data, 'html.parser')

def add_class_to_element(elem, css_class):
    if not elem.get('class'):
        elem['class'] = css_class
    else:
        try:
            elem['class'].append(css_class)
        except AttributeError:
            elem['class'] += ' ' + css_class



class SooFresh():
    def __init__(self, html, framework):
        self.html = html
        self.framework = framework


def get_bulma_starter():
    # hack since 'name' is reserved
    meta = Tag(builder=soup.builder,
               name='meta',
               attrs={'name': "viewport", 'content': 'width=device-width, initial-scale=1'})

    stylesheet = soup.new_tag(
        'link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
    )
    return meta, stylesheet


def initialize_framework(head: Tag):
    meta, stylesheet = get_bulma_starter()

    head.append(meta)
    head.append(stylesheet)


def apply_tag_styles(tag_dict: dict, soup):
    for tag, css_class in tag_dict.items():
        for elem in soup.find_all(tag):
            add_class_to_element(elem, css_class)


def add_form_classes(soup, tag_dict: dict):
    for form in soup.find_all('form'):
        form_contents = form.contents
        spotted_label = None
        for elem in form.children:
            if elem.name == 'label':
                spotted_label = elem
                add_class_to_element(elem, 'label')
            elif elem.name == 'input':
                add_class_to_element(elem, 'input')

                if elem.get('type') == 'radio':
                    if 'radio' in tag_dict:
                        add_class_to_element(elem, tag_dict['radio'])
                elif elem.get('type') == 'checkbox':
                    if 'checkbox' in tag_dict:
                        add_class_to_element(elem, tag_dict['checkbox'])

                # Add overall wrapper
                if not spotted_label:
                    # add wrapper
                    field_div = soup.new_tag('div', **{'class': 'field'})
                    elem.wrap(field_div)
                else:
                    # the input has a preceding label
                    field_div = soup.new_tag('div', **{'class': 'field'})
                    spotted_label.wrap(field_div)
                    field_div.append(elem)
                    spotted_label = None

                 # Add input wrapper
                control_div = soup.new_tag('div', **{'class': 'control'})
                elem.wrap(control_div)
            elif type(elem) == Tag: # ignore  NavigableStrings like /n
                spotted_label = None
                if (tag_dict.get(elem.name)):
                    add_class_to_element(elem, tag_dict[elem.name])

def output_soup(soup, file_path):
    folder = os.path.dirname(file_path)
    file = os.path.basename(file_path)
    file_name, ext = os.path.splitext(file)

    new_file_name = os.path.join(folder, file_name + '-fresh' + ext)
    with open(new_file_name, 'w') as out_file:
        out_file.write(soup.prettify())



def freshify(soup):
    initialize_framework(soup.head)
    # apply_tag_styles(tag_styles, soup)
    add_form_classes(soup, tag_styles)
    output_soup(soup, file_path)




tag_styles = {
    'input': 'input',
    'label': 'label',
    'textarea': 'textarea',
    'select': 'select',
    'button': 'button',
    'checkbox': 'checkbox',
    'radio': 'radio',
}

freshify(soup)



# print(btn.get('class', []))


# soup = BeautifulSoup("<b></b>")
# original_tag = soup.b
#
# new_tag = soup.new_tag("a", href="http://www.example.com")
# original_tag.append(new_tag)
