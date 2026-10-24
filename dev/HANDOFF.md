# カード秒数ドリル 作業メモ（引き継ぎ用）

#コンパス【戦闘摂理解析システム】のカードCTとカード名を覚える非公式ドリル。作者：あたりん（X @atr_d4c）。

## 公開場所
- 公開サイト：https://atarin2.github.io/compass-card-drill/ （GitHub Pages、main ブランチの直下を配信）
- 作者用ページ（claude.ai）：https://claude.ai/artifact/XSYvQXSJ5ysnwY56ZpU9Qz
  - 更新するときは Artifact の publish に必ず url（上のURL）を付けること。付けないと別ページが新しくできてしまう
  - 同じ内容に加え、短縮名・チェック・削除・「あとで」を claude.ai アカウントで端末間同期する（db/user 機能）
- アクセス解析：GoatCounter（https://atarin2.goatcounter.com）。github.io で開いたときだけ数える

## ファイル構成
- `dev/compass-ct.html` … **元ファイル（ここを編集する）**。claude.ai 版はこれをそのまま公開
- `index.html` … 公開用。`python3 dev/build_site.py` で元ファイルから作る（head の title/OGP を足すだけ）
- `cimg/` … カード画像（480px JPEG、ファイル名はカード名の md5 先頭12桁）
- `fx/` … 背景で落ちるアイテム（coin/pad/mark/can/bat.png）とアイコン（icon-ct.png）
- `bgm/dive.mp3` … デフォルトBGM「Dive」（作者からもらったフリーBGM。クレジット要否は未確認）
- `dev/add_cards.py` … スクショからカード絵を切り抜いて登録する
- `dev/all-cards-yagi.json` … やぎシミュの全カードデータ（2026/9/28版）。カード追加時の元データ

## 元ファイル内の主なデータ
- `CARDS` … [名前, CT秒, 発動, レア, 属性, タイプ, 効果, 大会使用率%]。UR全部＋画像のあるSRだけ
  - タイプのカウンターは「返」に統一。属性は表示時に 火→赤 水→青 木→緑
- `PRESET` … カード名 → 画像パス
- `DEFAULT_DEL` … 初めて開いた人で最初から「削除」になっているカード（画像なし中心の29枚）
- `AUTHOR_NICK` … 一括ボタンで入る作者の短縮名。作者の最新の短縮名は claude.ai 版の db
  （data/users/me/prefs の nick）から読める
- `HEROES` … キャラモード（CT短縮）。倍率は CT×m。整数モードは切り捨て・切り上げどちらも正解
- データ最終更新の表示は `<div class="upd">` を書き換える

## 利用者のデータ（サーバーなし）
- localStorage（キー接頭辞 `cdrill:`）… 設定・短縮名(nick)・チェック(excl)・削除(del)・あとで(mada)・苦手(miss, カード名キー)・ベスト記録
- IndexedDB `cdrill` / store `img` … 自分で登録した画像、`__bgm__` に自分の音源
- **カード名を変えるとその カードの利用者データは引き継がれない**ので、名前の変更は慎重に

## データの確認
- 2026/10/25 にコンパス攻略Wiki（gamerch）と全カード照合済み。やぎシミュの誤り
  （超大型巨人・ミリア 14→20秒、ケルマト 26→32秒）を修正済み。アペプはWikiに無く未確認

## 更新の手順
1. `dev/compass-ct.html` を編集（カード追加は `dev/add_cards.py`）
2. `python3 dev/build_site.py`
3. claude.ai 版も同じ `dev/compass-ct.html` で公開し直す
4. commit して push（反映まで1〜2分）

## 更新履歴の書き方
- compass-ct.html の `const UPDATES=[...]` の先頭に ["YYYY/MM/DD",["内容",...]] を追加する（同じ日なら既存の配列に追記）。最終更新日は先頭の日付が自動で表示される

## 反映の進め方（2026/10/25 本人と決めたこと）
- 修正のたびに作者用ページ（claude.ai）だけ更新して本人に試してもらう
- 公開サイト（GitHub）へはある程度たまってから、または本人が「公開して」と言ったときにまとめて反映する
- 公開サイトに反映する前に必ず `NODE_PATH=$(npm root -g) node dev/test_all.js` で全体の動作チェックを通す（機能を増やしたらテストも足す）
