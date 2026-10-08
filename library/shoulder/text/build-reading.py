#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the standalone HTML, app reading page, and Markdown from reviewed sources."""
from pathlib import Path
from html.parser import HTMLParser
import html,json,re,shutil,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
TOPIC=HERE.parent
ASSETS=TOPIC/'figures'
APP=TOPIC/'3d'
BASE='http://127.0.0.1:5178/'
models=json.loads((HERE/'data/model-links.json').read_text())
terms={v['english'].lower():v['term'] for v in models.values()}
terms.update({'rotator cuff':'rotator-cuff','scapula':'scapula','clavicle':'clavicle','humerus':'humerus','humeral head':'humeral-head','greater tubercle':'greater-tubercle','lesser tubercle':'lesser-tubercle','scapular spine':'scapular-spine','inferior angle':'inferior-angle','acromion':'acromion','infraspinous fossa':'infraspinous-fossa','supraspinous fossa':'supraspinous-fossa','surgical neck':'surgical-neck','deltoid tuberosity':None})
pattern=re.compile(r'(?<![A-Za-z])(?:'+'|'.join(re.escape(k) for k in sorted(terms,key=len,reverse=True))+r')(?![A-Za-z])',re.I)

def term_link(match,markdown=False):
 label=match.group();term=terms[label.lower()]
 if term is None:return label
 url=BASE+'?term='+term
 if markdown:return f'[{label}]({url})'
 return f'<a class="anatomy-link" href="{url}" target="_blank" rel="noreferrer" title="Explore {label} in 3D · 在三维模型中查看">{label}</a>'

class Linker(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  self.parts.append(self.get_starttag_text())
  if tag in ('a','svg','script','style'):self.skip+=1
 def handle_startendtag(self,tag,attrs):self.parts.append(self.get_starttag_text())
 def handle_endtag(self,tag):
  self.parts.append(f'</{tag}>')
  if tag in ('a','svg','script','style'):self.skip-=1
 def handle_data(self,data):self.parts.append(data if self.skip else pattern.sub(term_link,data))
 def handle_entityref(self,name):self.parts.append('&'+name+';')
 def handle_charref(self,name):self.parts.append('&#'+name+';')
 def handle_comment(self,data):self.parts.append('<!--'+data+'-->')

def linked_html(s):
 parser=Linker();parser.feed(s);parser.close();assert parser.skip==0;return ''.join(parser.parts)

def linked_md(s):
 parts=re.split(r'(!?\[[^\]]*\]\([^)]*\)|<[^>]+>)',s)
 return ''.join(p if i%2 else pattern.sub(lambda m:term_link(m,True),p) for i,p in enumerate(parts))

assets={p.name[:2]:p for p in ASSETS.glob('*.svg')}
figure_ids=[]
def link_svg_label(match):
 raw=match.group(0)
 plain=html.unescape(re.sub(r'<[^>]+>','',raw)).strip()
 for name,term in sorted(terms.items(),key=lambda item:len(item[0]),reverse=True):
  if plain.lower().startswith(name) and (len(plain)==len(name) or not plain[len(name)].isascii() or not plain[len(name)].isalpha()):
   if term:return f'<a href="{BASE}?term={term}" target="_blank" aria-label="Explore {name} in 3D">{raw}</a>'
   break
 return raw

def embed(match):
 number=match.group(1);path=assets[number];s=path.read_text(encoding='utf-8');ET.fromstring(s)
 figure_ids.append(number)
 s=re.sub(r'<text\b[^>]*>.*?</text>',link_svg_label,s,flags=re.S)
 # Keep every figure's definitions local to its number and preserve exact artwork.
 return re.sub(r'<svg\b',f'<svg data-figure="{number}"',s,count=1)

chapters=[];md_chapters=[]
for number,name in [(1,'anatomy'),(2,'nerve'),(3,'motion'),(4,'clinical'),(5,'review'),(6,'reading')]:
 raw=(HERE/'sections'/f'{number:02d}-{name}.html').read_text(encoding='utf-8').replace('href="./?point=',f'href="{BASE}?point=')
 chapters.append(re.sub(r'\{\{FIGURE:(\d\d)\}\}',embed,linked_html(raw)))
 md_chapters.append(linked_md((HERE/'sections'/f'{number:02d}-{name}.md').read_text(encoding='utf-8')))
shell=(HERE/'templates/reading-shell.html').read_text(encoding='utf-8')
css=(HERE/'reading.css').read_text(encoding='utf-8')
page=shell.replace('{{CHAPTERS}}','\n'.join(chapters)).replace('</style>',css+'\n</style>')
assert '{{FIGURE:' not in page and '{{CHAPTERS}}' not in page
# Do not let a duplicated SVG filter/marker ID silently connect to a different figure.
ids=re.findall(r'\bid="([^"]+)"',page);assert len(ids)==len(set(ids)),[x for x in ids if ids.count(x)>1]
for name in ['anatomy','nerve','motion','clinical','review','reading']:assert f'id="{name}"' in page
vocab=(APP/'src/vocabulary.ts').read_text()
valid_terms=set(re.findall(r"id: '([a-z-]+)'",vocab))
for filename in ['humerus-landmarks.json','scapula-landmarks.json']:
 valid_terms.update(item['id'] for item in json.loads((APP/'src'/filename).read_text()))
for term in set(re.findall(r'\?term=([a-z-]+)',page)):assert term in valid_terms,term
for target in [HERE/'2026-10-06-肩袖-阅读优化版.html',APP/'public/reading.html']:
 target.write_text(page,encoding='utf-8')
md=(HERE/'templates/reading-prefix.md').read_text()+'\n\n'.join(md_chapters)+'\n'+(HERE/'templates/reading-footer.md').read_text()
for path in re.findall(r'!\[[^]]*\]\(([^)]+)\)',md):assert (HERE/path).exists(),path
(HERE/'2026-10-06-肩袖-阅读优化版.md').write_text(md,encoding='utf-8')
# The live static server serves dist. Vite build may run afterwards for app code changes.
(APP/'dist').mkdir(exist_ok=True)
shutil.copyfile(APP/'public/reading.html',APP/'dist/reading.html')
summary={'chapters':6,'figure_occurrences':len(figure_ids),'figures':figure_ids,'model_links':sorted(set(re.findall(r'\?term=([a-z-]+)',page))),'source':'library/shoulder/text/sections','html_and_markdown_built':True}
(HERE/'build-report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
