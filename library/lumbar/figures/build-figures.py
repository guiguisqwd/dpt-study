#!/usr/bin/env python3
"""Build the lumbar chapter's numbered SVG figures (AN-10..AN-17) into library/lumbar/figures/.
Run from the repo root:  python3 library/lumbar/figures/build-figures.py [figure numbers...] [--out DIR]
Base art comes from tools/outlines.json (projected from the 3D model by tools/project-outlines.py).
Figures are registered by the modules in tools/figs_*.py; each module has register(fig)."""
import importlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'tools'))
import lumbarfig  # noqa: E402

OUT_DIR = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else Path(__file__).resolve().parent
lumbarfig.set_out(OUT_DIR)
FIGS = {}


def fig(num):
    def wrap(fn): FIGS[num] = fn; return fn
    return wrap


for path in sorted((Path(__file__).resolve().parent / 'tools').glob('figs_*.py')):
    importlib.import_module(path.stem).register(fig)

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--') and a != str(OUT_DIR)]
    for num in sorted(FIGS):
        if args and num not in args: continue
        FIGS[num]()
        print('built', num)
    if not args and OUT_DIR == Path(__file__).resolve().parent:
        rows = {num: {'oi': [dict(zip(['muscleId', 'originEn', 'originZh', 'insertionEn', 'insertionZh'], r))
                             for r in lumbarfig.LABELS.get(num, [])],
                      'labels': [{'en': en, 'zh': zh} for en, zh in dict.fromkeys(lumbarfig.TEXTS.get(num, []))]}
                for num in sorted(set(lumbarfig.LABELS) | set(lumbarfig.TEXTS))}
        (OUT_DIR / 'figure-labels.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
