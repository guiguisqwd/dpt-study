"""Shared topic contracts, publication gates and renderer (Python standard library)."""
from __future__ import annotations
import hashlib
import html
import json
import math
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.parse import urlencode, urlparse

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r'^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$')
SECTIONS = [
    ('anatomy', 'Anatomy', '解剖基础'),
    ('innervation', 'Innervation and nerve course', '神经支配与走行'),
    ('movement', 'Movement and coordination', '动作与配合'),
    ('clinical', 'Clinical and regional anatomy', '临床与局部解剖'),
    ('review', 'Review and complete answers', '复习与完整答案'),
    ('papers', 'Critical reading', '论文阅读'),
]
QA_CHECKS = ['medicalSources', 'bilingual', 'originInsertionLabels', 'modelLinks',
             'layoutDesktop', 'layoutMobile', 'fullAnswers', 'paperAppraisal']
MUSCLE_FIELDS = ['origin', 'insertion', 'course', 'actions', 'innervation']
PAPER_FIELDS = ['question', 'design', 'population', 'methods', 'results', 'limitations', 'applicability']
NERVE_NOTATION = {
    'cervical': {'en': 'C denotes cervical levels.', 'zh': 'C 表示颈部节段。'},
    'thoracic': {'en': 'T denotes thoracic levels.', 'zh': 'T 表示胸部节段。'},
    'lumbar': {'en': 'L denotes lumbar levels.', 'zh': 'L 表示腰部节段。'},
    'sacral': {'en': 'S denotes sacral levels.', 'zh': 'S 表示骶部节段。'},
    'spinalNerveVsVertebra': {'en': 'A spinal nerve level identifies a nerve, whereas a vertebral level identifies a bone. Specify which is being described.', 'zh': '脊神经节段表示神经，椎骨节段表示骨骼；描述时应明确区分。'},
}


def pair(en='', zh=''):
    return {'en': en, 'zh': zh}


def skeleton(topic_id, en, zh, region_en='', region_zh=''):
    if not isinstance(topic_id, str) or not ID.fullmatch(topic_id):
        raise ValueError('Topic id must be a lowercase slug, e.g. hip or knee-joint.')
    manifest = {'schemaVersion': 1, 'id': topic_id, 'title': pair(en, zh),
                'summary': pair('Content is being prepared and has not been reviewed.', '内容正在整理，尚未完成核验。'),
                'region': pair(region_en or en, region_zh or zh), 'status': 'draft', 'adapter': 'standard',
                'viewer': {'enabled': False, 'defaultTerm': None, 'terms': []}}
    content = {'schemaVersion': 1, 'sections': [
        {'id': sid, 'title': pair(e, z), 'overview': pair(), 'blocks': [], 'diagramIds': []}
        for sid, e, z in SECTIONS], 'muscles': [], 'landmarks': [], 'diagrams': [],
        'review': [], 'papers': [], 'sources': [],
        'nerveNotation': json.loads(json.dumps(NERVE_NOTATION)),
        'qa': {'reviewedBy': '', 'reviewedOn': '', 'checks': {k: False for k in QA_CHECKS}}}
    manifest_template = ROOT / 'platform/templates/topic.json'
    content_template = ROOT / 'platform/templates/content.json'
    if manifest_template.exists(): manifest = {**read_json(manifest_template), **manifest}
    if content_template.exists(): content = read_json(content_template)
    return manifest, content


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def inside(base, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('Expected a relative asset path.')
    base = Path(base).resolve()
    target = (base / relative).resolve()
    if not target.is_relative_to(base):
        raise ValueError('Asset path leaves its topic directory.')
    return target


def catalog_models(root=ROOT):
    result = {}
    for system in ['skeletal', 'muscular']:
        path = Path(root) / '肩部3D学习/public/models' / (system + '.metadata.json')
        for s in read_json(path)['structures']:
            result[s['id']] = s
    return result


def normal_model_name(name):
    return re.sub(r'\s+', ' ', re.sub(r'\s+muscle\b|\.[lr]$', '', name, flags=re.I)).strip().lower()


def content_digest(content, topic_dir):
    digest = hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode())
    for diagram in content.get('diagrams', []):
        path = inside(topic_dir, diagram['file'])
        digest.update(path.read_bytes())
    return digest.hexdigest()


def valid_review_date(value):
    try:
        return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value)) and bool(date.fromisoformat(value))
    except (ValueError, TypeError):
        return False


def valid_source_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme == 'https' and bool(parsed.hostname) and not any(c.isspace() for c in value)
    except (ValueError, TypeError):
        return False


