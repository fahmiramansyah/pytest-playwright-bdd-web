# conftest.py

import os
import pytest
import webbrowser
from datetime import datetime
from playwright.sync_api import sync_playwright
from features.page_object.login_object import LoginPage
from features.page_object.login_mweb_object import LoginMwebPage

def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="auto", help="Device to run tests on: desktop or mobile")
    parser.addoption("--headless", action="store", default="false", help="Run browser in headless mode: true or false")

@pytest.fixture(scope="function")
def browser_page(request):
    headless_option = request.config.getoption("--headless")
    headless = headless_option.lower() == "true"

    markers = {mark.name for mark in request.node.iter_markers()}

    # Default ke desktop jika tidak ada
    if "mobile" in markers:
        device = "mobile"
    else:
        device = "desktop"

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)

    if device == "mobile":
        iphone = playwright.devices["iPhone 13"]
        context = browser.new_context(**iphone)
    else:
        context = browser.new_context(viewport={"width": 1455, "height": 768})

    page = context.new_page()
    yield page

    context.close()
    browser.close()
    playwright.stop()


def pytest_configure(config):
    reports_dir = os.path.join(os.getcwd(), "reports", "html")
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"report_{timestamp}.html")
    config.option.htmlpath = report_path

def pytest_sessionfinish(session, exitstatus):
    report_path = session.config.option.htmlpath
    if report_path and os.path.exists(report_path):
        webbrowser.open(f"file://{report_path}")

def pytest_metadata(metadata):
    # Remove unwanted metadata
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)
    metadata.pop("JAVA_HOME", None)

    # Custom metadata
    metadata["Domain"] = "jamtangan.com"
    metadata["Environment"] = "Production"

    # Get CLI marker/tag used
    tags = None
    try:
        import inspect
        frame = inspect.currentframe()
        while frame:
            if "session" in frame.f_locals:
                session = frame.f_locals["session"]
                tags = session.config.option.markexpr
                break
            frame = frame.f_back
    except Exception:
        tags = None

    metadata["Tags"] = tags if tags else "None"
    metadata["Platform"] = "Website"

@pytest.fixture
def login_page(browser_page, request):
    markers = {marker.name for marker in request.node.iter_markers()}
    if "mobile" in markers:
        return LoginMwebPage(browser_page)
    else:
        return LoginPage(browser_page)
