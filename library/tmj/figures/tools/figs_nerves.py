"""Figures 08-10: trigeminal nerve and its skin territories, branches of the mandibular nerve, and the facial nerve.
Nerve centre lines come from the model where it has them; branches the model lacks are drawn by hand and listed in the notes."""
from tmjfig import *  # noqa: F401,F403

V1C, V2C, V3C, CC = '#365e91', '#4f8a4a', '#7a5aa6', '#8d8779'


def poly(st, pts): return 'M' + ' L'.join('%.1f,%.1f' % st.L(*p) for p in pts) + ' Z'


def register(fig):

    @fig('08')
    def trigeminal():
        f = Fig('08', 1900, 1330, 'Trigeminal nerve (CN V): three divisions and their skin territories', '三叉神经（CN V）：三个分支及其皮肤分布')
        f.bi(470, 150, 'Skin territories, right lateral view', '皮肤分布区，右侧面观', 17, INK, 'middle', '700')
        clip_begin(f, 40, 190, 900, 780)
        st = Stage(f, 'lat', 0.0, -1.62, 470, 590, 2850); L = st.L
        cid = f.id('skin')
        f.raw(f'<clipPath id="{cid}"><path d="{st.d(st.rings("skin"))}"/></clipPath><g clip-path="url(#{cid})">')
        f.raw(f'<rect x="0" y="100" width="950" height="1100" fill="{SKIN_F}"/>')
        zones = [
            (V1C, [(-0.02, 1.76), (0.14, 1.76), (0.14, 1.566), (0.113, 1.566), (0.087, 1.600), (0.060, 1.598), (0.045, 1.630), (0.0, 1.700)]),
            (V2C, [(0.060, 1.598), (0.087, 1.600), (0.113, 1.566), (0.14, 1.566), (0.14, 1.546), (0.083, 1.545), (0.060, 1.560), (0.040, 1.585), (0.030, 1.620), (0.045, 1.630)]),
            (V3C, [(0.083, 1.545), (0.14, 1.546), (0.14, 1.47), (0.075, 1.492), (0.040, 1.512), (0.012, 1.540), (-0.002, 1.575), (-0.012, 1.610), (-0.020, 1.660), (0.0, 1.700),
                   (0.045, 1.630), (0.030, 1.620), (0.040, 1.585), (0.060, 1.560)]),
            (CC, [(-0.002, 1.575), (0.012, 1.540), (0.040, 1.512), (0.075, 1.492), (0.14, 1.47), (0.14, 1.40), (-0.16, 1.40), (-0.16, 1.76), (-0.02, 1.76), (0.0, 1.700),
                  (-0.020, 1.660), (-0.012, 1.610)])]
        for col, pts in zones: f.raw(f'<path d="{poly(st, pts)}" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="1.6" stroke-dasharray="6 4"/>')
        f.end()
        st.shape('skin', SKIN, 'none', 1.8, rough=False)
        ear_lat(st, op=0.9)
        eye = L(0.074, 1.598); f.raw(f'<path d="M{eye[0] - 22:.1f},{eye[1]:.1f} q22,-14 44,0 q-22,12 -44,0" fill="#fff" stroke="#6b6458" stroke-width="1.4"/><circle cx="{eye[0] + 4:.1f}" cy="{eye[1]:.1f}" r="5" fill="#6b6458"/>')
        mo = L(0.085, 1.545); f.raw(f'<path d="M{mo[0]:.1f},{mo[1]:.1f} l30,3" stroke="#6b6458" stroke-width="1.6"/>')
        for col, code, p in [(V1C, 'V1', L(0.06, 1.66)), (V2C, 'V2', L(0.072, 1.572)), (V3C, 'V3', L(0.055, 1.522)), (CC, 'C2–C3', L(-0.05, 1.62))]:
            f.text(p[0], p[1], code, 24, shade(col, 0.75), 'middle', '700')
        f.text(*L(-0.012, 1.512), 'C2–C3', 17, shade(CC, 0.7), 'middle', '700')
        f.end()
        column(f, 40, 1015, 58, [('V1 Ophthalmic nerve: forehead and scalp to the vertex, upper eyelid, cornea, bridge and tip of the nose', 'V1 眼神经：前额和头皮至头顶、上睑、角膜、鼻背和鼻尖', None)], 'start', 14, V1C)
        column(f, 40, 1073, 58, [('V2 Maxillary nerve: lower eyelid, side of the nose, cheek, upper lip', 'V2 上颌神经：下睑、鼻侧、面颊、上唇', None)], 'start', 14, V2C)
        column(f, 40, 1131, 58, [('V3 Mandibular nerve: lower lip, chin, lower jaw, the area in front of the ear and the temple', 'V3 下颌神经：下唇、颏部、下颌、耳前区和颞部', None)], 'start', 14, V3C)
        column(f, 40, 1189, 58, [('Skin over the angle of the mandible: C2–C3 (cervical plexus), not CN V', '下颌角表面的皮肤：C2–C3（颈丛），不是 CN V', None)], 'start', 14, shade(CC, 0.7))
        # the nerve on the skull
        f.bi(1420, 150, 'The nerve and its three exits from the skull', '神经和三个出颅位置', 17, INK, 'middle', '700')
        clip_begin(f, 1000, 260, 860, 680)
        st = Stage(f, 'lat', 0.035, -1.585, 1420, 560, 6400); L = st.L
        skull_lat(st, op=0.5)
        st.cord('Trigeminal nerve (V)', w=7, splines=[0])
        for nm, sp in [('Ophthalmic nerve', None), ('Maxillary nerve', None), ('Trigeminal nerve (V)', [1]), ('Anterior division of mandibular nerve', None), ('Posterior division of mandibular nerve', None),
                       ('Buccal nerve', [0]), ('Lingual nerve', None), ('Inferior alveolar nerve', [0]), ('Mental nerve', None)]:
            st.cord(nm, w=4, splines=sp)
        g = L(0.002, 1.600); f.raw(f'<ellipse cx="{g[0]:.1f}" cy="{g[1]:.1f}" rx="26" ry="15" fill="{NERVE}" stroke="{shade(NERVE)}" stroke-width="1.6" transform="rotate(-20 {g[0]:.1f} {g[1]:.1f})"/>')
        for col, code, p in [(V1C, 'V1', L(0.040, 1.611)), (V2C, 'V2', L(0.040, 1.5765)), (V3C, 'V3', L(0.0065, 1.586))]:
            f.circle(p[0], p[1], 15, col, '#fff', 2); f.text(p[0], p[1] + 5, code, 13, '#fff', 'middle', '700')
        f.end()
        label(f, 1010, 205, 'Sensory root and motor root, from the pons', '感觉根和运动根，自脑桥发出', INK, 'start', 14, to=L(-0.013, 1.5925))
        label(f, 1420, 205, 'Trigeminal ganglion (in the trigeminal cave)', '三叉神经节（位于三叉神经腔）', INK, 'start', 14, to=g)
        column(f, 1010, 985, 54, [('V1: superior orbital fissure, to the orbit and forehead', 'V1：经眶上裂，至眶和前额', None)], 'start', 14, V1C)
        column(f, 1010, 1093, 54, [('V3: foramen ovale, to the infratemporal fossa; the motor root joins it', 'V3：经卵圆孔至颞下窝；运动根加入其中', None)], 'start', 14, V3C)
        column(f, 1010, 1039, 54, [('V2: foramen rotundum, to the cheek and upper teeth', 'V2：经圆孔，至面颊和上牙', None)], 'start', 14, V2C)
        note(f, 1010, 1160, ['The mnemonic for the three exits is "Standing Room Only": Superior orbital fissure, foramen Rotundum, foramen Ovale.',
                             'V1 and V2 are purely sensory; V3 is mixed because the motor root joins only V3.'],
             ['三个出颅位置的英文口诀是 Standing Room Only：眶上裂、圆孔、卵圆孔。', 'V1、V2 是纯感觉神经；运动根只加入 V3，所以 V3 是混合神经。'])
        f.save('三叉神经分支与皮肤分布')

    @fig('09')
    def mandibular_nerve():
        f = Fig('09', 1900, 1320, 'Mandibular nerve (CN V3): branches in the infratemporal fossa', '下颌神经（CN V3）：颞下窝内的分支')
        clip_begin(f, 420, 150, 1060, 1000)
        st = Stage(f, 'lat', 0.034, -1.548, 950, 640, 10800); L = st.L
        skull_lat(st, op=0.55)
        st.muscle('lateral-pterygoid', op=0.22)
        fo = L(0.0145, 1.5785); f.raw(f'<ellipse cx="{fo[0]:.1f}" cy="{fo[1]:.1f}" rx="16" ry="9" fill="#5b5448" opacity=".8"/>')
        st.cord('Chorda tympani', '#b06fb0', 2.6, dash='6 4')
        hand = {'meningeal': [L(0.0155, 1.5745), L(0.006, 1.578), L(0.002, 1.588)],
                'mp': [L(0.0165, 1.573), L(0.024, 1.566), L(0.026, 1.556)],
                'masseteric': [L(0.021, 1.568), L(0.027, 1.5625), L(0.031, 1.557), L(0.033, 1.546)],
                'dt-post': [L(0.020, 1.570), L(0.018, 1.583), L(0.012, 1.602)], 'dt-ant': [L(0.021, 1.568), L(0.030, 1.580), L(0.036, 1.602)],
                'lp': [L(0.021, 1.568), L(0.016, 1.5655), L(0.012, 1.569)],
                'at': [L(0.0175, 1.571), L(0.009, 1.566), L(0.003, 1.5655), L(-0.001, 1.573), L(-0.001, 1.590), L(0.001, 1.606)]}
        for k, pts in hand.items(): cord(f, pts, NERVE, 3.2)
        for nm, sp, w in [('Trigeminal nerve (V)', [1], 6), ('Anterior division of mandibular nerve', None, 5), ('Posterior division of mandibular nerve', None, 5), ('Buccal nerve', None, 3.6),
                          ('Lingual nerve', None, 3.8), ('Inferior alveolar nerve', None, 3.4), ('Mental nerve', None, 3.4), ('Nerve to mylohyoid muscle', None, 3.2)]:
            st.cord(nm, w=w, splines=sp)
        mfo = L(0.0195, 1.546); f.raw(f'<ellipse cx="{mfo[0]:.1f}" cy="{mfo[1]:.1f}" rx="8" ry="11" fill="none" stroke="#5b5448" stroke-width="2"/>')
        mef = L(0.067, 1.510); f.raw(f'<ellipse cx="{mef[0]:.1f}" cy="{mef[1]:.1f}" rx="7" ry="6" fill="none" stroke="#5b5448" stroke-width="2"/>')
        f.end()
        column(f, 30, 215, 76, [
            ('Meningeal branch (back through the foramen spinosum)', '脑膜支（经棘孔返回颅内）', hand['meningeal'][-1]),
            ('Mandibular nerve trunk', '下颌神经主干', L(0.013, 1.583)),
            ('Foramen ovale', '卵圆孔', fo),
            ('Auriculotemporal nerve (behind the joint, then up)', '耳颞神经（经关节后方，再沿耳前上行）', hand['at'][3]),
            ('Chorda tympani (CN VII) joins the lingual nerve', '鼓索（CN VII）加入舌神经', st.curve3('Chorda tympani')[0][2]),
            ('Nerve to lateral pterygoid', '翼外肌神经', hand['lp'][-1]),
            ('Posterior division', '后干', L(0.018, 1.566)),
            ('Inferior alveolar nerve, entering the mandibular foramen', '下牙槽神经，进入下颌孔', mfo),
            ('Lingual nerve (anterior two-thirds of the tongue)', '舌神经（舌前三分之二）', L(0.026, 1.532)),
            ('Nerve to mylohyoid (mylohyoid, anterior belly of digastric)', '下颌舌骨肌神经（下颌舌骨肌、二腹肌前腹）', L(0.030, 1.528)),
        ], 'start', 14)
        column(f, 1500, 290, 76, [
            ('Deep temporal nerves (to temporalis)', '颞深神经（至颞肌）', hand['dt-ant'][1]),
            ('Anterior division', '前干', L(0.0205, 1.569)),
            ('Nerve to medial pterygoid (from the trunk)', '翼内肌神经（发自主干）', hand['mp'][-1]),
            ('Masseteric nerve (through the mandibular notch)', '咬肌神经（穿下颌切迹）', hand['masseteric'][-1]),
            ('Buccal nerve (sensory, to the cheek)', '颊神经（感觉，至面颊）', L(0.047, 1.5365)),
            ('Inferior dental branches (lower teeth)', '下牙支（下牙）', L(0.047, 1.514)),
            ('Mental nerve, leaving the mental foramen', '颏神经，出颏孔', mef),
        ], 'start', 14)
        note(f, 40, 1180, ['Drawn by hand because the 3D model has no mesh for them: meningeal branch, auriculotemporal, masseteric and deep temporal nerves, nerves to the pterygoids.',
                           'The outline of the lateral pterygoid is shown faintly; the nerve lies deep to it. Purple dashed line: chorda tympani.'],
             ['以下分支 3D 模型里没有，为手工绘制：脑膜支、耳颞神经、咬肌神经、颞深神经和两条翼肌神经。', '翼外肌轮廓以浅色显示，下颌神经位于其深面。紫色虚线：鼓索。'])
        f.save('下颌神经分支')

    @fig('10')
    def facial_nerve():
        f = Fig('10', 1900, 1300, 'Facial nerve (CN VII): course and five terminal branches', '面神经（CN VII）：走行与五条终末支')
        clip_begin(f, 480, 150, 810, 1010)
        st = Stage(f, 'lat', 0.012, -1.578, 800, 640, 5600); L = st.L
        skin_lat(st); skull_lat(st, op=0.5)
        st.shape('Parotid gland', '#9a8f7c', '#e8dcc6', 1.5, op=0.75, outer=True)
        ear_lat(st, op=0.6)
        fn = st.curve3('Facial nerve (VII)')
        cord(f, fn[0][:10], NERVE, 3, dash='5 4', op=0.75)
        exit_i = min(range(len(fn[0])), key=lambda i: math.dist(fn[0][i], L(-0.008, 1.559)))
        cord(f, fn[0][exit_i:], NERVE, 4.6)
        for i in (1, 2, 3, 4, 5, 6, 7, 8): cord(f, fn[i], NERVE, 3.6)
        pa = [L(-0.008, 1.559), L(-0.022, 1.566), L(-0.036, 1.580), L(-0.052, 1.592)]
        cord(f, pa, NERVE, 3)
        dg = [L(-0.006, 1.557), L(-0.004, 1.548), L(0.001, 1.540)]
        cord(f, dg, NERVE, 2.6)
        sm = L(-0.008, 1.559); f.circle(sm[0], sm[1], 7, '#5b5448', '#fff', 2)
        f.end()
        column(f, 30, 420, 84, [
            ('Inside the temporal bone (dashed line): facial canal', '颞骨内（虚线）：面神经管', fn[0][4]),
            ('Posterior auricular nerve (occipital belly)', '耳后神经（至枕腹）', pa[2]),
            ('Stylomastoid foramen', '茎乳孔', sm),
            ('Parotid gland (crossed, not supplied)', '腮腺（穿过但不支配）', L(0.010, 1.548)),
            ('Branches to the posterior belly of digastric and stylohyoid', '至二腹肌后腹和茎突舌骨肌的分支', dg[-1]),
            ('Cervical branch → platysma', '颈支 → 颈阔肌', fn[2][-2]),
        ], 'start', 14)
        column(f, 1310, 240, 84, [
            ('Temporal branches → frontal belly, upper orbicularis oculi', '颞支 → 额腹、眼轮匝肌上部', fn[8][-1]),
            ('Zygomatic branches → lower orbicularis oculi', '颧支 → 眼轮匝肌下部', fn[7][-1]),
            ('Buccal branches → buccinator, orbicularis oris, zygomaticus major', '颊支 → 颊肌、口轮匝肌、颧大肌', fn[5][-3]),
            ('Marginal mandibular branch → lower lip and chin', '下颌缘支 → 下唇和颏部', fn[0][-1]),
        ], 'start', 14)
        y = card(f, 1310, 610, 550, 'Greater petrosal nerve: lacrimal gland and glands of the nose and palate. Nerve to stapedius: damps loud sound. Chorda tympani: taste from the anterior two-thirds of the tongue; submandibular and sublingual glands.',
                 '岩大神经：泪腺及鼻、腭腺体。镫骨肌神经：缓冲强声。鼓索：舌前三分之二的味觉；下颌下腺和舌下腺。', NERVE, 13, ('Branches inside the temporal bone', '颞骨内的分支'))
        card(f, 1310, y + 6, 550, 'From top to bottom: Temporal, Zygomatic, Buccal, Marginal mandibular, Cervical ("To Zanzibar By Motor Car").',
             '从上到下：颞支、颧支、颊支、下颌缘支、颈支（英文口诀 To Zanzibar By Motor Car）。', INK, 13, ('Order of the five branches', '五条终末支的顺序'))
        note(f, 40, 1190, ['Nerve lines follow the 3D model; the posterior auricular nerve and the branches to digastric and stylohyoid are added by hand.'],
             ['神经走行依照 3D 模型；耳后神经以及到二腹肌后腹、茎突舌骨肌的分支为手工添加。'])
        f.save('面神经走行与终末支')
