"""dev/compass-ct.html（claude.ai版の元ファイル）から、公開用の index.html を作る。
使い方（リポジトリの一番上で）: python3 dev/build_site.py
cimg/ fx/ bgm/ はリポジトリ直下のものをそのまま使う。"""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(os.path.join(ROOT,'dev','compass-ct.html'),encoding='utf-8').read()
s=s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','').replace('<title>カード秒数ドリル</title>\n','',1)
head='''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<title>カード秒数ドリル｜#コンパス CTドリル</title>
<meta property="og:title" content="カード秒数ドリル｜#コンパス CTドリル">
<meta property="og:description" content="#コンパスのカードのクールタイム（CT）とカード名を覚える非公式ドリル">
<meta property="og:type" content="website">
<meta property="og:url" content="https://atarin2.github.io/compass-card-drill/">
<meta property="og:image" content="https://atarin2.github.io/compass-card-drill/fx/icon-ct.png">
<meta name="twitter:card" content="summary">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="#コンパスのカードのクールタイム（CT）とカード名を覚える非公式ドリル">
<meta name="theme-color" content="#10142a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="CTドリル">
<link rel="apple-touch-icon" href="fx/icon-ct.png">
<link rel="icon" href="fx/icon-ct.png">
<style>*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}</style>
</head><body>
'''
open(os.path.join(ROOT,'index.html'),'w',encoding='utf-8').write(head+s+'\n</body></html>\n')
print('index.html を作成しました')
