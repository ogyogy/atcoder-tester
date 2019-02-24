# atcoder-scraper

Atcoderの問題の入出力例を取得

## 開発環境

### OS
- Windows 10

### シェル
- [Git for Windows](https://gitforwindows.org/)

### 言語
- Python 3.7.1

### Pythonパッケージ

|ライブラリ|機能|
|---|---|
|[Requests](http://docs.python-requests.org/en/master/)|HTMLのデータ取得|
|[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|HTMLの解析|
|[colorama](https://pypi.org/project/colorama/)|文字色の設定|


pipでインストール

```
$ pip install requests
$ pip install beautifulsoup4
$ pip install colorama
```

## (Option)Pythonをexeに変換する
[Pythonパッケージ](#Pythonパッケージ)と、PyInstallerをインストール
```
$ pip install pyinstaller
```
Pythonをexeに変換
```
$ pyinstaller atcoder-scraper.py --onefile --clean
```
dist/atcoder-scraper.exeが生成される

PyInstallerの使い方の詳細は[Using PyInstaller — PyInstaller 3.4 documentation](https://pyinstaller.readthedocs.io/en/stable/usage.html)

## 使い方
### 初期設定

設定ファイルをsetting.jsonという名前で作成し、実行ファイル(pyまたはexe)と同じディレクトリに格納

```
{
    "username": "xxxx",
    "password": "1234"
}
```

### Python
```
$ python atcoder-scraper.py [-h] [-t] [-n] [-d] url
```

### (Option)exe
[Python](#Python)で実行できる状態で、[(Option)Pythonをexeに変換する](#OptionPythonをexeに変換する) を実施する必要がある
```
$ ./atcoder-scraper.exe [-h] [-t] [-n] [-d] url
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