"""Figures 11-12: rib movements; breathing and the core cylinder."""
from trunkfig import *  # noqa: F401,F403

HI = '#f3c9a0'


def register(fig):

    @fig('11')
    def handles():
        f = Fig('11', 1800, 1220, 'Rib movements in inspiration: pump handle and bucket handle', '吸气时肋骨的运动：泵柄与桶柄')
        K = 1900
        a = Stage(f, 'lat', 0.0, -1.27, 470, 600, K)
        a.cage(sides=('',), op=0.6); cartilages(a, sides=(1,), op=0.6); a.bones(('manubrium', 'sternum-body', 'xiphoid'), op=0.7)
        for n in range(2, 7): a.shape(BONES[f'rib{n}'], '#a8572a', HI, 1.8, layer='lat-near')
        title(f, 470, 128, 'A. Pump handle: ribs 2–6 (right lateral view)', 'A. 泵柄运动：第 2–6 肋（右侧面观）')
        for n in (2, 4, 6):
            e = LM[f'rib{n}-end']; p = a.P([0, e[1], e[2] + 0.03]); q = a.P([0, e[1] + 0.03, e[2] + 0.05])
            f.arrow(f'M{p[0]:.1f},{p[1]:.1f} Q{p[0] + 30:.1f},{(p[1] + q[1]) / 2:.1f} {q[0]:.1f},{q[1]:.1f}', '#a8572a', 3)
        ax = a.at('rib4-head'); f.circle(ax[0], ax[1], 9, '#8c2f39', '#fff', 2)
        label(f, 40, 215, 'Axis: nearly side to side, through the two posterior joints', '轴：接近左右方向，穿过后方两个关节', '#8c2f39', 'start', 14, to=(ax[0] - 6, ax[1] - 4))
        label(f, 610, 330, 'Front ends and sternum move up and forward', '肋骨前端和胸骨向前上方抬起', '#a8572a', 'start', 14)
        p1, p2 = a.P([0, 1.3, -0.06]), a.P([0, 1.3, 0.125])
        f.path(f'M{p1[0]:.1f},1040 L{p2[0]:.1f},1040', '#444', 2, rough=False)
        f.arrow(f'M{p2[0] - 40:.1f},1040 L{p2[0] + 40:.1f},1040', '#444', 2.4)
        f.bi((p1[0] + p2[0]) / 2, 1072, 'Front-to-back diameter increases', '前后径增大', 15, '#444', 'middle', '700')
        b = Stage(f, 'ant', 0.0, -1.27, 1300, 600, K)
        b.cage(op=0.6); cartilages(b, op=0.6); b.bones(('manubrium', 'sternum-body', 'xiphoid'), op=0.7)
        for n in range(7, 11):
            for side in ('', '-left'): b.shape(BONES[f'rib{n}{side}'], '#a8572a', HI, 1.8, op=0.85)
        title(f, 1300, 128, 'B. Bucket handle: ribs 7–10 (anterior view)', 'B. 桶柄运动：第 7–10 肋（前面观）')
        for sgn in (1, -1):
            for n in (7, 9):
                e = LM[f'rib{n}-lat']; p = b.P([(e[0] - 0.012) * sgn, e[1], 0]); q = b.P([(e[0] - 0.04) * sgn, e[1] + 0.028, 0])
                f.arrow(f'M{p[0]:.1f},{p[1]:.1f} Q{q[0]:.1f},{p[1]:.1f} {q[0]:.1f},{q[1]:.1f}', '#a8572a', 3)
            h, e = LM['rib8-head'], cartilage_line(8)[8]
            p, q = b.P([h[0] * sgn, h[1], 0]), b.P([e[0] * sgn, e[1], 0])
            f.path(f'M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}', '#8c2f39', 2.2, dash='9 6', rough=False)
        label(f, 1010, 1130, 'Dashed lines = axis: nearly front to back, from the spine to the front of the rib', '虚线 = 轴：接近前后方向，从脊柱到肋骨前端', '#8c2f39', 'start', 14)
        f.bi(1300, 205, 'The middle of each rib moves up and out', '肋骨中段向外上方抬起', 14, '#a8572a', 'middle', '700')
        p1, p2 = (b.P([-0.15, 1.0, 0])[0], 1040), (b.P([0.15, 1.0, 0])[0], 1040)
        f.path(f'M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}', '#444', 2, rough=False)
        f.arrow(f'M{p2[0] - 40:.1f},{p2[1]:.1f} L{p2[0] + 40:.1f},{p2[1]:.1f}', '#444', 2.4); f.arrow(f'M{p1[0] + 40:.1f},{p1[1]:.1f} L{p1[0] - 40:.1f},{p1[1]:.1f}', '#444', 2.4)
        f.bi(1300, 1072, 'Side-to-side diameter increases', '左右径增大', 15, '#444', 'middle', '700')
        note(f, 40, 1125, ['Highlighted ribs are the ones named for each movement. Arrows show the direction of movement in inspiration; they are not to scale.'], ['着色的肋骨是各运动对应的肋。箭头表示吸气时的运动方向，不按比例。'])
        f.save('泵柄与桶柄运动')

    @fig('12')
    def breathing_core():
        f = Fig('12', 1800, 1180, 'Breathing and the core cylinder', '呼吸与核心圆筒')
        DI, TA, PF = COLOR['diaphragm'], COLOR['transversus-abdominis'], COLOR['puborectalis']
        K = 1500
        a = Stage(f, 'ant', 0.0, -1.2, 520, 640, K)
        torso(a, ribs=range(1, 13), op=0.5, pelvis=False)
        P = lambda x, y: a.P([x, y, 0])
        ex = [P(x, y) for x, y in [(-0.112, 1.1), (-0.105, 1.2), (-0.075, 1.266), (-0.045, 1.282), (-0.015, 1.27), (0.015, 1.262), (0.045, 1.268), (0.075, 1.25), (0.105, 1.19), (0.112, 1.1)]]
        ins = [P(x, y) for x, y in [(-0.118, 1.085), (-0.112, 1.16), (-0.08, 1.215), (-0.045, 1.232), (-0.015, 1.226), (0.015, 1.22), (0.045, 1.224), (0.08, 1.205), (0.112, 1.15), (0.118, 1.085)]]
        f.raw(f'<path d="{curve(ex)}" fill="none" stroke="{DI}" stroke-width="3.5" stroke-dasharray="10 7"/>')
        f.raw(f'<path d="{curve(ins)}" fill="none" stroke="{DI}" stroke-width="5"/>')
        for x in (-0.05, 0.05):
            p, q = P(x, 1.275), P(x, 1.238); f.arrow(f'M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}', DI, 3)
        for sgn in (1, -1):
            p, q = P(-0.142 * sgn, 1.2), P(-0.172 * sgn, 1.225); f.arrow(f'M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}', '#a8572a', 3)
        ph = [P(-0.02, 1.455), P(-0.03, 1.4), P(-0.045, 1.33), P(-0.04, 1.285)]
        nerve(f, ph, 3.5, smooth=True)
        title(f, 520, 128, 'A. Quiet inspiration (anterior view)', 'A. 平静吸气（前面观）')
        label(f, 40, 290, 'Phrenic nerve (C3–C5)', '膈神经（C3–C5）', '#8a6a10', 'start', 14, to=P(-0.032, 1.39))
        label(f, 40, 420, 'End of expiration (dashed)', '呼气末的膈（虚线）', DI, 'start', 14, to=P(-0.085, 1.252))
        label(f, 40, 540, 'Inspiration: flatter and lower', '吸气时的膈：变平并下降', DI, 'start', 14, to=P(-0.095, 1.195))
        label(f, 790, 330, 'Lower ribs move up and out', '下位肋骨向外上方抬起', '#a8572a', 'start', 14, to=P(0.165, 1.218))
        label(f, 790, 430, 'External intercostals lift the ribs', '肋间外肌上提肋骨', COLOR['external-intercostals'], 'start', 14, to=P(0.125, 1.27))
        note(f, 40, 1010, ['Quiet expiration is passive: the diaphragm relaxes back to the dashed line.', 'The phrenic nerve and both diaphragm positions are schematic.'], ['平静呼气是被动的：膈放松，回到虚线位置。', '膈神经和膈的两个位置均为示意。'])
        # Panel B: core cylinder, schematic sagittal section (anterior to the left)
        title(f, 1320, 128, 'B. The core cylinder (side view, front to the left)', 'B. 核心圆筒（侧面观，前方在左）')
        x0, x1, y0, y1 = 1150, 1480, 330, 860
        f.path(f'M{x0},{y0 + 40} Q{(x0 + x1) / 2},{y0 - 90} {x1},{y0 + 40}', DI, 9, rough=False)                       # diaphragm
        f.path(f'M{x0 + 30},{y1 - 20} Q{(x0 + x1) / 2},{y1 + 70} {x1 - 10},{y1 - 20}', PF, 9, rough=False)              # pelvic floor
        f.path(f'M{x0},{y0 + 50} Q{x0 - 46},{(y0 + y1) / 2} {x0 + 28},{y1 - 26}', TA, 9, rough=False)                    # abdominal wall
        f.path(f'M{x1 + 6},{y0 + 50} Q{x1 + 26},{(y0 + y1) / 2} {x1 - 6},{y1 - 26}', '#365e91', 9, rough=False)         # deep back muscles
        for k in range(5):  # lumbar vertebrae blocks
            yy = y0 + 110 + k * 84; xx = x1 - 62 + (8 - abs(k - 2) * 6)
            f.box(xx - 30, yy, 54, 62, BONE_E, BONE)
        cxm, cym = (x0 + x1) / 2 - 30, (y0 + y1) / 2
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            f.arrow(f'M{cxm + dx * 120:.0f},{cym + dy * 190:.0f} L{cxm + dx * 50:.0f},{cym + dy * 80:.0f}', '#444', 3)
        f.bi(cxm, cym - 8, 'Intra-abdominal', '腹内压', 16, '#444', 'middle', '700'); f.text(cxm, cym + 36, 'pressure', 16, '#444', 'middle', '700')
        label(f, 1530, 300, 'Roof: diaphragm', '顶：膈', DI, 'start', 15, to=((x0 + x1) / 2 + 60, y0 - 18))
        label(f, 1530, 900, 'Floor: pelvic floor', '底：盆底（肛提肌）', PF, 'start', 15, to=((x0 + x1) / 2 + 60, y1 + 20))
        label(f, 870, 620, 'Front and sides: abdominal wall', '前壁和侧壁：腹横肌等腹肌', TA, 'start', 15, to=(x0 - 20, (y0 + y1) / 2))
        label(f, 1530, 560, 'Back: deep back muscles', '后壁：多裂肌等背部深层肌', '#365e91', 'start', 15, to=(x1 + 14, (y0 + y1) / 2 - 30))
        label(f, 1530, 700, 'Lumbar spine', '腰椎', GREY, 'start', 15, to=(x1 - 40, y0 + 310))
        note(f, 880, 1000, ['When the four walls contract together, intra-abdominal pressure rises and the lumbar spine is stiffened.', 'When pressure rises in a cough or a lift, the pelvic floor has to contract with the other walls.'],
             ['四面壁一起收缩时，腹内压升高，腰椎变得稳固。', '咳嗽或提重物使腹内压升高时，盆底要和其他几面壁一起收缩。'])
        f.save('呼吸与核心圆筒')
