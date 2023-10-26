# graduation-research

## PSのvenv実行コマンド

 `PowerShell -ExecutionPolicy RemoteSigned`
 `{venvname}/Scripts/activate`

## PSのvenv終了

  `deactivate`

- 仮想環境時は、カレントが仮想環境内にあることになる。

## DBの初期化

- DBに対するSQLは全部小文字じゃないとダメ。

  `flask --app muno init-db`

## 別PCでの作業環境構築

　`py -3 -m venv venv`
　`pip install -r require.txt`
  `flask --app muno init-db`
