"""Figures 12–14: movement. 12: lines of pull and the lumbar movements; 13: pelvic tilt force couples;
14: lumbopelvic rhythm in forward bending and the timing of trunk muscle activity."""
from lumbarfig import *  # noqa: F401,F403

ACT = '#2f4858'   # movement arrows (solid = force or movement, AN-13)
HIP_C = [0.0, 0.875, 0.012]   # approximate centre of the right hip joint (lateral view)


def arrow_line(f, a, b, col, w=3.2, dash=None):
    f.arrow(f'M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}', col, w, dash=dash, rough=False)


def arc(f, cx, cy, r, a0, a1, col=ACT, w=3, ccw=False):
    """Curved movement arrow around (cx, cy), angles in degrees (0 = right, 90 = down)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if ccw else 1
    f.arrow(f'M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}', col, w, rough=False)


def lat_skeleton(f, st, femur=True, clip=None):
    if clip: clip_begin(f, *clip)
    st.bones(('rib10', 'rib11', 'rib12'), op=0.7)
    st.bones(('hip-bone',))
    if femur: st.shape('appendicular-skeleton-femur-right', BONE_E, BONE, 1.5)
    st.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'))
    if clip: f.end()


def register(fig):

    @fig('12')
    def lines_of_pull():
        f = Fig('12', 1750, 1260, 'Lines of pull and lumbar movements: what lies behind, beside and in front of the axis',
                '拉力线与腰椎动作：在运动轴之后、之旁和之前的肌肉')
        # ---- A: right lateral view, flexion–extension
        a = Stage(f, 'lat', -0.01, -1.0, 330, 600, 2300)
        f.bi(330, 150, 'A. Right lateral view (anterior right): extension', 'A. 右侧面观（前方在右）：后伸', 16, INK, 'middle', '700')
        lat_skeleton(f, a, clip=(40, 190, 550, 930))
        P = a.P
        es = [P([-0.04, 0.975, -0.085]), P([-0.045, 1.10, -0.09]), P([-0.06, 1.17, -0.095])]
        f.path(curve(es), COLOR['iliocostalis-lumborum'], 14, op=0.35, rough=False)
        arrow_line(f, es[2], (es[2][0] + 3, es[2][1] + 90), COLOR['iliocostalis-lumborum'], 4)
        mf = [P([0, 0.93, -0.092]), P([0, 0.975, -0.08]), P([0, 1.03, -0.07])]
        f.path(curve(mf), COLOR['multifidus'], 10, op=0.45, rough=False)
        arrow_line(f, mf[2], (mf[2][0] - 2, mf[2][1] + 60), COLOR['multifidus'], 4)
        ps = [P([-0.03, 1.10, 0.0]), P([-0.04, 1.0, 0.012]), P([-0.06, 0.90, 0.045]), P([-0.085, 0.80, -0.02])]
        f.path(curve(ps), COLOR['psoas-major'], 12, op=0.4, rough=False)
        arrow_line(f, ps[3], (ps[3][0] + 18, ps[3][1] - 55), COLOR['psoas-major'], 4)
        ax = P([0, 1.03, -0.006]); f.circle(ax[0], ax[1], 7, ACT, '#fff', 2)
        arc(f, ax[0], ax[1], 330, 290, 250, ACT, 3.4, ccw=True)
        label(f, 40, 720, 'Erector spinae', '竖脊肌', COLOR['iliocostalis-lumborum'], 'start', 14, to=es[0])
        label(f, 40, 820, 'Multifidus', '多裂肌', COLOR['multifidus'], 'start', 14, to=mf[0])
        label(f, 390, 1080, 'Psoas major', '腰大肌', COLOR['psoas-major'], 'start', 14, to=ps[3])
        label(f, 420, 252, 'Axis (schematic, near the disc)', '运动轴（示意，靠近椎间盘）', ACT, 'start', 14, to=ax)
        # ---- B: posterior view, lateral flexion
        b = Stage(f, 'post', 0.0, -1.03, 900, 610, 2700)
        f.bi(900, 150, 'B. Posterior view: lateral flexion', 'B. 后面观：侧屈', 16, INK, 'middle', '700')
        clip_begin(f, 600, 190, 600, 800)
        b.bones(('hip-bone', 'hip-bone-left', 'rib11', 'rib11-left', 'rib12', 'rib12-left'))
        b.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'))
        b.muscle('quadratus-lumborum', op=0.8)
        f.end()
        q1, q2 = b.P([-0.075, 1.055, -0.04]), b.P([-0.058, 1.0, -0.04])
        arrow_line(f, q1, (q1[0] + 4, q1[1] + 70), COLOR['quadratus-lumborum'], 4)
        it = [b.P([0.042, 1.075, -0.04]), b.P([0.042, 1.055, -0.04])]
        arrow_line(f, it[0], it[1], COLOR['intertransversarii'], 3)
        arc(f, 900, 610, 300, 255, 290, ACT, 3.4)
        label(f, 900, 1040, 'Quadratus lumborum: bends the trunk to its own side', '腰方肌：使躯干向同侧屈', COLOR['quadratus-lumborum'], 'middle', 14, to=q2)
        label(f, 620, 300, 'Intertransversarii', '横突间肌', COLOR['intertransversarii'], 'start', 14, to=it[0])
        # ---- C: superior view of the L3–L4 joints: rotation
        c = Stage(f, 'sup', 0.0, 0.03, 1470, 520, 4200)
        f.bi(1470, 150, 'C. From above: rotation is blocked by the joints', 'C. 上面观：关节突关节限制旋转', 16, INK, 'middle', '700')
        c.shape('skeleton-vertebra-l4', BONE_E, SHADE, 1.5)
        c.shape('skeleton-vertebra-l4', BONE_E, BONE, 1.3, layer='sup-1')
        Q = lambda x, z: c.P([x, 1, z])
        for sg in (1, -1):
            j = [Q(sg * 0.014, -0.026), Q(sg * 0.0165, -0.034), Q(sg * 0.021, -0.041), Q(sg * 0.027, -0.044)]
            f.path(curve(j), '#6f7d8c', 3, rough=False)
            iap = [Q(sg * 0.0105 + 0.004 * math.cos(t), -0.035 + 0.008 * math.sin(t)) for t in [k * math.pi / 6 for k in range(12)]]
            f.path(blob(iap), '#6f7d8c', 1.6, '#e8edf2', dash='5 3', rough=False)
        cx, cy = Q(0, -0.003)
        arc(f, cx, cy, 100, 200, 330, ACT, 3.4)
        hit = Q(-0.014, -0.033); f.text(hit[0] + 20, hit[1] + 6, '×', 30, HERN if 'HERN' in globals() else '#b04a3a', 'middle', '700')
        label(f, 1290, 840, 'Superior articular process of L4', 'L4 上关节突', GREY, 'start', 13, to=Q(0.02, -0.04))
        label(f, 1290, 920, 'Inferior articular process of L3 (dashed)', 'L3 下关节突（虚线）', '#6f7d8c', 'start', 13, to=Q(0.0105, -0.04))
        note(f, 1290, 1000, ['The joint surfaces face mostly sideways, so they', 'block rotation but let flexion and extension glide.'],
             ['关节面大多朝向侧方，', '所以挡住旋转，允许屈伸滑动。'])
        note(f, 40, 1150, ['A: erector spinae and, deep to them, multifidus lie behind the axis; both extend the lumbar spine. Psoas major runs close to the axis and mainly flexes the hip.'],
             ['A：竖脊肌及其深面的多裂肌位于运动轴后方，二者都使腰椎后伸。腰大肌靠近运动轴，主要屈髋。'])
        f.save('作用线与腰椎动作')

    @fig('13')
    def pelvic_tilt():
        f = Fig('13', 1700, 1235, 'Pelvic tilt force couples (teaching model): two pairs of muscles turn the pelvis about the hip joints',
                '骨盆倾斜的力偶（教学模型）：两对肌肉使骨盆绕髋关节转动')
        for k, (title, zh, cx) in enumerate([('A. Anterior tilt: lordosis increases', 'A. 前倾：腰椎前凸增加', 430),
                                              ('B. Posterior tilt: lordosis decreases', 'B. 后倾：腰椎前凸减少', 1230)]):
            st = Stage(f, 'lat', 0.0, -0.95, cx, 560, 2200)
            f.bi(cx, 150, title, zh, 17, INK, 'middle', '700')
            clip_begin(f, cx - 400, 190, 800, 800)
            st.bones(('hip-bone',)); st.shape('appendicular-skeleton-femur-right', BONE_E, BONE, 1.5)
            st.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'))
            f.end()
            P = st.P
            hc = P(HIP_C); f.circle(hc[0], hc[1], 8, ACT, '#fff', 2)
            band = lambda pts, col, w=14: f.path(curve(pts), col, w, op=0.35, rough=False)
            if k == 0:
                es = [P([0, 0.975, -0.068]), P([0, 1.05, -0.07]), P([0, 1.12, -0.075])]
                band(es, COLOR['iliocostalis-lumborum'])
                arrow_line(f, es[0], (es[0][0] - 2, es[0][1] - 120), COLOR['iliocostalis-lumborum'], 4.5)
                hf = [P([0, 1.04, 0.0]), P([0, 0.94, 0.03]), P([0, 0.885, 0.048]), P([0, 0.79, -0.02])]
                band(hf, COLOR['psoas-major'])
                arrow_line(f, hf[1], (hf[1][0] + 30, hf[1][1] + 95), COLOR['psoas-major'], 4.5)
                arc(f, hc[0], hc[1], 150, 260, 330, ACT, 3.6)
                label(f, cx - 380, 260, 'Erector spinae', '竖脊肌', COLOR['iliocostalis-lumborum'], 'start', 14, to=es[2])
                label(f, cx + 120, 960, 'Hip flexors (iliopsoas)', '屈髋肌（髂腰肌）', COLOR['psoas-major'], 'start', 14, to=hf[3])
                label(f, cx - 380, 900, 'Hip joint: the pivot', '髋关节：转动中心', ACT, 'start', 14, to=hc)
            else:
                ra = [P([0, 0.86, 0.062]), P([0, 1.0, 0.085]), P([0, 1.12, 0.10])]
                band(ra, '#3f7f6e')
                arrow_line(f, ra[0], (ra[0][0] + 8, ra[0][1] - 120), '#3f7f6e', 4.5)
                gm = [P([0, 0.935, -0.085]), P([0, 0.85, -0.075]), P([0, 0.77, -0.035])]
                band(gm, '#a8423a')
                arrow_line(f, gm[0], (gm[0][0] + 14, gm[0][1] + 110), '#a8423a', 4.5)
                hm = [P([0, 0.826, -0.058]), P([0, 0.765, -0.062])]
                band(hm, '#7a5230', 12)
                arrow_line(f, hm[0], (hm[0][0] - 3, hm[0][1] + 110), '#7a5230', 4.5)
                arc(f, hc[0], hc[1], 150, 330, 260, ACT, 3.6, ccw=True)
                label(f, cx + 190, 860, 'Rectus abdominis', '腹直肌', '#3f7f6e', 'start', 14, to=ra[1])
                label(f, cx - 390, 300, 'Gluteus maximus', '臀大肌', '#a8423a', 'start', 14, to=gm[0])
                label(f, cx - 390, 960, 'Hamstrings (unverified)', '腘绳肌（未核实）', '#7a5230', 'start', 14, to=hm[1])
                label(f, cx + 190, 960, 'Hip joint: the pivot', '髋关节：转动中心', ACT, 'start', 14, to=hc)
        note(f, 40, 1030, ['A: erector spinae pull the back of the pelvis up while the hip flexors pull the front down, so the pelvis tips forward.',
                           'B: the abdominals pull the front up while gluteus maximus and the hamstrings pull the back down, so the pelvis tips back.',
                           'Teaching model, not yet checked in a kinesiology textbook. Sourced: rectus abdominis works on posterior pelvic tilt; the deep abdominals may assist gluteus maximus in controlling anterior pelvic rotation.'],
             ['A：竖脊肌向上拉骨盆后部，屈髋肌向下拉骨盆前部，骨盆前倾。', 'B：腹肌向上拉骨盆前部，臀大肌和腘绳肌向下拉骨盆后部，骨盆后倾。',
              '教学模型，尚未在运动学教材中核对。有来源的部分：腹直肌参与骨盆后倾；深层腹肌可能协助臀大肌控制骨盆前旋。'])
        f.save('骨盆倾斜力偶')

    @fig('14')
    def rhythm_timing():
        f = Fig('14', 1700, 1040, 'Lumbopelvic rhythm in forward bending, and trunk muscles switching on before the limb moves',
                '前屈时的腰椎-骨盆节律，以及肢体动作前躯干肌的提前激活')
        f.bi(560, 140, 'A. Forward bending and return (side view, facing right)', 'A. 前屈与回位（侧面观，面向右）', 16, INK, 'middle', '700')
        def person(cx, base, lumbar, pelvis, col_l, col_p):
            """Stick figure: feet at (cx, base); pelvis tilted forward by `pelvis` degrees at the hip; lumbar flexion `lumbar`."""
            hip = (cx, base - 250)
            f.path(f'M{cx},{base} L{hip[0]},{hip[1]}', '#6b6257', 7, rough=False)            # leg
            f.circle(hip[0], hip[1], 9, ACT, '#fff', 2)                                     # hip joint
            pr = math.radians(pelvis)
            sac = (hip[0] + 44 * math.sin(pr) - 8 * math.cos(pr), hip[1] - 44 * math.cos(pr) - 8 * math.sin(pr))
            pel = [(hip[0] + 30 * math.cos(t) * math.cos(pr) - 44 * math.sin(t) * math.sin(pr) + 18 * math.sin(pr),
                    hip[1] + 30 * math.cos(t) * math.sin(pr) + 44 * math.sin(t) * math.cos(pr) - 18 * math.cos(pr)) for t in [k * math.pi / 8 for k in range(16)]]
            f.path(blob(pel), col_p, 2.4, tint(col_p, 0.7), rough=False)
            # lumbar spine: 5 segments from the sacrum, flexion spread evenly
            pts = [sac]; ang = pr
            for k in range(5):
                ang += math.radians(lumbar) / 5
                x, y = pts[-1]; pts.append((x + 21 * math.sin(ang), y - 21 * math.cos(ang)))
            f.path(curve(pts), col_l, 7, rough=False)
            x, y = pts[-1]
            th = (x + 115 * math.sin(ang), y - 115 * math.cos(ang))
            f.path(f'M{x:.1f},{y:.1f} L{th[0]:.1f},{th[1]:.1f}', '#6b6257', 7, rough=False)   # thorax
            hd = (th[0] + 30 * math.sin(ang), th[1] - 30 * math.cos(ang)); f.circle(hd[0], hd[1], 21, '#efe6d2', '#6b6257', 3)
            return hip, pts
        LC, PC = '#365e91', '#9c3f6e'
        poses = [(170, 0, 0, '1. Upright', '1. 直立'), (480, 45, 10, '2. Classic model: lumbosacral flexion leads', '2. 经典模型：腰骶部屈曲在前'),
                 (850, 55, 60, '3. The pelvis tilts forward at the hips', '3. 骨盆在髋关节处前倾')]
        for cx, lum, pel, en, zh in poses:
            person(cx, 760, lum, pel, LC, PC)
            f.bi(cx, 820, en, zh, 14, INK, 'middle', '700')
        f.arrow('M260,650 L380,650', ACT, 3, rough=False); f.arrow('M590,650 L710,650', ACT, 3, rough=False)
        f.bi(560, 880, 'Return to standing: the hips lead (posterior pelvic tilt by the hip extensors), then the lumbar spine extends.',
             '回到站立：髋部先动（伸髋肌使骨盆后倾），然后腰椎后伸。', 14, ACT, 'middle', '600')
        f.bi(560, 930, 'Going down, erector spinae and the hip extensors work eccentrically; coming up, the hip extensors start the posterior pelvic tilt, then erector spinae work concentrically.',
             '向下时竖脊肌和伸髋肌离心工作；向上时伸髋肌先启动骨盆后倾，随后竖脊肌向心工作。', 13, GREY, 'middle', '400')
        tag(f, 1000, 250, 'L', LC, 13); f.bi(1022, 256, 'Lumbar spine', '腰椎', 13, LC, 'start', '700')
        tag(f, 1000, 300, 'P', PC, 13); f.bi(1022, 306, 'Pelvis', '骨盆', 13, PC, 'start', '700')
        # ---- B: timing (qualitative)
        x0, x1, zero = 1180, 1660, 1440
        f.bi(1420, 140, 'B. Who switches on first (rapid arm movement)', 'B. 谁先激活（快速上肢运动）', 16, INK, 'middle', '700')
        f.path(f'M{x0},700 L{x1},700', INK, 2, rough=False)
        f.path(f'M{zero},230 L{zero},700', '#8c2f39', 2, dash='6 4', rough=False)
        f.bi(zero, 735, 'Deltoid starts the arm movement', '三角肌启动上肢运动', 13, '#8c2f39', 'middle', '700')
        f.bi(x0, 735, 'earlier', '更早', 12, GREY, 'start', '400'); f.bi(x1, 735, 'later', '更晚', 12, GREY, 'end', '400')
        bars = [('Transversus abdominis, healthy', '腹横肌，健康人', 1330, '#2b6c7c', None),
                ('Other trunk muscles: onset varies', '其他躯干肌：激活时间不定', 1400, '#7a8f9e', '8 4'),
                ('Transversus abdominis, low back pain', '腹横肌，腰痛者', 1500, '#b04a3a', None)]
        for i, (en, zh, xs, col, dash) in enumerate(bars):
            y = 300 + i * 130
            f.bi(x0, y - 20, en, zh, 13, col, 'start', '700')
            if dash:  # onset range only: it varied with movement direction, before or after the deltoid
                f.path(f'M{zero - 80},{y + 30} L{zero + 80},{y + 30}', col, 16, dash=dash, rough=False, op=0.8)
                continue
            f.path(f'M{xs},{y + 30} L{x1},{y + 30}', col, 16, dash=dash, rough=False, op=0.8)
            f.circle(xs, y + 30, 7, col, '#fff', 2)
        note(f, 1180, 800, ['Healthy: transversus abdominis came on before the deltoid in every direction.', 'Low back pain: its onset was delayed.'],
             ['健康人：无论哪个方向，腹横肌都在三角肌之前激活。', '腰痛者：其激活延迟。'])
        f.save('腰椎骨盆节律与前馈激活')
