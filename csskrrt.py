from bs4 import BeautifulSoup, Tag, NavigableString
import os
from abc import ABC, abstractmethod
from typing import List

file_path = 'test/test1.html'

f = open(file_path)
f_data = f.read()

class Csskrrt():
    def __init__(self, html, tag_styles):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.tag_styles = tag_styles

    @abstractmethod
    def get_starter_tags(self) -> List[Tag]:
        pass

    def add_class_to_element(self, elem, css_class):
        if not elem.get('class'):
            elem['class'] = css_class
        else:
            try:
                elem['class'].append(css_class)
            except AttributeError:
                elem['class'] += ' ' + css_class

    def initialize_framework(self, head: Tag, tags: List[Tag]):
        for tag in tags:
            head.append(tag)

    def add_form_classes(self, tag_dict: dict):
        for form in self.soup.find_all('form'):
            for elem in form.children:
                if elem.name == 'label':
                    self.add_class_to_element(elem, tag_dict['label'])

                elif elem.name == 'input':
                    self.add_class_to_element(elem, tag_dict['input'])

                    if elem.get('type') == 'radio':
                        if 'radio' in tag_dict:
                            self.add_class_to_element(elem, tag_dict['radio'])
                    elif elem.get('type') == 'checkbox':
                        if 'checkbox' in tag_dict:
                            self.add_class_to_element(elem, tag_dict['checkbox'])

                elif type(elem) == Tag: # ignore  NavigableStrings like /n
                    if (tag_dict.get(elem.name)):
                        self.add_class_to_element(elem, tag_dict[elem.name])

    def output(self, file_path):
        folder = os.path.dirname(file_path)
        file = os.path.basename(file_path)
        file_name, ext = os.path.splitext(file)

        new_file_name = os.path.join(folder, file_name + '-fresh' + ext)
        with open(new_file_name, 'w') as out_file:
            out_file.write(self.soup.prettify())

    def freshify(self):
        starter_tags = self.get_starter_tags()
        self.initialize_framework(self.soup.head, starter_tags)
        self.add_form_classes(self.tag_styles)
        self.output(file_path)


"""
 folder = os.path.dirname(file_path)
        file = os.path.basename(file_path)
        file_name, ext = os.path.splitext(file)

        new_file_name = os.path.join(folder, file_name + '-fresh' + ext)
        with open(new_file_name, 'w') as out_file:
            out_file.write(self.soup.prettify())

"""



# print(btn.get('class', []))


# soup = BeautifulSoup("<b></b>")
# original_tag = soup.b
#
# new_tag = soup.new_tag("a", href="http://www.example.com")
# original_tag.append(new_tag)