def validate_shape(value, schema, label='data'):
    """Check the structural subset used by our checked-in schemas, without dependencies."""
    errors = []
    if 'anyOf' in schema:
        if all(validate_shape(value, choice, label) for choice in schema['anyOf']):
            return [label + ': does not match an allowed field shape']
        return []
    if 'const' in schema and value != schema['const']: errors.append(label + ': unexpected schema version')
    if 'enum' in schema and value not in schema['enum']: errors.append(label + ': unexpected value')
    types = schema.get('type', [])
    if isinstance(types, str): types = [types]
    matched = {'object': isinstance(value, dict), 'array': isinstance(value, list), 'string': isinstance(value, str),
               'number': type(value) in [int, float] and math.isfinite(value), 'integer': type(value) is int,
               'boolean': type(value) is bool, 'null': value is None}
    if types and not any(matched.get(t, False) for t in types): return errors + [label + ': wrong field type']
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value: errors.append(label + '.' + key + ': required field is missing')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            for key in value:
                if key not in props: errors.append(label + '.' + key + ': unexpected field')
        for key, child in props.items():
            if key in value: errors.extend(validate_shape(value[key], child, label + '.' + key))
    elif isinstance(value, list):
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', float('inf')):
            errors.append(label + ': invalid number of items')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(label + ': duplicate items')
        for i, item in enumerate(value): errors.extend(validate_shape(item, schema.get('items', {}), label + '[' + str(i) + ']'))
    elif isinstance(value, str):
        if schema.get('pattern') and not re.search(schema['pattern'], value): errors.append(label + ': invalid format')
    elif type(value) in [int, float]:
        if value < schema.get('minimum', -float('inf')) or value > schema.get('maximum', float('inf')):
            errors.append(label + ': number outside allowed range')
    return errors


