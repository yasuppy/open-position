# AGENTS.md

このファイルは、AI開発アシスタント（Geminiなど）がこのプロジェクトを理解し、効率的に支援するためのコンテキストを提供します。

## プロジェクト概要

このプロジェクトは、OANDA Japanの公開するオープンポジションの情報をウェブスクレイピングし、買いまたは売りのポジション比率が70%以上の通貨ペアを抽出して表示するPythonスクリプトです。

## 技術スタック

- **言語:** Python 3.10
- **主要ライブラリ:**
    - `selenium`: ブラウザ操作とスクレイピングに使用します。
- **開発環境:**
    - Docker / devcontainer: 開発環境をコンテナ化し、再現性を高めています。
    - GitHub Codespaces: リモートでの開発環境を提供します。

## 開発環境のセットアップ

### GitHub Codespaces / devcontainer (推奨)

このリポジトリには`.devcontainer`設定が含まれています。

1.  GitHub上でCodespacesを起動するか、ローカルのVS Codeで「Remote-Containers: Reopen in Container」コマンドを実行してください。
2.  コンテナのビルドが自動的に開始されます。
3.  `postCreateCommand`により、`requirements.txt`に記載されたPythonパッケージが自動でインストールされます。

## スクリプトの実行

以下のコマンドでスクリプトを実行します。

```bash
python open_position_scraper.py
```

スクリプトはヘッドレスモードのChromeを起動し、結果を標準出力に表示します。

## コードの変更について

- `open_position_scraper.py`: メインのスクリプトです。devcontainer環境で動作するように、ChromeDriverのパスがハードコードされています。
- `.devcontainer/`: devcontainerとGitHub Codespacesの設定ファイルが含まれています。
    - `Dockerfile`: 開発コンテナのベースイメージと、ChromeおよびChromeDriverのインストール手順を定義しています。
    - `devcontainer.json`: VS Codeの拡張機能やコンテナ作成後のコマンドなどを定義しています。
