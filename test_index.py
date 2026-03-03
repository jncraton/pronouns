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
    expect(root).to_have_title('Pronouns')

def test_lookup_ada(root: Page):
    root.locator('#displayName').fill('Ada Lovelace')
    expect(root.locator('#status')).to_contain_text('Lookup complete', timeout=10000)
    expect(root.locator('#displayName')).to_have_text('Ada Lovelace')
    expect(root.locator('#pronouns')).to_have_text('she/her')

def test_lookup_fragment(page: Page):
    page.goto(f'{file_url}#Alan Turing')
    expect(page.locator('#status')).to_contain_text('Lookup complete', timeout=10000)
    expect(page.locator('#displayName')).to_have_text('Alan Turing')
    expect(page.locator('#pronouns')).to_have_text('he/him')
