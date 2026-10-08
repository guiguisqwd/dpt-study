#!/usr/bin/env python3
"""Build the shared topic library from validated, auto-discovered topic packages."""
from pathlib import Path
import html
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / 'library' / 'shoulder' / '3d' / 'public'
DAILY_PUBLIC = ROOT / 'site' / 'public' / 'daily'


def esc(value):
    return html.escape(str(value), quote=True)


def daily_link():
    """Link to the daily study packs when the daily pipeline has published any (public/daily/index.html)."""
    if not (DAILY_PUBLIC / 'index.html').exists():
        return ''
    return ('<p class="daily-entry" style="margin:18px 0 0"><a href="./daily/index.html" style="font-weight:600">'
            'Daily study packs <span lang="zh-CN">每日学习包</span><span aria-hidden="true"> ↗</span></a></p>')


def build_library():
    catalog = json.loads((PUBLIC / 'topics.json').read_text())
    topics = sorted(catalog['topics'], key=lambda topic: (topic['status'] != 'published', topic['title']['en']))
    published = sum(topic['status'] == 'published' for topic in topics)
    cards = []
    for topic in topics:
        ready = topic['status'] == 'published'
        title, summary = topic['title'], topic['summary']
        region = topic.get('region', {'en': 'Anatomy', 'zh': '解剖'})
        home = topic.get('links', {}).get('home', f"./topics/{topic['id']}/index.html")
        search = ' '.join([topic['id'], title['en'], title['zh'], summary['en'], summary['zh'], region['en'], region['zh']])
        cards.append(f'''<article class="topic-card" data-search="{esc(search.lower())}" data-status="{topic['status']}">
          <div class="card-top"><span class="region">{esc(region['en'])}<small lang="zh-CN">{esc(region['zh'])}</small></span>
          <span class="status {'ready' if ready else 'draft'}">{'Available' if ready else 'In preparation'}<small lang="zh-CN">{'可学习' if ready else '筹备中'}</small></span></div>
          <h2>{esc(title['en'])}<small lang="zh-CN">{esc(title['zh'])}</small></h2>
          <p>{esc(summary['en'])}<span class="translation" lang="zh-CN">{esc(summary['zh'])}</span></p>
          <a class="open-topic" href="{esc(home)}">{'Open topic' if ready else 'View topic'} <span lang="zh-CN">{'进入学习' if ready else '查看主题'}</span><span aria-hidden="true"> ↗</span></a>
        </article>''')
    css = (ROOT / 'site/build/platform/library.css').read_text()
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anatomy study · 解剖学习</title><style>{css}</style></head>
    <body><main><header><div class="eyebrow">ANATOMY · LANGUAGE · EVIDENCE</div><h1>Anatomy study<span lang="zh-CN">解剖学习</span></h1>
    <p class="intro">Explore a region. Follow its structures. Explain it in English.<span class="translation" lang="zh-CN">按部位学习结构与联系，用完整英语描述解剖。</span></p>
    <div class="counts"><span>{published} available<small lang="zh-CN">可学习主题</small></span><span>{len(topics)-published} in preparation<small lang="zh-CN">筹备中的主题</small></span><span>English first<small lang="zh-CN">英文在前 · 中文随后</small></span></div>{daily_link()}</header>
    <section class="library" aria-labelledby="library-title"><div class="library-heading"><h2 id="library-title">Topic library <span lang="zh-CN">主题库</span></h2><label for="search">Find a region or structure<small lang="zh-CN">搜索部位或结构</small></label><input id="search" type="search" placeholder="Shoulder, hip… / 肩、髋…" autocomplete="off"></div>
    <div class="filters" role="group" aria-label="Topic status · 主题状态"><button type="button" aria-pressed="true" data-filter="all">All <span lang="zh-CN">全部</span></button><button type="button" aria-pressed="false" data-filter="published">Available <span lang="zh-CN">可学习</span></button><button type="button" aria-pressed="false" data-filter="draft">In preparation <span lang="zh-CN">筹备中</span></button></div>
    <div class="topic-grid">{''.join(cards)}</div><p id="empty" role="status" hidden>No matching topics.<span class="translation" lang="zh-CN">没有匹配的主题。</span></p></section>
    <section class="approach" aria-label="Learning sequence"><h2>A familiar path in every topic<span lang="zh-CN">每个主题，沿用一致的学习顺序</span></h2><ol>'''
    for en, zh in [('Anatomy', '结构与起止点'), ('Innervation', '神经与走行'), ('Movement', '动作与配合'), ('Clinical anatomy', '临床与体表'), ('Review', '简记与完整答案'), ('Paper reading', '论文与证据')]:
        page += f'<li>{en}<small lang="zh-CN">{zh}</small></li>'
    page += '''</ol></section><footer>Study progress is saved in this browser.<span lang="zh-CN">学习进度保存在当前浏览器。</span> <a href="./licenses/ATTRIBUTION.txt">Model attribution · 模型署名</a></footer></main>
    <script>const search=document.querySelector('#search'),cards=[...document.querySelectorAll('.topic-card')],buttons=[...document.querySelectorAll('[data-filter]')];let filter='all';function update(){const query=search.value.trim().toLowerCase();let visible=0;for(const card of cards){card.hidden=!(card.dataset.search.includes(query)&&(filter==='all'||card.dataset.status===filter));if(!card.hidden)visible++;}document.querySelector('#empty').hidden=visible>0;}search.addEventListener('input',update);for(const button of buttons)button.addEventListener('click',()=>{filter=button.dataset.filter;for(const b of buttons)b.setAttribute('aria-pressed',String(b===button));update();});</script></body></html>'''
    (PUBLIC / 'study.html').write_text(page)
    print(json.dumps({'library': 'study.html', 'topics': len(topics), 'published': published}))


if __name__ == '__main__':
    subprocess.run([sys.executable, str(ROOT / 'site/build/build-topics.py')], cwd=ROOT, check=True)
    build_library()
