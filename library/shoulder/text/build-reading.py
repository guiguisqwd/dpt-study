#!/usr/bin/env python3
"""Build the rotator cuff reading page and Markdown from library/shoulder/content.json.

The chapter has one source (content.json, figures/, pronunciation.json); this script only writes the
outputs at the paths that existing links and the PDF export use. Run from anywhere.
"""
from pathlib import Path
import json
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
TOPIC = HERE.parent
ROOT = TOPIC.parents[1]
APP = TOPIC / '3d'
sys.path.insert(0, str(ROOT / 'site/build/platform'))
import reading
from topiclib import chapter, read_json, validate

# Absolute local addresses are rewritten to the live site by site/build/prepare-web-release.py.
BASE = 'http://127.0.0.1:5178/'

manifest = read_json(TOPIC / 'topic.json')
content = read_json(TOPIC / 'content.json')
errors, missing = validate(manifest, content, TOPIC)
if errors: raise SystemExit('library/shoulder does not pass validation:\n  ' + '\n  '.join(errors))

page, markdown = reading.render_page(chapter(manifest, content, TOPIC, ROOT, model_base=BASE, audio_base=BASE, figure_prefix='../'))
for target in [HERE / '2026-10-06-肩袖-阅读优化版.html', APP / 'public/reading.html']:
    target.write_text(page, encoding='utf-8')
(HERE / '2026-10-06-肩袖-阅读优化版.md').write_text(markdown, encoding='utf-8')
for path in re.findall(r'!\[[^]]*\]\(([^)]+)\)', markdown):
    if not (HERE / path).exists(): raise SystemExit('Markdown image path is broken: ' + path)
# The local static server serves dist; a later Vite build replaces it with the same file.
(APP / 'dist').mkdir(exist_ok=True)
shutil.copyfile(APP / 'public/reading.html', APP / 'dist/reading.html')

figures = re.findall(r'data-figure="(\d+)"', page)
summary = {'chapters': len(content['sections']), 'figure_occurrences': len(figures), 'figures': figures,
           'model_links': sorted(set(re.findall(r'\?term=([a-z-]+)', page))), 'points': sorted(set(re.findall(r'\?point=([A-Z0-9]+)', page))),
           'pronunciation_terms': len(read_json(TOPIC / 'pronunciation.json').get('terms', {})), 'source': 'library/shoulder/content.json',
           'pending': missing}
(HERE / 'build-report.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'pending'} | {'pending': len(missing)}, ensure_ascii=False))
