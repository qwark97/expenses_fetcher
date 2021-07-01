import os

CHROMEDRIVER_PATH = os.getenv("EF_CHROMEDRIVER_PATH", "chromedriver")
ACCOUNT_LOGIN = os.getenv("EF_ACCOUNT_LOGIN")
ACCOUNT_PASSWORD = os.getenv("EF_ACCOUNT_PASSWORD")
HTML_RESULTS = os.getenv("EF_HTML_RESULTS", os.path.join(os.getcwd(), "html_results"))
MBANK_LOGIN_PAGE = "https://online.mbank.pl/pl/Login"
MBANK_HISTORY_PAGE = "https://online.mbank.pl/history"
BROWSER_PROFILE_PATH = os.getenv("EF_BROWSER_PROFILE_PATH")
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
ERROR_SCREENS = os.getenv("EF_ERROR_SCREENS", os.path.join(os.getcwd(), "error_screens"))
