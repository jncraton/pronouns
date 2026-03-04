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
    expect(root.locator('#pronouns')).to_have_text('she/her', timeout=10000)
    expect(root.locator('#displayName')).to_have_text('Ada Lovelace')
    expect(root.locator('#details')).to_contain_text('Ada Lovelace')

def test_lookup_fragment(page: Page):
    page.goto(f'{file_url}#Alan Turing')
    expect(page.locator('#pronouns')).to_have_text('he/him', timeout=10000)
    expect(page.locator('#displayName')).to_have_text('Alan Turing')
    # Detailed entity lookup for Alan Turing often returns "Alan" as the first entity label
    expect(page.locator('#details')).to_contain_text('Alan')

def test_lookup_precached(root: Page):
    root.locator('#displayName').fill('James')
    expect(root.locator('#pronouns')).to_have_text('he/him', timeout=10000)
    expect(root.locator('#details')).to_contain_text('James')
    expect(root.locator('#details')).to_contain_text('male given name')

def test_lookup_ambiguous(root: Page):
    root.locator('#displayName').fill('Jordan')
    # Jordan is precached as male only currently
    expect(root.locator('#pronouns')).to_have_text('he/him', timeout=10000)
    expect(root.locator('#details')).to_contain_text('Jordan')
    expect(root.locator('#details')).to_contain_text('male given name')

def test_lookup_mars(root: Page):
    root.locator('#displayName').fill('Mars')
    expect(root.locator('#pronouns')).to_have_text('he/him', timeout=10000)
    expect(root.locator('#details')).to_contain_text('Mars')
    expect(root.locator('#details')).to_contain_text('given name')

def test_lookup_jon(root: Page):
    root.locator('#displayName').fill('Jon')
    expect(root.locator('#pronouns')).to_have_text('he/him', timeout=10000)
    expect(root.locator('#details')).to_contain_text('Jon')

