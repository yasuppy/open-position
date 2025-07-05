from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ヘッドレスオプション設定（CodexなどGUIがない環境向け）
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ChromeDriver サービス開始（webdriver_managerを使用）
service = Service(ChromeDriverManager().install())

# ドライバ起動
driver = webdriver.Chrome(service=service, options=options)

try:
    # URLにアクセス
    url = 'https://www.oanda.jp/lab-education/oanda_lab/oanda_rab/openpositon/'
    driver.get(url)
    print("ページソースの最初の500文字:")
    print(driver.page_source[:500])

    # iframeの存在を確認
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        print(f"iframeが見つかりました: {len(iframes)}個")
        # 最初のiframeに切り替えてみる（必要に応じて適切なiframeを選択）
        driver.switch_to.frame(iframes[0])
        print("iframeに切り替えました。")

    # テーブルの行がロードされるまで最大20秒待機
    wait = WebDriverWait(driver, 20)
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr')))
    print(f"見つかった行の数: {len(rows)}")

    result = []
    for row in rows:
        # 通貨ペアは<th>タグ、比率は<td>タグにある
        pair_element = row.find_element(By.TAG_NAME, 'th')
        data_elements = row.find_elements(By.TAG_NAME, 'td')

        if pair_element and len(data_elements) >= 2:
            pair = pair_element.text.strip()
            long_ratio = float(data_elements[0].text.strip().replace('%', ''))
            short_ratio = float(data_elements[1].text.strip().replace('%', ''))

            if long_ratio >= 70 or short_ratio >= 70:
                result.append((pair, long_ratio, short_ratio))

    # 結果表示
    for pair, long_ratio, short_ratio in result:
        print(f"{pair}: ロング {long_ratio}%, ショート {short_ratio}%")

    if not result:
        print("70%以上の比率の通貨ペアは見つかりませんでした。")

finally:
    driver.quit()
