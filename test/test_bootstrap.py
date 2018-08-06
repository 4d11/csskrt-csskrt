import sys, os
import copy
import unittest
import pytest
from bs4 import BeautifulSoup

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from csskrt.bootstrapCsskrt import BootstrapCsskrt


@pytest.fixture()
def bootstrap_csskrt():
    bs_csskrt = BootstrapCsskrt(os.path.join(os.path.dirname(__file__), 'input/test1.html'))
    before = copy.copy(bs_csskrt.soup)
    bs_csskrt.freshify()
    after = bs_csskrt.soup
    return before, after

# Fix checkbox case

class TestBootstrapButtons():
    def test_compare_num_button_tags(self, bootstrap_csskrt):
        before: BeautifulSoup = bootstrap_csskrt[0]
        after: BeautifulSoup = bootstrap_csskrt[1]
        tag = 'button'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        assert (len(old_tags) == len(new_tags))

    def test_buttons_styles(self, bootstrap_csskrt):
        before: BeautifulSoup = bootstrap_csskrt[0]
        after: BeautifulSoup = bootstrap_csskrt[1]
        tag = 'button'
        style = ['btn', 'btn-primary']

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        for old_t, new_t in zip(old_tags, new_tags):
            old_class = old_t.get('class', [])
            new_class = new_t.get('class', [])

            if type(new_class) == str:  # sometimes get returns str instead of list
                new_class = new_class.strip().split(' ')

            assert(set(old_class).issubset(new_class))

    def test_buttons_content(self, bootstrap_csskrt):
        before: BeautifulSoup = bootstrap_csskrt[0]
        after: BeautifulSoup = bootstrap_csskrt[1]
        tag = 'button'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        for old_t, new_t in zip(old_tags, new_tags):
            assert old_t.get_text() == new_t.get_text()


class TestBootstrapForm():
    def test_number_form_tags(self, bootstrap_csskrt):
        before: BeautifulSoup = bootstrap_csskrt[0]
        after: BeautifulSoup = bootstrap_csskrt[1]
        tag = 'form'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        assert (len(old_tags) == len(new_tags))

    def test_form_wrapper(self, bootstrap_csskrt):
        before: BeautifulSoup = bootstrap_csskrt[0]
        after: BeautifulSoup = bootstrap_csskrt[1]
        tag = 'form'
        wrapper_class = 'form-group'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        for form in new_tags:
            wrappers = form.find_all('div', recursive=False, attrs={'class': wrapper_class})
            inputs = form.find_all('input')
            assert len(wrappers) == len(inputs)  # 1 input per wrapper ?

            for wrapper in wrappers:
                inputs = wrapper.find_all('input')
                assert len(inputs) == 1



