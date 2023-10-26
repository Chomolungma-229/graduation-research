import functools
import MeCab
import markovify
import json
import sqlite3

from flask import Blueprint, jsonify

from muno.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/mimicry-sentence', methods=['GET'])
def random():
    msg = getMessage()
    test_j = {
        'context' : msg
    }
    json_string = json.dumps(test_j, ensure_ascii=False)
    return json_string

@bp.route('/mimicry-sentence/<string:username>', methods=['GET'])
def munouser(username):
    return f"It's muno sentence by {username}"

@bp.route('/mimicry-sentence/<string:username>/abc', methods=['GET'])
def yunouser(username):
    return f"It's yuno sentence by {username}"

def getMessage():
    # inputs = [
    #     "恥の多い生涯を送って来ました。",
    #     "自分には、人間の生活というものが、見当つかないのです。",
    #     "自分は東北の田舎に生れましたので、汽車をはじめて見たのは、よほど大きくなってからでした。",
    #     "自分は子供の頃から病弱で、よく寝込みましたが、寝ながら、敷布、枕のカヴァ、掛蒲団のカヴァを、つくづく、つまらない装飾だと思い、それが案外に実用品だった事を、二十歳ちかくになってわかって、人間のつましさに暗然とし、悲しい思いをしました。",
    #     "('自分は、空腹という事を知りませんでした。,')",
    #     "('自分だって、それは勿論、大いにものを食べますが、しかし、空腹感から、ものを食べた記憶は、ほとんどありません。',)",
    # ]
    inputs = getDb() 
    print(inputs)

    mecab = MeCab.Tagger()

    # 上手く解釈できない文字列を定義しておく
    breaking_chars = ['(', ')', '[', ']', '"', "'"]
    # 最終的に1文に収めるための変数
    splitted_meigen = ''

    for line in inputs:
        # lineの文字列をパースする
        parsed_nodes = mecab.parseToNode(line)
        print(parsed_nodes)

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
                print(splitted_meigen)
                parsed_nodes = parsed_nodes.next
    # マルコフ連鎖のモデルを作成
    model = markovify.NewlineText(splitted_meigen, state_size=2)
    # 文章を生成する
    sentence = model.make_sentence(tries=100)
    print(sentence)
    if sentence is not None:
        # 分かち書きされているのを結合して出力する
        return ''.join(sentence.split())

    else:
        return 'None'

def getDb():
    conn = sqlite3.connect('instance/muno.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT content FROM sentence')
    list = []
    for row in cur:
        list.append(str(row))
    cur.close()
    conn.close()
    return list