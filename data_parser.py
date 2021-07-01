from bs4 import BeautifulSoup

from expenses_fetcher.variables import RELEVANT_CATEGORIES


def parse_html(file_path: str) -> (list, str):
    try:
        with open(file_path) as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        operations_table = soup.find_all("table")[-1]
        rows = operations_table.find_all('tr')[1:]
        data = []
        for row in rows:
            cells = row.find_all('td')
            category = cells[3].text
            if category not in RELEVANT_CATEGORIES:
                continue
            amount_plain = cells[4].text.replace(',', '.').replace(' PLN', '')
            amount = float(amount_plain)
            data.append({"category": category, 'amount': amount})
    except Exception as e:
        return [], str(e)
    else:
        return data, ""
