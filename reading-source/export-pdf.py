"""Export the complete shoulder reading page to a paginated bilingual PDF.
Run with the bundled Python runtime (reportlab, lxml, Pillow).
Diagram PNGs are rendered from SVG into tmp/pdfs/shoulder-export beforehand.
"""
from pathlib import Path
import re, json, html as esc
from lxml import html
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, NextPageTemplate, Image, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
TMP=ROOT/'tmp/pdfs/shoulder-export'
OUT=BASE/'output/pdf/肩袖-英中双语学习简报.pdf'
INK=colors.HexColor('#243B33'); GREEN=colors.HexColor('#42695E'); GRAY=colors.HexColor('#626A64'); LINE=colors.HexColor('#D8DDD5')
pdfmetrics.registerFont(TTFont('ArialUnicode','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('ArialRegular','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('ArialUnicode',normal='ArialUnicode',bold='ArialUnicode',italic='ArialUnicode',boldItalic='ArialUnicode')
styles={}
for name,size,lead,col,before,after in [('body',10.5,16.4,INK,0,7),('zh',9.7,16,GRAY,0,10),('h1',25,33,GREEN,0,19),('h2',19,26,GREEN,0,18),('h3',13.8,21,GREEN,14,10),('h4',11.6,18,GREEN,10,7),('small',8.4,13,GRAY,0,8),('cell',8.4,12.4,INK,0,0),('cellhead',8.6,13,GREEN,0,0),('caption',9.5,15,GRAY,10,0)]:
 styles[name]=ParagraphStyle(name,fontName='ArialUnicode',fontSize=size,leading=lead,textColor=col,spaceBefore=before,spaceAfter=after,wordWrap='CJK',allowWidows=0,allowOrphans=0,keepWithNext=name.startswith('h'))

root=html.fromstring((BASE/'2026-10-06-肩袖-阅读优化版.html').read_text())
story=[]; inventory={'figures':[],'tables':0,'questions':0,'chapters':[]}; outlines=[]; consumed=set()

def norm(s):
 return re.sub(r'\s+',' ',s or '').strip().replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
def text(e):return norm(''.join(e.itertext()))
def plain(e):return esc.escape(text(e))
def markup(e):
 if not isinstance(e.tag,str):return ''
 if e.tag in ('script','style','svg'):return ''
 out=esc.escape(norm(e.text)) if e.text else ''
 for c in e:
  tag=c.tag
  if not isinstance(tag,str):continue
  inner=markup(c)
  if tag=='br':s='<br/>'
  elif tag in ('b','strong'):s='<b>'+inner+'</b>'
  elif tag in ('em','i'):s='<i>'+inner+'</i>'
  elif tag=='a' and c.get('href','').startswith(('http://','https://')):
   s='<link href="'+esc.escape(c.get('href'),quote=True)+'" color="#42695E">'+inner+'</link>'
  elif tag in ('span','small') and ('translation' in c.get('class','') or tag=='small'):
   s='<br/><font size="9.5" color="#626A64">'+inner+'</font>'
  else:s=inner
  # Keep spaces around inline nodes; don't concatenate ordinary English words.
  if out and e.text and len(e)==1:pass
  if c.getprevious() is None and e.text and e.text[-1:].isspace():out+=' '
  out+=s
  if c.tail:
   tail=norm(c.tail)
   out+=(' ' if c.tail[:1].isspace() else '')+esc.escape(tail)+(' ' if c.tail[-1:].isspace() else '')
 return out.strip()
def para(e,kind='body'):
 return Paragraph(markup(e),styles[kind])
def ptxt(s,kind='body'):return Paragraph(s,styles[kind])
def newpage(template='portrait'):
 if story and not isinstance(story[-1],PageBreak):
  story.extend([NextPageTemplate(template),PageBreak()])
 elif story:
  story.insert(len(story)-1,NextPageTemplate(template))
def chinese(e):return e.get('lang','').startswith('zh') or 'translation' in e.get('class','')
def heading(e,kind='h3'):
 p=Paragraph(markup(e).replace('展开：',''),styles[kind]);p._heading=text(e);return p

def image_for(num,maxw,maxh):
 path=TMP/(num+'.png')
 with PILImage.open(path) as im:w,h=im.size
 s=min(maxw/w,maxh/h)
 return Image(str(path),width=w*s,height=h*s)

def figure(e):
 svg=e.xpath('.//svg')[0];num=svg.get('data-figure')
 inventory['figures'].append(num)
 vb=[float(x) for x in svg.get('viewbox').split()];ratio=vb[2]/vb[3]
 template='plate-wide' if ratio>=1.15 and num not in ('16','17') else 'plate-tall'
 ps=landscape(A3) if template=='plate-wide' else A3
 w,h=ps[0]-92,ps[1]-106
 tail=[]
 following=list(e.itersiblings())
 if num=='13':following=list(e.getparent().itersiblings())
 if num in ('08','13','16','17'):
  for sib in following:
   cl=sib.get('class','')
   if sib.tag=='p':
    tail.append(para(sib,'small' if 'source' in cl else 'zh' if chinese(sib) else 'body'));consumed.add(sib)
   elif 'bilingual-pair' in cl:
    tail.extend(para(c,'zh' if chinese(c) else 'body') for c in sib if c.tag=='p');consumed.add(sib)
   else:break
 caption=e.xpath('./figcaption')
 cap=para(caption[0],'caption') if caption else None
 pending=None
 if story and isinstance(story[-1],Paragraph) and hasattr(story[-1],'_heading'):
  pending=story.pop()
 newpage(template)
 title=svg.xpath('./title')
 titletext=(pending.getPlainText() if pending else (text(title[0]) if title else next((p.stem[3:] for p in (BASE/'2026-10-06-肩袖-阅读优化版-资源').glob(num+'-*.svg')), 'Anatomical illustration · 解剖示意图')))
 # SVG titles may be long; use their first English/Chinese pair as a clean plate heading.
 label=ptxt('FIGURE '+num+' · '+esc.escape(titletext),'h3')
 label.style=ParagraphStyle('plate-title',parent=styles['h3'],spaceBefore=0)
 story.append(label)
 titleh=label.wrap(w,h)[1]
 caph=cap.wrap(w,h)[1]+14 if cap else 0
 tailh=sum(x.wrap(w,h)[1]+x.getSpaceBefore()+x.getSpaceAfter() for x in tail)
 pic=image_for(num,w,h-titleh-caph-tailh-26)
 story.append(pic)
 if cap:story.append(cap)
 if tail:story.extend([Spacer(1,12),*tail])
 newpage('portrait')

def table(e):
 inventory['tables']+=1
 rows=e.xpath('./thead/tr|./tbody/tr|./tr')
 data=[]
 for i,row in enumerate(rows):
  data.append([para(c,'cellhead' if i==0 else 'cell') for c in row if c.tag in ('td','th')])
 n=max(map(len,data));width=A4[0]-92
 ratios={2:[.33,.67],3:[.30,.34,.36],4:[.19,.30,.26,.25],5:[.15,.25,.23,.19,.18]}.get(n,[1/n]*n)
 if n==3 and 'SPADI' in text(e):ratios=[.49,.21,.30]
 t=Table(data,colWidths=[width*x for x in ratios],repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF0E9')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F6F0')]),('LINEBELOW',(0,0),(-1,-1),.4,LINE)]))
 story.extend([Spacer(1,7),t,Spacer(1,13)])

