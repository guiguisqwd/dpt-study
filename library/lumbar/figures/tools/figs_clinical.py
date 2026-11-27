"""Figures 11, 15, 16: clinical anatomy. 11: where a disc herniation meets the roots (traversing vs exiting root);
15: L2–S1 root map (dermatomes, key muscles, reflexes) on the leg; 16: acupoints over the lower back (AN-21)."""
from lumbarfig import *  # noqa: F401,F403
from figs_nerves import EXIT, DURA

DISC = '#7a8fa6'
HERN = '#b04a3a'


def register(fig):

    @fig('11')
    def herniation():
        f = Fig('11', 1700, 1120, 'Disc herniation at L4–L5: a paracentral one meets the traversing L5 root, a far-lateral one the exiting L4 root',
                'L4–L5 椎间盘突出：旁中央型压到 L5 走行根，极外侧型压到 L4 出口根')
        # ---- panel A: posterior view, L3–S1, arches see-through
        st = Stage(f, 'post', 0.0, -1.0, 470, 610, 5600)
        f.bi(470, 140, 'A. Posterior view, arches see-through', 'A. 后面观，椎弓画成半透明', 16, INK, 'middle', '700')
        clip_begin(f, 40, 180, 860, 720)
        st.spine(('l3', 'l4', 'l5'), op=0.4)
        # L4–L5 disc seen through the canal
        yd = (LM['l4-body'][1] + LM['l5-body'][1]) / 2 - 0.002
        disc = [st.P([0.024, yd + 0.004, 0]), st.P([-0.024, yd + 0.004, 0]), st.P([-0.024, yd - 0.004, 0]), st.P([0.024, yd - 0.004, 0])]
        f.path('M' + ' L'.join('%.1f,%.1f' % p for p in disc) + 'Z', DISC, 1.6, '#dfe6ee', rough=False, op=0.9)
        sac = [st.P([0.0095, 1.06, -0.02]), st.P([0.0098, 1.0, -0.02]), st.P([0.0088, 0.95, -0.02]), st.P([-0.0088, 0.95, -0.02]),
               st.P([-0.0098, 1.0, -0.02]), st.P([-0.0095, 1.06, -0.02])]
        f.path(curve(sac), DURA, 1.4, '#f3eadb', dash='6 4', rough=False, op=0.8)
        for side in (1, -1):
            for nm, x_in in (('L3', 0.0075), ('L4', 0.0068), ('L5', 0.006), ('S1', 0.005)):
                y_e = EXIT[nm]
                bend = 0.0 if not (side == -1 and nm == 'L5') else -0.003   # person's right L5 root pushed by the paracentral herniation
                pts = [st.P([side * x_in, 1.065, -0.02]), st.P([side * (x_in + (0.002 if nm == 'L5' else 0)) + bend * side * -1, y_e + 0.02, -0.02]),
                       st.P([side * 0.011, y_e + 0.005, -0.02]), st.P([side * 0.02, y_e - 0.001, -0.02])]
                if nm == 'S1': pts = pts[:2] + [st.P([side * 0.012, 0.95, -0.02])]
                nerve(f, pts, 2.6, smooth=True)
                if nm != 'S1':
                    gx, gy = st.P([side * 0.0225, y_e - 0.0015, -0.02])
                    f.raw(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="10" ry="13" fill="#e7b730" stroke="#8a6a10" stroke-width="1.4"/>')
                    nerve(f, [st.P([side * 0.025, y_e - 0.003, -0.02]), st.P([side * 0.034, y_e - 0.009, -0.02])], 3.4)
        # paracentral herniation (person's right = image right) and far-lateral herniation (person's left = image left)
        hp = st.P([-0.0085, yd, -0.02]); hl = st.P([0.027, EXIT['L4'] - 0.004, -0.02])
        f.path(blob([(hp[0] + 22 * math.cos(a), hp[1] + 15 * math.sin(a)) for a in [k * math.pi / 5 for k in range(10)]]), HERN, 2, '#e9b8ad', rough=False, op=0.92)
        f.path(blob([(hl[0] + 20 * math.cos(a), hl[1] + 14 * math.sin(a)) for a in [k * math.pi / 5 for k in range(10)]]), HERN, 2, '#e9b8ad', rough=False, op=0.92)
        f.end()
        for lvl in ('l3', 'l4', 'l5'):
            x, y = st.P([-0.05, LM[f'{lvl}-body'][1], -0.02]); f.text(x, y + 5, lvl.upper(), 15, GREY, 'start', '700')
        label(f, 600, 960, 'Paracentral herniation: traversing L5 root', '旁中央型突出：压到 L5 走行根', HERN, 'start', 14, to=hp)
        label(f, 40, 930, 'Far-lateral herniation: exiting L4 root', '极外侧型突出：压到 L4 出口根', HERN, 'start', 14, to=hl)
        label(f, 40, 230, 'L4 root leaves at L4–L5', 'L4 神经根从 L4–L5 出孔', '#8a6a10', 'start', 14, to=st.P([0.034, EXIT['L4'] - 0.009, -0.02]))
        label(f, 640, 230, 'L5 root crosses the L4–L5 disc', 'L5 神经根越过 L4–L5 椎间盘', '#8a6a10', 'start', 14, to=st.P([-0.0085, yd + 0.012, -0.02]))
        label(f, 40, 1010, 'L4–L5 disc (in front of the dural sac)', 'L4–L5 椎间盘（在硬脊膜囊前方）', DISC, 'start', 14, to=st.P([0.02, yd, 0]))
        # ---- panel B: the disc from above with the zones
        sb = Stage(f, 'sup', 0.0, 0.028, 1290, 580, 6200)
        f.bi(1290, 140, 'B. L4–L5 disc from above: zones of herniation', 'B. 上面观 L4–L5 椎间盘：突出的分区', 16, INK, 'middle', '700')
        sb.shape('skeleton-vertebra-l5', BONE_E, SHADE, 1.5)
        sb.shape('skeleton-vertebra-l5', BONE_E, BONE, 1.3, layer='sup-1')
        Q = lambda x, z: sb.P([x, 1, z])
        kid = [Q(0.0, 0.012), Q(0.018, 0.01), Q(0.025, 0.0), Q(0.022, -0.012), Q(0.012, -0.0175), Q(0.0, -0.0155),
               Q(-0.012, -0.0175), Q(-0.022, -0.012), Q(-0.025, 0.0), Q(-0.018, 0.01)]
        f.path(blob(kid), DISC, 2, '#dfe6ee', rough=False)
        f.path(blob([Q(0.011 * math.cos(a), -0.003 + 0.007 * math.sin(a)) for a in [k * math.pi / 6 for k in range(12)]]), '#4d6a8a', 1.6, '#b9cbe0', rough=False)
        f.path(blob([Q(0.009 * math.cos(a), -0.028 + 0.0075 * math.sin(a)) for a in [k * math.pi / 6 for k in range(12)]]), DURA, 1.4, '#f3eadb', dash='5 3', rough=False)
        for sg in (1, -1):
            x, y = Q(sg * 0.0125, -0.025); f.circle(x, y, 9, '#e7b730', '#8a6a10', 1.6)      # traversing L5 root in the lateral recess
            x, y = Q(sg * 0.026, -0.021); f.raw(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="13" ry="10" fill="#e7b730" stroke="#8a6a10" stroke-width="1.6"/>')  # exiting L4 root
        # zone boundaries (dashed): canal edge, medial and lateral edge of the pedicle
        for xb in (0.009, 0.017, 0.031):
            for sg in (1, -1):
                a, b = Q(sg * xb, -0.012), Q(sg * xb, -0.05)
                f.path(f'M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}', '#8c7f6a', 1.2, dash='4 4', rough=False)
        zones = [('Central', '中央型', 0.0), ('Paracentral', '旁中央型', 0.013), ('Foraminal', '椎间孔型', 0.024), ('Extraforaminal', '椎间孔外型', 0.038)]
        for k, (en, zh, xz) in enumerate(zones):
            x, y = Q(-xz, -0.05)
            ty = 880 + 52 * (k % 2)
            f.leader(x, y, x, ty - 16, HERN, dash='2 3')
            f.bi(x, ty, en, zh, 13, HERN, 'middle', '700')
        label(f, 1560, 280, 'Nucleus pulposus', '髓核', '#4d6a8a', 'start', 14, to=Q(-0.006, -0.003))
        label(f, 1560, 360, 'Annulus fibrosus', '纤维环', DISC, 'start', 14, to=Q(-0.021, 0.004))
        label(f, 1560, 600, 'Exiting L4 root', 'L4 出口根', '#8a6a10', 'start', 14, to=Q(-0.026, -0.021))
        label(f, 1560, 700, 'Traversing L5 root', 'L5 走行根', '#8a6a10', 'start', 14, to=Q(-0.0125, -0.025))
        label(f, 1290, 250, 'Dural sac', '硬脊膜囊', DURA, 'middle', 14, to=Q(0.0, -0.022))
        note(f, 1000, 1010, ['The same rule at other levels: a paracentral L5–S1 herniation usually meets the S1 root.'],
             ['其他节段同理：L5–S1 旁中央型突出通常压到 S1 神经根。'])
        f.save('椎间盘突出与受压神经根')

    @fig('15')
    def root_map():
        f = Fig('15', 1700, 1260, 'L2–S1 roots on the leg: key sensory points and the reflexes that test them',
                'L2–S1 神经根在下肢的表现：关键感觉点与对应反射')
        ROOT = {'L2': '#6a4fa3', 'L3': '#365e91', 'L4': '#2b6c7c', 'L5': '#4f8a4a', 'S1': '#9c3f6e'}
        a = Stage(f, 'ant', -0.075, -0.52, 400, 650, 980)
        p = Stage(f, 'post', 0.075, -0.52, 900, 650, 980)
        f.bi(400, 150, 'Right leg, front', '右下肢前面', 17, INK, 'middle', '700')
        f.bi(900, 150, 'Right leg, back', '右下肢后面', 17, INK, 'middle', '700')
        for st in (a, p):
            clip_begin(f, st.fx - 240, 300, 480, 925)
            st.skin(key='leg-skin')
            for b in LEG: st.shape(b, BONE_E, BONE, 1.0, op=0.45, rough=False)
            f.end()
        def dot(st, xyz, root, r=11):
            x, y = st.P(xyz); f.circle(x, y, r, ROOT[root], '#fff', 2.5); return (x, y)
        pts = {'L2': dot(a, [-0.062, 0.69, 0.06], 'L2'), 'L3': dot(a, [-0.035, 0.47, 0.03], 'L3'),
               'L4': dot(a, [-0.043, 0.085, 0.0], 'L4'), 'L5': dot(a, [-0.10, 0.035, 0.08], 'L5'), 'S1': dot(p, [-0.10, 0.035, -0.06], 'S1')}
        label(f, 40, 480, 'L2: anteromedial thigh, halfway down', 'L2：大腿前内侧中点', ROOT['L2'], 'start', 14, to=pts['L2'])
        label(f, 40, 640, 'L3: medial femoral condyle', 'L3：股骨内侧髁', ROOT['L3'], 'start', 14, to=pts['L3'])
        label(f, 40, 1010, 'L4: medial malleolus', 'L4：内踝', ROOT['L4'], 'start', 14, to=pts['L4'])
        label(f, 40, 1170, 'L5: dorsum of foot, 3rd MTP joint', 'L5：足背第 3 跖趾关节处', ROOT['L5'], 'start', 14, to=pts['L5'])
        label(f, 1060, 1170, 'S1: lateral heel', 'S1：足跟外侧', ROOT['S1'], 'start', 14, to=pts['S1'])
        # reflex sites (hammer marks)
        def hammer(x, y, col):
            f.raw(f'<g stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round"><path d="M{x + 14:.1f},{y - 14:.1f} L{x + 40:.1f},{y - 40:.1f}"/>'
                  f'<path d="M{x + 30:.1f},{y - 50:.1f} L{x + 50:.1f},{y - 30:.1f}" stroke-width="7"/></g>')
            f.circle(x, y, 6, col, '#fff', 2)
        kx, ky = a.P([-0.075, 0.405, 0.06]); hammer(kx, ky, ROOT['L4'])
        hx, hy = p.P([-0.035, 0.5, -0.06]); hammer(hx, hy, ROOT['L5'])
        ax_, ay = p.P([-0.06, 0.1, -0.06]); hammer(ax_, ay, ROOT['S1'])
        label(f, 560, 360, 'Patellar reflex: mainly L4 (L3–L4)', '膝反射：主要 L4（L3–L4）', ROOT['L4'], 'start', 14, to=(kx, ky))
        label(f, 1060, 420, 'Medial hamstring reflex: L5', '内侧腘绳肌反射：L5', ROOT['L5'], 'start', 14, to=(hx, hy))
        label(f, 1060, 860, 'Achilles reflex: S1', '跟腱反射：S1', ROOT['S1'], 'start', 14, to=(ax_, ay))
        # key muscles (myotomes), ISNCSCI
        f.bi(1180, 520, 'Key muscles (ISNCSCI)', '关键肌（ISNCSCI）', 16, INK, 'start', '700')
        rows = [('L2', 'Hip flexors', '屈髋肌'), ('L3', 'Knee extensors', '伸膝肌'), ('L4', 'Ankle dorsiflexors', '踝背屈肌'),
                ('L5', 'Long toe extensors', '趾长伸肌群'), ('S1', 'Ankle plantar flexors', '踝跖屈肌')]
        for i, (r, en, zh) in enumerate(rows):
            y = 580 + i * 50
            tag(f, 1192, y - 6, r, ROOT[r], 15)
            f.bi(1218, y, en, zh, 14, INK, 'start', '600')
        note(f, 1180, 960, ['Dots: ISNCSCI key sensory points.', 'The dermatome itself is a wider band.'], ['圆点：ISNCSCI 关键感觉点。', '皮节本身是更宽的带状区域。'])
        f.save('神经根感觉点与反射')

    @fig('16')
    def acupoints():
        f = Fig('16', 1700, 1330, 'Acupoints of the lower back on the local anatomy: Governor Vessel, Bladder lines and Jiaji',
                '下背部穴位与局部解剖：督脉、膀胱经两条线与夹脊')
        CUN = 0.021   # schematic B-cun for this figure (6 B-cun between the medial borders of the scapulae)
        st = Stage(f, 'post', 0.0, -1.03, 700, 640, 3300)
        clip_begin(f, 300, 190, 800, 900)
        st.bones(('hip-bone', 'hip-bone-left', 'rib11', 'rib11-left', 'rib12', 'rib12-left'), op=0.55)
        st.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'), op=0.75)
        # kidneys lie in front of quadratus lumborum, about T12–L3 (deep; dashed)
        for sg in (1, -1):
            kid = [st.P([sg * (0.055 + 0.022 * math.cos(t)), 1.075 + 0.05 * math.sin(t), 0.0]) for t in [k * math.pi / 8 for k in range(16)]]
            f.path(blob(kid), '#8c5a4a', 1.6, 'none', dash='6 5', rough=False, op=0.8)
        # meridian lines: midline (GV), Jiaji 0.5 cun, Bladder 1.5 and 3 cun
        top, bot = 1.17, 0.93
        for xc, col, w, dash in ((0, '#7a3e9d', 2.4, None), (0.5, '#a3271a', 1.2, '3 5'), (1.5, '#1f5f8b', 2.0, None), (3.0, '#1f5f8b', 2.0, '8 5')):
            for sg in ((1, -1) if xc else (1,)):
                a, b = st.P([sg * xc * CUN, top, -0.08]), st.P([sg * xc * CUN, (LM['l5-sp'][1] - 0.02) if xc == 0.5 else bot, -0.08])
                f.path(f'M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}', col, w, dash=dash, rough=False, op=0.85)
        f.end()
        below = lambda lvl: LM[f'{lvl}-sp'][1] - 0.006
        pts = {'GV4': (0, below('l2')), 'GV3': (0, below('l4')),
               'BL23': (-1.5, below('l2')), 'BL24': (-1.5, below('l3')), 'BL25': (-1.5, below('l4')), 'BL26': (-1.5, below('l5')),
               'BL52': (-3.0, below('l2'))}
        xy = {}
        for code, (c, y) in pts.items():
            xy[code] = st.P([c * CUN, y, -0.08])
            point(f, *xy[code], code)
        for lvl in ('l1', 'l2', 'l3', 'l4', 'l5'):   # Jiaji points beside each lumbar spinous process (left side shown)
            x, y = st.P([0.5 * CUN, below(lvl), -0.08]); f.circle(x, y, 5, '#c0392b', '#fff', 1.6)
        xj, yj = st.P([0.5 * CUN, below('l3'), -0.08])
        # iliac crest line (≈ L4) for finding the levels
        a, b = st.P([0.11, LM['iliac-crest-top'][1], -0.06]), st.P([-0.11, LM['iliac-crest-top'][1], -0.06])
        f.path(f'M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}', '#8c2f39', 1.6, dash='9 6', rough=False)
        f.bi(a[0] + 8, a[1] - 28, 'Iliac crests ≈ L4', '髂嵴连线 ≈ L4', 13, '#8c2f39', 'start', '700')
        for lvl in ('l2', 'l3', 'l4', 'l5'):
            x, y = st.P([0.0, LM[f'{lvl}-sp'][1], -0.08]); f.bi(292, y - 2, f'{lvl.upper()} spinous process', f'第 {lvl[1]} 腰椎棘突', 12, GREY, 'end', '600')
        rows = [('GV4', 'Mingmen', '命门', 'posterior midline, below the L2 spinous process', '后正中线上，第 2 腰椎棘突下'),
                ('GV3', 'Yaoyangguan', '腰阳关', 'posterior midline, below the L4 spinous process', '后正中线上，第 4 腰椎棘突下'),
                ('BL23', 'Shenshu', '肾俞', '1.5 cun lateral, level with the lower border of the L2 spinous process', '第 2 腰椎棘突下，旁开 1.5 寸'),
                ('BL24', 'Qihaishu', '气海俞', '1.5 cun lateral, level with the lower border of the L3 spinous process', '第 3 腰椎棘突下，旁开 1.5 寸'),
                ('BL25', 'Dachangshu', '大肠俞', '1.5 cun lateral, level with the lower border of the L4 spinous process', '第 4 腰椎棘突下，旁开 1.5 寸'),
                ('BL26', 'Guanyuanshu', '关元俞', '1.5 cun lateral, level with the lower border of the L5 spinous process', '第 5 腰椎棘突下，旁开 1.5 寸'),
                ('BL52', 'Zhishi', '志室', '3 cun lateral, level with the lower border of the L2 spinous process', '第 2 腰椎棘突下，旁开 3 寸'),
                ('EX-B2', 'Jiaji', '夹脊', '0.5 cun lateral, below each spinous process, T1–L5 (conventional)', '第 1 胸椎至第 5 腰椎棘突下，旁开 0.5 寸（常规定位）')]
        for i, (code, en, zh, loc_en, loc_zh) in enumerate(rows):
            y = 240 + i * 92
            label(f, 1130, y, f'{code} {en}', f'{code} {zh}', '#a3271a', 'start', 14)
            f.bi(1130, y + 40, loc_en, loc_zh, 12, GREY, 'start', '400')
        label(f, 40, 330, 'Kidney (deep, about T12–L3)', '肾（深部，约 T12–L3）', '#8c5a4a', 'start', 14, to=st.P([0.077, 1.09, 0.0]))
        f.text(xj - 12, yj + 22, 'EX-B2', 12, '#a3271a', 'end', '700')
        # line key
        ky = 1110
        for i, (en, zh, col, dash) in enumerate([('Posterior midline: Governor Vessel', '后正中线：督脉', '#7a3e9d', None),
                                                  ('1.5 cun: Bladder meridian (BL23–BL26)', '旁开 1.5 寸：膀胱经（肾俞至关元俞）', '#1f5f8b', None),
                                                  ('3 cun: Bladder meridian (BL52)', '旁开 3 寸：膀胱经（志室）', '#1f5f8b', '8 5'),
                                                  ('0.5 cun: Jiaji (EX-B2), conventional location', '旁开 0.5 寸：夹脊（常规定位）', '#a3271a', '3 5')]):
            y = ky + i * 46
            f.path(f'M40,{y - 5} L90,{y - 5}', col, 2.4, dash=dash, rough=False)
            f.bi(100, y, en, zh, 13, col, 'start', '600')
        note(f, 1130, 1010, ['Learning reference only, not clinically calibrated.', 'It does not show needle depth, direction or path.'],
             ['仅作学习参照，未经临床校准。', '不表示进针深度、方向或路径。'])
        f.save('下背部穴位与局部解剖')
