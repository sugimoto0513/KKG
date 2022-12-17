#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
例題プログラム：この例題を改変して大きなプログラムを作る足がかりにしてください。
"""

__author__ = 'AOKI Atsushi'
__version__ = '1.0.3'
__date__ = '2022/11/28'

import os
import datetime


def main():
    """
    明治の板チョコもどきを出力するプログラムを作り出す例題のメイン（main）プログラムです。
    このプログラムによって作り出されたプログラム自身が、明治の板チョコの形になってます。(笑)
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """

    # バナーファイル（入力ファイル）とスクリプトファイル（出力ファイル）を求めておく。
    current_directory = os.getcwd()
    banner_file = current_directory + os.sep + 'MeijiChocolateBar.txt'
    script_file = current_directory + os.sep + 'MeijiChocolateBar.py'

    # バナーファイルを読み込んで、全行・シャープ数・行の長さの3つを求める。
    banner_lines, number_of_shapes, line_length = read_banner(banner_file)

    # バナーの全行を出力するためのPythonスクリプトの全行を求める。
    script_lines = convert_banner_to_python_script(banner_lines)

    # Pythonスクリプトの全行を、バナーのシャープ数に見合うように調整し、一行のPythonスクリプト文字列を作成する。
    one_line_string = make_one_line_string_of_python_script(
        script_lines, number_of_shapes, line_length)

    # バナーのシャープの部分を、一行のPythonスクリプト文字列の構成文字で順々に置き換え、Pythonスクリプトとしての体裁を整える。
    script_list = replace_shapes_in_banner_with_one_line_string_of_python_script(
        banner_lines, one_line_string)

    # 求まったPythonスクリプトの全行をスクリプトファイルに書き込む。
    write_lines(script_file, script_list)

    # 正常終了する。
    return 0


def read_banner(file_name):
    """
    file_nameで指定された旗印（banner：バナー）ファイルを読み込み、すべての行・シャープの数・行の長さの3つを応答します。
    """

    shape = '#'

    banner_lines = []
    number_of_shapes = 0
    line_length = 0
    with open(file_name, 'r', encoding='utf-8') as a_file:  # file_name を a_file として読み込む
        for script_count in a_file:  # 一行一行、順々に読み込む
            a_string = script_count.split()[0]  # 1行を改行コードを除いた上で束縛する
            banner_lines.append(a_string)  # a_string を banner_linesの要素として追加する
            number_of_shapes += len([x for x in a_string if x == shape])
            line_length = max(len(a_string), line_length)

    return banner_lines, number_of_shapes, line_length


def convert_banner_to_python_script(banner_lines):
    """
    banner_linesで指定されたバナーの全行をPythonスクリプトのリストに変換して応答します。
    """

    dot = '.'

    script_lines = ['a=".";', 'b="#";', 'p=print;']

    for script_count in banner_lines:
        count = 0  # '.' と '#' の数をカウントする変数
        code = 'p('

        # 行の最初の文字が'.' と '#' のどちらなのかを判断する
        if script_count[0] == dot:  # '.' のときは flag を 0 とする
            flag = 0
        elif script_count[0] != dot:  # '#' のときは flag を 1 とする
            flag = 1

        for a_string in script_count:
            if a_string == dot:  # 今見ている文字が '.' のとき
                if flag == 1:  # ひとつ前の文字が '#' だったとき
                    flag = 0  # 見る文字が変わったため、 flag を入れ替える
                    code += 'b*' + str(count) + '+'
                    count = 0  # 見る文字が変わったため、 count を初期化
                count += 1
            elif a_string != dot:  # 今見ている文字が '#' のとき
                if flag == 0:  # ひとつ前の文字が '.' だったとき
                    flag = 1  # 見る文字が変わったため、 flag を入れ替える
                    code += 'a*' + str(count) + '+'
                    count = 0  # 見る文字が変わったため、 count を初期化
                count += 1

        # 最後に現在見ている文字の追加を行う
        if flag == 0:
            code += 'a*' + str(count)
        elif flag == 1:
            code += 'b*' + str(count)

        code += ');'
        script_lines.append(code)  # 文字列を script_lines に要素として追加

    # print('\n'.join(script_lines))

    return script_lines


def make_one_line_string_of_python_script(script_lines, number_of_shapes, line_length):
    """
    Pythonスクリプトのリストを結合し、一行のPythonスクリプトの文字列を作り上げて応答します。
    バナーのシャープ数に見合うようにパディング文字列（詰め物：水増し）で長さの調整を行います。
    """

    one_line_string = "s='''"
    one_line_string += ''.join(script_lines)
    last_string = "''';exec(''.join(s.split()));"
    padding_string = 'p(end="");'

    # script_count には現在の文字数('#' の数をのぞく)を束縛
    script_count = len(one_line_string) + len(last_string) - number_of_shapes
    while script_count != line_length:  # 1行の長さ(80文字)になるまで padding_string を追加
        one_line_string += padding_string  # one_line_string に padding_string を追加
        # padding_string の文字数を script_count に追加
        script_count += len(padding_string)

    one_line_string += last_string  # 文字列の最後に last_string を追加

    # print(one_line_string)

    return one_line_string


def replace_shapes_in_banner_with_one_line_string_of_python_script(banner_lines, script_string):
    """
    banner_linesで指定されたバナーの全行のシャープの部分をPythonスクリプトの文字列で置き換えたリストにして応答します。
    バナーのシャープの部分を、一行のPythonスクリプトの構成文字で順々に置き換えますから、バナーの形をしたものなります。
    """

    shape = '#'
    space = ' '

    script_list = [
        '#! /usr/bin/env python',
        '# -*- coding: utf-8 -*-',
        '',
        '"""',
        '明治の板チョコもどきを出力するプログラムです。そのプログラム自身が板チョコ。(笑)',
        '"""',
        '',
        '__author__ = "' + __author__ + '"',
        '__version__ = "' + __version__ + '"',
        '__date__ = "' + __date__ + '"',
        '',
    ]

    i = 0  # カウンタ変数
    for a_line in banner_lines:  # 1行ずつ読み込む
        code = ""  # 1行ごとのスクリプトを束縛
        for a_string in a_line:  # 1文字ずつ読み込む
            if a_string == shape:  # 今見ている文字が  '#' のとき
                code += script_string[i]  # i 番目の文字を code に追加
                i += 1  # 次の文字を見るために i の値を 1 進める
            elif a_string != shape:  # 今見ている文字が '.' のとき
                code += space  # code にスペースを追加

        script_list.append(code)  # 完成した code を script_list に要素として追加

    # 余った部分を1行あけて、 script_list に追加
    script_list.append("")
    script_list.append(script_string[i:])
    script_list.append("")

    today = datetime.date.today().strftime("%Y年%m月%d日")
    now = datetime.datetime.now().strftime("%H時%M分%S秒")

    script_list.append(f'# このプログラムは{today}{now}にプログラムによって生成されました。')
    script_list.append('# このプログラムを生成するプログラムを作成してください。おきばりやしとくれやす！')
    script_list.append('')

    # print('\n'.join(script_list))

    return script_list


def write_lines(file_name, list_of_lines):
    """
    file_nameで指定されたファイルに、list_of_linesで指定されたリストの各要素（文字列）を、改行で結合して書き出します。
    file_nameがNoneの場合は、標準出力に書き出します。常にNoneを応答します。
    """

    code = '\n'.join(list_of_lines)  # 明治の板チョコ型のコードにするために要素ごとに '\n' で区切る
    if file_name is None:  # 出力先のファイルが指定されなかったとき
        print(code)  # ターミナルに出力
    else:  # 出力先のファイルが指定されたとき
        with open(file_name, 'w', encoding='utf-8') as a_file:  # 指定されたファイルを書き込み用で開き、中にコードを書き込む
            a_file.write(code)


if __name__ == '__main__':
    # 上記のifによって、このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。

    # 組み込みモジュールsysをインポートする。exit関数を用いるために。
    import sys

    # このモジュールのmain()を呼び出して結果を得て、Pythonシステムに終わりを告げる。
    sys.exit(main())
