# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import argparse
import os
import subprocess
import glob
import re
import colorama
from colorama import Fore  # , Back, Style

colorama.init(autoreset=True)

parser = argparse.ArgumentParser(description='Atcoderの入出力例を取得')
parser.add_argument('url', help='AtCoderの問題のURL')
parser.add_argument('-t', '--test', action='store_true', help='コンパイル&テストを実行')
parser.add_argument('-n', '--nodownload',
                    action='store_true', help='入出力例をダウンロードしない')
parser.add_argument('-d', '--debug',
                    action='store_true', help='AC時に入力例と出力を表示')
args = parser.parse_args()

target_url = args.url
testcase_dir = 'testcase'
sourcename = 'main'

if not os.path.isdir(testcase_dir):
    os.makedirs(testcase_dir)

r = requests.get(target_url)
soup = BeautifulSoup(r.text, 'html.parser')

in_idx = 1
out_idx = 1
if not args.nodownload:
    for part in soup.select('.part'):
        h3 = part.h3.text
        if '入力例' in h3:
            filename = 'input{}.txt'.format(in_idx)
            with open(os.path.join(testcase_dir, filename), 'w') as f:
                line = part.find('pre').contents[0].splitlines()
                for s in line:
                    f.write(s + '\n')
            in_idx += 1
        elif '出力例' in h3:
            filename = 'output{}.txt'.format(out_idx)
            with open(os.path.join(testcase_dir, filename), 'w') as f:
                line = part.find('pre').contents[0].splitlines()
                for s in line:
                    f.write(s + '\n')
            out_idx += 1

if args.test:
    # compile
    print('==========\nBUILD\n==========')
    cmd = 'g++ {}.cpp'.format(sourcename)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if res.returncode != 0:
        print(res.stdout.decode('sjis'))
        exit()
    print(Fore.GREEN + 'BUILD SUCCESS')
    # run test
    print('==========\nTEST\n==========')
    ac_cnt = 0
    wa_cnt = 0
    filelist = glob.glob('{}/*.txt'.format(testcase_dir))
    testcase_num = len([f for f in filelist if re.match('.*input.*', f)])
    for i in range(1, testcase_num + 1):
        in_path = os.path.join(testcase_dir, 'input{}.txt'.format(i))
        out_path = os.path.join(testcase_dir, 'output{}.txt'.format(i))
        cmd = 'a.exe < {}'.format(in_path)
        print('input{}.txt '.format(i), end='')
        res = subprocess.run(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        if res.returncode != 0:
            print(res.stdout.decode('sjis'))
            exit()
        with open(out_path, 'r') as f:
            expected = f.read().rstrip()
            ans = res.stdout.decode().rstrip()
            if ans.strip() == expected.strip():
                print(Fore.GREEN + 'AC')
                if args.debug:
                    print(Fore.GREEN + 'expected = {}'.format(expected))
                    print(Fore.GREEN + 'answer = {}'.format(ans))
                ac_cnt += 1
            else:
                print(Fore.YELLOW + 'WA')
                print(Fore.YELLOW + 'expected = {}'.format(expected))
                print(Fore.YELLOW + 'answer = {}'.format(ans))
                wa_cnt += 1
    print('==========\nRESULT\n==========')
    print('AC = {}, WA = {}'.format(ac_cnt, wa_cnt))
    print(Fore.GREEN + 'AC') if wa_cnt == 0 else print(Fore.YELLOW + 'WA')
