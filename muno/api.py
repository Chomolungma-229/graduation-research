import functools
import MeCab
import markovify
import json
import sqlite3

from flask import Blueprint, jsonify

from muno.db import get_db, get_sentence

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/mimicry-sentence', methods=['GET'])
def random():
    msg = getMessage()
    result = {
        'context' : msg
    }
    json_string = json.dumps(result, ensure_ascii=False)
    return json_string

@bp.route('/mimicry-sentence/<string:username>', methods=['GET'])
def munouser(username):
    msg = getMessage(username)
    result = {
        'context' : msg
    }
    json_string = json.dumps(result, ensure_ascii=False)
    return json_string

@bp.route('/mimicry-sentence/<string:username>/abc', methods=['GET'])
def yunouser(username):
    return f"It's yuno sentence by {username}"

def getMessage(username = None):
    inputs = get_sentence(username)
    print(inputs)

    mecab = MeCab.Tagger()

    # 上手く解釈できない文字列を定義しておく
    breaking_chars = ['(', ')', '[', ']', '"', "'"]
    # 最終的に1文に収めるための変数
    splitted_meigen = ''

    for line in inputs:
        # lineの文字列をパースする
        parsed_nodes = mecab.parseToNode(line)

        while parsed_nodes:
            try:
                # 上手く解釈できない文字列は飛ばす
                if parsed_nodes.surface not in breaking_chars:
                    splitted_meigen += parsed_nodes.surface
                # 句読点以外であればスペースを付与して分かち書きをする
                if parsed_nodes.surface != '。' and parsed_nodes.surface != '、':
                    splitted_meigen += ' '
                # 句点が出てきたら文章の終わりと判断して改行を付与する
                if parsed_nodes.surface == '。':
                    splitted_meigen += '\n'
            except UnicodeDecodeError as error:
                print('Error : ', line)
            finally:
                # 次の形態素に上書きする。なければNoneが入る
                parsed_nodes = parsed_nodes.next

    print('解析結果 :\n', splitted_meigen)

    # マルコフ連鎖のモデルを作成
    model = markovify.NewlineText(splitted_meigen, state_size=2)
    # 文章を生成する
    sentence = model.make_sentence(tries=100)
    if sentence is not None:
        # 分かち書きされているのを結合して出力する
        return ''.join(sentence.split())

    else:
        return 'None'