def validate(manifest, content, topic_dir, models=None, root=ROOT, published_override=False):
    """Return (errors, missing). Draft omissions are visible; unsafe/invalid data always errors."""
    errors, missing = [], []
    models = catalog_models(root) if models is None else models
    topic_dir = Path(topic_dir)
    errors.extend(validate_shape(manifest, read_json(ROOT / 'platform/topic.schema.json'), 'topic'))
    if isinstance(manifest, dict) and manifest.get('adapter') == 'standard':
        errors.extend(validate_shape(content, read_json(ROOT / 'platform/content.schema.json'), 'content'))
    if errors: return errors, missing
    ready = published_override or manifest.get('status') == 'published'

    def fail(message): errors.append(message)
    def require(condition, message):
        if not condition: missing.append(message)
    def bi(value, label, required=True):
        if not isinstance(value, dict) or set(value) != {'en', 'zh'} or any(not isinstance(value.get(k), str) for k in ['en', 'zh']):
            fail(label + ': expected {en: string, zh: string}')
            return
        if required: require(bool(value['en'].strip()) and bool(value['zh'].strip()), label + ': English and Chinese are required')
        # Deliberate visible placeholders cannot pass a publication gate.
        if ready and any(re.search(r'\b(?:TODO|TBD|placeholder)\b|待补|待核|待填', value[k], re.I) for k in ['en', 'zh']):
            fail(label + ': unresolved placeholder')
    def sourced(value, label):
        ids = value.get('sources', [])
        require(bool(ids), label + ': source references required')
        if not isinstance(ids, list) or any(x not in source_ids for x in ids): fail(label + ': unknown source reference')

    tid = manifest.get('id')
    if not isinstance(tid, str) or not ID.fullmatch(tid): fail('Invalid topic id')
    elif topic_dir.name != tid: fail('Topic id must match its directory')
    if manifest.get('schemaVersion') != 1: fail('Unsupported manifest schemaVersion')
    if manifest.get('status') not in ['draft', 'published']: fail('status must be draft or published')
    if manifest.get('adapter') not in ['shoulder', 'standard']: fail('Unknown adapter')
    for key in ['title', 'summary', 'region']: bi(manifest.get(key), key)
    viewer = manifest.get('viewer', {})
    if not isinstance(viewer, dict):
        fail('viewer must be an object'); viewer = {}
    if type(viewer.get('enabled')) is not bool: fail('viewer.enabled must be boolean')
    terms = viewer.get('terms', [])
    if not isinstance(terms, list): fail('viewer.terms must be a list'); terms = []
    term_ids = set()
    for term in terms:
        label = 'viewer term ' + str(term.get('id'))
        if not ID.fullmatch(str(term.get('id', ''))) or term.get('id') in term_ids: fail(label + ': invalid or duplicate id')
        term_ids.add(term.get('id'))
        bi(term.get('name'), label + '.name')
        kind = term.get('kind')
        if kind not in ['bone', 'muscle']: fail(label + ': invalid tissue kind')
        structures = term.get('structures', {})
        if set(structures) != {'right', 'left'}: fail(label + ': both anatomical sides required')
        for side in ['right', 'left']:
            key = structures.get(side)
            structure = models.get(key)
            if not structure or structure.get('objectCount', 0) < 1:
                fail(label + ': no renderable geometry for ' + side + ' ' + str(key)); continue
            expected_system = 'skeletal' if kind == 'bone' else 'muscular'
            if structure.get('system') != expected_system: fail(label + ': incorrect tissue mapping for ' + str(key))
            if key.endswith(('-right', '-left')) and not key.endswith('-' + side): fail(label + ': swapped anatomical side')
            name = term.get('name', {}).get('en', '')
            if normal_model_name(name) != normal_model_name(structure['name']):
                fail(label + ': name does not match model anatomy ' + structure['name'])
    if viewer.get('enabled'):
        if not terms or viewer.get('defaultTerm') not in term_ids: fail('Enabled viewer needs a mapped defaultTerm')
    elif viewer.get('defaultTerm') is not None: fail('Disabled viewer defaultTerm must be null')
    landmarks = viewer.get('landmarks', [])
    if not isinstance(landmarks, list): fail('viewer.landmarks must be a list'); landmarks = []
    landmark_ids = set()
    for landmark in landmarks:
        label = 'viewer landmark ' + str(landmark.get('id'))
        if not ID.fullmatch(str(landmark.get('id', ''))) or landmark.get('id') in landmark_ids or landmark.get('id') in term_ids:
            fail(label + ': invalid or duplicate id')
        landmark_ids.add(landmark.get('id'))
        bi(landmark.get('name'), label + '.name')
        if landmark.get('reviewStatus') not in ['reviewed', 'pending']: fail(label + ': invalid reviewStatus')
        for side in ['right', 'left']:
            sid = landmark.get('structures', {}).get(side)
            if sid not in {t.get('structures', {}).get(side) for t in terms}: fail(label + ': structure is outside this topic')
            position = landmark.get('positions', {}).get(side)
            if landmark.get('reviewStatus') == 'reviewed' or position is not None:
                if (not isinstance(position, list) or len(position) != 3 or
                    any(type(x) not in [int, float] or not math.isfinite(x) or abs(x) > 20 for x in position)):
                    fail(label + ': invalid finite model coordinates')
        if landmark.get('reviewStatus') == 'reviewed':
            review = landmark.get('review', {})
            if not review.get('reviewedBy', '').strip() or not valid_review_date(review.get('reviewedOn', '')):
                fail(label + ': reviewed coordinates need reviewer/date signoff')
            if not review.get('sourceUrls') or not all(valid_source_url(u) for u in review.get('sourceUrls', [])):
                fail(label + ': reviewed coordinates need anatomical source URLs')

    if manifest.get('adapter') == 'shoulder':
        # One explicit backwards-compatibility adapter, never a bypass for new courses.
        if tid != 'shoulder': fail('The shoulder adapter is reserved for the existing shoulder topic')
        for relative in ['reading-source/sections/01-anatomy.html', '肩部3D学习/public/reading.html', '肩部3D学习/public/reading-claude.html']:
            if not (Path(root) / relative).is_file(): fail('Missing preserved shoulder source: ' + relative)
        return errors, missing

    if not isinstance(content, dict): return errors + ['content.json must be an object'], missing
    if content.get('schemaVersion') != 1: fail('Unsupported content schemaVersion')
    for field in ['sections', 'muscles', 'landmarks', 'diagrams', 'review', 'papers', 'sources']:
        if not isinstance(content.get(field), list):
            fail(field + ' must be a list')
            content = dict(content, **{field: []})
    source_ids = set()
    for source in content['sources']:
        sid = source.get('id')
        if not ID.fullmatch(str(sid)) or sid in source_ids: fail('Invalid or duplicate source id')
        source_ids.add(sid)
        if not source.get('title', '').strip(): fail('Source requires title')
        if not valid_source_url(source.get('url', '')): fail('Source requires a valid HTTPS URL')
    require(bool(source_ids), 'Evidence sources are missing')
    for field in NERVE_NOTATION:
        bi(content.get('nerveNotation', {}).get(field), 'nerveNotation.' + field)

    diagrams = {}
    for diagram in content['diagrams']:
        did = diagram.get('id')
        if not ID.fullmatch(str(did)) or did in diagrams: fail('Invalid or duplicate diagram id')
        diagrams[did] = diagram
        bi(diagram.get('alt'), str(did) + '.alt')
        bi(diagram.get('caption'), str(did) + '.caption')
        sourced(diagram, str(did))
        try:
            asset = inside(topic_dir, diagram.get('file'))
            if asset.suffix.lower() != '.svg': raise ValueError('Anatomical diagrams must be editable SVG files')
            if not str(diagram.get('file')).startswith('assets/'):
                raise ValueError('Topic diagrams must be stored under assets/')
            svg = ET.fromstring(asset.read_text())
            if svg.tag.split('}')[-1] != 'svg': raise ValueError('Expected an SVG root element')
            for element in svg.iter():
                if element.tag.split('}')[-1] in ['script', 'foreignObject']:
                    raise ValueError('Active SVG content is not allowed')
                if any(k.lower().startswith('on') for k in element.attrib): raise ValueError('SVG event handlers are not allowed')
                if any(k.split('}')[-1] == 'href' and not v.startswith('#') for k, v in element.attrib.items()):
                    raise ValueError('SVG must not load remote or external assets')
            visible = ' '.join(' '.join(element.itertext()) for element in svg.iter() if element.tag.split('}')[-1] == 'text')
            for label in diagram.get('labels', []):
                bi(label.get('text'), str(did) + '.label')
                for lang in ['en', 'zh']:
                    text = label.get('text', {}).get(lang, '')
                    if text and text not in visible: fail(str(did) + ': declared label is absent from SVG text: ' + text)
            require(bool(diagram.get('labels')), str(did) + ': meaningful structure labels are required')
        except (ValueError, OSError, ET.ParseError, TypeError) as exc: fail(str(did) + ': ' + str(exc))

    def diagram_refs(ids, label, required=False):
        if not isinstance(ids, list) or any(i not in diagrams for i in ids): fail(label + ': unknown diagram reference')
        if required: require(bool(ids), label + ': anatomical diagram required')

    sections = content['sections']
    if [s.get('id') for s in sections] != [s[0] for s in SECTIONS]: fail('Six sections must appear in the standard anatomy-to-paper order')
    for section in sections:
        label = 'section ' + str(section.get('id'))
        bi(section.get('title'), label + '.title')
        bi(section.get('overview'), label + '.overview')
        diagram_refs(section.get('diagramIds', []), label, section.get('id') in ['anatomy', 'innervation', 'movement', 'clinical'])
        for block in section.get('blocks', []):
            bi(block.get('heading'), label + '.heading')
            bi(block.get('body'), label + '.body')
            if any(t not in term_ids for t in block.get('termIds', [])): fail(label + ': unknown 3D term')
    require(bool(content['muscles']), 'Muscle attachment/course records are missing')
    seen_muscles = set()
    for muscle in content['muscles']:
        mid = muscle.get('id')
        if not ID.fullmatch(str(mid)) or mid in seen_muscles: fail('Invalid or duplicate muscle id')
        seen_muscles.add(mid)
        bi(muscle.get('name'), str(mid) + '.name')
        for key in MUSCLE_FIELDS: bi(muscle.get(key), str(mid) + '.' + key)
        course = muscle.get('course', {}).get('en', '')
        if course and not all(re.search(pattern, course, re.I) for pattern in [r'\boriginates?\b|\barises?\b', r'\bfrom\b', r'\binserts?\b|\battaches?\b']):
            require(False, str(mid) + ': course must be a complete English origin-to-insertion description')
        sourced(muscle, str(mid))
        mapped = muscle.get('modelTermId')
        if mapped:
            term = next((t for t in terms if t['id'] == mapped), None)
            if not term or term.get('kind') != 'muscle': fail(str(mid) + ': invalid muscle 3D mapping')
            elif normal_model_name(term['name']['en']) != normal_model_name(muscle['name']['en']): fail(str(mid) + ': muscle maps to a different anatomy')
        else:
            bi(muscle.get('modelUnavailableReason'), str(mid) + '.modelUnavailableReason')
        refs = muscle.get('diagramIds', [])
        diagram_refs(refs, str(mid), True)
        for label_kind in ['origin', 'insertion']:
            found = any(label.get('kind') == label_kind and label.get('muscleId') == mid
                        and label_kind in label.get('text', {}).get('en', '').lower()
                        and ('起点' if label_kind == 'origin' else '止点') in label.get('text', {}).get('zh', '')
                        for did in refs if did in diagrams for label in diagrams[did].get('labels', []))
            require(found, str(mid) + ': a diagram must visibly label its ' + label_kind)
    require(bool(content['landmarks']), 'Named bony landmark records and diagrams are missing')
    for landmark in content['landmarks']:
        bi(landmark.get('name'), 'landmark.name'); bi(landmark.get('description'), 'landmark.description')
        sourced(landmark, 'landmark')
        diagram_refs(landmark.get('diagramIds', []), 'landmark', True)
        mapped = landmark.get('modelTermId')
        if mapped:
            term = next((t for t in terms if t['id'] == mapped), None)
            if not term or term.get('kind') != 'bone': fail('Bony landmark needs a bone modelTermId')
        marker_id = landmark.get('viewerLandmarkId')
        if marker_id:
            marker = next((l for l in landmarks if l['id'] == marker_id), None)
            if not mapped: fail('Landmark marker needs its parent bone modelTermId')
            if not marker or marker.get('reviewStatus') != 'reviewed': fail('Landmark marker is not reviewed')
            elif mapped and term and marker.get('structures') != term.get('structures'): fail('Landmark marker belongs to another structure')
            elif normal_model_name(marker['name']['en']) != normal_model_name(landmark['name']['en']): fail('Landmark marker refers to a different anatomical name')
        else:
            bi(landmark.get('modelUnavailableReason'), 'landmark.modelUnavailableReason')
    require(bool(content['review']), 'Full English/Chinese review questions and answers are missing')
    for review in content['review']:
        for field in ['question', 'answer', 'mnemonic']: bi(review.get(field), 'review.' + field)
        sourced(review, 'review')
        require(len(review.get('answer', {}).get('en', '').split()) >= 12, 'Review answer must include a complete English explanation, not only a mnemonic')
    require(bool(content['papers']), 'Critical paper reading is missing')
    for paper in content['papers']:
        require(bool(paper.get('citation', '').strip()), 'Paper citation is missing')
        for field in PAPER_FIELDS: bi(paper.get(field), 'paper.' + field)
        sourced(paper, 'paper')
        require(bool(paper.get('terms')), 'Paper methodology terms are missing')
        for term in paper.get('terms', []):
            bi(term.get('term'), 'paper.term'); bi(term.get('explanation'), 'paper.explanation')
    qa = content.get('qa', {})
    require(bool(qa.get('reviewedBy', '').strip()), 'Reviewer signoff is missing')
    require(valid_review_date(qa.get('reviewedOn', '')), 'A valid review date is required (YYYY-MM-DD)')
    for key in QA_CHECKS: require(qa.get('checks', {}).get(key) is True, 'QA pending: ' + key)
    if manifest.get('pdf'):
        pdf = manifest['pdf']
        try:
            path = inside(topic_dir, pdf.get('file'))
            if path.suffix != '.pdf' or not path.is_file(): fail('Declared PDF is missing')
            if pdf.get('contentDigest') != content_digest(content, topic_dir): fail('PDF is stale relative to content/diagrams')
            if not pdf.get('reviewedBy', '').strip() or not valid_review_date(pdf.get('reviewedOn', '')): fail('PDF visual review signoff is missing')
        except (ValueError, OSError, KeyError) as exc: fail('PDF: ' + str(exc))
    if ready: errors.extend(missing)
    return errors, missing


