"""Regression tests for new-topic isolation and honest publication, not medical facts."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'site/build/platform'))
from topiclib import QA_CHECKS, build, catalog_models, pair, skeleton, validate, write_json


class TopicTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.models = catalog_models()

    def tearDown(self): self.temp.cleanup()

    def draft(self, tid='test-topic'):
        manifest, content = skeleton(tid, 'Test topic', '测试主题')
        path = self.base / 'topics' / tid
        path.mkdir(parents=True)
        return manifest, content, path

    def completed_fixture(self):
        """Artificial prose kept inside a temporary directory; never a real medical lesson."""
        m, c, path = self.draft()
        m['status'] = 'published'
        m['viewer'] = {'enabled': True, 'defaultTerm': 'humerus', 'terms': [
            {'id': 'humerus', 'name': pair('Humerus', '肱骨'), 'kind': 'bone', 'structures': {
                'right': 'appendicular-skeleton-humerus-right', 'left': 'appendicular-skeleton-humerus-left'}},
            {'id': 'supraspinatus', 'name': pair('Supraspinatus', '冈上肌'), 'kind': 'muscle', 'structures': {
                'right': 'rotator-cuff-muscles-supraspinatus-muscle-right', 'left': 'rotator-cuff-muscles-supraspinatus-muscle-left'}}]}
        artificial = pair('This is artificial test prose for renderer verification only.', '这是仅用于渲染核验的测试文字。')
        for section in c['sections']:
            section['overview'] = artificial
            section['diagramIds'] = ['test-diagram']
            section['blocks'] = [{'heading': pair('Test heading', '测试标题'), 'body': artificial, 'termIds': ['humerus']}]
        c['sources'] = [{'id': 'test-source', 'title': 'Synthetic test reference', 'url': 'https://example.invalid/test'}]
        c['muscles'] = [{'id': 'supraspinatus', 'name': pair('Supraspinatus', '冈上肌'),
                         **{k: artificial for k in ['origin', 'insertion', 'actions', 'innervation']},
                         'course': pair('The test muscle originates from the artificial test origin and inserts onto the artificial test insertion.', '测试肌肉从虚构测试起点起始，止于虚构测试止点。'),
                         'modelTermId': 'supraspinatus', 'modelUnavailableReason': None,
                         'diagramIds': ['test-diagram'], 'sources': ['test-source']}]
        c['landmarks'] = [{'id': 'test-landmark', 'name': pair('Test landmark', '测试标志'), 'description': artificial,
                           'modelTermId': 'humerus', 'viewerLandmarkId': None,
                           'modelUnavailableReason': pair('Exact landmark position is not mapped in this test.', '本测试未标注该标志的准确位置。'),
                           'diagramIds': ['test-diagram'], 'sources': ['test-source']}]
        c['diagrams'] = [{'id': 'test-diagram', 'file': 'figures/test.svg', 'alt': artificial, 'caption': artificial,
                          'labels': [{'kind': 'origin', 'muscleId': 'supraspinatus', 'text': pair('Origin: test site', '起点：测试部位')},
                                     {'kind': 'insertion', 'muscleId': 'supraspinatus', 'text': pair('Insertion: test site', '止点：测试部位')}],
                          'sources': ['test-source']}]
        (path / 'figures').mkdir()
        (path / 'figures/test.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>Origin: test site 起点：测试部位</text><text>Insertion: test site 止点：测试部位</text></svg>')
        c['review'] = [{'id': 'test-question', 'question': pair('What is the test question?', '测试问题是什么？'),
                        'answer': pair('This complete English answer contains enough words to verify that a full explanation survives rendering before its Chinese translation.', '这是一段完整测试答案，用于检查中文位于英文之后。'),
                        'mnemonic': pair('Test mnemonic', '测试简记'), 'sources': ['test-source']}]
        c['papers'] = [{'id': 'test-paper', 'citation': 'Artificial fixture, not a real paper.',
                        **{key: artificial for key in ['question', 'design', 'population', 'methods', 'results', 'limitations', 'applicability']},
                        'terms': [{'term': pair('Test term', '测试术语'), 'explanation': artificial}], 'sources': ['test-source']}]
        m['structures'] = [{'id': 'supraspinatus', 'kind': 'muscle', 'name': pair('Supraspinatus', '冈上肌'),
                            'chapters': ['anatomy'], 'modelTermId': 'supraspinatus'}]
        c['qa'] = {'reviewedBy': 'Test fixture only', 'reviewedOn': '2026-10-06', 'checks': {key: True for key in QA_CHECKS}}
        return m, c, path

    def write_topic(self, m, c, path):
        write_json(path / 'topic.json', m); write_json(path / 'content.json', c)

    def test_two_independent_topics_scaffold_without_core_changes(self):
        topics = self.base / 'topics'
        core_before = (ROOT / 'site/build/platform/topiclib.py').read_bytes()
        for tid in ['knee-test', 'elbow-test']:
            result = subprocess.run([sys.executable, str(ROOT / 'site/build/new-topic.py'), '--id', tid, '--en', tid,
                                     '--zh', '测试主题', '--topics-dir', str(topics)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
        catalog = build(topics, self.base / 'public')
        self.assertEqual({t['id'] for t in catalog}, {'knee-test', 'elbow-test'})
        self.assertTrue(all(t['status'] == 'draft' for t in catalog))
        self.assertEqual((ROOT / 'site/build/platform/topiclib.py').read_bytes(), core_before)
        for topic in catalog:
            self.assertTrue((self.base / 'public/topics' / topic['id'] / 'index.html').exists())

    def test_new_topic_refuses_overwrite_and_path_traversal(self):
        topics = self.base / 'topics'
        command = [sys.executable, str(ROOT / 'site/build/new-topic.py'), '--en', 'Test', '--zh', '测试', '--topics-dir', str(topics)]
        self.assertEqual(subprocess.run(command + ['--id', 'knee'], capture_output=True).returncode, 0)
        existing = (topics / 'knee/topic.json').read_bytes()
        self.assertNotEqual(subprocess.run(command + ['--id', 'knee'], capture_output=True).returncode, 0)
        self.assertEqual((topics / 'knee/topic.json').read_bytes(), existing)
        for invalid in ['../escape', '/tmp/escape', 'Hip', 'hip/other', 'hip--other']:
            self.assertNotEqual(subprocess.run(command + ['--id', invalid], capture_output=True).returncode, 0)
        self.assertFalse((self.base / 'escape').exists())

    def test_draft_has_no_fake_course_or_reading_link(self):
        m, c, path = self.draft(); self.write_topic(m, c, path)
        catalog = build(path.parent, self.base / 'public')
        self.assertNotIn('reading', catalog[0]['links'])
        data = json.loads((self.base / 'public/topics/test-topic/data.json').read_text())
        self.assertIsNone(data['content'])
        text = (self.base / 'public/topics/test-topic/reading.html').read_text()
        self.assertIn('Draft', text); self.assertIn('草稿', text)
        self.assertNotIn('class="muscle"', text)
        self.assertLess(text.index('Test topic'), text.index('测试主题'))

    def test_published_empty_topic_rejected_and_existing_output_preserved(self):
        m, c, path = self.draft(); m['status'] = 'published'; self.write_topic(m, c, path)
        output = self.base / 'public'; (output / 'topics').mkdir(parents=True)
        sentinel = output / 'topics/keep'; sentinel.write_text('existing build')
        with self.assertRaises(ValueError): build(path.parent, output)
        self.assertEqual(sentinel.read_text(), 'existing build')

    def test_invalid_root_and_nested_shapes_report_errors_without_tracebacks(self):
        m, c, path = self.draft()
        self.assertTrue(validate([], c, path, self.models)[0])
        malformed = copy.deepcopy(c); malformed['sections'][0]['blocks'] = [None]
        self.assertTrue(validate(m, malformed, path, self.models)[0])
        write_json(path / 'topic.json', [])
        result = subprocess.run([sys.executable, str(ROOT / 'site/build/validate-topics.py'), '--topics-dir', str(path.parent)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must contain an object', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_complete_topic_generates_bilingual_answers_and_exact_links(self):
        m, c, path = self.completed_fixture()
        errors, missing = validate(m, c, path, self.models)
        self.assertEqual(errors, []); self.assertEqual(missing, [])
        self.write_topic(m, c, path); build(path.parent, self.base / 'public')
        destination = self.base / 'public/topics/test-topic'
        text = (destination / 'reading.html').read_text()
        english, chinese = c['review'][0]['answer']['en'], c['review'][0]['answer']['zh']
        self.assertLess(text.index(english), text.index(chinese))
        self.assertIn('topic=test-topic&amp;term=supraspinatus', text)
        self.assertTrue((destination / 'figures/test.svg').exists())
        markdown = (destination / 'reading.md').read_text()
        self.assertIn(english, markdown); self.assertIn('Test mnemonic', markdown)
        self.assertIn('Study design', markdown); self.assertIn('lumbar', text)

    def test_structure_list_must_exist_be_complete_and_match_the_text(self):
        m, c, path = self.completed_fixture()
        bad = copy.deepcopy(m); bad['structures'] = []
        errors, _ = validate(bad, c, path, self.models)
        self.assertIn('ST-1 structure list is missing (topic.json structures)', errors)
        self.assertIn('supraspinatus: muscle record is not in the ST-1 structure list', errors)
        bad = copy.deepcopy(m); bad['structures'][0]['chapters'] = ['papers']
        self.assertIn('structure supraspinatus: not mentioned in chapter papers', validate(bad, c, path, self.models)[0])
        bad = copy.deepcopy(m); bad['structures'][0]['modelTermId'] = 'guessed-id'
        self.assertIn('structure supraspinatus: modelTermId is not a real 3D id', validate(bad, c, path, self.models)[0])
        bad = copy.deepcopy(m); bad['structures'][0]['kind'] = 'organ'
        self.assertTrue(validate(bad, c, path, self.models)[0])
        draft = copy.deepcopy(m); draft['status'] = 'draft'; draft['structures'] = []
        errors, missing = validate(draft, c, path, self.models)
        self.assertEqual(errors, []); self.assertIn('ST-1 structure list is missing (topic.json structures)', missing)

    def test_nonexistent_incorrect_tissue_and_wrong_anatomy_mappings_fail(self):
        m, c, path = self.completed_fixture()
        for wrong in ['not-a-model', 'skeleton-hip-bone-right', 'rotator-cuff-muscles-supraspinatus-muscle-right']:
            edited = copy.deepcopy(m); edited['viewer']['terms'][0]['structures']['right'] = wrong
            errors, _ = validate(edited, c, path, self.models)
            self.assertTrue(errors, wrong)
        edited = copy.deepcopy(m); edited['viewer']['terms'][0]['structures']['right'] = 'appendicular-skeleton-humerus-left'
        errors, _ = validate(edited, c, path, self.models)
        self.assertTrue(any('swapped' in e for e in errors))

    def test_origin_insertion_must_exist_in_actual_svg(self):
        m, c, path = self.completed_fixture()
        (path / 'figures/test.svg').write_text('<svg><text>Origin: test site 起点：测试部位</text></svg>')
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('absent from SVG' in error for error in errors))
        c['diagrams'][0]['labels'] = c['diagrams'][0]['labels'][:1]
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('label its insertion' in error for error in errors))

    def test_bony_landmark_requirement_and_false_point_links_rejected(self):
        m, c, path = self.completed_fixture(); c['landmarks'] = []
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('bony landmark' in error for error in errors))
        m, c, path = self.completed_fixture_at_new_path('second')
        c['landmarks'][0]['viewerLandmarkId'] = 'imaginary-point'
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('not reviewed' in error for error in errors))

    def completed_fixture_at_new_path(self, suffix):
        # Keep the public topic id consistent while reusing the temporary test helper.
        old_base = self.base; self.base = self.base / suffix
        result = self.completed_fixture(); self.base = old_base
        return result

    def test_reviewed_coordinates_need_finite_values_sources_and_signoff(self):
        m, c, path = self.completed_fixture()
        m['viewer']['landmarks'] = [{'id': 'test-point', 'name': pair('Point', '点'), 'structures': m['viewer']['terms'][0]['structures'],
                                    'reviewStatus': 'reviewed', 'positions': {'right': [float('nan'), 0, 0], 'left': [0, 0, 0]}}]
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('positions' in e for e in errors))
        m['viewer']['landmarks'][0]['positions']['right'] = [0, 0, 0]
        self.assertTrue(any('signoff' in e for e in validate(m, c, path, self.models)[0]))
        m['viewer']['landmarks'][0]['reviewStatus'] = 'pending'
        del m['viewer']['landmarks'][0]['positions']
        self.assertEqual(validate(m, c, path, self.models)[0], [])

    def test_asset_path_traversal_and_active_svg_rejected(self):
        m, c, path = self.completed_fixture()
        c['diagrams'][0]['file'] = '../outside.svg'
        self.assertTrue(validate(m, c, path, self.models)[0])
        c['diagrams'][0]['file'] = 'figures/test.svg'
        (path / 'figures/test.svg').write_text('<svg><script>alert(1)</script></svg>')
        self.assertTrue(any('Active SVG' in e for e in validate(m, c, path, self.models)[0]))

    def test_source_and_qa_omissions_cannot_publish(self):
        m, c, path = self.completed_fixture()
        c['muscles'][0]['sources'] = ['unknown']; c['qa']['checks']['layoutMobile'] = False
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('unknown source' in e for e in errors))
        self.assertIn('QA pending: layoutMobile', errors)

    def test_invalid_source_url_and_impossible_review_date_fail(self):
        m, c, path = self.completed_fixture()
        c['sources'][0]['url'] = 'https://['
        c['qa']['reviewedOn'] = '2026-99-99'
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('valid HTTPS' in e for e in errors))
        self.assertTrue(any('valid review date' in e for e in errors))

    def test_new_topic_cannot_bypass_quality_with_legacy_adapter(self):
        m, c, path = self.draft(); m['adapter'] = 'shoulder'; m['status'] = 'published'
        self.assertTrue(any('reserved' in e for e in validate(m, c, path, self.models)[0]))

    def test_missing_or_stale_pdf_is_not_advertised(self):
        m, c, path = self.completed_fixture()
        m['pdf'] = {'file': 'figures/missing.pdf', 'contentDigest': 'old', 'reviewedBy': 'Tester', 'reviewedOn': '2026-10-06'}
        errors, _ = validate(m, c, path, self.models)
        self.assertTrue(any('PDF is missing' in e for e in errors)); self.assertTrue(any('stale' in e for e in errors))


if __name__ == '__main__': unittest.main()
