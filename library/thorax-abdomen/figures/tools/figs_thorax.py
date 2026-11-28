"""Figures 03-04: intercostal space layers with transversus thoracis; diaphragm and its openings."""
from trunkfig import *  # noqa: F401,F403

VEIN, ART = '#3f6fb0', '#c0392b'


def register(fig):

    @fig('03')
    def intercostal():
        f = Fig('03', 1800, 1560, 'Intercostal space: three muscle layers and the neurovascular bundle', '肋间隙：三层肌与血管神经束')
        EI, II, IM, TT = (COLOR[k] for k in ('external-intercostals', 'internal-intercostals', 'innermost-intercostals', 'transversus-thoracis'))
        # Panel A: lateral window view of two spaces
        title(f, 420, 128, 'A. Right chest wall from the side, layers opened in windows', 'A. 右侧胸壁侧面观，分窗显示各层')
        x0, x1 = 80, 760
        ribs_y = [(200, 262), (410, 472), (620, 682)]
        for (a, b), n in zip(ribs_y, ('Rib 5', 'Rib 6', 'Rib 7')):
            f.path(f'M{x0},{a} L{x1},{a + 14} L{x1},{b + 14} L{x0},{b} Z', BONE_E, 1.6, BONE)
            f.text(x0 + 16, (a + b) / 2 + 6, n, 14, '#7a6a55', 'start', '700')
        wins = [(x0 + 110, x0 + 300, EI, 52, 'external-intercostals'), (x0 + 310, x0 + 490, II, 128, 'internal-intercostals'), (x0 + 500, x1, IM, 128, 'innermost-intercostals')]
        for k, ((a, b), (c, d)) in enumerate(zip(ribs_y, ribs_y[1:])):
            for wx0, wx1, col, ang, mid in wins:
                sl = lambda x: 14 * (x - x0) / (x1 - x0)
                pts = [(wx0, b + sl(wx0)), (wx1, b + sl(wx1)), (wx1, c + sl(wx1)), (wx0, c + sl(wx0))]
                poly(f, pts, col, tint(col), 1.6)
                hatch(f, pts, col, ang, 11, 1.4)
                if k == 0:
                    oc, ic = ((wx0 + wx1) / 2, b + sl((wx0 + wx1) / 2)), ((wx0 + wx1) / 2, c + sl((wx0 + wx1) / 2))
                    area(f, [(wx0 + 14, pts[0][1] + 2), (wx1 - 14, pts[1][1] + 2)], ORIGIN_C); area(f, [(wx0 + 14, pts[3][1] - 2), (wx1 - 14, pts[2][1] - 2)], INSERT_C)
                    tag(f, oc[0], oc[1] + 30, 'O', ORIGIN_C); tag(f, ic[0], ic[1] - 30, 'I', INSERT_C)
                else: tag(f, (wx0 + wx1) / 2, (b + c) / 2 + 6, LETTER[mid], col, 15)
        f.bi(x0 + 205, 760, 'External layer: fibres run down and forward', '外层：纤维向前下', 13, EI, 'middle', '700')
        f.bi(x0 + 400, 810, 'Internal layer: fibres run down and back', '中层：纤维向后下', 13, II, 'middle', '700')
        f.bi(x0 + 590, 760, 'Innermost layer: same direction as internal', '最内层：方向同肋间内肌', 13, IM, 'middle', '700')
        f.arrow(f'M{x0 + 250},880 L{x0 + 520},880', GREY, 2); f.bi(x0 + 385, 905, 'Anterior (toward the sternum)', '向前（朝胸骨）', 13, GREY, 'middle', '600')
        # Panel B: vertical section through one space
        title(f, 1290, 128, 'B. Vertical section through one space', 'B. 一个肋间隙的纵切面')
        cx = 1250
        f.bi(1000, 205, 'Outside (skin)', '外（皮肤侧）', 14, GREY, 'middle', '700'); f.bi(1560, 205, 'Inside (lung)', '内（肺侧）', 14, GREY, 'middle', '700')
        up = f'M{cx - 46},250 Q{cx + 60},240 {cx + 52},330 Q{cx + 50},372 {cx + 34},384 Q{cx + 20},360 {cx - 2},372 Q{cx - 40},380 {cx - 50},330 Z'
        lo = f'M{cx - 46},640 Q{cx + 56},628 {cx + 52},720 Q{cx + 40},776 {cx},772 Q{cx - 44},770 {cx - 50},715 Z'
        # layers between the ribs
        ext = [(cx - 44, 372), (cx - 10, 374), (cx - 10, 640), (cx - 44, 646)]
        inn = [(cx - 8, 374), (cx + 18, 362), (cx + 18, 636), (cx - 8, 640)]
        im = [(cx + 36, 384), (cx + 54, 330), (cx + 62, 330), (cx + 60, 700), (cx + 50, 660), (cx + 36, 636)]
        poly(f, ext, EI, tint(EI)); poly(f, inn, II, tint(II)); poly(f, im, IM, tint(IM))
        f.path(up, BONE_E, 1.8, BONE); f.path(lo, BONE_E, 1.8, BONE)
        f.text(cx - 10, 310, 'Rib above', 13, '#7a6a55', 'middle', '700'); f.text(cx - 2, 708, 'Rib below', 13, '#7a6a55', 'middle', '700')
        f.text(cx - 10, 328, '上位肋', 12, ZH, 'middle', '400', 'zh-CN'); f.text(cx - 2, 726, '下位肋', 12, ZH, 'middle', '400', 'zh-CN')
        f.path(f'M{cx + 74},240 L{cx + 74},790', '#8a8f6a', 2.2, rough=False); f.path(f'M{cx + 88},240 L{cx + 88},790', '#b0567a', 2.6, rough=False)
        for yy, col, t in ((398, VEIN, 'V'), (426, ART, 'A'), (454, NERVE, 'N')):
            f.circle(cx + 27, yy, 11, col, '#fff', 2); f.text(cx + 27, yy + 4.5, t, 12, '#fff', 'middle', '700')
        for yy, col in ((606, NERVE), (620, ART)): f.circle(cx + 27, yy, 5, col, '#fff', 1.5)
        f.arrow(f'M{cx - 330},585 L{cx - 60},630', '#444', 2.2, dash='7 5')
        f.bi(cx - 400, 545, 'Needle or drain: upper border of the rib below', '针或引流管：沿下位肋的上缘进入', 13, '#444', 'start', '700')
        R = 1440
        label(f, R, 300, 'Costal groove', '肋沟', INK, 'start', 14, to=(cx + 30, 372))
        label(f, R, 380, 'Intercostal vein, artery, nerve (VAN, top to bottom)', '肋间静脉、动脉、神经（自上而下）', NERVE, 'start', 14, to=(cx + 39, 426))
        label(f, R, 470, 'Innermost intercostals', '肋间最内肌', IM, 'start', 14, to=(cx + 56, 500))
        label(f, R, 540, 'Endothoracic fascia', '胸内筋膜', '#6d7250', 'start', 14, to=(cx + 74, 560))
        label(f, R, 610, 'Parietal pleura', '壁层胸膜', '#b0567a', 'start', 14, to=(cx + 88, 630))
        label(f, R, 690, 'Collateral branches', '侧副支', GREY, 'start', 14, to=(cx + 33, 612))
        label(f, 900, 400, 'External intercostals', '肋间外肌', EI, 'start', 14, to=(cx - 30, 440))
        label(f, 900, 470, 'Internal intercostals', '肋间内肌', II, 'start', 14, to=(cx + 4, 490))
        # Panel C: transversus thoracis from behind
        title(f, 420, 990, 'C. Transversus thoracis: back of the sternum, seen from inside the chest', 'C. 胸横肌：从胸腔内向前看胸骨后面')
        s = Stage(f, 'post', 0.0, -1.31, 350, 1235, 2600)
        for n in range(2, 8):
            for side in ('', '-left'): clip = None
        clip_begin(f, 50, 1040, 600, 430)
        for n in range(2, 8):
            for side in ('', '-left'): s.shape(BONES[f'rib{n}{side}'], BONE_E, SHADE, 1.3, layer='ant-front')
        cartilages(s, ribs=range(2, 8), w=13)
        s.bones(('manubrium', 'sternum-body', 'xiphoid'))
        for sgn in (1, -1):
            for n, oy in zip(range(2, 7), (1.264, 1.255, 1.246, 1.237, 1.228)):
                c = cartilage_line(n)[6]
                o = [s.P([-0.004 * sgn, oy + 0.004, 0.1]), s.P([-0.004 * sgn, oy - 0.004, 0.1])]
                i = [s.P([c[0] * sgn, c[1] + 0.004, c[2]]), s.P([c[0] * sgn, c[1] - 0.004, c[2]])]
                f.path(smooth_band(o, i), TT, 1.5, tint(TT), op=0.88)
        f.end()
        o_pts = [s.P([0.0, 1.268, 0.1]), s.P([0.0, 1.228, 0.1])]
        c2, c6 = cartilage_line(2)[6], cartilage_line(6)[6]
        i_pts = [s.P(c2), s.P(cartilage_line(4)[6]), s.P(c6)]
        oi(f, o_pts, i_pts)
        tag(f, *s.P([0.03, 1.275, 0.1]), 'TT', TT, 15)
        label(f, 665, 1090, 'Costal cartilage 2', '第 2 肋软骨', CART_E, 'start', 14, to=s.P([-c2[0], c2[1], c2[2]]))
        label(f, 665, 1430, 'Xiphoid process', '剑突', INK, 'start', 14, to=s.P([0.0, 1.232, 0.1]))
        y = legend_oi(f, 860, 1010, [
            ('external-intercostals', 'inferior border of the rib above', '上位肋下缘', 'superior border of the rib below', '下位肋上缘'),
            ('internal-intercostals', 'costal groove of the rib above', '上位肋的肋沟', 'superior border of the rib below, deep layer', '下位肋上缘（深层）')])
        legend_oi(f, 1330, 1010, [
            ('innermost-intercostals', 'inner lip of the costal groove above', '上位肋肋沟内唇', 'inner surface of the rib below', '下位肋内面'),
            ('transversus-thoracis', 'back of the lower sternum and xiphoid', '胸骨体下部和剑突后面', 'inner surfaces of costal cartilages 2–6', '第 2–6 肋软骨内面')])
        key_oi(f, 870, 1290)
        note(f, 860, 1350, ['Panels A and B are schematic. In panel C the model has no costal cartilages or transversus thoracis;', 'both are drawn in schematically on the model sternum.'],
             ['A、B 两图为示意。C 图中模型没有肋软骨和胸横肌，', '两者都是在模型的胸骨上示意补画的。'])
        f.save('肋间隙三层肌与血管神经束')

    @fig('04')
    def diaphragm():
        f = Fig('04', 1700, 1250, 'Diaphragm: domes, central tendon and the three openings (anterior view)', '膈：穹窿、中心腱与三个裂孔（前面观）')
        DI = COLOR['diaphragm']
        K = 2700
        a = Stage(f, 'ant', 0.0, -1.19, 800, 640, K)
        a.cage(ribs=range(6, 13), vertebrae=['t7', 't8', 't9', 't10', 't11', 't12', 'l1', 'l2', 'l3'], sternum=False, op=0.55)
        cartilages(a, ribs=range(6, 11), op=0.5)
        a.bones(('sternum-body', 'xiphoid'), op=0.6)
        P = a.P
        rim_r = [[-0.004, 1.236, 0.1]] + [cartilage_line(7)[k] for k in (9, 6, 3)] + [LM['rib8-end'], LM['rib9-end'], LM['rib10-end'], LM['rib11-end']]
        top = [[-0.112, 1.1, 0], [-0.108, 1.2, 0], [-0.08, 1.264, 0], [-0.045, 1.282, 0], [-0.015, 1.27, 0], [0.015, 1.262, 0], [0.045, 1.268, 0], [0.08, 1.25, 0], [0.108, 1.19, 0], [0.112, 1.1, 0]]
        back = [[0.1, 1.068, 0], [0.06, 1.082, 0], [0.03, 1.1, 0], [0.0, 1.106, 0], [-0.03, 1.1, 0], [-0.06, 1.082, 0], [-0.1, 1.068, 0]]
        f.path(blob([P(p) for p in top + back], 0.45), DI, 1.8, tint(DI), op=0.78)
        ct = [P(p) for p in ([-0.05, 1.262, 0], [-0.025, 1.274, 0], [0.0, 1.262, 0], [0.03, 1.262, 0], [0.055, 1.25, 0], [0.03, 1.238, 0], [0.0, 1.244, 0], [-0.03, 1.24, 0])]
        f.path(blob(ct), '#8a7d6a', 1.5, '#f3ead8', op=0.95)
        # crura
        for sgn, low in ((-1, 'l3-body'), (1, 'l2-body')):
            o = [P([0.012 * sgn, LM[low][1] - 0.008, 0]), P([0.022 * sgn, LM[low][1] + 0.01, 0])]
            i = [P([0.006 * sgn, 1.165, 0]), P([0.03 * sgn, 1.17, 0])]
            f.path(smooth_band(o, i), DI, 1.6, tint(DI, 0.5), op=0.9)
        # openings
        cav, oes, aor = P([-0.024, LM['t8-body'][1], 0]), P([0.012, LM['t10-body'][1], 0]), P([0.0, LM['t12-body'][1], 0])
        f.raw(f'<ellipse cx="{cav[0]:.1f}" cy="{cav[1]:.1f}" rx="26" ry="19" fill="#3f6fb0" stroke="#fff" stroke-width="2.5"/>')
        f.raw(f'<ellipse cx="{oes[0]:.1f}" cy="{oes[1]:.1f}" rx="21" ry="16" fill="#c9a36a" stroke="#fff" stroke-width="2.5"/>')
        f.raw(f'<ellipse cx="{aor[0]:.1f}" cy="{aor[1]:.1f}" rx="24" ry="18" fill="#c0392b" stroke="#fff" stroke-width="2.5"/>')
        # arcuate ligaments
        for sgn in (-1, 1):
            m0, m1, l1 = P([0.024 * sgn, 1.125, 0]), P([0.058 * sgn, 1.118, 0]), P([0.098 * sgn, 1.09, 0])
            f.path(f'M{m0[0]:.1f},{m0[1]:.1f} Q{(m0[0] + m1[0]) / 2:.1f},{m0[1] - 46:.1f} {m1[0]:.1f},{m1[1]:.1f}', '#5b4a7a', 3, rough=False)
            f.path(f'M{m1[0]:.1f},{m1[1]:.1f} Q{(l1[0] + m1[0]) / 2:.1f},{m1[1] - 50:.1f} {l1[0]:.1f},{l1[1]:.1f}', '#5b4a7a', 3, rough=False)
        title(f, 800, 128, 'Anterior view; the ribs and sternum are drawn faint', '前面观；肋骨和胸骨画得较淡')
        L, R = 60, 1290
        for lvl, q, en, zh, col in (('t8', cav, 'Caval opening, T8: inferior vena cava', '腔静脉孔，平 T8：下腔静脉', '#3f6fb0'), ('t10', oes, 'Oesophageal hiatus, T10: oesophagus, vagal trunks', '食管裂孔，平 T10：食管、迷走神经干', '#9a7434'),
                                    ('t12', aor, 'Aortic hiatus, T12: aorta, thoracic duct, azygos vein', '主动脉裂孔，平 T12：主动脉、胸导管、奇静脉', '#c0392b')):
            label(f, R - 60, q[1] - 6, en, zh, col, 'start', 14, to=(q[0] + 24, q[1]))
        label(f, L, 300, 'Right dome (higher, over the liver)', '右穹窿（较高，下方是肝）', DI, 'start', 14, to=P([-0.05, 1.28, 0]))
        label(f, R - 60, 300, 'Left dome', '左穹窿', DI, 'start', 14, to=P([0.05, 1.266, 0]))
        label(f, L, 400, 'Central tendon', '中心腱', '#6b5f4c', 'start', 14, to=P([-0.04, 1.255, 0]))
        label(f, L, 520, 'Costal part: from the lower six costal cartilages and ribs', '肋部：起自下 6 对肋软骨和肋骨', DI, 'start', 14, to=P([-0.1, 1.17, 0]))
        label(f, L, 250, 'Sternal part: from the xiphoid process', '胸骨部：起自剑突', DI, 'start', 14, to=P([-0.003, 1.238, 0]))
        label(f, L, 940, 'Right crus: L1–L3 vertebrae', '右膈脚：第 1–3 腰椎', DI, 'start', 14, to=P([-0.018, 1.09, 0]))
        label(f, R - 60, 1010, 'Left crus: L1–L2 vertebrae', '左膈脚：第 1–2 腰椎', DI, 'start', 14, to=P([0.018, 1.1, 0]))
        label(f, L, 780, 'Medial arcuate ligament (over psoas major)', '内侧弓状韧带（跨过腰大肌）', '#5b4a7a', 'start', 14, to=P([-0.04, 1.132, 0]))
        label(f, L, 860, 'Lateral arcuate ligament (over quadratus lumborum)', '外侧弓状韧带（跨过腰方肌）', '#5b4a7a', 'start', 14, to=P([-0.078, 1.115, 0]))
        oi(f, [P(p) for p in rim_r[1:8]], [ct[0], ct[7]])
        legend_oi(f, 60, 1040, [('diaphragm', 'xiphoid process, lower six costal cartilages and ribs, L1–L3 vertebrae (crura)', '剑突、下 6 对肋软骨和肋骨、第 1–3 腰椎（膈脚）', 'central tendon', '中心腱')])
        key_oi(f, 760, 1070)
        note(f, 760, 1120, ['The model has no diaphragm; the muscle, its tendon and the openings are drawn schematically on the model bones.', 'Each opening is placed at the height of its vertebra.'],
             ['模型没有膈；肌、中心腱和裂孔都是在模型骨骼上示意画的。', '每个裂孔画在对应椎体的高度。'])
        f.save('膈与三个裂孔')
