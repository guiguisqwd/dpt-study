"""Figures 05-07: abdominal wall muscles, rectus sheath, pelvic floor."""
from trunkfig import *  # noqa: F401,F403


def register(fig):

    @fig('05')
    def wall():
        f = Fig('05', 1800, 1240, 'Muscles of the anterolateral abdominal wall (anterior view)', '腹前外侧壁的肌（前面观）')
        K = 1500
        A = Stage(f, 'ant', 0.0, -1.07, 330, 610, K); Bp = Stage(f, 'ant', 0.0, -1.07, 900, 610, K)
        for st in (A, Bp): torso(st)
        # Panel A: right external oblique, left internal oblique
        mhatch(A, 'external-oblique', 50); mhatch(A, 'internal-oblique-left', 48)
        A.shape('linea-alba', '#8a7d6a', '#f3ead8', 1.2); A.muscle('inguinal-ligament', col='#6b5f4c'); A.muscle('inguinal-ligament-left', col='#6b5f4c')
        title(f, 330, 128, 'A. Right external oblique, left internal oblique', 'A. 右侧腹外斜肌，左侧腹内斜肌')
        tag(f, *A.P([-0.1, 1.1, 0]), 'EO', COLOR['external-oblique'], 15); tag(f, *A.P([0.09, 1.03, 0]), 'IO', COLOR['internal-oblique'], 15)
        oi(f, [A.at(f'rib{n}-lat', dx=0.012, dy=-0.018) for n in (6, 8, 10)], [A.P([-0.008, 1.1, 0]), A.P([-0.008, 0.95, 0])])
        oi(f, [A.P([0.118, 0.975, 0]), A.P([0.1, 0.95, 0])], [A.P([0.008, 1.05, 0]), A.P([0.008, 0.9, 0])])
        label(f, 40, 1050, 'Inguinal ligament', '腹股沟韧带', '#6b5f4c', 'start', 14, to=A.P([-0.07, 0.905, 0]))
        label(f, 255, 1050, 'Linea alba', '白线', '#6b5f4c', 'start', 14, to=A.P([0.0, 1.0, 0]))
        note(f, 40, 1125, ['The right external oblique and the left internal oblique lie on one diagonal: together they turn the trunk to the left.'], ['右侧腹外斜肌与左侧腹内斜肌的纤维连成一条斜线：两者一起使躯干向左转。'])
        # Panel B: right rectus abdominis and pyramidalis, left transversus abdominis
        mhatch(Bp, 'transversus-abdominis-left', 0); mhatch(Bp, 'rectus-abdominis', 90, 12); Bp.muscle('pyramidalis', op=0.95)
        Bp.shape('linea-alba', '#8a7d6a', '#f3ead8', 1.2)
        for y in (1.2, 1.15, 1.09):  # tendinous intersections
            p1, p2 = Bp.P([-0.075 + (1.2 - y) * 0.2, y, 0]), Bp.P([-0.006, y, 0])
            f.path(f'M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}', '#fcfaf4', 4, rough=False)
        title(f, 900, 128, 'B. Right rectus abdominis and pyramidalis, left transversus abdominis', 'B. 右侧腹直肌和锥状肌，左侧腹横肌')
        tag(f, *Bp.P([-0.04, 1.12, 0]), 'RA', COLOR['rectus-abdominis'], 15); tag(f, *Bp.P([0.09, 1.08, 0]), 'TA', COLOR['transversus-abdominis'], 15)
        tag(f, *Bp.P([-0.03, 0.885, 0]), 'PY', COLOR['pyramidalis'], 13)
        oi(f, [Bp.P([-0.02, 0.853, 0]), Bp.P([-0.004, 0.85, 0])], [Bp.P([-0.07, 1.245, 0]), Bp.P([-0.03, 1.25, 0]), Bp.P([-0.006, 1.236, 0])])
        oi(f, [Bp.P([0.11, 1.12, 0]), Bp.P([0.118, 1.0, 0])], [Bp.P([0.012, 1.14, 0]), Bp.P([0.012, 0.93, 0])])
        label(f, 610, 1050, 'Tendinous intersections', '腱划', GREY, 'start', 14, to=Bp.P([-0.05, 1.15, 0]))
        label(f, 840, 1050, 'Linea semilunaris (lateral edge of rectus abdominis)', '半月线（腹直肌外侧缘）', GREY, 'start', 14, to=Bp.P([-0.079, 1.05, 0]))
        y = legend_oi(f, 1240, 150, [
            ('rectus-abdominis', 'pubic symphysis and pubic crest', '耻骨联合和耻骨嵴', 'xiphoid process and costal cartilages 5–7', '剑突和第 5–7 肋软骨'),
            ('pyramidalis', 'pubic crest and pubic symphysis', '耻骨嵴和耻骨联合', 'linea alba', '白线'),
            ('external-oblique', 'outer surfaces of ribs 5–12', '第 5–12 肋外面', 'linea alba, pubic tubercle, anterior iliac crest', '白线、耻骨结节、髂嵴前部'),
            ('internal-oblique', 'thoracolumbar fascia and iliac crest', '胸腰筋膜和髂嵴', 'ribs 10–12, linea alba, pubic crest', '第 10–12 肋、白线、耻骨嵴'),
            ('transversus-abdominis', 'costal cartilages 7–12, thoracolumbar fascia, iliac crest', '第 7–12 肋软骨、胸腰筋膜、髂嵴', 'linea alba and pubic crest', '白线和耻骨嵴')])
        key_oi(f, 1240, y + 20)
        note(f, 1240, y + 80, ['Muscle outlines are from the 3D model; hatching shows fibre direction.', 'Costal cartilages are drawn schematically.'], ['肌的轮廓取自 3D 模型；斜线表示纤维方向。', '肋软骨为示意补画。'])
        f.save('腹前外侧壁的肌')

    @fig('06')
    def sheath():
        f = Fig('06', 1800, 1180, 'Rectus sheath above and below the arcuate line (transverse sections)', '弓状线上下的腹直肌鞘（横断面）')
        EO, IO, TA, RA = (COLOR[k] for k in ('external-oblique', 'internal-oblique', 'transversus-abdominis', 'rectus-abdominis'))
        cx = 1080

        def section(my, above, ttl):
            f.bi(cx, my - 150, *ttl, 17, INK, 'middle', '700')
            f.path(f'M{cx - 640},{my - 96} Q{cx},{my - 118} {cx + 640},{my - 96}', '#b7ab95', 2.2, rough=False)  # skin
            f.path(f'M{cx - 640},{my + 78} Q{cx},{my + 96} {cx + 640},{my + 78}', '#b0567a', 2.4, rough=False)  # peritoneum
            f.path(f'M{cx - 640},{my + 62} Q{cx},{my + 80} {cx + 640},{my + 62}', '#8a8f6a', 2, rough=False, dash='10 5')  # transversalis fascia
            for sgn in (-1, 1):
                x_m, x_l = cx + sgn * 330, cx + sgn * 640
                for k, col in enumerate((EO, IO, TA)):
                    y0 = my - 36 + k * 24
                    poly(f, [(x_m, y0), (x_l, y0 + 6), (x_l, y0 + 28), (x_m, y0 + 22)], col, tint(col), 1.6)
                rx0, rx1 = cx + sgn * 40, cx + sgn * 300
                f.raw(f'<ellipse cx="{(rx0 + rx1) / 2:.1f}" cy="{my:.1f}" rx="130" ry="36" fill="{tint(RA)}" stroke="{RA}" stroke-width="1.8"/>')
                front, back = my - 46, my + 46
                def line(col, pts, w=4):
                    f.raw(f'<path d="{curve(pts, 0.35)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
                line(EO, [(x_m, my - 25), (rx1 + sgn * 6, front - 4), ((rx0 + rx1) / 2, front - 6), (rx0 - sgn * 6, front - 4), (cx, my - 2)])
                if above:
                    line(IO, [(x_m, my - 1), (rx1 + sgn * 14, my - 1), (rx1 - sgn * 10, front + 3), ((rx0 + rx1) / 2, front + 1), (rx0 - sgn * 4, front + 3), (cx, my + 2)])
                    line(IO, [(rx1 + sgn * 14, my - 1), (rx1 - sgn * 10, back - 3), ((rx0 + rx1) / 2, back - 1), (rx0 - sgn * 4, back - 3), (cx, my + 4)])
                    line(TA, [(x_m, my + 23), (rx1 + sgn * 6, back + 5), ((rx0 + rx1) / 2, back + 6), (rx0 - sgn * 6, back + 4), (cx, my + 6)])
                else:
                    line(IO, [(x_m, my - 1), (rx1 + sgn * 14, my - 8), (rx1 - sgn * 10, front + 3), ((rx0 + rx1) / 2, front + 1), (rx0 - sgn * 4, front + 3), (cx, my + 2)])
                    line(TA, [(x_m, my + 23), (rx1 + sgn * 22, my + 4), (rx1 - sgn * 4, front + 10), ((rx0 + rx1) / 2, front + 8), (rx0 - sgn * 2, front + 9), (cx, my + 5)])
            f.raw(f'<ellipse cx="{cx}" cy="{my + 1}" rx="9" ry="13" fill="#f3ead8" stroke="#8a7d6a" stroke-width="1.6"/>')

        section(330, True, ('A. Above the arcuate line', 'A. 弓状线以上'))
        section(760, False, ('B. Below the arcuate line', 'B. 弓状线以下'))
        f.bi(cx - 640, 205, 'Anterior (skin)', '前（皮肤）', 13, GREY, 'start', '600'); f.bi(cx - 640, 440, 'Posterior (abdominal cavity)', '后（腹腔）', 13, GREY, 'start', '600')
        R = cx + 250
        label(f, cx - 620, 258, 'External abdominal oblique', '腹外斜肌', EO, 'start', 14, to=(cx - 560, 300))
        label(f, cx - 380, 258, 'Internal abdominal oblique', '腹内斜肌', IO, 'start', 14, to=(cx - 420, 328))
        label(f, cx - 520, 500, 'Transversus abdominis', '腹横肌', TA, 'start', 14, to=(cx - 480, 356))
        label(f, cx - 300, 500, 'Rectus abdominis', '腹直肌', RA, 'start', 14, to=(cx - 200, 345))
        label(f, cx + 10, 500, 'Linea alba', '白线', '#6b5f4c', 'start', 14, to=(cx, 340))
        label(f, R, 192, 'Anterior layer: external oblique + half of internal oblique', '前层：腹外斜肌腱膜 + 腹内斜肌腱膜的一半', INK, 'start', 14, to=(cx + 200, 281))
        label(f, R, 500, 'Posterior layer: half of internal oblique + transversus abdominis', '后层：腹内斜肌腱膜的一半 + 腹横肌腱膜', INK, 'start', 14, to=(cx + 200, 378))
        label(f, R, 622, 'Anterior layer: all three aponeuroses', '前层：三层腱膜全部在前', INK, 'start', 14, to=(cx + 200, 716))
        label(f, R, 930, 'No posterior layer: rectus abdominis rests on the transversalis fascia', '没有后层：腹直肌后面直接贴着腹横筋膜', '#6d7250', 'start', 14, to=(cx + 200, 833))
        label(f, cx - 620, 930, 'Transversalis fascia (dashed)', '腹横筋膜（虚线）', '#6d7250', 'start', 14, to=(cx - 520, 826))
        label(f, cx - 330, 930, 'Parietal peritoneum', '壁层腹膜', '#b0567a', 'start', 14, to=(cx - 300, 849))
        # locator
        s = Stage(f, 'ant', 0.0, -1.05, 215, 620, 1250)
        torso(s, op=0.55)
        s.muscle('rectus-abdominis', op=0.75); s.muscle('rectus-abdominis-left', op=0.75); s.shape('linea-alba', '#8a7d6a', '#f3ead8', 1.1)
        um = s.P([0, 1.02, 0]); f.circle(um[0], um[1], 6, '#6b5f4c', '#fff', 1.5)
        for y, t in ((1.1, 'A'), (0.9, 'B')):
            p1, p2 = s.P([-0.13, y, 0]), s.P([0.13, y, 0])
            f.path(f'M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}', '#444', 1.6, dash='8 5', rough=False); f.text(p2[0] + 12, p2[1] + 5, t, 16, '#444', 'start', '700')
        p1, p2 = s.P([-0.085, 0.94, 0]), s.P([0.085, 0.94, 0])
        f.path(f'M{p1[0]:.1f},{p1[1]:.1f} Q{(p1[0] + p2[0]) / 2:.1f},{p1[1] - 22:.1f} {p2[0]:.1f},{p2[1]:.1f}', '#8c2f39', 3, rough=False)
        label(f, 40, 1000, 'Arcuate line', '弓状线', '#8c2f39', 'start', 14, to=(p1[0] + 30, p1[1] - 9))
        label(f, 230, 1000, 'Umbilicus (schematic position)', '脐（示意位置）', '#6b5f4c', 'start', 14, to=um)
        f.bi(215, 150, 'Levels of sections A and B', '断面 A、B 的平面', 15, INK, 'middle', '700')
        note(f, 480, 1040, ['Schematic sections. Sources place the arcuate line about 2.5 cm below the umbilicus or midway between the umbilicus and the pubic symphysis.'],
             ['示意断面。弓状线的位置，资料写脐下约 2.5 cm 或脐与耻骨联合连线的中点。'])
        f.save('弓状线上下的腹直肌鞘')

    @fig('07')
    def pelvic_floor():
        f = Fig('07', 1800, 1120, 'Pelvic floor muscles seen from above', '盆底肌（上面观）')
        PR, PC, IC, CO = (COLOR[k] for k in ('puborectalis', 'pubococcygeus', 'iliococcygeus', 'coccygeus'))
        K = 4300
        s = Stage(f, 'sup', 0.0, 0.012, 600, 580, K)
        for sid in OUTLINES['sup-low']: s.shape(sid, BONE_E, BONE, 1.6, layer='sup-low')
        P = lambda x, z: s.P([x, 0.85, z])
        for sgn in (-1, 1):
            g = lambda pts: [P(x * sgn, z) for x, z in pts]
            f.path(blob(g([(0.0422, -0.0499), (0.036, -0.066), (0.016, -0.076), (0.004, -0.072), (0.02, -0.062)]), 0.4), CO, 1.6, tint(CO), op=0.9)
            f.path(blob(g([(0.031, 0.014), (0.047, -0.012), (0.0435, -0.047), (0.02, -0.06), (0.003, -0.069), (0.003, -0.05), (0.02, -0.03), (0.026, -0.005)]), 0.4), IC, 1.6, tint(IC), op=0.9)
            f.path(blob(g([(0.013, 0.031), (0.024, 0.027), (0.027, -0.005), (0.021, -0.03), (0.004, -0.052), (0.003, -0.044), (0.014, -0.028), (0.017, -0.004)]), 0.4), PC, 1.6, tint(PC), op=0.92)
        pr = [P(x, z) for x, z in [(-0.011, 0.031), (-0.016, 0.0), (-0.014, -0.03), (0.0, -0.045), (0.014, -0.03), (0.016, 0.0), (0.011, 0.031), (0.005, 0.031), (0.009, 0.0), (0.008, -0.027), (0.0, -0.036), (-0.008, -0.027), (-0.009, 0.0), (-0.005, 0.031)]]
        f.path(blob(pr, 0.4), PR, 1.6, tint(PR), op=0.95)
        for sgn in (-1, 1):  # tendinous arch
            a, b, c = P(0.021 * sgn, 0.03), P(0.052 * sgn, -0.008), P(0.0422 * sgn, -0.0499)
            f.path(f'M{a[0]:.1f},{a[1]:.1f} Q{b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}', '#5b4a7a', 3.4, rough=False)
        rect, ur, vg, pb = P(0, -0.026), P(0, 0.016), P(0, 0.002), P(0, -0.0115)
        f.raw(f'<ellipse cx="{rect[0]:.1f}" cy="{rect[1]:.1f}" rx="27" ry="30" fill="#e9d3b8" stroke="#8a6a40" stroke-width="2"/>')
        f.raw(f'<ellipse cx="{vg[0]:.1f}" cy="{vg[1]:.1f}" rx="26" ry="11" fill="#f2d5d9" stroke="#b0567a" stroke-width="2"/>')
        f.circle(ur[0], ur[1], 9, '#f0e2a8', '#9a7434', 2)
        f.raw(f'<rect x="{pb[0] - 9:.1f}" y="{pb[1] - 7:.1f}" width="18" height="14" rx="4" fill="#6b5f4c"/>')
        a, b = P(0, -0.047), P(0, -0.069)
        f.path(f'M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}', '#6b5f4c', 5, rough=False)
        f.bi(600, 150, 'Anterior (pubis)', '前（耻骨）', 15, GREY, 'middle', '700'); f.bi(900, 960, 'Posterior (sacrum and coccyx)', '后（骶骨和尾骨）', 15, GREY, 'middle', '700')
        L, R = 40, 960
        label(f, R, 250, 'Puborectalis (U-shaped sling)', '耻骨直肠肌（U 形吊带）', PR, 'start', 14, to=P(-0.013, -0.02))
        label(f, R, 330, 'Pubococcygeus', '耻骨尾骨肌', PC, 'start', 14, to=P(-0.023, 0.005))
        label(f, R, 410, 'Iliococcygeus', '髂骨尾骨肌', IC, 'start', 14, to=P(-0.037, -0.02))
        label(f, R, 760, 'Coccygeus (on the sacrospinous ligament)', '尾骨肌（贴在骶棘韧带上）', CO, 'start', 14, to=P(-0.03, -0.062))
        label(f, R, 500, 'Tendinous arch of levator ani', '肛提肌腱弓', '#5b4a7a', 'start', 14, to=P(-0.049, -0.012))
        label(f, R, 680, 'Ischial spine', '坐骨棘', INK, 'start', 14, to=P(-0.0422, -0.0499))
        label(f, L, 250, 'Pubic symphysis', '耻骨联合', INK, 'start', 14, to=P(0, 0.036))
        label(f, L, 340, 'Urethra', '尿道', '#9a7434', 'start', 14, to=ur)
        label(f, L, 420, 'Vagina (female)', '阴道（女性）', '#b0567a', 'start', 14, to=(vg[0] - 20, vg[1]))
        label(f, L, 500, 'Perineal body', '会阴体', '#6b5f4c', 'start', 14, to=pb)
        label(f, L, 580, 'Anal canal and rectum', '肛管与直肠', '#8a6a40', 'start', 14, to=(rect[0] - 22, rect[1]))
        label(f, L, 760, 'Anococcygeal ligament', '肛尾韧带', '#6b5f4c', 'start', 14, to=P(0, -0.058))
        label(f, L, 860, 'Coccyx', '尾骨', INK, 'start', 14, to=P(0.002, -0.075))
        label(f, L, 680, 'Urogenital hiatus (gap between the two sides)', '尿生殖裂孔（两侧肌之间的裂隙）', GREY, 'start', 14, to=P(0.006, 0.009))
        oi(f, [P(0.031, 0.012), P(0.047, -0.02)], [P(0.004, -0.056), P(0.004, -0.066)])
        oi(f, [P(0.0422, -0.0499)], [P(0.022, -0.073), P(0.008, -0.075)])
        oi(f, [P(0.006, 0.032), P(0.022, 0.03)], [P(0.0, -0.041)])
        key_oi(f, 60, 960)
        y = legend_oi(f, 1330, 150, [
            ('puborectalis', 'back of the body of the pubis', '耻骨体后面', 'sling behind the anorectal junction (no bone)', '肛管直肠连接处后方的吊带（无骨性止点）'),
            ('pubococcygeus', 'back of the pubis, front of the tendinous arch', '耻骨后面、腱弓前部', 'anococcygeal ligament, coccyx, perineal body', '肛尾韧带、尾骨、会阴体'),
            ('iliococcygeus', 'tendinous arch of levator ani, ischial spine', '肛提肌腱弓、坐骨棘', 'coccyx and anococcygeal ligament', '尾骨和肛尾韧带'),
            ('coccygeus', 'ischial spine', '坐骨棘', 'lateral margin of the lower sacrum and coccyx', '骶骨下部和尾骨的外侧缘')])
        note(f, 1330, y + 20, ['Levator ani = puborectalis + pubococcygeus + iliococcygeus.', 'The model has no pelvic floor muscles; they are drawn', 'schematically on the model pelvis (upper pelvis removed).'],
             ['肛提肌 = 耻骨直肠肌 + 耻骨尾骨肌 + 髂骨尾骨肌。', '模型没有盆底肌；它们是在模型骨盆上示意画的', '（骨盆上部已去掉）。'])
        f.save('盆底肌上面观')
