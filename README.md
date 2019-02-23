# atcoder-scraper

Atcoderの問題の入出力例を取得

## 開発環境

### OS
- Windows 10

### 言語
- Python 3.7.1

### ライブラリ

|ライブラリ|機能|
|---|---|
|[Requests](http://docs.python-requests.org/en/master/)|HTMLのデータ取得|
|[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|HTMLの解析|
|[colorama](https://pypi.org/project/colorama/)|文字色の設定|

```
$ pip install requests
$ pip install beautifulsoup4
$ pip install colorama
```

### (Option) Pythonをexeに変換する
PyInstallerをインストール
```
$ pip install pyinstaller
```
Pythonをexeに変換するには
```
$ pyinstaller atcoder-scraper.py --onefile --clean
```
dist/atcoder-scraper.exeが生成される

PyInstallerの使い方の詳細は[Using PyInstaller — PyInstaller 3.4 documentation](https://pyinstaller.readthedocs.io/en/stable/usage.html)

# 使い方

```
$ python atcoder-scraper.py [-h] [-t] [-n] [-d] url
```
exeに変換したときは
```
$ atcoder-scraper.exe [-h] [-t] [-n] [-d] url
```

### オプション
```
positional arguments:
  url               AtCoderの問題のURL

optional arguments:
  -h, --help        show this help message and exit
  -t, --test        コンパイル&テストを実行
  -n, --nodownload  入出力例をダウンロードしない
  -d, --debug       AC時に入力例と出力を表示
```