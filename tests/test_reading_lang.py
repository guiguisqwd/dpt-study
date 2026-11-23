"""English-only view (EN / 中英 switch): every Chinese text on a chapter reading page must sit inside a
lang="zh-Hans" / lang="zh-CN" element, so the switch can hide it. Shared template: site/build/platform/reading.py."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'site/build/platform'))
from topiclib import build

CJK = re.compile(r'[㐀-鿿！-～]')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
# Kept on purpose: the switch's own "中英" label, and source titles cited in their original language.
ALLOWED = (re.compile(r'^中英$'), re.compile(r'^GB/T '))


class ChineseOutsideLang(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.problems = [], []

    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        lang = dict(attrs).get('lang')
        parent = self.stack[-1][1] if self.stack else False
        self.stack.append((tag, parent or bool(lang and lang.startswith('zh') and lang != 'zh-Latn') or tag in ('script', 'style', 'title', 'desc', 'metadata')))  # not displayed

    def handle_startendtag(self, tag, attrs): pass

    def handle_endtag(self, tag):
        if tag in VOID: return
        while self.stack:
            if self.stack.pop()[0] == tag: break

    def handle_data(self, data):
        text = data.strip()
        if text and CJK.search(text) and not (self.stack and self.stack[-1][1]) and not any(p.search(text) for p in ALLOWED):
            self.problems.append(text[:80])


def problems(path):
    parser = ChineseOutsideLang()
    parser.feed(Path(path).read_text(encoding='utf-8'))
    return parser.problems


class ReadingLanguageTests(unittest.TestCase):
    def test_every_chapter_page_hides_all_chinese_in_english_view(self):
        with tempfile.TemporaryDirectory() as temp:
            build(output=temp)
            pages = sorted(Path(temp, 'topics').glob('*/reading.html'))
            pages = [p for p in pages if 'class="lang-switch"' in p.read_text(encoding='utf-8')]
            self.assertTrue(pages, 'no chapter reading page with the language switch was built')
            for page in pages:
                with self.subTest(page=page.parent.name):
                    self.assertEqual(problems(page), [])

    def test_shoulder_legacy_reading_page(self):
        self.assertEqual(problems(ROOT / 'library/shoulder/3d/public/reading.html'), [])


if __name__ == '__main__':
    unittest.main()