def muscle(e):
 num=e.xpath('.//svg')[0].get('data-figure')
 if num!='02':newpage()
 title=e.xpath('.//h4')[0]
 zh=e.xpath('.//small')[0]
 story.append(ptxt(markup(title)+'<br/><font size="12" color="#626A64">'+plain(zh)+'</font>','h2'))
 svg=e.xpath('.//svg')[0];num=svg.get('data-figure');inventory['figures'].append(num)
 story.extend([image_for(num,230,250),Spacer(1,12)])
 dl=e.xpath('./dl')[0]
 for dt in dl.xpath('./dt'):
  dd=dt.getnext(); story.append(ptxt('<b>'+markup(dt)+'</b><br/>'+markup(dd),'body'))
 for child in e:
  if 'bilingual-pair' in child.get('class','') or child.tag=='p':walk(child)

def walk(e):
 if not isinstance(e.tag,str) or e in consumed:return
 tag=e.tag;cl=e.get('class','')
 if tag in ('script','style','svg') or 'bridge' in cl:return
 if tag=='figure':figure(e);return
 if 'muscle-card' in cl:muscle(e);return
 if tag=='table':table(e);return
 if tag in ('h3','h4'):
  if text(e).startswith('Describing a muscle'):newpage()
  story.append(heading(e,tag));return
 if tag=='p':
  if text(e):story.append(para(e,'zh' if chinese(e) else 'small' if 'source' in cl or 'model-link-row' in cl else 'body'))
  return
 if 'bilingual-pair' in cl:
  items=[para(c,'zh' if chinese(c) else 'body') for c in e if c.tag=='p']
  if items:story.append(KeepTogether(items));return
 if tag=='details':
  if 'quiz' in cl:
   inventory['questions']+=1
   s=e.xpath('./summary')[0];q=s.xpath('.//*[contains(@class,"question-pair")]')[0]
   qs=[]
   for c in q:qs.append(para(c,'zh' if chinese(c) else 'h4'))
   answers=[]
   for c in e:
    if c.tag!='summary':
     for pp in c.xpath('.//p') if c.tag!='p' else [c]:answers.append(para(pp,'zh' if chinese(pp) else 'body'))
   story.append(KeepTogether(qs+answers));return
  else:
   s=e.xpath('./summary')[0];story.append(heading(s,'h3'))
  for c in e:
   if c.tag!='summary':walk(c)
  return
 if tag in ('ul','ol'):
  for i,li in enumerate(e,1):
   # Preserve nested paragraphs, including palpation instructions.
   hasp=li.xpath('./p')
   if hasp:
    if li.text and li.text.strip():story.append(ptxt(esc.escape(li.text),'body'))
    for c in li:walk(c)
   else:story.append(ptxt(('• ' if tag=='ul' else str(i)+'. ')+markup(li),'body'))
  return
 if tag=='header' and 'chapter-head' in cl:return
 if tag in ('div','article','section'):
  if not any(c.tag in ('div','p','h3','h4','article','section','figure','table','ul','ol','details','dl','header') for c in e) and text(e):
   story.append(para(e,'small' if 'paper-meta' in cl else 'body'));return
  # Preserve stage angles and compressed mnemonics before nested paragraphs.
  for c in e:
   if c.tag in ('strong','b','span') and text(c):story.append(para(c,'h4'))
   else:walk(c)
  return
 if tag=='a' and text(e):story.append(para(e,'small'));return
 if tag in ('span','small','strong','b','li','dt','dd') and text(e):story.append(para(e,'body'))

