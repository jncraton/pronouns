import re
from playwright.sync_api import Page, expect
import pytest

from pathlib import Path

file_url = Path("index.html").resolve().as_uri()

@pytest.fixture
def root(page: Page):
    page.goto(f"{file_url}#")
    return page

def test_page_title(root):
    expect(root).to_have_title("Pronoun Lookup (Wikidata)")

def test_lookup_ada(root: Page):
    root.locator('#nameInput').fill('Ada Lovelace')
    root.locator('#go').click()
    expect(root.locator('#status')).to_contain_text('Lookup complete', timeout=10000)
    expect(root.locator('#summary')).to_contain_text('Ada Lovelace → female (she/her)')

def test_lookup_fragment(page: Page):
    page.goto(f'{file_url}#Alan Turing')
    expect(page.locator('#status')).to_contain_text('Lookup complete', timeout=10000)
    expect(page.locator('#summary')).to_contain_text('Alan Turing → male (he/him)')
