アプリケーションから実行する方法
アプリケーションはbuild/main.exeを実行することでPython無しでも実行できると思います。
ただし、動作できるのはWindowsのみです。

ソースコードから実行する方法

必須
python 3.6～
推奨
anaconda,virtualenvなどの仮想環境
IDE(Pycharm,visual studio codeなど)
非推奨
python本体でのインストール

仮想環境
仮想環境から起動する場合、事前に仮想環境を構築してください
1.仮想環境の構築
2.仮想環境が有効になった状態で以下のコマンドを入力してください
pip install pygame
再度、入力が可能になるまでしばらくお待ちください。
3.完了

python本体でのインストール
1.以下のコマンドを入力してください
pip install pygame
再度、入力が可能になるまでしばらくお待ちください。
2.完了

起動方法
main.pyを実行することでゲームが始まります。
ただし、仮想環境やコマンドで起動したい場合は以下の手順で行ってください

1.(仮想環境経由の場合)ターミナルを起動
  pygameをインストールした仮想環境を有効にしてください
2.main.pyがあるディレクトリまで移動してください
3.コマンドを入力する
  python main.py
