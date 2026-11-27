"""Figures 09–10: the lumbar nerves drawn on the spine (AN-12): spinal cord, conus medullaris, cauda equina and the
nerve roots leaving the intervertebral foramina (09); the dorsal ramus branches and the sinuvertebral nerve (10)."""
from lumbarfig import *  # noqa: F401,F403

DURA = '#9b8f7a'
PED = {lvl: LM[f'{lvl}-pedicle'][1] for lvl in ('t12', 'l1', 'l2', 'l3', 'l4', 'l5')}
# height (model y) of each root's exit: the foramen below the pedicle of its own vertebra (L5: L5–S1; S1/S2: sacral foramina)
EXIT = {'L1': (PED['l1'] + PED['l2']) / 2, 'L2': (PED['l2'] + PED['l3']) / 2, 'L3': (PED['l3'] + PED['l4']) / 2,
        'L4': (PED['l4'] + PED['l5']) / 2, 'L5': PED['l5'] - 0.019, 'S1': 0.944, 'S2': 0.921}
CONUS_Y = (LM['l1-body'][1] + LM['l2-body'][1]) / 2  # the L1–L2 disc level


def root_path(st, side, i, name):
    """One root from the conus down the dural sac to its foramen, then out as the spinal nerve (figure points).
    side = +1 for the person's left (image left in the posterior view), -1 for the right."""
    y_e = EXIT[name]
    x_in = 0.0018 + 0.0009 * (6 - i)          # roots for lower levels run nearer the midline
    sacral = name.startswith('S')
    pts = [[side * 0.0012, CONUS_Y + 0.004 - 0.0015 * i, -0.02], [side * x_in, CONUS_Y - 0.006 - 0.002 * i, -0.02]]
    pts += [[side * x_in, y_e + 0.016, -0.02], [side * (0.011 if not sacral else 0.010), y_e + 0.004, -0.02]]
    pts += [[side * (0.020 if not sacral else 0.017), y_e - 0.001, -0.02]]
    return [st.P(p) for p in pts]