def discover(topics_dir=None, root=ROOT):
    topics_dir = Path(topics_dir or Path(root) / 'topics')
    result = []
    for path in sorted(topics_dir.glob('*/topic.json')):
        if path.parent.is_symlink(): raise ValueError('Symlinked topic directories are not allowed')
        manifest = read_json(path)
        if not isinstance(manifest, dict): raise ValueError(str(path) + ': topic.json must contain an object')
        content = read_json(path.parent / 'content.json') if (path.parent / 'content.json').exists() else None
        result.append((manifest, content, path.parent))
    return result


def links(manifest):
    tid = manifest['id']
    output = {'home': './topics/' + tid + '/index.html'}
    if manifest['adapter'] == 'shoulder':
        output.update(reading='./reading.html', claude='./reading-claude.html', pdf='./downloads/shoulder-bilingual.pdf', markdown='./reading.md')
    elif manifest['status'] == 'published':
        output.update(reading='./topics/' + tid + '/reading.html', markdown='./topics/' + tid + '/reading.md')
        if manifest.get('pdf'): output['pdf'] = './topics/' + tid + '/' + manifest['pdf']['file']
    if manifest['viewer']['enabled']:
        output['viewer'] = './?' + urlencode({'topic': tid, 'term': manifest['viewer']['defaultTerm']})
    return output


