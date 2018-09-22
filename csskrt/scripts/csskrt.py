from bs4 import BeautifulSoup, Tag
import os
from abc import ABC, abstractmethod
from typing import List, Dict, NoReturn


class Csskrt(ABC):
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

    @abstractmethod
    def get_table_styles(self) -> Dict:
        """
        Return a dictionary of the table-specific tag and the corresponding
        css styles
        Eg. { 'table': 'my-table-class, 'thead': 'my-thead-class' }
        :return:
        """

    @abstractmethod
    def version(self) -> str:
        """
        :return: The version number
        """

    @abstractmethod
    def get_list_styles(self) -> Dict:
        """
        :return:
        """

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

    def add_form_classes(self, tag_dict: dict) -> NoReturn:
        """
        Adds classes for form fields
        :param tag_dict:
        :return:
        """
        for form in self.soup.find_all('form'):
            for elem in form.children:
                if elem.name == 'label':
                    if 'label' in tag_dict:
                        self.add_class_to_element(elem, tag_dict['label'])

                elif elem.name == 'input':
                    self.add_class_to_element(elem, tag_dict['input'])

                    if elem.get('type') == 'radio':
                        if 'radio' in tag_dict:
                            self.add_class_to_element(elem, tag_dict['radio'])
                    elif elem.get('type') == 'checkbox':
                        if 'checkbox' in tag_dict:
                            self.add_class_to_element(elem, tag_dict['checkbox'])

                # elif type(elem) == Tag:  # ignore  NavigableStrings like /n
                #     if tag_dict.get(elem.name):
                #         self.add_class_to_element(elem, tag_dict[elem.name])

    def add_table_classes(self, table_tag_dict: dict) -> NoReturn:
        """
        Apply the styles to table elements
        Supports the following tags:
            ('table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td')

        :param table_tag_dict:
        :return:
        """
        table_keys = ('thead', 'tbody', 'tfoot', 'tr', 'th', 'td')

        for table in self.soup.find_all('table'):
            if table_tag_dict.get('table'):  # Add style to table tag
                self.add_class_to_element(table, table_tag_dict['table'])

            for tk in table_keys:
                if table_tag_dict.get(tk):
                    all_table_elems = table.find_all(tk)
                    for elem in all_table_elems:
                        self.add_class_to_element(elem, table_tag_dict[tk])

    def add_list_classes(self, list_tags: dict) -> NoReturn:
        """
        Supports the following tags:
            ('ul', 'ol', 'li')
        :param list_tags:
        :return:
        """
        for list in self.soup.find_all(['ol', 'ul']):
            if list.name == 'ul' and list_tags.get('ul'):
                self.add_class_to_element(list, list_tags['ul'])
            elif list.name == 'ol' and list_tags.get('ol'):
                self.add_class_to_element(list, list_tags['ol'])

            if list_tags.get('li'):
                for li in list.find_all('li', recursive=False):
                    # recursive=False to prevent double modifying for nested lists
                    self.add_class_to_element(li, list_tags['li'])

    def add_general_classes(self):
        """
        Adds styles to single elements
        :return:
        """
        supported_classes = (
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'button', 'a', 'nav'
        )
        for tag in self.tag_styles:
            if tag in supported_classes:
                for elem in self.soup.find_all(tag):
                    self.add_class_to_element(elem, self.tag_styles[tag])

    def output(self, pretty_print: bool) -> NoReturn:
        """
        Outputs a new file.
        :return:
        """
        folder = os.path.dirname(self.file_path)
        file = os.path.basename(self.file_path)
        file_name, ext = os.path.splitext(file)

        new_file_name = os.path.join(folder, file_name + '_csskrt' + ext)
        with open(new_file_name, 'w') as out_file:
            if pretty_print:
                out_file.write(str(self.soup))
            else:
                out_file.write(self.soup.prettify())

    def freshify(self) -> NoReturn:
        """
        Main function that applies all the necessary styles

        :return:
        """
        starter_tags = self.get_starter_tags()
        wrapper_tag = self.get_wrapper_tag()
        table_styles = self.get_table_styles()
        list_styles = self.get_list_styles()

        # Modify the head
        if self.soup.head:
            self.initialize_framework(self.soup.head, starter_tags)

        # Add the "wrapper" tag
        if wrapper_tag:
            self.add_wrapper_tag(wrapper_tag)

        #  Elements that have children eg. tables, lists, forms have their own
        #  dedicated function to support complex operations if necessary.
        self.add_form_classes(self.tag_styles)
        self.add_list_classes(list_styles)
        self.add_table_classes(table_styles)

        # Add styles for the rest of the elements
        self.add_general_classes()

        return self.soup
