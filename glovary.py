#coding: utf-8

import sys
import readline
from dictionary import dictionary

def commandline(dic):
    while True:
        prompt = '[glovary:' + dic.pwd  + ']$ '
        dic.command(input(prompt))

args = sys.argv
argNum = len(args)

#python3 glovary.py /dictData/ -l /entry/
#辞書データから単語を引く
if argNum == 4 and args[2] == '-l':
    dic = dictionary(args[1])
    dic.lookup(args[3])
    sys.exit(0)

#python3 glovary.py /dictData/ -s /script/
#辞書データについてスクリプトを実行
if argNum == 4 and args[2] == '-s':
    dic = dictionary(args[1])
    dic.readScript(args[3])
    sys.exit(0)

#python3 glovary.py -s /script/
#スクリプトを実行
if argNum == 3 and args[1] == '-s':
    dic = dictionary()
    dic.readScript(args[2])
    sys.exit(0)

#python3 glovary.py /dictData/
#辞書データを開く
if argNum == 2:
    dic = dictionary(args[1])

#python3 glovary.py
#新規作成する
if argNum == 1:
    dic = dictionary()

commandline(dic)