class Book(BaseDocTemplate):
 def afterFlowable(self,f):
  if getattr(f,'chapter_key',None):
   self.canv.bookmarkPage(f.chapter_key)
   self.canv.addOutlineEntry(f.chapter_title,f.chapter_key,0,False)
   outlines.append({'title':f.chapter_title,'page':self.page})

def page_frame(c,doc):
 w,h=c._pagesize;c.saveState();c.setStrokeColor(LINE);c.setLineWidth(.45)
 c.line(42,h-29,w-42,h-29);c.line(42,32,w-42,32)
 c.setFont('ArialUnicode',8);c.setFillColor(GRAY)
 c.drawString(43,h-22,'ROTATOR CUFF  /  肩袖英中双语学习')
 c.drawString(43,20,'2026-10-06  ·  English first / 中文随后')
 c.drawRightString(w-43,20,str(doc.page));c.restoreState()

templates=[]
for name,size in [('portrait',A4),('plate-wide',landscape(A3)),('plate-tall',A3)]:
 w,h=size;frame=Frame(46,48,w-92,h-94,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
 templates.append(PageTemplate(id=name,frames=[frame],pagesize=size,onPage=page_frame))
doc=Book(str(OUT),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=46,bottomMargin=48,title='Rotator cuff | 肩袖英中双语学习简报',author='肩部学习笔记',pageTemplates=templates)
# Cover and linked contents.
story.extend([Spacer(1,58),ptxt('ROTATOR CUFF','h1'),ptxt('肩袖 · 英中双语学习简报','h2'),ptxt('Anatomy, innervation, movement and research reading','body'),ptxt('解剖基础、神经走行、动作配合与论文阅读','zh'),Spacer(1,25)])
sections=root.xpath('//section[contains(@class,"chapter")]')
for i,s in enumerate(sections,1):
 h2=s.xpath('.//h2')[0];en=norm(h2.text or '')
 # Full heading with links stripped only for contents.
 heading_text=text(h2)
 story.append(ptxt('<link href="#'+s.get('id')+'" color="#42695E">'+str(i).zfill(2)+'  '+esc.escape(heading_text)+'</link>','body'))
story.extend([Spacer(1,28),ptxt('Full edition · 完整版','h4'),ptxt('6 chapters · 17 illustrations · Complete bilingual questions and answers','small'),ptxt('6 个章节、17 张图示，包含网页折叠区和完整双语问答。正文采用 A4 纵向；复杂解剖图采用 A3 图版，便于放大查看。','small'),ptxt('3D links open the local model viewer and require the learning service on this computer to be running.','small'),ptxt('3D 链接需要本机学习页面运行；正文与解剖图可以完全离线阅读。','small')])
for s in sections:
 newpage()
 h2=s.xpath('.//h2')[0];p=para(h2,'h2');p.chapter_key=s.get('id');p.chapter_title=text(h2)
 inventory['chapters'].append(s.get('id'));story.append(p)
 for e in s:walk(e)
# Remove final blank transition when the last section ends with a figure.
while story and isinstance(story[-1],(PageBreak,NextPageTemplate)):story.pop()
# Keep a subsection heading with the complete following bilingual paragraph.
packed=[];i=0
while i<len(story):
 if isinstance(story[i],Paragraph) and story[i].style.name in ('h2','h3','h4') and i+1<len(story) and isinstance(story[i+1],KeepTogether):
  packed.append(KeepTogether([story[i],*story[i+1]._content]));i+=2
 else:packed.append(story[i]);i+=1
doc.build(packed)
inventory['pages']=doc.page;inventory['outline']=outlines;inventory['output']=str(OUT)
(TMP/'export-report.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
print(json.dumps(inventory,ensure_ascii=False,indent=2))
