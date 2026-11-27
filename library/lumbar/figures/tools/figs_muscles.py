"""Figures 04-07: back muscles, their origins and insertions (posterior and anterior views).
O/I label texts are the short figure labels; content.json diagram labels repeat them (figure-labels.json)."""
from lumbarfig import *  # noqa: F401,F403

RIBS = ('rib6', 'rib7', 'rib8', 'rib9', 'rib10', 'rib11', 'rib12')
THOR = ('t6', 't7', 't8', 't9', 't10', 't11', 't12')
LUMB = ('l1', 'l2', 'l3', 'l4', 'l5')


def off(name, dx=0.0, dy=0.0, dz=0.0):
    p = LM[name]; return [p[0] + dx, p[1] + dy, p[2] + dz]


def back_panel(f, cx, cy, K, levels=THOR + LUMB, ribs=RIBS, both=True, clip=None, my=-1.1):
    """Posterior view skeleton for muscle panels; returns the Stage."""
    st = Stage(f, 'post', 0.0, my, cx, cy, K)
    if clip: clip_begin(f, *clip)
    low = st.P2(0, -0.865)[1]
    clip_begin(f, cx - 600, 0, 1200, low); st.bones(('hip-bone', 'hip-bone-left')); f.end()
    st.bones(tuple(ribs) + (tuple(r + '-left' for r in ribs) if both else ()))
    st.spine(levels)
    if clip: f.end()
    return st


