"""Figures 11-15: opening in two stages, lines of pull, disc displacement, facial palsy, and the acupoints of the jaw and face.
Figures 11 and 13 use the schematic sagittal joint from tmjfig.tmj_sag; figure 14 is a diagram, not anatomy to scale."""
from tmjfig import *  # noqa: F401,F403

BLUE, RED, GREY = '#3f6f8f', '#c0392b', '#6b6458'


def face(f, cx, cy, weak, k=1.0):
    """Schematic face seen from the front (the patient's right is on the left of the picture).
    weak = set of 'upper', 'lower' for the patient's right side."""
    X = lambda x: cx + x * k
    Y = lambda y: cy + y * k
    f.raw(f'<ellipse cx="{cx}" cy="{cy}" rx="{150 * k}" ry="{200 * k}" fill="{SKIN_F}" stroke="{SKIN}" stroke-width="2"/>')
    if 'upper' in weak:
        f.raw(f'<path d="M{X(0)},{Y(-200)} A{150 * k},{200 * k} 0 0 0 {X(-150)},{Y(0)} L{X(0)},{Y(0)} Z" fill="{RED}" fill-opacity=".22"/>')
    if 'lower' in weak:
        f.raw(f'<path d="M{X(-150)},{Y(0)} A{150 * k},{200 * k} 0 0 0 {X(0)},{Y(200)} L{X(0)},{Y(0)} Z" fill="{RED}" fill-opacity=".22"/>')
    f.raw(f'<path d="M{X(0)},{Y(-200)} L{X(0)},{Y(200)}" stroke="{SKIN}" stroke-width="1" stroke-dasharray="4 5"/>')
    # forehead wrinkles: both sides when the forehead works, absent on a weak side
    for dy in (-150, -132, -114):
        f.raw(f'<path d="M{X(18)},{Y(dy)} q{45 * k},{-8 * k} {90 * k},0" fill="none" stroke="{GREY}" stroke-width="1.6"/>')
        if 'upper' not in weak: f.raw(f'<path d="M{X(-18)},{Y(dy)} q{-45 * k},{-8 * k} {-90 * k},0" fill="none" stroke="{GREY}" stroke-width="1.6"/>')
    # eyebrows (raised on a working side) and eyes (open wider on a weak side)
    f.raw(f'<path d="M{X(25)},{Y(-88)} q{38 * k},{-16 * k} {78 * k},0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    by = -70 if 'upper' in weak else -88
    f.raw(f'<path d="M{X(-25)},{Y(by)} q{-38 * k},{(-4 if "upper" in weak else -16) * k} {-78 * k},0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    f.raw(f'<ellipse cx="{X(62)}" cy="{Y(-45)}" rx="{26 * k}" ry="{9 * k}" fill="#fff" stroke="{INK}" stroke-width="1.6"/><circle cx="{X(62)}" cy="{Y(-45)}" r="{7 * k}" fill="{INK}"/>')
    f.raw(f'<ellipse cx="{X(-62)}" cy="{Y(-45)}" rx="{26 * k}" ry="{(15 if "upper" in weak else 9) * k}" fill="#fff" stroke="{INK}" stroke-width="1.6"/><circle cx="{X(-62)}" cy="{Y(-45)}" r="{7 * k}" fill="{INK}"/>')
    f.raw(f'<path d="M{X(0)},{Y(-30)} L{X(-14)},{Y(40)} L{X(10)},{Y(44)}" fill="none" stroke="{GREY}" stroke-width="1.8"/>')
    # mouth: the weak corner droops and the mouth is pulled toward the working side
    droop = 26 if 'lower' in weak else -6
    f.raw(f'<path d="M{X(-58)},{Y(98 + droop)} Q{X(-10)},{Y(112)} {X(62)},{Y(92)}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    f.raw(f'<path d="M{X(40)},{Y(60)} q{22 * k},{20 * k} {30 * k},{48 * k}" fill="none" stroke="{GREY}" stroke-width="1.4"/>')
    if 'lower' not in weak: f.raw(f'<path d="M{X(-40)},{Y(60)} q{-22 * k},{20 * k} {-30 * k},{48 * k}" fill="none" stroke="{GREY}" stroke-width="1.4"/>')
    f.bi(X(-150), Y(232), "Patient's right", '患者右侧', 13, GREY, 'start', '600')
    f.bi(X(150), Y(232), "Patient's left", '患者左侧', 13, GREY, 'end', '600')


def register(fig):

    @fig('11')
    def opening():
        f = Fig('11', 1900, 1150, 'Mouth opening in two stages: rotation, then translation', '张口的两个阶段：先转动，后滑动')
        K = 1.12
        panels = [(330, 'Mouth closed', '闭口位', 0, 0.0), (950, 'Stage 1: rotation', '第一阶段：转动', 11, 0.0), (1570, 'Stage 2: translation', '第二阶段：滑动', 26, 1.0)]
        pts = []
        for cx, en, zh, turn, slide in panels:
            f.bi(cx + 20, 150, en, zh, 18, INK, 'middle', '700')
            clip_begin(f, cx - 240, 190, 560, 500)
            if turn: tmj_sag(f, cx, 400, K, 0, 0, ghost=True)
            pts.append(tmj_sag(f, cx, 400, K, turn, slide, muscles=True))
            f.end()
        p0, p1, p2 = pts
        column(f, 40, 722, 48, [('Mandibular fossa', '下颌窝', p0['fossa']), ('Articular disc', '关节盘', p0['disc']), ('Head of the mandible', '下颌头', p0['head'])], 'start', 14)
        column(f, 330, 722, 48, [('Articular tubercle', '关节结节', p0['tubercle']), ('Lateral pterygoid', '翼外肌', p0['lp-inf'])], 'start', 14)
        # rotation arrow under the head, translation arrow along the slope
        c = p1['head']
        arrow(f, [(c[0] + 95, c[1] + 150), (c[0] + 70, c[1] + 190), (c[0] + 30, c[1] + 215)], BLUE, 4)
        label(f, 700, 730, 'Rotation in the lower compartment (hinge)', '转动发生在关节下腔（铰链）', BLUE, 'start', 14, to=p1['lower'])
        label(f, 700, 784, 'Dashed outline: closed position', '虚线轮廓：闭口位', GREY, 'start', 14)
        a, b = p0['head'], p2['head']
        dx = 1570 - 330
        arrow(f, [(a[0] + dx, a[1]), b], RED, 4)
        label(f, 1330, 730, 'Translation in the upper compartment (glide)', '滑动发生在关节上腔', RED, 'start', 14, to=p2['upper'])
        label(f, 1330, 784, 'Retrodiscal tissue stretches', '盘后组织被拉长', GREY, 'start', 14, to=p2['retro'])
        y = 880
        card(f, 60, y, 560, 'The condyle sits in the mandibular fossa with the disc on top; the posterior band lies over the crest of the condyle.',
             '髁突位于下颌窝内，关节盘盖在上面，后带位于髁突顶上。', INK, 13, ('Closed', '闭口'), num=1)
        card(f, 670, y, 560, 'The condyle turns like a hinge under the disc. This gives roughly the first 20 mm between the incisors.',
             '髁突在关节盘下方像铰链一样转动，大约提供切牙间最初的 20 mm。', BLUE, 13, ('Rotation', '转动'), num=2)
        card(f, 1280, y, 560, 'Condyle and disc glide forward together down the slope of the articular tubercle while rotation continues.',
             '髁突和关节盘一起沿关节结节斜面向前滑动，转动仍在继续。', RED, 13, ('Translation', '滑动'), num=3)
        f.save('张口的两个阶段')

    @fig('12')
    def lines_of_pull():
        f = Fig('12', 1900, 1240, 'Lines of pull of the muscles that move the jaw', '下颌运动肌的拉力方向')
        clip_begin(f, 480, 150, 940, 960)
        st = Stage(f, 'lat', 0.030, -1.553, 950, 610, 6600); L = st.L
        skull_lat(st, hyoid=True, op=0.75)
        f.end()
        C = COLOR
        pulls = [('temporalis', [L(0.045, 1.570), L(0.043, 1.616)], None), ('temporalis', [L(0.043, 1.572), L(0.022, 1.596), L(-0.012, 1.606)], None),
                 ('masseter', [L(0.016, 1.530), L(0.040, 1.577)], None), ('medial-pterygoid', [L(0.010, 1.528), L(0.030, 1.563)], '9 6'),
                 ('lateral-pterygoid', [L(0.009, 1.568), L(0.040, 1.566)], None), ('digastric', [L(0.078, 1.497), L(0.032, 1.499)], None)]
        for mid, pts, dash in pulls: arrow(f, pts, C.get(mid, INK), 6, dash)
        arrow(f, [L(0.020, 1.496), L(0.017, 1.474)], GREY, 4, '6 5')
        column(f, 30, 215, 96, [
            ('Temporalis, posterior fibres: pull back (retrusion)', '颞肌后部纤维：向后拉（后缩）', L(0.005, 1.603)),
            ('Lateral pterygoid: pulls the neck forward', '翼外肌：把下颌颈向前拉', L(0.022, 1.567)),
            ('Masseter: pulls up, on the outside of the ramus', '咬肌：在下颌支外侧向上拉', L(0.026, 1.550)),
            ('Medial pterygoid (deep, dashed): pulls up', '翼内肌（深面，虚线）：向上拉', L(0.018, 1.542)),
            ('Infrahyoid muscles hold the hyoid bone down', '舌骨下肌把舌骨固定在下方', L(0.018, 1.485)),
        ], 'start', 14)
        column(f, 1440, 215, 96, [
            ('Temporalis, anterior fibres: pull straight up', '颞肌前部纤维：垂直向上提', L(0.044, 1.605)),
            ('Coronoid process', '冠突', L(0.045, 1.567)),
            ('Suprahyoid muscles: pull the chin down and back', '舌骨上肌：把颏部向后下方拉', L(0.055, 1.498)),
            ('Hyoid bone', '舌骨', L(0.024, 1.5005)),
        ], 'start', 14)
        y = card(f, 1440, 640, 420, 'Close: masseter, temporalis, medial pterygoid. Open: gravity, then lateral pterygoid and the suprahyoid muscles. Protrude: both lateral pterygoids. Retrude: posterior temporalis. Side to side: the pterygoids of the opposite side.',
                 '闭口：咬肌、颞肌、翼内肌。张口：先靠重力，再靠翼外肌和舌骨上肌。前伸：两侧翼外肌。后缩：颞肌后部。侧方：对侧的两块翼肌。', INK, 13, ('Which muscles for which movement', '哪个动作用哪些肌'))
        note(f, 40, 1150, ['Arrows start at the attachment on the mandible and point along the pull of the muscle.'], ['箭头从肌在下颌骨上的附着处出发，指向肌的拉力方向。'])
        f.save('下颌运动肌的拉力方向')

    @fig('13')
    def disc_displacement():
        f = Fig('13', 1900, 1500, 'Disc displacement: with reduction and without reduction', '关节盘移位：可复性与不可复性')
        K = 0.92
        xs = [560, 1070, 1580]
        rows = [(190, 'With reduction', '可复性移位', BLUE, [('anterior', 0, 0.0), ('recaptured', 12, 0.45), ('recaptured', 26, 1.0)],
                 [('Closed: the disc lies in front of the condyle', '闭口：关节盘位于髁突前方'), ('Opening: the condyle slips back under the disc, with a click', '张口：髁突滑回关节盘下方，出现弹响'),
                  ('Fully open: normal range', '完全张口：张口度正常')]),
                (800, 'Without reduction (closed lock)', '不可复性移位（闭锁）', RED, [('anterior', 0, 0.0), ('anterior', 11, 0.12), None],
                 [('Closed: the disc lies in front of the condyle', '闭口：关节盘位于髁突前方'), ('Opening: the disc stays in front and blocks the glide', '张口：关节盘留在前方，挡住滑动'), None])]
        for y0, en, zh, col, states, caps in rows:
            f.bi(40, y0 + 40, en, zh, 20, col, 'start', '700')
            for cx, stt, cap in zip(xs, states, caps):
                if not stt: continue
                clip_begin(f, cx - 200, y0, 470, 430)
                p = tmj_sag(f, cx, y0 + 190, K, stt[1], stt[2], disc=stt[0], muscles=False)
                f.end()
                f.bi(cx + 30, y0 + 470, cap[0], cap[1], 14, INK, 'middle', '600')
                if y0 == 190 and stt[1] == 0:
                    label(f, 40, y0 + 150, 'Displaced disc', '移位的关节盘', BLUE, 'start', 14, to=p['disc'])
                    label(f, 40, y0 + 210, 'Retrodiscal tissue under load', '盘后组织受压', '#c0706a', 'start', 14, to=p['retro'])
                    label(f, 40, y0 + 270, 'Condyle', '髁突', INK, 'start', 14, to=p['head'])
                if stt[0] == 'recaptured' and stt[1] == 12:
                    q = p['disc']; f.raw(f'<path d="M{q[0] + 46:.1f},{q[1] - 52:.1f} l14,-18 M{q[0] + 60:.1f},{q[1] - 36:.1f} l22,-10 M{q[0] + 28:.1f},{q[1] - 62:.1f} l4,-22" stroke="{RED}" stroke-width="3.5" stroke-linecap="round"/>')
                    label(f, cx + 150, y0 + 60, 'Click', '弹响', RED, 'start', 15)
                if y0 == 800 and stt[1]:
                    q = p['disc']; f.raw(f'<path d="M{q[0] + 30:.1f},{q[1] - 26:.1f} l26,26 m0,-26 l-26,26" stroke="{RED}" stroke-width="4.5" stroke-linecap="round"/>')
        y = card(f, 1380, 830, 470, 'Opening is limited, typically to 30 mm or less when the lock is recent. The chin deflects toward the affected side and stays there. The earlier click has disappeared.',
                 '闭锁初期张口受限，通常不超过 30 mm。颏部偏向患侧且不回到中线。原有的弹响消失。', RED, 13, ('Result', '结果'))
        card(f, 1380, y + 4, 470, 'With reduction: range is normal; the chin swings toward the affected side until the click and then returns to the midline.',
             '可复性移位：张口度正常；弹响之前颏部偏向患侧，弹响后回到中线。', BLUE, 13, ('Compare', '对比'))
        note(f, 40, 1400, ['Blue band: articular disc. Pink: retrodiscal tissue. The joint is drawn as a schematic sagittal section, anterior to the right.'],
             ['蓝色带：关节盘。粉色：盘后组织。关节为矢状切面示意图，右侧为前方。'])
        f.save('关节盘移位可复性与不可复性')

    @fig('14')
    def facial_palsy():
        f = Fig('14', 1900, 1280, 'Facial palsy: peripheral or central', '面瘫：周围性还是中枢性')
        # pathway diagram in the middle
        f.bi(950, 150, 'Why the forehead is spared in a central lesion', '中枢性病变为什么不累及前额', 17, INK, 'middle', '700')
        bx = lambda x, y, w, h, col, en, zh: (f.box(x, y, w, h, col, '#fffdf7'), f.bi(x + w / 2, y + h / 2 - 2, en, zh, 13, col, 'middle', '700'))
        bx(700, 200, 200, 64, INK, 'Right motor cortex', '右侧运动皮质'); bx(1000, 200, 200, 64, INK, 'Left motor cortex', '左侧运动皮质')
        bx(700, 520, 230, 64, NERVE, 'Upper part of the nucleus', '面神经核上部'); bx(700, 600, 230, 64, NERVE, 'Lower part of the nucleus', '面神经核下部')
        f.bi(686, 588, 'Right facial nucleus (pons)', '右侧面神经核（脑桥）', 13, shade(NERVE), 'end', '700')
        arrow(f, [(790, 264), (790, 518)], GREY, 3)
        arrow(f, [(1070, 264), (1010, 400), (900, 522)], GREY, 3)
        arrow(f, [(1130, 264), (1090, 480), (932, 632)], GREY, 3)
        bx(700, 800, 230, 56, NERVE, 'Right facial nerve', '右侧面神经')
        arrow(f, [(815, 664), (815, 798)], NERVE, 4)
        bx(640, 940, 170, 56, INK, 'Right forehead and eye', '右侧前额和眼'); bx(830, 940, 170, 56, INK, 'Right lower face', '右侧面下部')
        arrow(f, [(790, 856), (730, 938)], NERVE, 3); arrow(f, [(840, 856), (910, 938)], NERVE, 3)
        # lesion markers
        for (x, y), code, col in (((1105, 340), 'A', BLUE), ((815, 730), 'B', RED)):
            f.raw(f'<path d="M{x - 26},{y - 12} l52,24 m0,-24 l-52,24" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
            f.circle(x + 52, y, 15, col, '#fff', 2); f.text(x + 52, y + 5, code, 14, '#fff', 'middle', '700')
        label(f, 1120, 560, 'The upper part receives fibres from both sides', '核上部接受双侧皮质的纤维', GREY, 'start', 13)
        label(f, 1120, 640, 'The lower part receives fibres from the opposite side only', '核下部只接受对侧皮质的纤维', GREY, 'start', 13)
        # faces
        f.bi(300, 150, 'B. Peripheral palsy (nerve or nucleus)', 'B. 周围性面瘫（面神经或面神经核）', 17, RED, 'middle', '700')
        face(f, 300, 460, {'upper', 'lower'})
        card(f, 60, 760, 480, 'Same side as the lesion. The whole half of the face is weak: the forehead does not wrinkle, the eye does not close and the corner of the mouth droops.',
             '与病变同侧。半侧面部全部无力：不能皱额，闭不上眼，口角下垂。', RED, 13, ('Forehead involved', '前额受累'))
        f.bi(1600, 150, 'A. Central palsy (above the nucleus)', 'A. 中枢性面瘫（面神经核以上）', 17, BLUE, 'middle', '700')
        face(f, 1600, 460, {'lower'})
        card(f, 1360, 760, 480, 'Opposite side to the lesion, for example a stroke. Only the lower face is weak: the forehead still wrinkles and the eye still closes.',
             '在病变对侧，例如脑卒中。只有面下部无力：仍能皱额，仍能闭眼。', BLUE, 13, ('Forehead spared', '前额不受累'))
        card(f, 60, 1040, 1780, 'Ask the patient to raise the eyebrows, close the eyes tightly, show the teeth and puff out the cheeks. A spared forehead points to the brain and needs urgent assessment for stroke.',
             '让患者抬眉、用力闭眼、示齿、鼓腮。前额不受累提示病变在脑内，需要按脑卒中紧急评估。', INK, 13, ('Bedside test', '床旁检查'))
        f.save('周围性与中枢性面瘫')

    @fig('15')
    def acupoints():
        f = Fig('15', 1900, 1300, 'Acupoints around the jaw joint and face, right lateral view', '颞下颌关节与面部周围的穴位，右侧面观')
        clip_begin(f, 420, 150, 960, 1000)
        st = Stage(f, 'lat', 0.036, -1.560, 900, 650, 7400); L = st.L
        skin_lat(st); skull_lat(st, op=0.6)
        st.shape('Parotid gland', '#9a8f7c', '#e8dcc6', 1.3, op=0.55, outer=True)
        st.muscle('masseter', op=0.45)
        ear_lat(st, op=0.9, region=False)
        f.end()
        P = {'ST7': L(0.027, 1.5725), 'ST6': L(0.022, 1.534), 'ST4': L(0.081, 1.545), 'SI18': L(0.060, 1.570), 'SI19': L(0.0015, 1.5775), 'TE21': L(0.0015, 1.5845), 'GB2': L(0.0015, 1.5705),
             'TE17': L(-0.010, 1.556)}
        for code, p in P.items():
            if code in ('SI19', 'TE21', 'GB2'): point(f, p[0], p[1], code, dx=13, dy=5, anchor='start')
            elif code == 'TE17': point(f, p[0], p[1], code, dx=-13, dy=5, anchor='end')
            else: point(f, p[0], p[1], code)
        column(f, 30, 300, 92, [
            ('TE21 Ermen: in front of the supratragic notch', 'TE21 耳门：耳屏上切迹前', P['TE21']),
            ('SI19 Tinggong: in front of the middle of the tragus', 'SI19 听宫：耳屏正中前', P['SI19']),
            ('GB2 Tinghui: in front of the intertragic notch', 'GB2 听会：耳屏间切迹前', P['GB2']),
            ('TE17 Yifeng: behind the ear lobe', 'TE17 翳风：耳垂后方', P['TE17']),
            ('Angle of the mandible', '下颌角', L(0.0105, 1.524)),
        ], 'start', 14)
        column(f, 1400, 300, 92, [
            ('Zygomatic arch', '颧弓', L(0.036, 1.579)),
            ('ST7 Xiaguan: below the zygomatic arch, over the mandibular notch', 'ST7 下关：颧弓下缘与下颌切迹之间', P['ST7']),
            ('Mandibular notch', '下颌切迹', L(0.031, 1.5585)),
            ('SI18 Quanliao: below the zygomatic bone, under the outer canthus', 'SI18 颧髎：颧骨下缘，目外眦直下', P['SI18']),
            ('Masseter', '咬肌', L(0.030, 1.548)),
            ('ST4 Dicang: beside the angle of the mouth', 'ST4 地仓：口角旁', P['ST4']),
            ('ST6 Jiache: on masseter, in front of and above the angle', 'ST6 颊车：咬肌上，下颌角前上方一横指', P['ST6']),
        ], 'start', 14)
        note(f, 40, 1180, ['The three points in front of the ear lie between the tragus and the condyle; they are located with the mouth slightly open.',
                           'Positions are marked from the written standard locations on a schematic head; palpate the landmarks on a real person.'],
             ['耳前三穴位于耳屏和髁突之间，微张口取穴。', '位置按标准定位文字标在示意头部上；实际取穴要触摸骨性标志。'])
        f.save('颞下颌关节与面部穴位')
