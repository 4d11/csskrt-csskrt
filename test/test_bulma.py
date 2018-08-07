import sys, os
import copy
import pytest
from bs4 import BeautifulSoup

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from csskrt.scripts.bulmaCsskrt import BulmaCsskrt


@pytest.fixture()
def bulma_csskrt():
    bulma_csskrt = BulmaCsskrt(os.path.join(os.path.dirname(__file__), 'test1.html'))
    before = copy.copy(bulma_csskrt.soup)
    bulma_csskrt.freshify()
    after = bulma_csskrt.soup
    return before, after


class TestBulmaButtons():
    def test_compare_num_button_tags(self, bulma_csskrt):
        before: BeautifulSoup = bulma_csskrt[0]
        after: BeautifulSoup = bulma_csskrt[1]
        tag = 'button'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        assert (len(old_tags) == len(new_tags))

    def test_buttons_styles(self, bulma_csskrt):
        before: BeautifulSoup = bulma_csskrt[0]
        after: BeautifulSoup = bulma_csskrt[1]
        tag = 'button'
        style = ['button']

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        for old_t, new_t in zip(old_tags, new_tags):
            old_class = old_t.get('class', [])
            new_class = new_t.get('class', [])

            if type(new_class) == str:  # sometimes get returns str instead of list
                new_class = new_class.strip().split(' ')

            assert(set(old_class).issubset(new_class))

    def test_buttons_content(self, bulma_csskrt):
        before: BeautifulSoup = bulma_csskrt[0]
        after: BeautifulSoup = bulma_csskrt[1]
        tag = 'button'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        for old_t, new_t in zip(old_tags, new_tags):
            assert old_t.get_text() == new_t.get_text()


class TestBootstrapForm():
    def test_number_form_tags(self, bulma_csskrt):
        before: BeautifulSoup = bulma_csskrt[0]
        after: BeautifulSoup = bulma_csskrt[1]
        tag = 'form'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)
        assert (len(old_tags) == len(new_tags))

    def test_select_tags(self, bulma_csskrt):
        before: BeautifulSoup = bulma_csskrt[0]
        after: BeautifulSoup = bulma_csskrt[1]
        tag = 'form'

        old_tags = before.find_all(tag)
        new_tags = after.find_all(tag)

        for form in new_tags:
            for select in form.find_all('select'):
                assert(select.parent.name == 'div' and 'select' in select.parent['class']  )
                assert (select.parent.parent.name == 'div' and
                        'control' in select.parent.parent['class'])
                assert (select.parent.parent.parent.name == 'div' and
                        'field' in select.parent.parent.parent['class'])






