#!/usr/bin/env python3
"""Prepare only the learning site's public files, without publishing or changing the local viewer."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import argparse, hashlib, json, re, shutil, zipfile
ROOT=Path(__file__).resolve().parent.parent
APP=ROOT/'肩部3D学习'
p=argparse.ArgumentParser();p.add_argument('--site-url',default='');a=p.parse_args()
base=a.site_url.rstrip('/')+'/' if a.site_url else './'
if a.site_url and not re.fullmatch(r'https://[A-Za-z0-9.-]+(?::\d+)?(?:/[A-Za-z0-9_/-]*)?/?',a.site_url):
 raise SystemExit('site-url must be the verified HTTPS address of the deployed site')
OUT=ROOT/'website-release';DIST=OUT/'dist'
# A fresh release must not retain removed assets or pages from an earlier build.
if OUT.is_symlink() or DIST.is_symlink():
 raise SystemExit('Release output directories must not be symbolic links')
if DIST.exists():shutil.rmtree(DIST)
DIST.mkdir(parents=True,exist_ok=True)
# Explicit allowlist. Keep secrets, source voice staging, screenshots and other workspace files out.
files=['index.html','reading.html','reading-claude.html','calibration-evidence.json','geometry-validation.json','humerus-landmark-evidence.json','scapula-landmark-evidence.json']
for name in files:
 src=APP/'dist'/name
 if not src.is_file():raise SystemExit(f'Required build file is missing: {src}')
 shutil.copy2(src,DIST/name)
for name in ['assets','models','audio','licenses']:
 shutil.copytree(APP/'dist'/name,DIST/name,dirs_exist_ok=True)
for f in DIST.glob('*.html'):
 s=f.read_text();s=s.replace('http://127.0.0.1:5178/',base).replace('http://localhost:5178/',base)
 f.write_text(s)
# Portable article and figures for both people and tools that read text.
assets=ROOT/'2026-10-06-肩袖-阅读优化版-资源'
shutil.copytree(assets,DIST/'reading-assets',dirs_exist_ok=True)
md=(ROOT/'2026-10-06-肩袖-阅读优化版.md').read_text().replace('http://127.0.0.1:5178/',base).replace(assets.name+'/','reading-assets/')
(DIST/'reading.md').write_text(md)
(DIST/'downloads').mkdir(exist_ok=True)
pdf=ROOT/'output/pdf/肩袖-英中双语学习简报.pdf'
if not pdf.is_file():raise SystemExit(f'Reviewed PDF is missing: {pdf}')
shutil.copy2(pdf,DIST/'downloads/shoulder-bilingual.pdf')
# Update only embedded PDF URL annotations when a real public origin is known; do not redraw pages.
if a.site_url:
 from pypdf import PdfReader,PdfWriter
 from pypdf.generic import TextStringObject,NameObject
 writer=PdfWriter();writer.clone_document_from_reader(PdfReader(pdf))
 for page in writer.pages:
  for ref in page.get('/Annots',[]):
   action=ref.get_object().get('/A')
   if action:
    uri=str(action.get('/URI',''))
    for local_url in ('http://127.0.0.1:5178/','http://localhost:5178/'):
     if uri.startswith(local_url):
      action[NameObject('/URI')]=TextStringObject(uri.replace(local_url,base,1))
 with (DIST/'downloads/shoulder-bilingual.pdf').open('wb') as stream:writer.write(stream)
with zipfile.ZipFile(DIST/'downloads/shoulder-markdown.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('reading.md',md)
 for f in sorted((DIST/'reading-assets').glob('*.svg')):z.write(f,'reading-assets/'+f.name)
(DIST/'content').mkdir(exist_ok=True)
data={'title':'Shoulder study / 肩袖学习','muscles':json.loads((ROOT/'reading-source/data/muscles.json').read_text()),'model_links':json.loads((ROOT/'reading-source/data/model-links.json').read_text()),'humerus_landmarks':json.loads((APP/'src/humerus-landmarks.json').read_text()),'scapula_landmarks':json.loads((APP/'src/scapula-landmarks.json').read_text()),'scope':'Anatomical study references; not clinically calibrated acupoint or needling coordinates.'}
(DIST/'content/anatomy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(DIST/'llms.txt').write_text('''# Shoulder study / 肩袖学习\n\nEnglish-first bilingual shoulder anatomy learning materials.\n\n- Study hub: study.html\n- Full static reading page: reading.html\n- Claude reading edition: reading-claude.html\n- Plain Markdown article: reading.md\n- Anatomy and model mapping data: content/anatomy.json\n- PDF: downloads/shoulder-bilingual.pdf\n- 3D viewer: index.html?term=humerus\n- Model attribution: licenses/ATTRIBUTION.txt\n\nThe 3D view requires JavaScript and WebGL. Text retrieval does not rotate or inspect its geometry.\nPublic URLs provide read access only. They do not grant permission to edit source code or deploy.\nPersonal study progress is saved in the browser's localStorage and is not synchronized across devices.\n''')
css='''*{box-sizing:border-box}body{margin:0;background:#f7f4ec;color:#263d33;font:17px/1.75 system-ui,sans-serif}main{max-width:1000px;margin:0 auto;padding:64px 28px}small{display:block;color:#67756a;font-size:14px}h1{font-size:42px;line-height:1.2;margin:12px 0}h2{font-size:22px;margin:0}header p{max-width:700px}section{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:36px}a.card{display:block;padding:26px;border:1px solid #ccd4c9;border-radius:12px;background:#fffdf7;color:inherit;text-decoration:none}a.card:hover{border-color:#42695e;background:#edf3e9}a.card:focus-visible{outline:3px solid #9d772b}p{margin:10px 0}footer{margin-top:38px;font-size:13px;color:#647166}footer a{color:inherit}@media(max-width:620px){main{padding:35px 20px}h1{font-size:34px}section{grid-template-columns:1fr}}'''
cards=[('reading.html','Reading notes','双语阅读笔记','Anatomy, innervation, movement, clinical anatomy and research.','解剖、神经、动作、临床与论文阅读。'),('reading-claude.html','Claude reading edition','Claude 阅读版','Bilingual, English-only and self-test reading modes.','双语、纯英文与自测模式。'),('./?term=humerus','3D anatomy','三维解剖','Explore muscles, bones and anatomical landmarks.','旋转查看肌肉、骨骼与骨性标志。'),('downloads/shoulder-bilingual.pdf','PDF edition','PDF 完整版','Diagrams and complete bilingual answers for offline reading.','配图与完整双语答案，可下载、批注。'),('downloads/shoulder-markdown.zip','Markdown + diagrams','Markdown 与配图','An editable offline copy with its figures.','可编辑、可迁移的完整离线包。'),('reading.md','Plain-text article','纯文本阅读','The complete article in Markdown format.','便于复制、引用或交给 AI 阅读。')]
cardhtml=''.join(f'<a class="card" href="{url}"><h2>{en}</h2><small>{zh}</small><p>{desc}<small>{cn}</small></p></a>' for url,en,zh,desc,cn in cards)
(DIST/'study.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shoulder study · 肩袖学习</title><style>{css}</style><main><header><small>SHOULDER · ANATOMY &amp; ENGLISH</small><h1>Shoulder study</h1><small>肩袖学习 · 英文在前，中文随后</small><p>Learn the structures, follow their connections, and describe them in English.<small>从结构与连接关系出发，用完整英语描述解剖。</small></p></header><section>{cardhtml}</section><footer><p>Progress is saved on this browser. <span lang="zh">学习进度保存在当前浏览器。</span></p><a href="licenses/ATTRIBUTION.txt">Model attribution · 模型署名</a> · <a href="content/anatomy.json">Anatomy data · 解剖数据</a></footer></main></html>')
(DIST/'.nojekyll').write_text('')
# Catch broken downloads, model entry links, and relative HTML assets before upload.
class LocalLinks(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  self.urls.extend(value for key,value in attrs if key in ('href','src','poster') and value)
for page in DIST.glob('*.html'):
 parser=LocalLinks();parser.feed(page.read_text())
 for url in parser.urls:
  if a.site_url and url.startswith(base):url='./'+url[len(base):]
  parsed=urlsplit(url)
  if parsed.scheme or parsed.netloc or not parsed.path:continue
  if parsed.path.startswith('/'):
   raise SystemExit(f'Root-relative URL would break project Pages hosting: {page.name}: {url}')
  target=(page.parent/unquote(parsed.path)).resolve()
  if not target.is_relative_to(DIST.resolve()):
   raise SystemExit(f'Link escapes release directory: {page.name}: {url}')
  if not target.exists():raise SystemExit(f'Broken local link: {page.name}: {url}')
# Stable paths allow /?term= and /?point= to keep working on root or subpath hosting.
for path in DIST.rglob('*'):
 if path.is_file() and path.suffix in ('.html','.js','.json','.md','.txt'):
  s=path.read_text(errors='strict')
  if re.search(r'https?://(?:127\.0\.0\.1|localhost):5178',s):raise SystemExit(f'Unconverted local address: {path}')
manifest={'entry':'study.html','site_url':a.site_url or None,'files':[]}
for f in sorted(DIST.rglob('*')):
 if f.is_file():manifest['files'].append({'path':str(f.relative_to(DIST)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(OUT/'release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(OUT/'shoulder-website.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(DIST.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(DIST)))
print(json.dumps({'directory':str(DIST),'files':len(manifest['files']),'megabytes':round(sum(f['bytes'] for f in manifest['files'])/1e6,2),'localhost_links':0,'claude_edition_preserved':(DIST/'reading-claude.html').exists()},ensure_ascii=False))