def esc(value): return html.escape(str(value), quote=True)


def bilingual(value, tag='p', cls=''):
    return f'<{tag} class="bilingual {cls}"><span lang="en">{esc(value["en"])}</span><span lang="zh-CN" class="zh">{esc(value["zh"])}</span></{tag}>'


def md_pair(value): return value['en'] + '\n\n' + value['zh'] + '\n\n'


def shell(manifest, body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(manifest["title"]["en"])} · {esc(manifest["title"]["zh"])}</title>'
            '<link rel="stylesheet" href="../../topic.css"></head><body><header><a href="../../study.html">Anatomy study · 解剖学习</a></header><main>'
            + bilingual(manifest['title'], 'h1') + body + '</main></body></html>')


def render(manifest, content, missing):
    tid, status = manifest['id'], manifest['status']
    entry_links = links(manifest)
    local_link = lambda link: '../../' + link.removeprefix('./')
    # One main entry (course) plus the 3D model; other editions and downloads sit in one quiet line.
    main_labels = {'reading': pair('Start reading', '开始学习'), 'viewer': pair('3D model', '三维模型')}
    extra_labels = {'claude': 'Claude 版', 'pdf': 'PDF', 'markdown': 'Markdown'}
    nav = '<nav class="cards">' + ''.join('<a class="card' + (' primary' if key == 'reading' else '') + '" href="' + esc(local_link(url)) + '">' + bilingual(main_labels[key], 'strong') + '</a>'
                                         for key, url in entry_links.items() if key in main_labels) + '</nav>'
    extras = [(extra_labels[key], url) for key, url in entry_links.items() if key in extra_labels]
    if extras:
        nav += '<p class="more">Other formats · 其他格式：' + ' · '.join('<a href="' + esc(local_link(url)) + '">' + esc(label) + '</a>' for label, url in extras) + '</p>'
    if status == 'draft':
        notice = bilingual(pair('Draft — the course is not yet available.', '草稿：课程尚未完成，不能作为已核验的学习材料。'), 'p', 'notice')
        if manifest['viewer']['enabled']:
            notice += bilingual(pair('The preview contains only the mapped model structures. Muscles, attachment labels and the six-part course still need preparation and review.',
                                     '预览仅包含已匹配的模型结构；肌肉、起止点标注和六部分课程仍需编写与核验。'))
        body = notice + nav + bilingual(pair('Preparation checklist', '待完成项目'), 'h2') + '<ul class="checklist">'
        checklist = [pair('Complete all six bilingual sections.', '完成六部分双语正文。'),
                     pair('Add sourced muscle origins, insertions, courses and actions.', '补齐有来源依据的肌肉起止点、走行与动作。'),
                     pair('Label anatomical diagrams, nerves and bony landmarks.', '在解剖图中标出神经、骨性结构与肌肉起止点。'),
                     pair('Match model links and review any landmark coordinates.', '匹配三维模型链接并核验骨性标志坐标。'),
                     pair('Write complete answers, mnemonics and paper appraisals.', '编写完整答案、简记与论文评析。'),
                     pair('Review sources and desktop/mobile layouts before publication.', '发布前核验来源与桌面、窄屏显示效果。')]
        body += ''.join('<li>' + bilingual(item, 'span') + '</li>' for item in checklist) + '</ul>'
        return shell(manifest, body), shell(manifest, body), '# ' + manifest['title']['en'] + ' · ' + manifest['title']['zh'] + '\n\nDraft · 草稿：课程尚未发布。\n\n'
    if manifest['adapter'] == 'shoulder':
        body = bilingual(manifest['summary']) + nav
        return shell(manifest, body), shell(manifest, body), '# ' + manifest['title']['en'] + ' · ' + manifest['title']['zh'] + '\n\n[Read the maintained course · 阅读维护中的课程](../../reading.md)\n'

    sources = {s['id']: s for s in content['sources']}
    diagrams = {d['id']: d for d in content['diagrams']}
    def source_html(item):
        return '<p class="sources">Sources · 来源: ' + ', '.join('<a href="' + esc(sources[s]['url']) + '">' + esc(sources[s]['title']) + '</a>' for s in item.get('sources', [])) + '</p>'
    def figure(d):
        return '<figure><a href="' + esc(d['file']) + '"><img loading="lazy" src="' + esc(d['file']) + '" alt="' + esc(d['alt']['en'] + ' · ' + d['alt']['zh']) + '"></a>' + bilingual(d['caption'], 'figcaption') + source_html(d) + '</figure>'
    toc = '<nav class="toc">' + ''.join('<a href="#' + s['id'] + '">' + bilingual(s['title'], 'span') + '</a>' for s in content['sections']) + '</nav>'
    body = nav + toc
    md = '# ' + manifest['title']['en'] + ' · ' + manifest['title']['zh'] + '\n\n'
    titles = {'origin': pair('Origin', '起点'), 'insertion': pair('Insertion', '止点'), 'course': pair('Course: from origin to insertion', '从起点到止点的走行'), 'actions': pair('Actions', '动作'), 'innervation': pair('Innervation', '神经支配')}
    for index, section in enumerate(content['sections'], 1):
        body += '<section id="' + section['id'] + '"><h2><small>' + f'{index:02}' + '</small>' + bilingual(section['title'], 'span') + '</h2>' + bilingual(section['overview'])
        md += '## ' + str(index) + '. ' + section['title']['en'] + ' · ' + section['title']['zh'] + '\n\n' + md_pair(section['overview'])
        for block in section.get('blocks', []):
            body += bilingual(block['heading'], 'h3') + bilingual(block['body'])
            md += '### ' + block['heading']['en'] + ' · ' + block['heading']['zh'] + '\n\n' + md_pair(block['body'])
            for term in block.get('termIds', []):
                href = '../../?' + urlencode({'topic': tid, 'term': term})
                body += '<a class="model-link" href="' + esc(href) + '">View in 3D · 查看三维结构: ' + esc(term) + '</a>'
                md += '[View in 3D · 查看三维结构](' + href + ')\n\n'
        if section['id'] == 'innervation':
            for notation in content['nerveNotation'].values():
                body += bilingual(notation, 'p', 'notice')
                md += md_pair(notation)
        if section['id'] in ['anatomy', 'movement']:
            for muscle in content['muscles']:
                body += '<article class="muscle">' + bilingual(muscle['name'], 'h3')
                md += '### ' + muscle['name']['en'] + ' · ' + muscle['name']['zh'] + '\n\n'
                for key in MUSCLE_FIELDS:
                    body += bilingual(titles[key], 'h4') + bilingual(muscle[key])
                    md += '**' + titles[key]['en'] + ' · ' + titles[key]['zh'] + '**\n\n' + md_pair(muscle[key])
                if muscle.get('modelTermId'):
                    href = '../../?' + urlencode({'topic': tid, 'term': muscle['modelTermId']})
                    body += '<a class="model-link" href="' + esc(href) + '">View this muscle in 3D · 查看该肌肉的三维模型</a>'
                    md += '[View this muscle in 3D · 查看该肌肉的三维模型](' + href + ')\n\n'
                else:
                    body += bilingual(muscle['modelUnavailableReason'], 'p', 'notice')
                    md += md_pair(muscle['modelUnavailableReason'])
                for did in muscle['diagramIds']:
                    body += figure(diagrams[did]); md += '![' + diagrams[did]['alt']['en'] + ' · ' + diagrams[did]['alt']['zh'] + '](' + diagrams[did]['file'] + ')\n\n'
                body += source_html(muscle) + '</article>'
        for did in section.get('diagramIds', []):
            body += figure(diagrams[did]); md += '![' + diagrams[did]['alt']['en'] + ' · ' + diagrams[did]['alt']['zh'] + '](' + diagrams[did]['file'] + ')\n\n' + md_pair(diagrams[did]['caption'])
        if section['id'] == 'anatomy':
            for landmark in content['landmarks']:
                body += bilingual(landmark['name'], 'h3') + bilingual(landmark['description']) + source_html(landmark)
                md += '### ' + landmark['name']['en'] + ' · ' + landmark['name']['zh'] + '\n\n' + md_pair(landmark['description'])
                if landmark.get('modelTermId'):
                    query = {'topic': tid, 'term': landmark['modelTermId']}
                    if landmark.get('viewerLandmarkId'): query['landmark'] = landmark['viewerLandmarkId']
                    href = '../../?' + urlencode(query)
                    body += '<a class="model-link" href="' + esc(href) + '">View the bone in 3D · 查看该骨的三维模型</a>'
                    md += '[View the bone in 3D · 查看该骨的三维模型](' + href + ')\n\n'
                if not landmark.get('viewerLandmarkId'):
                    body += bilingual(landmark['modelUnavailableReason'], 'p', 'notice')
                    md += md_pair(landmark['modelUnavailableReason'])
                for did in landmark['diagramIds']:
                    body += figure(diagrams[did]); md += '![' + diagrams[did]['alt']['en'] + ' · ' + diagrams[did]['alt']['zh'] + '](' + diagrams[did]['file'] + ')\n\n'
        if section['id'] == 'review':
            for review in content['review']:
                body += '<details class="answer"><summary>' + bilingual(review['question'], 'span') + '</summary>'
                body += bilingual(pair('Complete answer', '完整答案'), 'h3') + bilingual(review['answer'])
                body += bilingual(pair('Mnemonic', '简记'), 'h4') + bilingual(review['mnemonic']) + source_html(review) + '</details>'
                md += '### ' + review['question']['en'] + '\n\n' + review['question']['zh'] + '\n\n**Complete answer · 完整答案**\n\n' + md_pair(review['answer']) + '**Mnemonic · 简记**\n\n' + md_pair(review['mnemonic'])
        if section['id'] == 'papers':
            paper_labels = {'question': 'Research question · 研究问题', 'design': 'Study design · 研究设计', 'population': 'Population · 研究人群', 'methods': 'Methods · 方法', 'results': 'Results · 结果', 'limitations': 'Limitations · 局限', 'applicability': 'Applicability · 适用范围'}
            for paper in content['papers']:
                body += '<article class="paper"><h3>' + esc(paper['citation']) + '</h3>'
                md += '### ' + paper['citation'] + '\n\n'
                for key in PAPER_FIELDS:
                    body += '<h4>' + paper_labels[key] + '</h4>' + bilingual(paper[key]); md += '**' + paper_labels[key] + '**\n\n' + md_pair(paper[key])
                for term in paper['terms']:
                    body += bilingual(term['term'], 'h4') + bilingual(term['explanation'])
                    md += '**' + term['term']['en'] + ' · ' + term['term']['zh'] + '**\n\n' + md_pair(term['explanation'])
                body += source_html(paper) + '</article>'
        body += '</section>'
    body += '<section id="sources"><h2>Sources · 来源</h2><ul>' + ''.join('<li><a href="' + esc(s['url']) + '">' + esc(s['title']) + '</a></li>' for s in content['sources']) + '</ul></section>'
    md += '## Sources · 来源\n\n' + ''.join('- [' + s['title'] + '](' + s['url'] + ')\n' for s in content['sources'])
    landing = shell(manifest, bilingual(manifest['summary']) + nav)
    return landing, shell(manifest, body), md


