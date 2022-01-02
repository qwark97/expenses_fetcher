import os

"""OBLIGATORY VALUES"""
ACCOUNT_LOGIN = os.getenv("EF_ACCOUNT_LOGIN")
ACCOUNT_PASSWORD = os.getenv("EF_ACCOUNT_PASSWORD")
BROWSER_PROFILE_PATH = os.getenv("EF_BROWSER_PROFILE_PATH")

"""VALUES WITH DEFAULTS"""
CHROMEDRIVER_PATH = os.getenv("EF_CHROMEDRIVER_PATH", "chromedriver")
HTML_RESULTS = os.getenv("EF_HTML_RESULTS", os.path.join(os.getcwd(), "html_results"))
ERROR_SCREENS = os.getenv("EF_ERROR_SCREENS", os.path.join(os.getcwd(), "error_screens"))
BUDGET_MAINTAINER_URL = os.getenv("EF_BUDGET_MAINTAINER_URL", "http://localhost:9999")

"""STATIC VALUES"""
MBANK_LOGIN_PAGE = "https://online.mbank.pl/pl/Login"
MBANK_HISTORY_PAGE = "https://online.mbank.pl/history"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
RELEVANT_CATEGORIES = ['Żywność i chemia domowa']
