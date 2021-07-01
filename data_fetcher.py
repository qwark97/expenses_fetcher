import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from expenses_fetcher.variables import MBANK_LOGIN_PAGE, ACCOUNT_LOGIN, ACCOUNT_PASSWORD, MBANK_HISTORY_PAGE, \
    ERROR_SCREENS, HTML_RESULTS, BROWSER_PROFILE_PATH, USER_AGENT, CHROMEDRIVER_PATH


def run_browser() -> webdriver.Chrome:
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
    return driver


def fetch_today_expenses(driver: webdriver.Chrome) -> bool:
    try:
        # load page
        driver.get(MBANK_LOGIN_PAGE)

        # login
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.NAME, "userID"))).send_keys(ACCOUNT_LOGIN)
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.NAME, "pass"))).send_keys(ACCOUNT_PASSWORD)
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "submitButton"))).click()

        # load history page
        timeout = time.time() + 10
        while time.time() < timeout:
            current_url = driver.current_url
            if current_url != MBANK_LOGIN_PAGE:
                time.sleep(2)
                break
            else:
                time.sleep(1)
        driver.get(MBANK_HISTORY_PAGE)

        # set filters to default
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[@data-test-id="history:clearFilters"]'))).click()

        # set filter to today
        today = datetime.now().strftime("%d.%m.%Y")
        placeholder = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//div[@class="DateInput DateInput_1"]/input')))
        ac = ActionChains(driver)
        ac.double_click(placeholder).send_keys(today).perform()
        time.sleep(3)

        # download html
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[@data-test-id="history:exportHistoryMenuTrigger"]'))).click()
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//li[@data-test-id="list:1-listItem"]'))).click()
        time.sleep(2)

        # logout
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//a[@aria-label="Wyloguj"]'))).click()
    except Exception:
        now = datetime.now().strftime("%d.%m.%Y-%H:%M")
        try:
            driver.get_screenshot_as_file(f"{ERROR_SCREENS}/err-{now}.png")
        except Exception as e:
            with open(f"{ERROR_SCREENS}/err-{now}.txt", 'wt') as f:
                f.write(f'unexpected error - {str(e)}')
        finally:
            return False
    else:
        return True
    finally:
        if driver:
            driver.quit()
