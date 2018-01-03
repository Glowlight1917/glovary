#coding: utf-8

import json
import copy
import shlex
import traceback

'''
controll

    ツリー構造を持つデータを保持・処理するクラス.
    データへの個別の操作はprocessで設定することができる.
    人工言語の辞書やウェブページ作成, 自己相似図形を作るときに使える.
'''

__author__ = 'glowlight.info'
__version__ = '1.0'

class controll:
    comData = {}
    comCont = {}

    def __init__(self, path=None):
        '''
        controllインスタンスを作成する.

        path: str
            セーブデータへのパス
        '''

        if path == None:
            self.data = self.template('template.json', 'dictionary')
        else:
            try:
                with open(path, 'r') as fp:
                    self.data = json.load(fp)
            except IOError as e:
                print('セーブデータが開けない')
                print(e)
        self.current = self.data
        self.pwd = '/'
        self.comHistory = []

    #////////////// Static Methods ///////////////

    @staticmethod
    def keysOfLists(cr):
        '''
        リストに対応するキーの一覧を取得する.

        cr: dict
            編集対象の辞書データ
        '''

        return filter(lambda key: isinstance(cr[key], list), cr.keys())

    @staticmethod
    def keysOfData(cr):
        '''
        リスト以外のデータに対応するキーの一覧を取得する.

        cr: dict
            編集対象の辞書データ
        '''

        return filter(lambda key: not isinstance(cr[key], list), cr.keys())

    @staticmethod
    def setValue(cr, key, text):
        '''
        entryが保持する辞書のデータを変更する.
        ただし, リストデータを変更することはできない.
        また, リストデータへと変更するこのもできない.

        cr: dict
            編集対象の辞書データ

        key: str
            変更するデータに関連するキー

        text: str, int, double
            変更先のデータ
        '''

        if key in controll.keysOfData(cr):
            cr[key] = text

    @staticmethod
    def addEntry(cr, key, template, key2):
        '''
        entryを新規作成する. 作成したものはcurrent変数に格納される.
        柵際したものは, 現在選択中のentryにしか追加できない.

        cr: dict
            編集対象の辞書データ

        key: string
            編集対象の辞書データのキーを指定

        template: string
            テンプレートファイルのパス

        key2: string
            テンプレートを指定するキー
        '''
        
        data = controll.template(template, key2) 
        cr[key].append(data)

    @staticmethod
    def swapEntry(cr, key, index, index2):
        '''
        指定の子entryリストの要素を交換する

        cr: dict
            編集対象の辞書データ

        key: str
            子entryリストを指定する

        index, index2: int
            交換する要素を指定する数字
        '''

        if key in controll.keysOfLists(cr):
            temp = cr[key][int(index)]
            cr[key][int(index)] = cr[key][int(index2)]
            cr[key][int(index)] = temp

    @staticmethod
    def removeEntry(cr, key, index):
        '''
        指定の子entryのある要素を取り除く

        cr: dict
            編集対象の辞書データ

        key: str
            子entryリストを指定する

        index: int
            取り除く要素を指定する数字
        '''

        if key in controll.keysOfLists(cr):
            cr[key].pop(int(index))
    
    @staticmethod
    def template(path, key):
        '''
        テンプレートとなる辞書データを生成する.
        データは深層コピーで生成される.

        return: dict
            テンプレートとなる辞書データ

        path: str
            テンプレート一覧ファイル(JSON)へのパス

        key: str
            一覧ファイルから, 生成する辞書データに対応する
            キーを指定する.
        '''
        
        try:
            with open(path, 'r') as tpf:
                temp = json.load(tpf)
        except IOError as e:
            print('テンプレートファイルが開けない')
            print(e)
        return copy.deepcopy(temp[key])

    #////////////// Static Methods ///////////////

    def find(self, cond):
        '''
        entryを検索する. 条件関数が真となるentryを抽出して
        そのIDとともにタプルにしてリストに保存する.
        
        出力: print
            (ID0, entry0)
            (ID1, entry1)
            (ID2, entry2)

        cond: function
            検索するentryの条件を指定する関数.
            この関数の返り値はBooleanである.
        '''

        entryList = []
        for index, dic in enumerate(self.data['entries']):
            if cond(dic):
                entryList.append((index, dic))

        for t in entryList:
            print(str(t[0]) + ': ' + str(t[1]['index']))
        
        return entryList

    def exac(self, path, comKey, args):
        '''
        指定のパスを辿った先のentryに対して操作を行う.
        操作は関数を渡すことで実行する.

        path: str
            entyrへのパスを指定する.

            例: entryへのパス
            --
            centents.1/examples.2
            -> [contents.1, examples.2]
            -> [(contents, 1), (examples, 2)]

        command: function
            processインスタンスに行う操作を関数として指定する.
            ラムダ式を使うと, 複数パラメータを持つ操作でも指定
            のインスタンスに適用することができる.
            f(n, m, ...) -> h(process)

        args: list
            command の引数となるリスト
        '''
        
        ref = self.getEntryWithPath(self.data, self.pwd, path)[0]
        if ref == None or not isinstance(ref, dict):
            return
        self.comData[comKey](ref, args)
    
    def changeCurrent(self, path):
        '''
        指定したパスからentryインスタンスを取得する.
        ただし, パスの指定先は辞書データである必要がある.
        そうでなければ何もしない.

        path: str (/aaa/1/bbb/3/ccc/0/, ../bbb/1, ./ccc/5)
            パスを指定する. Unixのようにパスを書ける.
        '''

        temp = controll.getEntryWithPath(self.data, self.pwd, path)
        if temp == None or not isinstance(temp[0], dict):
            return
        else:
            self.current = temp[0]
            self.pwd = temp[1]

    @staticmethod
    def getAbsPath(ab, path):
        '''
        現在の絶対パスと移動先のパスを合わせて, 新たに絶対パスを作成する.

        return: str
            生成たれた絶対パス. 生成された絶対パスの最後尾には/が付かない.

        ab: str
            現在の絶対パス

        path: str
            移動先のパス. もしこれが/から始まれば, pathが次の絶対パスになる.
        '''

        if path[0] == '/':
            return path

        index = 0
        v = ab.split('/') + path.split('/')
        while index < len(v):
            if len(v) == 0:
                break
            if v[index] == '.':
                v.pop(index)
                continue
            if v[index] == '..':
                v.pop(index)
                index -= 1
                v.pop(index)
                continue
            if v[index] == '':
                v.pop(index)
                continue
            index += 1

        return '/'+'/'.join(v)

    @staticmethod
    def getEntryWithPath(rootEntry, ab, path):
        '''
        rootEntyを開始としたパスを辿ってデータを取得する.
        子entryは親entryのリストデータに保持されている.

        return; (entry, str)
            パス指定先のentryと最終的な絶対パスの2つによるタプル

        rootEntry: dict
            ルートとなる辞書データ.

        ab: str
            current辞書データの絶対パス. これは/で始まる.

            / : ルート
            /entries/10 : ルートが保持する子entryリストの10番目

        path: str
            移動先のデータのパス. linuxと同じように記述することが
            できる.

            ./ : 現在地のパス
            ../ : 1つ前のデータへのパス
            ../../ :  2つ前のデータへのパス
        '''
        
        try:
            temp = rootEntry
            pathAbs = controll.getAbsPath(ab, path)
            pathList = pathAbs[1:].split('/')

            if pathList == ['']: #絶対パスがルートのとき
                return (temp, pathAbs) 

            for now in pathList:
                if isinstance(temp, list):
                    temp = temp[int(now)]
                else:
                    temp = temp[now]
        except (KeyError, IndexError, UnboundLocalError) as e:
            print('パスの書式がおかしい', e.args)
            return

        return (temp, pathAbs) 

    def showHistory(self):
        '''
        コマンド実行履歴の表示する.

        出力: print
            実行したコマンドの一覧 
        '''

        for h in self.comHistory:
            print(h)

    def addHistory(self, command):
        '''
        実行したコマンドを履歴に保存する. このメソッドは自動的に
        実行される. なので明示的に実行する必要はない.

        command: string
            実行したコマンドの文字列
        '''

        self.comHistory.append(command)

    def save(self, path):
        '''
        rootEntryをJSONファイルとして保存する.

        出力: file
            dataの内容をJSONファイルに出力

        data: dict
            JSONファイルに保存する辞書データ.

        path: string
            保存先のパスを指定する.
        '''

        try:
            with open(path, 'w') as jsf:
                json.dump(self.data, jsf, indent=4, ensure_ascii=False)
        except IOError as e:
            print('スクリプトファイルが開けない')
            print(e)

    def readScript(self, path):
        '''
        スクリプトファイルを読み込んでコマンドを実行する.
        スクリプトはコマンドを一行ずつならべて記述する.
        コマンドの書き方はcommandメソッド参照.

        path: string
            スクリプトファイルのパス 
        '''
        try:
            with open(path, 'r') as sc:
                for com in sc.read().split('\n'):
                    if com == '': continue
                    print(com)
                    self.command(com)
        except IOError as e:
            print('スクリプトファイルが開けない')
            print(e)

    def command(self, command):
        '''
        command: com path arg1 arg2 ...
            -> com path [arg1, arg2, ... ]

        commandの文字列をスペースで分割する. ただし''ではひとまとめで
        数える. このcontrollクラスの継承先で, 下のif文を追加することで
        新たなコマンドを実装することが出来る.

        コマンドメソッドの実装例:
            ====================
            def command(self, command):
                #コマンドをスペースで分割
                tup = shlex.split(command) 
                
                #コマンド名
                com = tup[0]
                
                #引数のリスト
                args = tup[1:]

                #コマンドを履歴に保存
                self.addHistory(command)

                try:
                    #引数が3つ以上のとき
                    if len(tup) >= 3: 
                        ref = self.getEntryWithPath(self.data, self.pwd, args[0])[0]
                        if com == 'add': self.addEntry(ref, args[1], 'template.json', args[2])

                    #引数が2つのとき
                    if len(tup) == 2:
                        if com == 'save': self.save(args[0])

                    #引数が1つのとき
                    if len(tup) == 1:
                        if com == 'hs': self.showHistory()

                except (KeyError, IndexError) as e:
                    print('コマンドの書式がおかしい')
                    print(e)

                return tup
            ====================

        継承先での実装例:
            ====================
            def command(self, command):
                tup = super.command(command)
                com = tup[0]
                args = tup[1:]

                try:
                    if len(tup) == 2:
                        if com == 'lu': self.lookup(args[0])
                except (KeyError, IndexError) as e:
                    print('コマンドの書式がおかしい')
                print(e)
            ====================

        return; tupple
            コマンド文字列から生成したタプルを返す. この返却タプルは継承クラスのcommandメソッド
            で利用される.
        '''

        tup = shlex.split(command)
        com = tup[0]
        args = tup[1:]
        
        self.addHistory(command)
        try:
            if len(tup) >= 3: 
                ref = self.getEntryWithPath(self.data, self.pwd, args[0])[0]
                if com == 'add': self.addEntry(ref, args[1], 'template.json', args[2])
                if com == 'rm': self.removeEntry(ref, args[1], args[2])
                if com == 'ed': self.setValue(ref, args[1], args[2])
                if com == 'swap': self.swapEntry(ref, args[1], args[2], args[3])

            if len(tup) == 2:
                if com == 'save': self.save(args[0])
                if com == 'script': self.readScript(args[0])
                if com == 'cd': self.changeCurrent(args[0])

            if len(tup) == 1:
                if com == 'hs': self.showHistory()
                if com == 'exit': system.exit(0)
                if com == 'cccp': print('\033[33;41;1m *             \033[0m\n\033[33;41m ☭             \033[0m\n\033[33;41m               \033[0m\n\033[33;41m               \033[0m')
                if com == 'russia': print('\033[33;47m         \033[0m\n\033[33;44m         \033[0m\n\033[33;41m         \033[0m')

        except (KeyError, IndexError) as e:
            print('コマンドの書式がおかしい')
            print(e)

        return tup