def build(topics_dir=None, output=None, root=ROOT):
    output = Path(output or Path(root) / '肩部3D学习/public')
    records = discover(topics_dir, root)
    models = catalog_models(root)
    checked = []
    for manifest, content, path in records:
        errors, missing = validate(manifest, content, path, models, root)
        if errors: raise ValueError(str(manifest.get('id', path.name)) + ':\n  ' + '\n  '.join(errors))
        checked.append((manifest, content, path, missing))
    # Validate the entire catalog before mutating generated outputs.
    output.mkdir(parents=True, exist_ok=True)
    generated = output / 'topics'
    if generated.exists(): shutil.rmtree(generated)
    generated.mkdir()
    catalog = []
    for manifest, content, path, missing in checked:
        target = generated / manifest['id']
        target.mkdir()
        landing, reading, markdown = render(manifest, content, missing)
        (target / 'index.html').write_text(landing, encoding='utf-8')
        (target / 'reading.html').write_text(reading, encoding='utf-8')
        (target / 'reading.md').write_text(markdown, encoding='utf-8')
        public_manifest = dict(manifest, links=links(manifest), missing=missing)
        write_json(target / 'data.json', {'topic': public_manifest, 'content': content if manifest['status'] == 'published' else None})
        if manifest['adapter'] == 'standard' and manifest['status'] == 'published':
            for diagram in content['diagrams']:
                destination = inside(target, diagram['file']); destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(inside(path, diagram['file']), destination)
            if manifest.get('pdf'):
                destination = inside(target, manifest['pdf']['file']); destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(inside(path, manifest['pdf']['file']), destination)
        catalog.append(public_manifest)
    write_json(output / 'topics.json', {'schemaVersion': 1, 'topics': catalog})
    shutil.copy2(Path(root) / 'platform/topic.css', output / 'topic.css')
    return catalog
