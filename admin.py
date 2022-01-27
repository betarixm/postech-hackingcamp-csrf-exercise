from selenium import webdriver
import urllib
import uuid
import os

PORT = int(os.getenv("APP_PORT", "8000"))
ADMIN_KEY = str(uuid.uuid4().hex)


def _get_url(url, cookie=None):
    if cookie is None:
        cookie = {"name": "name", "value": "value"}

    cookie.update({"domain": "127.0.0.1"})

    options = webdriver.ChromeOptions()
    for _ in [
        "headless",
        "window-size=1920x1080",
        "disable-gpu",
        "no-sandbox",
        "disable-dev-shm-usage",
    ]:
        options.add_argument(_)

    driver = webdriver.Chrome("chromedriver", options=options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    driver.get(f"http://127.0.0.1:{PORT}/")
    driver.add_cookie(cookie)
    print(url)
    driver.get(url)
    driver.implicitly_wait(10)
    driver.quit()

    return True


def checks_client_page(title: str, content: str):
    url = f"http://127.0.0.1:{PORT}/check?title={urllib.parse.quote(title)}&content={urllib.parse.quote(content)}"

    _get_url(url, {"name": ADMIN_KEY, "value": ADMIN_KEY, "httpOnly": True})

    return True