def register(fig):

    @fig('04')
    def erector_spinae():
        f = Fig('04', 1750, 1290, 'Erector spinae: iliocostalis lumborum, longissimus thoracis and spinalis thoracis (posterior view, right side)',
                '竖脊肌：腰髂肋肌、胸最长肌与胸棘肌（后面观，右侧）')
        K, cy = 1450, 600
        panels = {}
        for i, (mid, cx) in enumerate([('iliocostalis-lumborum', 300), ('longissimus-thoracis', 875), ('spinalis-thoracis', 1450)]):
            st = back_panel(f, cx, cy, K, clip=(cx - 285, 170, 570, 800))
            name = name_of(mid)
            f.bi(cx, 160, name['en'], name['zh'], 18, COLOR[mid], 'middle', '700')
            panels[mid] = st
        # Iliocostalis lumborum: lateral column, iliac crest → angles of the lower ribs
        st = panels['iliocostalis-lumborum']
        st.band('iliocostalis-lumborum', [off('iliac-crest-post', dx=-0.022, dy=0.004), off('psis', dx=-0.004)],
                [off('rib7-angle', dx=0.008), off('rib7-angle', dx=-0.012)], bow=22)
        oi(f, [st.at('psis'), st.at('iliac-crest-post'), st.P(off('iliac-crest-post', dx=-0.015, dy=0.006))],
           [st.at(f'rib{n}-angle') for n in range(6, 13)], LETTER['iliocostalis-lumborum'], LETTER['iliocostalis-lumborum'])
        area(f, [st.at(f'{lv}-tp') for lv in ('l1', 'l2', 'l3', 'l4')], INSERT_C)  # lumbar part: L1–L4 transverse processes
        # Longissimus thoracis: intermediate column, sacrum and lumbar processes → thoracic transverse processes and ribs
        st = panels['longissimus-thoracis']
        st.band('longissimus-thoracis', [off('median-sacral-crest', dx=-0.006, dy=0.02), off('psis', dx=0.008)],
                [off('t6-tp', dx=0.004), off('rib6-angle', dx=0.025)], bow=10)
        oi(f, [st.P(off('median-sacral-crest', dx=-0.008, dy=0.03)), st.P(off('median-sacral-crest', dx=-0.012, dy=0.0)), st.at('psis', dx=0.006)],
           [st.at(f'{t}-tp') for t in THOR], LETTER['longissimus-thoracis'], LETTER['longissimus-thoracis'])
        # Spinalis thoracis: medial column, spinous processes T11–L2 → upper thoracic spinous processes
        st = panels['spinalis-thoracis']
        st.band('spinalis-thoracis', [off('l2-sp', dx=-0.003), off('l2-sp', dx=-0.011)], [off('t6-sp', dx=-0.003), off('t6-sp', dx=-0.010)], bow=6)
        oi(f, [st.at(f'{lv}-sp') for lv in ('t11', 't12', 'l1', 'l2')], [st.at(f'{t}-sp') for t in ('t6', 't7', 't8')],
           LETTER['spinalis-thoracis'], LETTER['spinalis-thoracis'])
        key_oi(f, 60, 1015)
        legend_oi(f, 40, 1075, [('iliocostalis-lumborum', 'sacrum, iliac crest and thoracolumbar fascia', '骶骨、髂嵴和胸腰筋膜',
                                 'lower rib angles and L1–L4 transverse processes', '下部肋角和 L1–L4 横突')])
        legend_oi(f, 610, 1075, [('longissimus-thoracis', 'sacrum, iliac crest and lumbar processes', '骶骨、髂嵴和腰椎突起',
                                  'thoracic transverse processes and lower ribs', '胸椎横突和下部肋骨')])
        legend_oi(f, 1180, 1075, [('spinalis-thoracis', 'spinous processes T11–L2', 'T11–L2 棘突', 'spinous processes T2–T8', 'T2–T8 棘突')])
        note(f, 40, 1215, ['Not shown: attachments above T6 (rib 5, the T1–T5 transverse processes and the T2–T5 spinous processes) lie above the panels; sources differ on the exact ribs.'],
             ['图中未显示：T6 以上的附着（第 5 肋、T1–T5 横突、T2–T5 棘突）在画面上方；具体到哪几根肋骨，各来源说法不一。'])
        f.save('竖脊肌起点与止点')

    @fig('05')
    def multifidus_rotatores():
        f = Fig('05', 1700, 1180, 'Multifidus and rotatores (posterior view)', '多裂肌与回旋肌（后面观）')
        st = back_panel(f, 520, 600, 2600, levels=('t12',) + LUMB, ribs=('rib12',), clip=(80, 200, 880, 900), my=-1.035)
        # Multifidus fascicles on the right side (image right): spinous process → mammillary processes / sacrum / PSIS below
        mf = COLOR['multifidus']
        fasc = [('l1', ['l3-mammillary', 'l4-mammillary']), ('l2', ['l4-mammillary', 'l5-mammillary']),
                ('l3', ['l5-mammillary', 'sac1']), ('l4', ['sac1', 'sac2']), ('l5', ['sac2', 'psis'])]
        LM['sac1'] = [-0.017, 0.955, -0.08]; LM['sac2'] = [-0.021, 0.925, -0.085]
        for lv, targets in fasc:
            for t in targets:
                strip(f, [st.at(f'{lv}-sp', dx=-0.002), st.at(t)], mf, 9, 0.55)
        oi(f, [st.at(t) for t in ('l3-mammillary', 'l4-mammillary', 'l5-mammillary', 'sac1', 'sac2', 'psis')],
           [st.at(f'{lv}-sp') for lv in LUMB], LETTER['multifidus'], LETTER['multifidus'])
        # Rotatores on the left side (image left): transverse process root → lamina of the vertebra above
        ro = COLOR['rotatores']
        for up, lo in [('l1', 'l2'), ('l2', 'l3'), ('l3', 'l4'), ('l4', 'l5')]:
            strip(f, [st.P(mirror(LM[f'{lo}-tp-root'])), st.P(mirror(LM[f'{up}-lamina']))], ro, 8, 0.6)
        oi(f, [st.P(mirror(LM[f'{lv}-tp-root'])) for lv in ('l2', 'l3', 'l4', 'l5')],
           [st.P(mirror(LM[f'{lv}-lamina'])) for lv in ('l1', 'l2', 'l3', 'l4')], LETTER['rotatores'], LETTER['rotatores'])
        f.bi(300, 160, 'Rotatores (drawn on the left side)', '回旋肌（画在左侧）', 15, ro, 'middle', '700')
        f.bi(740, 160, 'Multifidus (drawn on the right side)', '多裂肌（画在右侧）', 15, mf, 'middle', '700')
        key_oi(f, 1000, 220)
        legend_oi(f, 1000, 320, [('multifidus', 'mammillary processes, sacrum and PSIS', '乳突、骶骨和髂后上棘', 'spinous processes 2–5 levels above', '上方 2–5 个节段的棘突'),
                                 ('rotatores', 'transverse process', '横突', 'lamina of the vertebra above', '上一位椎骨的椎弓板')])
        note(f, 1000, 620, ['Both muscles are paired; each is drawn on one side only.', 'Lumbar rotatores are often inconsistent; deep multifidus fibres may replace them.'],
             ['两块肌肉都是左右成对的，图中各只画一侧。', '腰部回旋肌常不恒定，可被多裂肌深层纤维取代。'])
        f.save('多裂肌与回旋肌起点与止点')

    @fig('06')
    def segmental_spi():
        f = Fig('06', 1700, 1120, 'Interspinales, intertransversarii and serratus posterior inferior (posterior view)',
                '棘间肌、横突间肌与下后锯肌（后面观）')
        st = back_panel(f, 450, 500, 1900, levels=('t8', 't9', 't10', 't11', 't12') + LUMB[:3], ribs=('rib8', 'rib9', 'rib10', 'rib11', 'rib12'),
                        clip=(60, 200, 780, 620), my=-1.16)
        sp = COLOR['serratus-posterior-inferior']
        LM['spi-ins'] = [off('rib9-angle', dx=-0.025, dy=-0.02), off('rib12-tip', dx=0.012, dy=0.03)]
        o = [st.at('l2-sp', dx=-0.003), st.at('t11-sp', dx=-0.003)]
        i = [st.P(off('rib12-angle', dx=-0.02, dy=-0.012)), st.P(off('rib9-angle', dx=-0.018, dy=-0.02))]
        f.path(smooth_band(o, i, 10), sp, 1.6, tint(sp), op=0.85)
        oi(f, [st.at(f'{lv}-sp') for lv in ('t11', 't12', 'l1', 'l2')],
           [st.P(off(f'rib{n}-angle', dx=-0.02, dy=-0.014)) for n in (9, 10, 11, 12)], LETTER['serratus-posterior-inferior'], LETTER['serratus-posterior-inferior'])
        f.bi(450, 170, 'Serratus posterior inferior (right side)', '下后锯肌（右侧）', 16, sp, 'middle', '700')

        s2 = back_panel(f, 1270, 500, 2600, levels=LUMB, ribs=(), clip=(900, 200, 760, 620), my=-1.055)
        isp, itr = COLOR['interspinales'], COLOR['intertransversarii']
        for up, lo in [('l1', 'l2'), ('l2', 'l3'), ('l3', 'l4'), ('l4', 'l5')]:
            strip(f, [s2.at(f'{lo}-sp', dy=0.004), s2.at(f'{up}-sp', dy=-0.002)], isp, 9, 0.6)
            strip(f, [s2.at(f'{lo}-tp', dx=0.006), s2.at(f'{up}-tp', dx=0.006)], itr, 8, 0.6)
            strip(f, [s2.P(mirror(off(f'{lo}-tp', dx=0.006))), s2.P(mirror(off(f'{up}-tp', dx=0.006)))], itr, 8, 0.6)
        oi(f, [s2.at(f'{lv}-sp', dy=0.006) for lv in ('l2', 'l3', 'l4', 'l5')], [s2.at(f'{lv}-sp', dy=-0.004) for lv in ('l1', 'l2', 'l3', 'l4')],
           LETTER['interspinales'], LETTER['interspinales'])
        oi(f, [s2.at(f'{lv}-tp', dy=-0.003) for lv in ('l1', 'l2', 'l3', 'l4')], [s2.at(f'{lv}-tp') for lv in ('l2', 'l3', 'l4', 'l5')],
           LETTER['intertransversarii'], LETTER['intertransversarii'])
        f.bi(1270, 170, 'Interspinales and intertransversarii', '棘间肌与横突间肌', 16, INK, 'middle', '700')
        key_oi(f, 60, 860)
        legend_oi(f, 40, 930, [('serratus-posterior-inferior', 'spinous processes T11–L2', 'T11–L2 棘突', 'inferior borders of ribs 9–12', '第 9–12 肋下缘')])
        legend_oi(f, 900, 930, [('interspinales', 'spinous process below', '下位棘突', 'spinous process above', '上位棘突')])
        legend_oi(f, 1300, 930, [('intertransversarii', 'transverse process above (L1–L4)', '上位横突（L1–L4）', 'transverse process below (L2–L5)', '下位横突（L2–L5）')])
        f.save('棘间肌横突间肌与下后锯肌')

    @fig('07')
    def ql_psoas():
        f = Fig('07', 1700, 1200, 'Quadratus lumborum and psoas major (anterior view)', '腰方肌与腰大肌（前面观）')
        st = Stage(f, 'ant', 0.0, -0.98, 520, 640, 2300)
        low = st.P2(0, -0.76)[1]
        clip_begin(f, 60, 160, 920, low - 160)
        st.bones(('hip-bone', 'hip-bone-left', 'rib11', 'rib11-left', 'rib12', 'rib12-left', 'appendicular-skeleton-femur-right', 'femur-left'))
        st.spine(('t11', 't12') + LUMB)
        st.muscle('quadratus-lumborum-left')
        pm = COLOR['psoas-major']
        medial = [st.P(off(f'{lv}-body', dx=-0.016 - k * 0.002)) for k, lv in enumerate(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'))]
        lateral = [st.P(off(f'{lv}-tp', dx=d)) for lv, d in (('l5', 0.012), ('l4', 0.016), ('l3', 0.018), ('l2', 0.016), ('l1', 0.012))]
        brim_m, brim_l = st.P([-0.064, 0.915, 0.03]), st.P([-0.086, 0.915, 0.03])
        lt = st.at('lesser-trochanter')
        pts = medial + [brim_m, (lt[0] + 6, lt[1] - 8), (lt[0] - 4, lt[1] - 14), brim_l] + lateral + [st.P(off('t12-body', dx=-0.022, dy=0.008))]
        f.path(blob(pts), pm, 1.6, tint(pm), op=0.85)
        f.end()
        oi(f, [st.P(off(f'{lv}-body', dx=-0.018)) for lv in ('t12', 'l1', 'l2', 'l3', 'l4')] + [st.at('l5-tp', dx=0.01)],
           [st.at('lesser-trochanter')], LETTER['psoas-major'], LETTER['psoas-major'])
        ql = lambda n, **k: st.P(mirror(off(n, **k)))
        oi(f, [ql('iliac-crest-top', dx=0.03, dy=-0.012), ql('iliac-crest-top', dx=0.045, dy=-0.01), ql('l5-tp', dx=-0.01)],
           [ql('rib12-tip', dx=0.008), ql('rib12-angle')] + [ql(f'{lv}-tp') for lv in ('l1', 'l2', 'l3', 'l4')], LETTER['quadratus-lumborum'], LETTER['quadratus-lumborum'])
        f.bi(330, 170, 'Psoas major (right side)', '腰大肌（右侧）', 16, pm, 'middle', '700')
        f.bi(720, 170, 'Quadratus lumborum (left side)', '腰方肌（左侧）', 16, COLOR['quadratus-lumborum'], 'middle', '700')
        key_oi(f, 1000, 230)
        legend_oi(f, 1000, 330, [('psoas-major', 'bodies and discs T12–L4, transverse processes L1–L5', 'T12–L4 椎体和椎间盘、L1–L5 横突', 'lesser trochanter of the femur', '股骨小转子'),
                                 ('quadratus-lumborum', 'iliac crest and iliolumbar ligament', '髂嵴和髂腰韧带', '12th rib and L1–L4 transverse processes', '第 12 肋和 L1–L4 横突')])
        note(f, 1000, 600, ['Both muscles are paired; each is drawn on one side.', 'Quadratus lumborum outline comes from the 3D model;', 'psoas major is drawn schematically (not in the model).'],
             ['两块肌肉都左右成对，图中各画一侧。', '腰方肌轮廓取自 3D 模型；', '腰大肌为示意画法（模型中没有）。'])
        f.save('腰方肌与腰大肌起点与止点')
