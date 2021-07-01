import os
import time

from selenium import webdriver

from expenses_fetcher.data_fetcher import fetch_today_expenses
from expenses_fetcher.notifier import notify_about_error
from expenses_fetcher.variables import CHROMEDRIVER_PATH, ACCOUNT_LOGIN, ACCOUNT_PASSWORD, HTML_RESULTS, \
    BROWSER_PROFILE_PATH, USER_AGENT, ERROR_SCREENS


def run():
    driver = None
    # run browser
    try:
        prefs = {'download.default_directory': HTML_RESULTS}
        o = webdriver.ChromeOptions()
        o.headless = True
        o.add_argument(f"user-data-dir={BROWSER_PROFILE_PATH}")
        o.add_argument(f"user-agent={USER_AGENT}")
        o.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH,
            options=o,
        )
        driver.set_window_size(1920, 1080)
    # handle error
    except Exception as e:
        notify_about_error(str(e))
    # fetch expenses
    else:
        result = fetch_today_expenses(driver)

    # close browser
    finally:
        if driver:
            driver.quit()


def init():
    if not ACCOUNT_LOGIN or not ACCOUNT_PASSWORD:
        print("pass account credentials")
        exit(1)
    if not BROWSER_PROFILE_PATH:
        print("point browser profile")
        exit(1)
    os.makedirs(HTML_RESULTS, exist_ok=True)
    os.makedirs(ERROR_SCREENS, exist_ok=True)


if __name__ == '__main__':
    init()
    run()
