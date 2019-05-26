# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import argparse
import os
import subprocess
import glob
import re
import colorama
from colorama import Fore, Back
import json

colorama.init(autoreset=True)

parser = argparse.ArgumentParser(description='Atcoderの問題の入出力例を取得')
parser.add_argument('-u', '--url', help='AtCoderの問題のURL')
parser.add_argument('-t', '--test', action='store_true', help='コンパイル&テストを実行')
parser.add_argument('-d', '--debug',
                    action='store_true', help='AC時に入力例と出力を表示')
parser.add_argument('-c', '--clean',
                    action='store_true', help='自動生成したファイルを削除')
args = parser.parse_args()

if args.clean:
    if os.path.isfile('a.exe'):
        cmd = 'del a.exe'
        res = subprocess.run(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        if res.returncode != 0:
            print(res.stdout.decode('sjis'))
            exit()
    if os.path.isdir('testcase'):
        cmd = 'rd /s /q testcase'
        res = subprocess.run(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        if res.returncode != 0:
            print(res.stdout.decode('sjis'))
            exit()

if args.url:
    target_url = args.url
    testcase_dir = 'testcase'

    if not os.path.isdir(testcase_dir):
        os.makedirs(testcase_dir)

    login_url = 'https://atcoder.jp/login/'

    s = requests.Session()

    r = s.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')

    with open('setting.json', 'r') as f:
        d = json.load(f)
        payload = {
            'csrf_token': csrf_token,
            'username': d['username'],
            'password': d['password'],
        }

    r = s.post(login_url, data=payload)

    if r.status_code == 200:
        print(Fore.GREEN + 'LOGIN SUCCESS')
    else:
        print(Fore.RED + 'LOGIN FAILURE {} {}'.format(r.status_code, r.reason))
        exit()

    r = s.get(target_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    if r.status_code == 200:
        print(Fore.GREEN + 'GET SUCCESS')
    else:
        print(Fore.RED + 'GET FAILURE {} {}'.format(r.status_code, r.reason))
        exit()

    in_idx = 1
    out_idx = 1
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
    sourcename = 'main'

    cpp_file_exists = os.path.exists('{}.cpp'.format(sourcename))
    py_file_exists = os.path.exists('{}.py'.format(sourcename))

    # compile
    if cpp_file_exists:
        print('==========\nBUILD\n==========')
        cmd = 'g++ {}.cpp'.format(sourcename)
        res = subprocess.run(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
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
        if cpp_file_exists:
            cmd = 'a.exe < {}'.format(in_path)
        elif py_file_exists:
            cmd = 'python {}.py < {}'.format(sourcename, in_path)
        print('input{}.txt '.format(i), end='')
        res = subprocess.run(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        if res.returncode != 0:
            print(res.stdout.decode('sjis'))
            exit()
        with open(out_path, 'r') as f:
            expected = f.read().replace('\r', '')
            ans = res.stdout.decode().replace('\r', '')
            if ans == expected:
                print(Fore.BLACK + Back.GREEN + 'AC')
                if args.debug:
                    print(Fore.GREEN + 'expected = {}'.format(expected))
                    print(Fore.GREEN + 'answer = {}'.format(ans))
                ac_cnt += 1
            else:
                print(Fore.BLACK + Back.YELLOW + 'WA')
                print(Fore.YELLOW + 'expected = {}'.format(expected))
                print(Fore.YELLOW + 'answer = {}'.format(ans))
                wa_cnt += 1
    print('==========\nRESULT\n==========')
    print('AC = {}, WA = {}'.format(ac_cnt, wa_cnt), end=' ')
    if wa_cnt == 0:
        print(Fore.BLACK + Back.GREEN + 'AC')
    else:
        print(Fore.BLACK + Back.YELLOW + 'WA')
