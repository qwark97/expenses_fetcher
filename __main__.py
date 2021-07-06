import asyncio
import os

from expenses_fetcher.data_fetcher import fetch_today_expenses, run_browser
from expenses_fetcher.data_parser import parse_html
from expenses_fetcher.data_sender import store_data
from expenses_fetcher.files_designator import designate_the_newest_result
from expenses_fetcher.notifier import notify_about_error
from expenses_fetcher.variables import ACCOUNT_LOGIN, ACCOUNT_PASSWORD, HTML_RESULTS, \
    BROWSER_PROFILE_PATH, ERROR_SCREENS


async def run():
    driver = None
    try:
        # run browser
        driver = run_browser()
    except Exception as e:
        # handle error during launching browser
        notify_about_error(msg=f"Uruchomienie przeglądarki się nie powiodło z błędem: {str(e)}")
    else:
        # fetch expenses
        ok = fetch_today_expenses(driver)
        if not ok:
            notify_about_error(msg="Pobieranie danych z banku się nie powiodło. Sprawdź screenshot'a")
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

        err = await store_data(data)
        if err:
            notify_about_error(msg=f"Przesłanie uzyskanych danych się nie powiodło z błędem: {err}")
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
    asyncio.run(run())
