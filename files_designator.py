import os

from expenses_fetcher.variables import HTML_RESULTS


def designate_the_newest_result() -> (str, bool):
    results = os.scandir(HTML_RESULTS)
    try:
        the_newest_file = sorted(results, key=lambda f: f.stat().st_mtime, reverse=True)[0]
    except Exception as e:
        return str(e), False
    else:
        return the_newest_file.path, True
