FROM python:3.10-slim-buster

# vscodeユーザーを作成
RUN useradd -m vscode

# ChromeとChromeDriverのインストールに必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    gnupg \
    # install chrome
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # install chromedriver
    && CHROME_VERSION=$(google-chrome --version | cut -f 3 -d ' ' | cut -d '.' -f 1) \
    && CHROME_DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリをvscodeユーザーのホームディレクトリに設定
WORKDIR /home/vscode/workspace

# ファイルの所有者をvscodeユーザーに変更
COPY --chown=vscode:vscode . .

# ユーザーをvscodeに切り替え
USER vscode

# 環境変数を設定
ENV PATH="/home/vscode/.local/bin:${PATH}"

