#!/usr/bin/env python3
"""Build the hip chapter's numbered SVG figures (AN-10..AN-17) into library/hip/figures/.
Run from the repo root:  python3 library/hip/figures/build-figures.py [figure numbers...]
Base art comes from tools/outlines.json (projected from the 3D model by tools/project-outlines.py)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'tools'))
from hipfig import *  # noqa: F401,F403

OUT_DIR = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else Path(__file__).resolve().parent
set_out(OUT_DIR)
FIGS = {}


def fig(num):
    def wrap(fn): FIGS[num] = fn; return fn
    return wrap


@fig('01')
def bones_overview():
    f = Fig('01', 1740, 1080, 'Right hip bone and femur: anterior, posterior and lateral views', '右侧髋骨与股骨：前面观、后面观与外侧面观')
    K = 1120
    a = Stage(f, 'ant', -0.06, -0.73, 330, 620, K)
    a.bones(('hip-bone', 'sacrum', 'coccyx', 'femur'))
    p = Stage(f, 'post', 0.06, -0.73, 850, 620, K)
    p.bones(('sacrum', 'coccyx', 'hip-bone', 'femur'))
    l = Stage(f, 'lat', -0.01, -0.90, 1500, 470, 1900)
    l.bones(('hip-bone',))
    ac = l.P([-0.12, 0.862, -0.004])
    f.raw(f'<circle cx="{ac[0]:.1f}" cy="{ac[1]:.1f}" r="44" fill="#efe4cc" stroke="{BONE_E}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    for x, y, en, zh in [(-0.03, 0.965, 'Ilium', '髂骨'), (-0.03, 0.825, 'Ischium', '坐骨'), (0.035, 0.84, 'Pubis', '耻骨')]:
        q = l.P([-0.12, y, x]); f.bi(q[0], q[1], en, zh, 15, GREY, 'middle', '700')
    f.bi(330, 150, 'Anterior view', '前面观', 18, INK, 'middle', '700')
    f.bi(850, 150, 'Posterior view', '后面观', 18, INK, 'middle', '700')
    f.bi(1500, 150, 'Lateral view of the hip bone', '髋骨外侧面观', 18, INK, 'middle', '700')
    # anterior labels (person's right = image left)
    label(f, 40, 250, 'Iliac crest', '髂嵴', to=a.at('iliac-crest'))
    label(f, 40, 320, 'ASIS', '髂前上棘', to=a.at('asis'))
    label(f, 40, 390, 'AIIS', '髂前下棘', to=a.at('aiis'))
    label(f, 40, 450, 'Femoral head', '股骨头', to=a.at('femoral-head'))
    label(f, 40, 520, 'Greater trochanter', '大转子', to=a.at('greater-trochanter'))
    label(f, 40, 590, 'Femoral neck', '股骨颈', to=a.P([-0.105, 0.845, 0.0]))
    label(f, 40, 660, 'Lesser trochanter', '小转子', to=a.at('lesser-trochanter'))
    label(f, 440, 250, 'Iliac fossa', '髂窝', to=a.P([-0.075, 0.955, 0.0]))
    label(f, 440, 470, 'Pubic tubercle', '耻骨结节', to=a.at('pubic-tubercle'))
    label(f, 440, 560, 'Obturator foramen', '闭孔', to=a.P([-0.045, 0.825, 0.03]))
    label(f, 440, 630, 'Ischiopubic ramus', '坐耻骨支', to=a.P([-0.03, 0.805, 0.02]))
    label(f, 440, 880, 'Adductor tubercle', '收肌结节', to=a.at('adductor-tubercle'))
    # posterior labels (person's right = image right)
    label(f, 985, 250, 'Iliac crest', '髂嵴', to=p.at('iliac-crest'))
    label(f, 690, 320, 'PSIS', '髂后上棘', anchor='end', to=p.at('psis'))
    label(f, 690, 420, 'Greater sciatic notch', '坐骨大切迹', anchor='end', to=p.P([-0.06, 0.885, -0.07]))
    label(f, 690, 600, 'Ischial tuberosity', '坐骨结节', anchor='end', to=p.at('ischial-tuberosity'))
    label(f, 985, 480, 'Greater trochanter', '大转子', to=p.at('greater-trochanter'))
    label(f, 985, 600, 'Intertrochanteric crest', '转子间嵴', to=p.P([-0.115, 0.82, -0.03]))
    label(f, 985, 720, 'Gluteal tuberosity', '臀肌粗隆', to=p.P([-0.118, 0.76, -0.03]))
    label(f, 985, 860, 'Linea aspera', '股骨粗线', to=p.P([-0.085, 0.62, -0.035]))
    # lateral labels
    label(f, 1700, 760, 'Acetabulum', '髋臼', anchor='end', to=(ac[0] + 20, ac[1] + 20))
    label(f, 1330, 470, 'Greater sciatic notch', '坐骨大切迹', anchor='end', to=l.P([-0.12, 0.89, -0.045]))
    label(f, 1330, 560, 'Ischial spine', '坐骨棘', anchor='end', to=l.P([-0.12, 0.86, -0.061]))
    label(f, 1330, 640, 'Lesser sciatic notch', '坐骨小切迹', anchor='end', to=l.P([-0.12, 0.848, -0.064]))
    label(f, 1700, 250, 'ASIS', '髂前上棘', anchor='end', to=l.at('asis'))
    note(f, 1240, 960, ['Sciatic notches + ligaments = foramina (see 02).'], ['坐骨切迹加上韧带围成坐骨大孔、小孔（见图 02）。'])
    f.save('右侧髋骨与股骨')


if __name__ == '__main__':
    want = [a for a in sys.argv[1:] if a[:1].isdigit()] or sorted(FIGS)
    for n in want:
        FIGS[n](); print('built', n)
