from bs4 import Tag
from .csskrt import Csskrt


class BulmaCsskrt(Csskrt):
    def __init__(self, fileName):
        tag_styles = {
            'input': 'input',
            'label': 'label',
            'textarea': 'textarea',
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
        super().__init__(fileName, tag_styles)

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

    def add_form_classes(self, tag_dict: dict):
        """
        The only difference between this and parent implementation is the addition of adding
         the 'input group' class
        :param tag_dict:
        :return:
        """
        for form in self.soup.find_all('form'):
            label, input_ = None, None
            for elem in form.children:
                if elem.name == 'label':
                    label = elem
                    if 'label' in tag_dict:
                        self.add_class_to_element(elem, tag_dict['label'])

                    # See if there is a input within the label (sometimes done for radio/cb)
                    input_within_label = elem.find_all('input', recursive=False)
                    if input_within_label:
                        input_type = input_within_label.get('type')
                        if input_type == 'checkbox':
                            self.add_class_to_element(label, 'checkbox')
                        elif input_type == 'radio':
                            self.add_class_to_element(label, 'radio')
                        label = None
                        input = None

                elif elem.name == 'input':
                    if input_:
                        raise Exception("Found input without adjacent label")
                    else:
                        input_ = elem

                    if elem.get('type') != 'radio' and elem.get('type') != 'checkbox':
                        # Radio/CB don't take a class but their label does
                        self.add_class_to_element(elem, tag_dict['input'])

                elif elem.name == 'select':
                    # Add select div
                    select_div = self.soup.new_tag('div', **{'class': 'select'})
                    elem.wrap(select_div)

                    # Add control div
                    control_div = self.soup.new_tag('div', **{'class': 'control'})
                    select_div.wrap(control_div)

                    # Add overall wrapper
                    field_div = self.soup.new_tag('div', **{'class': 'field'})
                    control_div.wrap(field_div)

                if input_ and label:
                    if input_.get('type') == 'radio' or input_.get('type') == 'checkbox':
                        if input_.get('type') == 'radio':
                            self.add_class_to_element(label, 'radio')
                        else:
                            self.add_class_to_element(label, 'checkbox')

                        # Add input then label
                        # todo wrap all consecutive inputs with wrapper
                        # control_div = self.soup.new_tag('div', **{'class': 'control'})
                        # label.wrap(control_div)
                        label.insert(0, input_)
                    else:
                        # Add overall wrapper
                        field_div = self.soup.new_tag('div', **{'class': 'field'})
                        label.wrap(field_div)
                        field_div.append(input_)

                        # Add input wrapper
                        control_div = self.soup.new_tag('div', **{'class': 'control'})
                        input_.wrap(control_div)

                    label, input_ = None, None

    def get_list_styles(self):
        return {}  # no list styles
