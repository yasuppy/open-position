#!/bin/bash

# 仮想環境が存在しない場合は作成する
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# 仮想環境を有効にする
source venv/bin/activate

# 必要なライブラリをインストールする
pip install -r requirements.txt

# スクレイピングスクリプトを実行する
python open_position_scraper.py

# 仮想環境を無効にする
deactivate
