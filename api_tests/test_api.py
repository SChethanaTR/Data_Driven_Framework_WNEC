import pytest
from playwright.sync_api import sync_playwright
import requests


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def context(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    yield context
    context.close()
    browser.close()


def test_api_status():
    url = "http://10.99.13.11/api/auth/login"  # Replace 'your_endpoint' with the actual endpoint
    response = requests.get(url)
    assert response.status_code == 200

