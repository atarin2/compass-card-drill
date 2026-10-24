"""ゲームのカード詳細画面のスクショからカード絵を切り抜き、ドリルに登録する。
使い方: python3 dev/add_cards.py list.txt
list.txt は1行に「画像ファイルのパス<TAB or 空白>カード名の一部」
  例: /path/to/IMG_0001.png 朝露
- カード名の一部で dev/compass-ct.html の CARDS を検索（1件に絞れる語にする）
- CARDS に無いカードは dev/all-cards-yagi.json から UR/SR を探して追加（使用率は0）
- 切り抜きは外枠の属性色（赤/青/緑）を検出。灰色枠（無属性）は画面比率で切り抜く
- cimg/<カード名のmd5先頭12桁>.jpg に保存し、PRESET に登録
終わったら python3 dev/build_site.py で index.html を作り直す。"""
import json,re,hashlib,sys,os,unicodedata
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=os.path.join(ROOT,'dev','compass-ct.html');s=open(P,encoding='utf-8').read()
m=re.search(r'const CARDS = \[\n(.*?)\n\]\.sort',s,re.S)
rows=[json.loads(l.rstrip(',')) for l in m.group(1).split('\n')];names=[r[0] for r in rows]
N=lambda x:unicodedata.normalize("NFKC",x).replace(" ","")
allc=[c for c in json.load(open(os.path.join(ROOT,'dev','all-cards-yagi.json'),encoding='utf-8')) if c[3] in("UR","SR") and c[6]!="-" and "キービジュアル" not in c[0]]
have={N(n) for n in names};extra=[c for c in allc if N(c[0]) not in have]
pm=re.search(r'const PRESET=(\{.*?\});\n',s,re.S);preset=json.loads(pm.group(1))
def frame(px):
    r,g,b=px;return (r>190 and g<60 and b<60) or (g>150 and r<90 and b<70) or (b>170 and r<60 and g<90)
for line in open(sys.argv[1],encoding='utf-8').read().strip().split('\n'):
    path,q=line.split(None,1)
    hits=[n for n in names if q in n]
    if not hits:
        ex=[c for c in extra if q in c[0]];assert len(ex)==1,(q,ex);rows.append(ex[0]+[0]);names.append(ex[0][0]);hits=[ex[0][0]]
    assert len(hits)==1,(q,hits);name=hits[0]
    im=Image.open(path).convert("RGB");W,H=im.size;sc=400/W
    sm=im.resize((400,round(H*sc)));px=sm.load();w,hh=sm.size
    pts=[(x,y) for y in range(hh) for x in range(w) if frame(px[x,y])]
    xs=[a for a,_ in pts];ys=[b for _,b in pts]
    if pts and max(xs)-min(xs)>w*.5 and max(ys)-min(ys)>hh*.45:
        bx,by,bw,bh=min(xs)/sc,min(ys)/sc,(max(xs)-min(xs))/sc,(max(ys)-min(ys))/sc
        box=(bx+bw*.0208,by+bh*.0807,bx+bw*.0208+bw*.9584,by+bh*.0807+bh*.8809)
    else: box=(W*.149,H*.179,W*.851,H*.85);print("枠が見つからないので画面比率で切り抜き:",name)
    c=im.crop(tuple(round(v) for v in box));c=c.resize((480,round(480*c.height/c.width)))
    fn='cimg/'+hashlib.md5(name.encode()).hexdigest()[:12]+'.jpg'
    c.save(os.path.join(ROOT,fn),'JPEG',quality=72,optimize=True,progressive=True);preset[name]=fn;print('登録:',name)
s=s[:pm.start(1)]+json.dumps(preset,ensure_ascii=False)+s[pm.end(1):]
m=re.search(r'const CARDS = \[\n(.*?)\n\]\.sort',s,re.S)
s=s[:m.start(1)]+'\n'.join(json.dumps(r,ensure_ascii=False)+',' for r in rows).rstrip(',')+s[m.end(1):]
open(P,'w',encoding='utf-8').write(s);print('画像付きカード:',len(preset))
