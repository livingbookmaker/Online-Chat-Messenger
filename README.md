## 本リポジトリについて

本リポジトリは、Recursionのバックエンドプロジェクト2の課題「Online Chat Messenger」のプログラムを作成するためのものです。

## 現状

ひとまずステージ1の要件を満たすプログラムを作成しました（本当に満たせているかはわかりませんが）。

## ステージ1のプログラムの流れ

1. ターミナルを3つ立ち上げて、そのうちの1つでserver.pyを、残り2つでclient.pyを起動する。
2. client.pyを起動したターミナルでユーザーネームを入力する。
3. server.pyがユーザーネームを受け取り、ユーザーがチャットに参加したことを各クライアントに伝える。
4. client.pyを起動したターミナルでメッセージを入力すると、サーバーを通じて各クライアントにメッセージが送信される。
5. client.pyを起動したターミナルで何も入力せずに60秒が経過するか、「q」と入力すると、server.pyにチャットを終了することを伝えるメッセージを送信し、client.pyを終了する。
6. server.pyがclient.pyからの終了メッセージを受け取り、そのクライアントのユーザーが退出したことを各クライアントに伝える。

## 参考にした記事

本リポジトリのプログラムは、以下の記事や公開リポジトリを参考にしています。

https://qiita.com/mashed_potatoes/items/2338852a41c6aaf8efbb

https://github.com/ayan2809/Multi-Client-Socket-using-UDP

https://ittrip.xyz/python/python-udp-socket-guide

https://daeudaeu.com/tkinter_after/#after_cancel_after
