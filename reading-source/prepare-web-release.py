#!/usr/bin/env python3
"""Prepare only the learning site's public files, without publishing or changing the local viewer."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import argparse, hashlib, json, os, re, shutil, zipfile
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
files=['study.html','topics.json','topic.css','index.html','reading.html','reading-claude.html','calibration-evidence.json','geometry-validation.json','humerus-landmark-evidence.json','scapula-landmark-evidence.json']
for name in files:
 src=APP/'dist'/name
 if not src.is_file():raise SystemExit(f'Required build file is missing: {src}')
 shutil.copy2(src,DIST/name)
for name in ['assets','models','audio','licenses','topics']:
 shutil.copytree(APP/'dist'/name,DIST/name,dirs_exist_ok=True)
for f in DIST.rglob('*.html'):
 page_base=base if a.site_url else os.path.relpath(DIST,f.parent)+'/'
 s=f.read_text();s=s.replace('http://127.0.0.1:5178/',page_base).replace('http://localhost:5178/',page_base)
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
catalog=json.loads((DIST/'topics.json').read_text())
# Downloaded topic Markdown keeps its figure paths, while 3D links use the live site.
if a.site_url:
 for topic in catalog['topics']:
  markdown=DIST/'topics'/topic['id']/'reading.md'
  if topic['adapter']=='standard' and topic['status']=='published':
   markdown.write_text(markdown.read_text().replace('](../../?',']('+base+'?'))
llm_lines=['# Anatomy study / 解剖学习', '', 'English-first bilingual anatomy learning, organized by topic.', '', '- Topic library: study.html', '- Topic registry: topics.json', '- Model attribution: licenses/ATTRIBUTION.txt', '']
for topic in catalog['topics']:
 llm_lines.append(f"- {topic['title']['en']} / {topic['title']['zh']} ({topic['status']}): topics/{topic['id']}/index.html")
llm_lines += ['', 'Shoulder legacy links remain available: reading.html, reading-claude.html, reading.md and downloads/shoulder-bilingual.pdf.', 'Draft topics are unfinished learning materials. Model previews do not establish reviewed anatomical descriptions or clinical coordinates.', 'The 3D view requires JavaScript and WebGL. Text retrieval does not inspect its geometry.', 'Public URLs provide read access. Source changes require authenticated repository access.', 'Learning progress is saved in this browser, not synchronized across devices.']
(DIST/'llms.txt').write_text('\n'.join(llm_lines)+'\n')
(DIST/'.nojekyll').write_text('')
# Catch broken downloads, model entry links, and relative HTML assets before upload.
class LocalLinks(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  self.urls.extend(value for key,value in attrs if key in ('href','src','poster') and value)
for page in DIST.rglob('*.html'):
 parser=LocalLinks();parser.feed(page.read_text())
 for url in parser.urls:
  if a.site_url and url.startswith(base):
   # Absolute links refer to the site root, even from nested topic pages.
   url=os.path.relpath(DIST, page.parent)+'/'+url[len(base):]
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
manifest={'entry':'study.html','site_url':a.site_url or None,'topics':[{'id':t['id'],'status':t['status']} for t in catalog['topics']],'files':[]}
for f in sorted(DIST.rglob('*')):
 if f.is_file():manifest['files'].append({'path':str(f.relative_to(DIST)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(OUT/'release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(OUT/'anatomy-website.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(DIST.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(DIST)))
print(json.dumps({'directory':str(DIST),'files':len(manifest['files']),'megabytes':round(sum(f['bytes'] for f in manifest['files'])/1e6,2),'localhost_links':0,'claude_edition_preserved':(DIST/'reading-claude.html').exists()},ensure_ascii=False))
