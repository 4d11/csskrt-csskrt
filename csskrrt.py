from bs4 import BeautifulSoup, Tag, NavigableString
import os
from abc import ABC, abstractmethod
from typing import List, Dict, NoReturn


class Csskrrt(ABC):
    def __init__(self, filename: str, tag_styles: Dict):
        f = open(filename)  # should be able to handle dirs (for later) todo
        f_data = f.read()

        self.file_path = filename
        self.soup = BeautifulSoup(f_data, 'html.parser')
        self.tag_styles = tag_styles

    @abstractmethod
    def get_starter_tags(self) -> List[Tag]:
        """
        Return a list of the Tags you want to add to the <head>
        :return:
        """
        pass

    @abstractmethod
    def get_wrapper_tag(self) -> List[Tag] or None:
        """
        Return the 'wrapper' class for your framework.
        Eg. 'container' for Bootstrap
        :return:
        """
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
        """
        Applys the header tags to the head
        :param head:
        :param tags:
        :return:
        """
        for tag in tags:
            head.append(tag)

    def add_wrapper_tag(self, wrapper_tag: Tag):
        """
        Add the container tag for the framework
        :param wrapper_tag:
        :return:
        """
        # potentially optimize by using wrap and swapping attributes?
        body_children = list(self.soup.body.children)
        self.soup.body.clear()
        self.soup.body.append(wrapper_tag)
        for child in body_children:
            wrapper_tag.append(child)

    def add_form_classes(self, tag_dict: dict):
        """
        Adds classes for form fields
        :param tag_dict:
        :return:
        """
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

    def output(self) -> NoReturn:
        """
        Outputs a new file.
        :return:
        """
        folder = os.path.dirname(self.file_path)
        file = os.path.basename(self.file_path)
        file_name, ext = os.path.splitext(file)

        new_file_name = os.path.join(folder, 'csskrrt_' + file_name + ext)
        with open(new_file_name, 'w') as out_file:
            out_file.write(self.soup.prettify())

    def freshify(self) -> NoReturn:
        """
        Main function that applies all the necessary styles
        :return:
        """
        starter_tags = self.get_starter_tags()
        wrapper_tag = self.get_wrapper_tag()

        self.initialize_framework(self.soup.head, starter_tags)
        if wrapper_tag:
            self.add_wrapper_tag(wrapper_tag)
        self.add_form_classes(self.tag_styles)
        self.output()

# print(btn.get('class', []))