def register(fig):

    @fig('09')
    def cauda_equina():
        f = Fig('09', 1700, 1280, 'The spinal cord ends at the conus medullaris; each lumbar root leaves below the vertebra of the same number',
                '脊髓止于脊髓圆锥；每条腰神经根在同序数椎骨下方穿出')
        st = Stage(f, 'post', 0.0, -1.045, 600, 640, 3700)
        f.bi(600, 128, 'Posterior view: laminae and spinous processes made see-through to show the vertebral canal',
             '后面观：椎板和棘突画成半透明，露出椎管', 15, INK, 'middle', '700')
        clip_begin(f, 0, 175, 1200, 1010)
        st.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'), op=0.42)
        # dural sac
        top, bot = st.P([0.0095, 1.17, -0.02]), st.P([0, 0.917, -0.02])
        sac = [st.P([0.0095, 1.17, -0.02]), st.P([0.0098, 1.0, -0.02]), st.P([0.0085, 0.95, -0.02]), bot,
               st.P([-0.0085, 0.95, -0.02]), st.P([-0.0098, 1.0, -0.02]), st.P([-0.0095, 1.17, -0.02])]
        f.path(curve(sac), DURA, 1.6, '#f3eadb', dash='7 4', rough=False, op=0.9)
        # spinal cord and conus medullaris
        cord = [st.P([0.0042, 1.17, -0.02]), st.P([0.0045, CONUS_Y + 0.018, -0.02]), st.P([0.0, CONUS_Y - 0.002, -0.02]),
                st.P([-0.0045, CONUS_Y + 0.018, -0.02]), st.P([-0.0042, 1.17, -0.02])]
        f.path(curve(cord), '#8a6a10', 1.8, '#f0d98a', rough=False)
        names = ['L1', 'L2', 'L3', 'L4', 'L5', 'S1', 'S2']
        for side in (1, -1):
            for i, nm in enumerate(names):
                pts = root_path(st, side, i, nm)
                y_e = EXIT[nm]
                sacral = nm.startswith('S')
                nerve(f, pts, 2.6 if not sacral else 2.2, dash='5 4' if sacral else None, smooth=True)
                if not sacral:
                    gx, gy = st.P([side * 0.0225, y_e - 0.0015, -0.02])
                    f.raw(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="9" ry="12" fill="#e7b730" stroke="#8a6a10" stroke-width="1.4"/>')
                    nerve(f, [st.P([side * 0.025, y_e - 0.003, -0.02]), st.P([side * 0.033, y_e - 0.008, -0.02])], 3.4)
        # person's right L4: the spinal nerve divides into a dorsal ramus (posterior) and a ventral ramus (anterior, dashed)
        y4 = EXIT['L4']
        div = st.P([-0.033, y4 - 0.008, -0.02])
        nerve(f, [div, st.P([-0.036, y4 - 0.016, -0.03]), st.P([-0.034, y4 - 0.026, -0.04])], 2.6, smooth=True)
        # person's left: ventral rami L1–L4 (anterior to the transverse processes, dashed) gather into the lumbar plexus
        plex = st.P([0.05, EXIT['L3'] - 0.03, 0.0])
        for nm in ('L1', 'L2', 'L3', 'L4'):
            a = st.P([0.033, EXIT[nm] - 0.008, -0.02])
            nerve(f, [a, st.P([0.045, (EXIT[nm] - 0.008 + EXIT['L3'] - 0.03) / 2, -0.01]), plex], 2.4, dash='6 4')
        fem_end = st.P([0.078, 0.925, 0.0])
        nerve(f, [plex, st.P([0.07, 0.975, 0.0]), fem_end], 3.6, dash='6 4')
        # person's right: L4 and L5 ventral rami (lumbosacral trunk) join S1–S3 for the sciatic nerve
        lst = st.P([-0.045, 0.955, 0.0])
        for nm in ('L4', 'L5'):
            nerve(f, [st.P([-0.033, EXIT[nm] - 0.008, -0.02]), st.P([-0.042, (EXIT[nm] + 0.955) / 2 - 0.01, -0.01]), lst], 2.4, dash='6 4')
        sci_end = st.P([-0.066, 0.9, 0.0])
        nerve(f, [lst, st.P([-0.052, 0.935, 0.0]), sci_end], 4.2, dash='6 4')
        f.end()
        # vertebral levels beside the bodies (image right)
        for lvl in ('t12', 'l1', 'l2', 'l3', 'l4', 'l5'):
            x, y = st.P([-0.057 if lvl != 'l5' else -0.062, LM[f'{lvl}-body'][1], -0.02])
            f.text(x + (0 if lvl != 't12' else -8), y + 5, lvl.upper(), 14, GREY, 'start', '700')
        x, y = st.P([-0.066, 0.94, -0.02]); f.text(x, y + 5, 'Sacrum', 14, GREY, 'start', '700')
        # numbered course 1 → 6
        marks = [(st.P([0.009, CONUS_Y + 0.004, -0.02]), 1), (st.P([0.0, EXIT['L4'] + 0.02, -0.02]), 2),
                 (st.P([-0.016, y4 + 0.011, -0.02]), 3), (st.P([-0.03, y4 + 0.004, -0.02]), 4),
                 (st.P([-0.03, y4 - 0.02, -0.02]), 5), (st.P([0.058, EXIT['L3'] - 0.045, 0.0]), 6)]
        for (x, y), n in marks: f.step(x - 11, y - 11, n, GOLD)
        # labels: person's left side (image left)
        label(f, 40, 230, 'Spinal cord', '脊髓', '#8a6a10', 'start', 14, to=st.P([0.003, 1.14, -0.02]))
        label(f, 40, 330, 'Conus medullaris (≈ L1–L2 vertebrae)', '脊髓圆锥（约第 1–2 腰椎）', '#8a6a10', 'start', 14, to=st.P([0.002, CONUS_Y + 0.006, -0.02]))
        label(f, 40, 430, 'Lumbar plexus (in psoas major)', '腰丛（在腰大肌内）', '#8a6a10', 'start', 14, to=plex)
        label(f, 40, 770, 'Cauda equina', '马尾', '#8a6a10', 'start', 14, to=st.P([0.004, EXIT['L4'] + 0.03, -0.02]))
        label(f, 40, 870, 'Dural sac', '硬脊膜囊', DURA, 'start', 14, to=st.P([0.0088, 0.97, -0.02]))
        label(f, 40, 1080, 'Femoral nerve (L2–L4)', '股神经（L2–L4）', '#8a6a10', 'start', 14, to=fem_end)
        # labels: person's right side (image right)
        label(f, 955, 590, 'Dorsal root ganglion (L4)', '背根神经节（L4）', '#8a6a10', 'start', 14, to=st.P([-0.0225, y4 - 0.0015, -0.02]))
        label(f, 955, 700, 'Dorsal ramus', '后支', '#8a6a10', 'start', 14, to=st.P([-0.034, y4 - 0.026, -0.04]))
        label(f, 955, 860, 'Ventral ramus (dashed: in front of the bone)', '前支（虚线：在骨前方）', '#8a6a10', 'start', 14, to=st.P([-0.04, EXIT['L4'] - 0.02, -0.01]))
        label(f, 955, 1100, 'Sciatic nerve (L4–S3)', '坐骨神经（L4–S3）', '#8a6a10', 'start', 14, to=sci_end)
        f.bi(40, 1200, 'Ventral rami and their nerves lie in front of the vertebrae; they are drawn dashed through the bone.',
             '前支及其神经在椎骨前方，透过骨画成虚线。', 13, GREY, 'start', '400')
        step_cards(f, 1250, 150, [
            ('The spinal cord ends as the conus medullaris at about the L1–L2 vertebral level in adults.', '成人脊髓在约第 1–2 腰椎水平止于脊髓圆锥。'),
            ('Below it, the lumbar and sacral roots run down the dural sac as the cauda equina.', '其下方的腰、骶神经根在硬脊膜囊内下行，组成马尾。'),
            ('Each lumbar root leaves below the vertebra of the same number, hooking around the pedicle above its own-level disc: the L4 root exits at L4–L5.', '每条腰神经根在同序数椎骨下方穿出，绕过本节段椎间盘上方的椎弓根：L4 神经根从 L4–L5 椎间孔出。'),
            ('The dorsal root ganglion lies in or close to the intervertebral foramen; lower lumbar ganglia are more often inside it.', '背根神经节位于椎间孔内或其附近；下腰椎的神经节更常位于孔内。'),
            ('Outside the foramen the spinal nerve splits into a dorsal ramus (back) and a ventral ramus (front).', '出孔后脊神经分为后支（向后）和前支（向前）。'),
            ('Ventral rami L1–L4 form the lumbar plexus in psoas major (femoral nerve L2–L4); L4–S3 join the sciatic nerve.', '前支 L1–L4 在腰大肌内组成腰丛（股神经 L2–L4）；L4–S3 汇成坐骨神经。'),
        ], w=410)
        f.save('脊髓圆锥马尾与神经根出口')

    @fig('10')
    def dorsal_ramus():
        f = Fig('10', 1800, 1180, 'Dorsal ramus branches and the sinuvertebral nerve: what the lumbar nerves supply in the back',
                '后支的分支与窦椎神经：腰神经在背部支配什么')
        # ---- panel A: section through L4 from above (anterior up); nerves on the person's left = image left
        st = Stage(f, 'sup', 0.0, 0.028, 560, 600, 3700)
        f.bi(560, 150, 'A. Seen from above at the L4 vertebra (anterior up)', 'A. 第 4 腰椎平面上面观（前方在上）', 16, INK, 'middle', '700')
        L = lambda x, z: st.P([x, 1, z])
        for sg in (1, -1):
            for mid, (x, z, rx, rz) in {'psoas-major': (0.031, -0.004, 0.016, 0.019), 'quadratus-lumborum': (0.058, -0.027, 0.017, 0.009),
                                        'multifidus': (0.013, -0.061, 0.011, 0.017), 'longissimus-thoracis': (0.033, -0.060, 0.012, 0.016),
                                        'iliocostalis-lumborum': (0.054, -0.056, 0.011, 0.013)}.items():
                f.path(blob(ell(st, sg * x, z, rx, rz)), COLOR[mid], 1.3, tint(COLOR[mid], 0.78), op=0.8)
                if sg == -1:
                    tx, ty = st.P([-x, 1, z]); tag(f, tx, ty, LETTER[mid], COLOR[mid], 13)
        st.shape('skeleton-vertebra-l4', BONE_E, SHADE, 1.6)
        st.shape('skeleton-vertebra-l4', BONE_E, BONE, 1.3, layer='sup-1')
        # dural sac with roots, posterior longitudinal ligament and the back of the disc
        f.path(blob([L(0.009 * math.cos(a), -0.028 + 0.007 * math.sin(a)) for a in [k * math.pi / 6 for k in range(12)]]), DURA, 1.4, '#f3eadb', dash='5 3', rough=False)
        f.path(curve([L(0.014, -0.0165), L(0.0, -0.0175), L(-0.014, -0.0165)]), '#6f7d8c', 4.0, rough=False)
        # spinal nerve with its ganglion, then the rami
        sn = [L(0.009, -0.026), L(0.016, -0.022), L(0.024, -0.02)]
        nerve(f, sn, 3.2, smooth=True)
        gx, gy = L(0.02, -0.021); f.raw(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="11" ry="8" fill="#e7b730" stroke="#8a6a10" stroke-width="1.4"/>')
        div = L(0.028, -0.022)
        nerve(f, [L(0.024, -0.02), div], 3.4)
        vr = [div, L(0.034, -0.012), L(0.036, 0.004)]                           # ventral ramus into psoas major
        nerve(f, vr, 3.4, smooth=True)
        svn = [L(0.026, -0.018), L(0.018, -0.0145), L(0.009, -0.0145), L(0.003, -0.0155)]   # sinuvertebral nerve back into the canal
        nerve(f, svn, 1.8, smooth=True)
        dr = [div, L(0.031, -0.03), L(0.033, -0.036)]                           # dorsal ramus backwards
        nerve(f, dr, 3.0, smooth=True)
        mb = [L(0.033, -0.036), L(0.026, -0.044), L(0.02, -0.05), L(0.014, -0.058)]   # medial branch: joint and multifidus
        nerve(f, mb, 2.2, smooth=True)
        nerve(f, [L(0.026, -0.044), L(0.021, -0.039)], 1.6)                      # articular twig
        ib = [L(0.033, -0.036), L(0.034, -0.048), L(0.034, -0.056)]             # intermediate branch: longissimus
        nerve(f, ib, 1.8, smooth=True)
        lb = [L(0.033, -0.036), L(0.045, -0.044), L(0.054, -0.054)]             # lateral branch: iliocostalis
        nerve(f, lb, 2.2, smooth=True)
        label(f, 40, 300, 'Ventral ramus (into psoas major)', '前支（进入腰大肌）', '#8a6a10', 'start', 14, to=L(0.036, 0.0))
        label(f, 40, 410, 'Sinuvertebral nerve', '窦椎神经', '#8a6a10', 'start', 14, to=L(0.012, -0.0145))
        label(f, 40, 500, 'Dorsal root ganglion', '背根神经节', '#8a6a10', 'start', 14, to=(gx, gy))
        label(f, 40, 590, 'Dorsal ramus', '后支', '#8a6a10', 'start', 14, to=L(0.031, -0.03))
        label(f, 40, 690, 'Zygapophyseal joint', '关节突关节', GREY, 'start', 14, to=L(0.021, -0.039))
        label(f, 40, 985, 'Medial branch', '内侧支', '#8a6a10', 'start', 14, to=L(0.02, -0.05))
        label(f, 40, 900, 'Intermediate branch (variable)', '中间支（不恒定）', '#8a6a10', 'start', 14, to=L(0.034, -0.054))
        label(f, 40, 785, 'Lateral branch', '外侧支', '#8a6a10', 'start', 14, to=L(0.05, -0.05))
        label(f, 560, 230, 'Posterior longitudinal ligament and back of the disc', '后纵韧带与椎间盘后部', '#6f7d8c', 'middle', 13, to=L(-0.004, -0.0172))
        note(f, 300, 1010, ['Letters: PM psoas major, QL quadratus lumborum, MF multifidus, LT longissimus, IL iliocostalis.'],
             ['字母：PM 腰大肌，QL 腰方肌，MF 多裂肌，LT 最长肌，IL 髂肋肌。'])
        # ---- panel B: posterior view of L3–S1, the person's right; medial branches supply two joints each
        pb = Stage(f, 'post', 0.0, -1.0, 1130, 640, 3600)
        f.bi(1330, 150, 'B. Posterior view, right side: each joint gets two medial branches', 'B. 后面观（右侧）：每个关节突关节受两条内侧支支配', 16, INK, 'middle', '700')
        clip_begin(f, 905, 330, 545, 580)
        pb.bones(['hip-bone'], op=0.6)
        pb.spine(('l2', 'l3', 'l4', 'l5'), w=1.4)
        f.end()
        R = lambda x, y: pb.P([-x, y, -0.04])
        joints = {'L3–L4': R(0.019, 1.040), 'L4–L5': R(0.022, 1.002), 'L5–S1': R(0.022, 0.968)}
        for nm, (x, y) in joints.items():
            f.raw(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="13" ry="17" fill="none" stroke="#6f7d8c" stroke-width="2.2" stroke-dasharray="4 3"/>')
        def ramus(y_tp, x_root, y_low):
            """Dorsal ramus over the root of the transverse process below: medial branch hooks round the superior articular
            process, gives a twig up to the joint above and down to the joint below, and ends in multifidus."""
            st0 = R(0.034, y_tp + 0.012)
            hook = R(x_root, y_tp + 0.003)
            nerve(f, [st0, R(x_root + 0.006, y_tp + 0.006), hook, R(x_root - 0.004, y_tp - 0.008), R(x_root - 0.008, y_low)], 2.6, smooth=True)
            return st0, hook
        a3, h3 = ramus(1.0224, 0.022, 0.99)     # L3 dorsal ramus over the L4 transverse process
        a4, h4 = ramus(0.9971, 0.026, 0.962)    # L4 dorsal ramus over the L5 transverse process
        nerve(f, [h3, R(0.019, 1.037)], 2.0); nerve(f, [R(0.017, 1.012), R(0.021, 1.005)], 2.0)
        nerve(f, [h4, R(0.022, 0.999)], 2.0); nerve(f, [R(0.021, 0.982), R(0.022, 0.971)], 2.0)
        l5 = [R(0.036, 0.975), R(0.03, 0.97), R(0.025, 0.963), R(0.018, 0.952)]   # L5 dorsal ramus over the sacral ala
        nerve(f, l5, 2.6, smooth=True)
        lat = [a3, R(0.05, 1.02), R(0.066, 0.998), R(0.08, 0.975)]               # L3 lateral branch heading over the iliac crest
        nerve(f, lat, 2.2, smooth=True)
        label(f, 1480, 490, 'L3 medial branch', 'L3 内侧支', '#8a6a10', 'start', 14, to=R(0.03, 1.029))
        label(f, 1480, 580, 'L4 medial branch', 'L4 内侧支', '#8a6a10', 'start', 14, to=R(0.031, 1.004))
        label(f, 1480, 850, 'L5 dorsal ramus', 'L5 后支', '#8a6a10', 'start', 14, to=R(0.03, 0.97))
        label(f, 1480, 670, 'L3 lateral branch', 'L3 外侧支', '#8a6a10', 'start', 14, to=R(0.075, 0.986))
        label(f, 1480, 400, 'L3–L4 zygapophyseal joint', 'L3–L4 关节突关节', GREY, 'start', 13, to=joints['L3–L4'])
        label(f, 1480, 760, 'L4–L5 joint: L3 + L4 medial branches', 'L4–L5 关节：L3 和 L4 内侧支', GREY, 'start', 13, to=joints['L4–L5'])
        label(f, 1480, 940, 'L5–S1 joint: L4 + L5 medial branches', 'L5–S1 关节：L4 和 L5 内侧支', GREY, 'start', 13, to=joints['L5–S1'])
        f.save('后支分支与窦椎神经')
