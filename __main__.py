import os

from selenium import webdriver

from expenses_fetcher.data_fetcher import fetch_today_expenses
from expenses_fetcher.data_parser import parse_html
from expenses_fetcher.files_designator import designate_the_newest_result
from expenses_fetcher.notifier import notify_about_error
from expenses_fetcher.variables import CHROMEDRIVER_PATH, ACCOUNT_LOGIN, ACCOUNT_PASSWORD, HTML_RESULTS, \
    BROWSER_PROFILE_PATH, USER_AGENT, ERROR_SCREENS


def run():
    driver = None
    try:
        # run browser
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
    except Exception as e:
        # handle error
        notify_about_error(msg=f"Uruchomienie przeglądarki się nie powiodło z błędem: {str(e)}")
    else:
        # fetch expenses
        ok = fetch_today_expenses(driver)
        if not ok:
            notify_about_error(msg="Pobieranie danych z banku się nie powiodło")
            exit(1)

        # designate the newest result
        file_path, ok = designate_the_newest_result()
        if not ok:
            # if ok == False, then 'file_path' contains raised exception
            notify_about_error(msg=f"Wyznaczenie najnowszego rezultatu się nie powiodło z błędem: {file_path}")
            exit(1)

        # parse fetched html
        data, err = parse_html(file_path)
        if err:
            notify_about_error(msg=f"Przetworzenie pobranych rezultatów się nie powiodło z błędem: {err}")
            exit(1)

    finally:
        if driver:
            # close browser if it hasn't been closed because of some reason
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
