#coding: utf-8
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

    def lookup(self, spelling):
        '''
        単語を引く

        spelling: str
            単語を指定する. いずれ正規表現に対応する予定
        '''

        word = self.find(spelling)
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
        except (KeyError, IndexError) as e:
            print('コマンドの書式がおかしい')
            print(e)
        
        return tup
