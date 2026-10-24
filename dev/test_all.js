// 公開前の動作チェック： NODE_PATH=$(npm root -g) node dev/test_all.js
const {chromium}=require('playwright');const path=require('path');
const URL='file://'+path.resolve(__dirname,'..','index.html');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));let ng=0;
const ok=(name,cond)=>{console.log((cond?'OK  ':'NG  ')+name);if(!cond)ng++};
await p.goto(URL);await p.waitForTimeout(600);
ok('ホーム表示',!!await p.$('#start'));
// 秒数クイズ：正解・不正解・スキップ
await p.click('#start');await p.waitForTimeout(200);
const ct=await p.evaluate(()=>exact(game.qs[game.i]));
for(const d of String(Math.round(ct)))await p.click(`[data-d="${d}"]`);
await p.click('[data-k="go"]');await p.waitForTimeout(100);
ok('正解判定',await p.$eval('.fb',e=>e.classList.contains('ok')));
await p.waitForTimeout(900);
ok('正解後に自動で次へ',(await p.textContent('.hud')).includes('第 2'));
await p.click('[data-d="1"]');await p.click('[data-k="go"]');await p.waitForTimeout(100);
ok('不正解判定',await p.$eval('.fb',e=>e.classList.contains('ng')));
await p.click('#next');await p.click('#skipBtn');
ok('スキップ',(await p.textContent('.hud')).includes('第 4'));
// 続きから
await p.click('#navBtn');await p.reload();await p.waitForTimeout(500);
ok('続きからボタン',(await p.textContent('#resumeBtn')||'').includes('第4問'));
await p.click('#resumeBtn');ok('続きから再開',(await p.textContent('.hud')).includes('第 4'));
for(let k=0;k<7;k++){await p.click('#skipBtn');await p.waitForTimeout(30)}
ok('結果画面',(await p.textContent('#view')).includes('正解（'));
await p.click('#back');ok('結果後は続きが消える',!await p.$('#resumeBtn'));
// ミュート
await p.click('#muteBtn');ok('ミュートON',(await p.textContent('#muteBtn')).includes('🔇'));
await p.click('#muteBtn');ok('ミュートOFF',(await p.textContent('#muteBtn')).includes('🔊'));
// キャラ短縮
await p.click('#heroBox summary');await p.click('[data-hero="archer"]');await p.waitForTimeout(100);
await p.click('#start');ok('キャラ短縮クイズ',(await p.textContent('.hud')).includes('アーチャー'));
ok('短縮後のCT計算',await p.evaluate(()=>{const c=game.qs[0];return Math.abs(exact(c)-Math.round(c.ct*.65*10)/10)<1e-9&&isOk(c,Math.floor(exact(c)+1e-9))}));
await p.click('#navBtn');
// カード名モード（キャラの影響を受けない）
await p.click('#flashBtn');await p.waitForTimeout(200);
ok('カード名モード',(await p.textContent('.hud')).includes('/ 30'));
await p.click('#fYes');await p.click('#fYes');await p.click('#fNo');await p.click('#fBack');
ok('カード名：表示・次へ・あとで・戻る',(await p.textContent('.hud')).startsWith('2 /'));
await p.click('#navBtn');await p.click('#resumeDel');
await p.click('[data-hero=""]').catch(async()=>{await p.click('#heroBox summary');await p.click('[data-hero=""]')});
// カード一覧
await p.click('#navBtn');await p.waitForTimeout(200);
ok('カード一覧',(await p.$$('.row')).length>50);
await p.click('#navBtn');
// 更新履歴
await p.click('#updBox summary');ok('更新履歴が開く',await p.$eval('#updBox',e=>e.open));
// データ
ok('全カードにCT・属性あり',await p.evaluate(()=>CARDS.every(c=>c.ct>0&&"火水木無".includes(c.el))));
ok('画像ファイルが全部ある',await p.evaluate(async()=>{for(const k in PRESET){const r=await new Promise(res=>{const i=new Image();i.onload=()=>res(1);i.onerror=()=>res(0);i.src=PRESET[k]});if(!r)return false}return true}));
ok('エラーなし',errs.length===0);if(errs.length)console.log(errs);
console.log(ng?`\n${ng}件の問題あり`:'\nすべてOK');await b.close();process.exit(ng?1:0)})();
