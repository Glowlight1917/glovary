# glovary
CUIで使う辞書ソフト

# インストール方法

このレポジトリをまるごとダウンロードするだけでよい.

# 使い方

## 起動の仕方 ー コマンドライン

* python3 glovary.py
辞書を新規作成する

* python3 glovary.py JSONファイル
人工言語の辞書データを読み込んで編集する

* python3 glovary.py JSONファイル -l 単語
指定した辞書データから単語を引く

* python3 glovary.py -s スクリプトファイル
スクリプトを実行する

* python3 glovary.py JSONファイル -s スクリプトファイル
指定の辞書データについてスクリプトを実行する

## コマンド一覧

* add パス キー 追加文字列
パス先の指定キーのリストにデータを追加する

* rm パス キー 添字
パス先の指定キーのリスト要素を削除する

* ed パス キー 添字 置換文字列
パス先の指定キーの内容を変更する

* swap パス キー 添字1 添字2
パス先の指定キーのentryリストの要素を入れ替える

* ent パス キー
 パス先の指定キーにentryを追加する

* save 保存先のパス(JSON)
現在の辞書データを外部ファイルに保存する

* script スクリプトのパス
スクリプトを実行する

* cd 移動先のパス
currentを変更する

* show
currentを表示する

* hs
コマンド実行履歴を表示する

* lu 正規表現
単語を引く

# ファイル一覧

* controll.py
ツリーデータを扱う基本クラス

* dictionary.py
辞書ソフトの基本機能を持つクラス

* glovary.py
このソフトのインターフェイス

* template.json
dictデータのテンプレート集

* test_script
glovaryを動かすスクリプトのサンプル
