"""DL-07 / N-5: each paper record in daily/papers/ carries every source it cites."""
import json
import unittest
from pathlib import Path

PAPERS = Path(__file__).resolve().parents[1] / 'daily/papers'


def cited_ids(node):
    """Source ids named by a record's `sources` list or by a `sources` block's `ids`."""
    if isinstance(node, list):
        for item in node: yield from cited_ids(item)
    elif isinstance(node, dict):
        if isinstance(node.get('sources'), list): yield from (s for s in node['sources'] if isinstance(s, str))
        if node.get('type') == 'sources': yield from node.get('ids', [])
        for value in node.values(): yield from cited_ids(value)


class DailyPaperTests(unittest.TestCase):
    def test_every_cited_source_is_defined_in_the_same_file(self):
        files = sorted(PAPERS.glob('*.json'))
        self.assertTrue(files)
        for path in files:
            paper = json.loads(path.read_text())
            defined = {s['id'] for s in paper['sources']}
            missing = set(cited_ids({'paper': paper['paper'], 'section': paper.get('section')})) - defined
            self.assertEqual(missing, set(), path.name)


if __name__ == '__main__':
    unittest.main()
