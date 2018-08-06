from bs4 import Tag
from .csskrt import Csskrt


class BootstrapCsskrt(Csskrt):
    def __init__(self, fileName, pretty_print):
        tag_styles = {
            'input': 'form-control',
            'select': 'custom-select',
            'button': 'btn btn-primary',
            'checkbox': 'form-check-input',
        }
        super().__init__(fileName, pretty_print, tag_styles)

    def version(self):
        return "v4.1"

    def get_starter_tags(self):
        charset_meta = self.soup.new_tag(
            'meta', charset='utf-8'
        )

        # hack since 'name' is reserve
        viewport_meta = Tag(
            builder=self.soup.builder,
            name='meta',
            attrs={'name': "viewport", 'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'}
        )

        stylesheet = self.soup.new_tag(
            'link',
            rel='stylesheet',
            href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
            integrity='sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
            crossorigin='anonymous'
        )
        return [charset_meta, viewport_meta, stylesheet]

    def get_wrapper_tag(self):
        div = self.soup.new_tag(
            'div', **{'class': 'container'}
        )
        return div

    def get_table_styles(self):
        return {
            'table': 'table',
            'thead': 'thead-light',
        }

    def get_list_styles(self):
        return {
            'ol': 'list-group',
            'ul': 'list-group',
            'li': 'list-group-item'
        }

    def add_form_classes(self, tag_dict: dict):
        """
        Applies form classes, only difference between this and parent implementation is the addition of adding
         the "input group wrapper" class
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
                        field_div = self.soup.new_tag('div', **{'class': 'form-group'})
                        elem.wrap(field_div)
                    else:
                        # the input has a preceding label
                        field_div = self.soup.new_tag('div', **{'class': 'form-group'})
                        spotted_label.wrap(field_div)
                        field_div.append(elem)
                        spotted_label = None

                    # Add input wrapper
                    control_div = self.soup.new_tag('div', **{'class': 'control'})
                    elem.wrap(control_div)
