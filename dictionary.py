#coding: utf-8

import json
import codecs
import shlex
import re
import pprint

from controll import controll

'''
dictionary

    controllクラスを継承した人工言語辞書作成用
    クラス
'''

__author__ = 'glowlight.info'
__version__ = '1.0'

class dictionary(controll):

    def __init__(self, path=None):
        '''
        controllインスタンスを作成する.

        path: str
            セーブデータへのパス
        '''
        super().__init__(path)

    @staticmethod
    def showData(indent, dic, keys):
        '''
        単語entryの表示を楽にする. dicデータ内の指定されたkeysに対する
        内容を全て表示する.

        indent: int
            インデントのスペースの数

        dic: dict
            表示する単語データ

        keys: str[]
            キーのリスト
        '''

        for key in keys:
            if isinstance(dic[key], (str, int)) or dic[key] == None:
                print(indent*' ' + key + ': ' + str(dic[key]))

            if isinstance(dic[key], list):
                f = lambda x,n: '['+str(n)+'] ' + x
                n = len(dic[key])
                print(indent*' ' + key + ': ' +  ' '.join(map(f, dic[key], range(n))))

    @staticmethod
    def show(cr):
        '''
        単語entryの全体を表示する.
        '''
        pprint.pprint(cr)

    def lookup(self, spelling):
        '''
        単語を引く

        spelling: str
            単語を指定する. いずれ正規表現に対応する予定
        '''

        word = self.find(lambda dic: dic['index'] == spelling)
        idNum = int(word[0][0])
        self.current = self.data['entries'][idNum]
        self.pwd = '/entries/' + str(idNum)
        self.show(self.current)

    def command(self, command):
        '''
        controllクラスのcommandメソッドを継承したもの
        '''

        tup = super().command(command)
        com = tup[0]
        args = tup[1:]

        try:
            if len(tup) == 2:
                if com == 'lu': self.lookup(args[0])
            if len(tup) == 1:
                if com == 'show': self.show(self.current)
        except (KeyError, IndexError) as e:
            print('コマンドの書式がおかしい')
            print(e)
        
        return tup
