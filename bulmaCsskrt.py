from bs4 import BeautifulSoup, Tag, NavigableString
from csskrt import Csskrt


class BulmaCsskrt(Csskrt):
    def __init__(self, fileName, pretty_print):
        tag_styles = {
            'input': 'input',
            'label': 'label',
            'textarea': 'textarea',
            'select': 'select',
            'button': 'button',
            'checkbox': 'checkbox',
            'radio': 'radio',
            'h1': 'title is-1',
            'h2': 'title is-2',
            'h3': 'title is-3',
            'h4': 'title is-4',
            'h5': 'title is-5',
            'h6': 'title is-6'
        }
        super().__init__(fileName, pretty_print, tag_styles)

    def version(self):
        return "v0.7.1"

    def get_starter_tags(self):
        # hack since 'name' is reserved
        meta = Tag(builder=self.soup.builder,
                   name='meta',
                   attrs={'name': "viewport", 'content': 'width=device-width, initial-scale=1'})

        stylesheet = self.soup.new_tag(
            'link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
        )
        return [meta, stylesheet]

    def get_wrapper_tag(self):
        div = self.soup.new_tag(
            'div', **{'class': 'container'}
        )
        return div

    def get_table_styles(self):
        return {
            'table': 'table',
            'thead': 'thead',
            'tbody': 'tbody',
            'tr': 'tr',
            'th': 'th',
            'td': 'td'
        }

    def get_list_styles(self):
        return {}  # no list styles

    def add_form_classes(self, tag_dict: dict):
        """
        The only difference between this and parent implementation is the addition of adding
         the 'input group' class
        :param tag_dict:
        :return:
        """
        for form in self.soup.find_all('form'):
            spotted_label = None
            for elem in form.children:
                if elem.name == 'label':
                    spotted_label = elem
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

                    # Add overall wrapper
                    if not spotted_label:
                        # add wrapper
                        field_div = self.soup.new_tag('div', **{'class': 'field'})
                        elem.wrap(field_div)
                    else:
                        # the input has a preceding label
                        field_div = self.soup.new_tag('div', **{'class': 'field'})
                        spotted_label.wrap(field_div)
                        field_div.append(elem)
                        spotted_label = None

                    # Add input wrapper
                    control_div = self.soup.new_tag('div', **{'class': 'control'})
                    elem.wrap(control_div)