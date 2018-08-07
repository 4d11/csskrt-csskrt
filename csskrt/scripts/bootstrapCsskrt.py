from bs4 import Tag
from .csskrt import Csskrt


class BootstrapCsskrt(Csskrt):
    def __init__(self, fileName):
        tag_styles = {
            'input': 'form-control',
            'select': 'custom-select',
            'button': 'btn btn-primary',
            'checkbox': 'form-check-input',
            'radio': 'form-check-input',
        }
        super().__init__(fileName, tag_styles)

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
            input_ = None
            label = None

            for elem in form.children:
                if elem.name == 'label':
                    label = elem
                    # See if there is a input within the label (sometimes done for radio/cb)
                    input_within_label = elem.find_all('input', recursive=False)
                    if input_within_label:
                        # todo handle this case
                        raise Warning("No support for inputs nested within labels for Bootstrap"
                                      "for now.")

                elif elem.name == 'input' or elem.name == 'select':
                    if input_:
                        raise Exception("Found input without adjacent label")
                    else:
                        input_ = elem

                    if elem.get('type') == 'radio':
                        if 'radio' in tag_dict:
                            self.add_class_to_element(elem, tag_dict['radio'])
                    elif elem.get('type') == 'checkbox':
                        if 'checkbox' in tag_dict:
                            self.add_class_to_element(elem, tag_dict['checkbox'])
                    else:
                        self.add_class_to_element(elem, tag_dict['input'])

                elif elem.name == 'div':
                    # todo handle the case we have a prexisting div in form
                    raise Warning("No support yet for input elements in divs within a form")

                # Add overall wrapper
                if input_ and label:
                    if input_.get('type') == 'radio' or input_.get('type') == 'checkbox':
                        self.add_class_to_element(label, 'form-check-label')
                        field_div = self.soup.new_tag('div', **{'class': 'form-check'})
                        # Add label then input
                        input_.wrap(field_div)
                        field_div.append(label)

                    else:
                        field_div = self.soup.new_tag('div', **{'class': 'form-group'})
                        # Add label then input
                        label.wrap(field_div)
                        field_div.append(input_)

                    input_, label = None, None
