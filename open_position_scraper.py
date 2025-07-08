"""Scrape OANDA open positions using Selenium.

The script accesses the open position page and extracts currency pairs where
either the long or short position ratio is greater than or equal to 70%.
The results are printed in a simple table format.
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate


def create_driver() -> webdriver.Chrome:
    """Create a Chrome WebDriver instance.

    If the environment variable ``CHROME_DRIVER_PATH`` is provided, it will be
    used directly. Otherwise ``webdriver_manager`` will try to download a driver
    dynamically (this may fail if internet access is restricted).
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver_path = os.environ.get("CHROME_DRIVER_PATH")
    if driver_path:
        service = Service(driver_path)
    else:
        service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


def scrape_open_positions(driver: webdriver.Chrome) -> tuple[list[str], list[str]]:
    """Return currency pairs with long or short ratio >= 70%.

    Parameters
    ----------
    driver:
        An active ``webdriver.Chrome`` instance.

    Returns
    -------
    tuple[list[str], list[str]]
        Two lists containing currency pairs with long ratio >= 70% and short
        ratio >= 70% respectively.
    """

    url = "https://www.oanda.jp/lab-education/oanda_lab/oanda_rab/openpositon/"
    driver.get(url)

    # ページ内のiframeを確認して最初のiframeに切り替える
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        driver.switch_to.frame(iframes[0])

    wait = WebDriverWait(driver, 20)
    rows = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    long_pairs: list[str] = []
    short_pairs: list[str] = []

    for row in rows:
        pair_el = row.find_element(By.TAG_NAME, "th")
        data = row.find_elements(By.TAG_NAME, "td")

        if pair_el and len(data) >= 2:
            pair = pair_el.text.strip()
            long_ratio = float(data[0].text.strip().replace("%", ""))
            short_ratio = float(data[1].text.strip().replace("%", ""))

            if long_ratio >= 70:
                long_pairs.append(pair)
            if short_ratio >= 70:
                short_pairs.append(pair)

    return long_pairs, short_pairs


def print_table(long_pairs: list[str], short_pairs: list[str]) -> None:
    """Print the results in a table format."""

    max_len = max(len(long_pairs), len(short_pairs))
    rows = []
    for i in range(max_len):
        row = [
            long_pairs[i] if i < len(long_pairs) else "",
            short_pairs[i] if i < len(short_pairs) else "",
        ]
        rows.append(row)

    print(tabulate(rows, headers=["ロング70%以上", "ショート70%以上"], tablefmt="github"))


def main() -> None:
    driver = create_driver()
    try:
        long_pairs, short_pairs = scrape_open_positions(driver)
        if not long_pairs and not short_pairs:
            print("70%以上の比率の通貨ペアは見つかりませんでした。")
            return
        print_table(long_pairs, short_pairs)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
