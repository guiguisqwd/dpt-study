"""Figures 13-14: inguinal canal with the inguinal triangle; acupoints."""
from trunkfig import *  # noqa: F401,F403


def register(fig):

    @fig('13')
    def inguinal():
        f = Fig('13', 1800, 1150, 'Right inguinal canal and the inguinal (Hesselbach) triangle (anterior view)', '右侧腹股沟管与腹股沟（Hesselbach）三角（前面观）')
        K = 5600
        s = Stage(f, 'ant', -0.062, -0.905, 640, 610, K)
        clip_begin(f, 30, 140, 1230, 900)
        s.bones(('hip-bone',), op=0.75)
        P = lambda x, y: s.P([x, y, 0])
        asis, pt = P(-0.1179, 0.9451), P(-0.022, 0.852)
        ra = [P(-0.004, 1.0), P(-0.072, 1.0), P(-0.066, 0.94), P(-0.04, 0.875), P(-0.022, 0.853), P(-0.004, 0.85)]
        poly(f, ra, COLOR['rectus-abdominis'], tint(COLOR['rectus-abdominis']), 1.6, op=0.7)
        s.muscle('inguinal-ligament', col='#6b5f4c', op=0.95)
        mid = P(-0.07, 0.8985)
        deep, sup = P(-0.069, 0.912), P(-0.031, 0.866)
        tri = [P(-0.059, 0.923), P(-0.0535, 0.905), P(-0.058, 0.889), P(-0.03, 0.861), P(-0.047, 0.895)]
        tri = [P(-0.0575, 0.925), P(-0.062, 0.893), P(-0.03, 0.862)]
        poly(f, tri, '#8c2f39', '#e7b8bd', 1.6, op=0.75, dash='7 5')
        ves = [P(-0.07, 0.888), P(-0.065, 0.905), P(-0.058, 0.925), P(-0.052, 0.96), P(-0.048, 1.0)]
        f.raw(f'<path d="{curve(ves)}" fill="none" stroke="#c0392b" stroke-width="7" stroke-linecap="round"/><path d="{curve([(x + 9, y) for x, y in ves])}" fill="none" stroke="#3f6fb0" stroke-width="6" stroke-linecap="round"/>')
        canal = [deep, P(-0.055, 0.897), P(-0.042, 0.88), sup]
        f.raw(f'<path d="{curve(canal)}" fill="none" stroke="#7a5aa6" stroke-width="30" stroke-linecap="round" opacity=".28"/>')
        f.raw(f'<path d="{curve(canal)}" fill="none" stroke="#7a5aa6" stroke-width="2.2" stroke-dasharray="9 6"/>')
        f.raw(f'<ellipse cx="{deep[0]:.1f}" cy="{deep[1]:.1f}" rx="20" ry="26" fill="#fff" stroke="#7a5aa6" stroke-width="3" transform="rotate(-35 {deep[0]:.1f} {deep[1]:.1f})"/>')
        f.raw(f'<path d="M{sup[0] - 26:.1f},{sup[1] + 16:.1f} L{sup[0] + 4:.1f},{sup[1] - 30:.1f} L{sup[0] + 26:.1f},{sup[1] + 14:.1f} Z" fill="#fff" stroke="#7a5aa6" stroke-width="3"/>')
        f.end()
        a1, a2 = P(-0.098, 0.96), (deep[0] - 14, deep[1] - 18)
        f.arrow(f'M{a1[0]:.1f},{a1[1]:.1f} L{a2[0]:.1f},{a2[1]:.1f}', '#365e91', 4)
        b1, b2 = P(-0.046, 0.94), P(-0.049, 0.9)
        f.arrow(f'M{b1[0]:.1f},{b1[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f}', '#8c2f39', 4)
        R = 1290
        label(f, R, 190, 'Indirect hernia: enters the deep ring, lateral to the vessels', '斜疝：从血管外侧进入深环', '#365e91', 'start', 14, to=a1)
        label(f, R, 270, 'Direct hernia: through the triangle, medial to the vessels', '直疝：在血管内侧穿过三角', '#8c2f39', 'start', 14, to=b1)
        label(f, R, 350, 'Inferior epigastric vessels', '腹壁下血管', '#c0392b', 'start', 14, to=P(-0.05, 0.975))
        label(f, R, 430, 'Rectus abdominis (lateral border)', '腹直肌（外侧缘）', COLOR['rectus-abdominis'], 'start', 14, to=P(-0.063, 0.95))
        label(f, R, 510, 'Inguinal (Hesselbach) triangle', '腹股沟（Hesselbach）三角', '#8c2f39', 'start', 14, to=P(-0.052, 0.895))
        label(f, R, 590, 'Deep inguinal ring (in the transversalis fascia)', '腹股沟管深环（在腹横筋膜上）', '#7a5aa6', 'start', 14, to=(deep[0] + 12, deep[1]))
        label(f, R, 670, 'Inguinal canal (3–5 cm)', '腹股沟管（长 3–5 cm）', '#7a5aa6', 'start', 14, to=P(-0.048, 0.887))
        label(f, R, 750, 'Superficial inguinal ring (in the external oblique aponeurosis)', '腹股沟管浅环（在腹外斜肌腱膜上）', '#7a5aa6', 'start', 14, to=(sup[0] + 10, sup[1]))
        label(f, R, 830, 'Pubic tubercle', '耻骨结节', INK, 'start', 14, to=pt)
        label(f, R, 910, 'Pubic symphysis', '耻骨联合', INK, 'start', 14, to=P(0, 0.845))
        label(f, 50, 250, 'Anterior superior iliac spine (ASIS)', '髂前上棘', INK, 'start', 14, to=asis)
        label(f, 50, 760, 'Inguinal ligament', '腹股沟韧带', '#6b5f4c', 'start', 14, to=P(-0.085, 0.913))
        label(f, 50, 900, 'Pubic crest', '耻骨嵴', INK, 'start', 14, to=P(-0.012, 0.853))
        note(f, 50, 1060, ['Bones and the inguinal ligament are from the 3D model. The rings, canal, vessels and the border of rectus abdominis are schematic.'],
             ['骨和腹股沟韧带取自 3D 模型。深环、浅环、腹股沟管、血管和腹直肌边缘为示意。'])
        f.save('腹股沟管与腹股沟三角')

    @fig('14')
    def acupoints():
        f = Fig('14', 1800, 1200, 'Eight acupoints on the trunk wall', '躯干壁上的 8 个穴位')
        K = 1450
        s = Stage(f, 'ant', 0.0, -1.12, 560, 620, K)
        s.skin(); torso(s, ribs=range(1, 13), op=0.5); s.bones(('manubrium',), op=0.5)
        s.shape('linea-alba', '#8a7d6a', '#f3ead8', 1.0, op=0.7)
        P = lambda x, y: s.P([x, y, 0])
        UM, XT, PS = 1.02, LM['xiphoid-tip'][1], LM['pubic-symphysis-top'][1]
        up, low, wide = (XT - UM) / 8, (UM - PS) / 5, 0.19 / 8      # one cun on each scale (model metres)
        um = P(0, UM); f.circle(um[0], um[1], 6, '#6b5f4c', '#fff', 1.5)
        ics4 = (LM['rib4-end'][1] + LM['rib5-end'][1]) / 2 + 0.012
        pts = {'CV17': (0, ics4), 'LR14': (4 * wide, 1.213), 'LR13': (-LM['rib11-end'][0], LM['rib11-end'][1] - 0.008),
               'CV12': (0, UM + 4 * up), 'ST25': (2 * wide, UM), 'CV4': (0, UM - 3 * low)}
        for code, (x, y) in pts.items(): point(f, *P(x, y), code)
        # proportional scales
        def scale(x, ya, yb, n, txt_en, txt_zh):
            a, b = P(x, ya), P(x, yb)
            f.path(f'M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}', '#8c2f39', 1.8, rough=False)
            for k in range(n + 1):
                yy = a[1] + (b[1] - a[1]) * k / n; f.path(f'M{a[0] - 5:.1f},{yy:.1f} L{a[0] + 5:.1f},{yy:.1f}', '#8c2f39', 1.4, rough=False)
            f.bi(a[0] - 14, (a[1] + b[1]) / 2, txt_en, txt_zh, 13, '#8c2f39', 'end', '700')
        scale(-0.2, LM['jugular-notch'][1], XT, 9, '9 cun', '9 寸'); scale(-0.2, XT, UM, 8, '8 cun', '8 寸'); scale(-0.2, UM, PS, 5, '5 cun', '5 寸')
        R = 900
        rows = [('CV17', 'CV17 Danzhong', '膻中：横平第 4 肋间隙，前正中线上', 250), ('LR14', 'LR14 Qimen', '期门：第 6 肋间隙，前正中线旁开 4 寸', 340),
                ('CV12', 'CV12 Zhongwan', '中脘：脐中上 4 寸，前正中线上', 470), ('LR13', 'LR13 Zhangmen', '章门：第 11 肋游离端的下际', 600),
                ('ST25', 'ST25 Tianshu', '天枢：横平脐中，前正中线旁开 2 寸', 690), ('CV4', 'CV4 Guanyuan', '关元：脐中下 3 寸，前正中线上', 800)]
        for code, en, zh, ly in rows:
            q = P(*pts[code]); label(f, R, ly, en, zh, '#a3271a', 'start', 15, to=(q[0] + 9, q[1]))
        label(f, 40, 300, 'Jugular notch (Tiantu)', '颈静脉切迹（天突）', GREY, 'start', 14, to=P(0, LM['jugular-notch'][1]))
        label(f, 40, 500, 'Tip of the xiphoid process', '剑突尖', GREY, 'start', 14, to=P(0, XT))
        label(f, 40, 760, 'Centre of the umbilicus', '脐中', GREY, 'start', 14, to=(um[0] - 6, um[1]))
        label(f, 40, 990, 'Upper border of the pubic symphysis', '耻骨联合上缘', GREY, 'start', 14, to=P(0, PS))
        # perineal inset
        title(f, 1470, 128, 'Perineum from below (front at the top)', '会阴下面观（前方在上）')
        i = Stage(f, 'inf', 0.0, 0.02, 1470, 400, 2300)
        for sid in OUTLINES['inf-low']: i.shape(sid, BONE_E, BONE, 1.4, op=0.8, layer='inf-low')
        Q = lambda x, z: i.P([x, 0.83, z])
        anus, gen, cx = Q(0, -0.035), Q(0, 0.012), Q(0, LM['coccyx-tip'][2])
        f.raw(f'<ellipse cx="{anus[0]:.1f}" cy="{anus[1]:.1f}" rx="10" ry="12" fill="#e9d3b8" stroke="#8a6a40" stroke-width="2"/>')
        f.raw(f'<ellipse cx="{gen[0]:.1f}" cy="{gen[1]:.1f}" rx="13" ry="22" fill="#f2d5d9" stroke="#b0567a" stroke-width="2"/>')
        cv1 = (anus[0], (anus[1] - 12 + gen[1] + 22) / 2); gv1 = (anus[0], (anus[1] + 12 + cx[1]) / 2)
        f.circle(*cv1, 7, '#c0392b', '#fff', 2); f.circle(*gv1, 7, '#c0392b', '#fff', 2)
        label(f, 1230, 720, 'CV1 Huiyin', '会阴：前后二阴连线的中点', '#a3271a', 'start', 14, to=(cv1[0] - 8, cv1[1]))
        label(f, 1230, 800, 'GV1 Changqiang', '长强：尾骨端与肛门连线的中点', '#a3271a', 'start', 14, to=(gv1[0] - 8, gv1[1]))
        label(f, 1530, 720, 'Posterior border of the genitals', '外生殖器后缘', '#b0567a', 'start', 13, to=(gen[0] + 10, gen[1] + 16))
        label(f, 1530, 790, 'Anus', '肛门', '#8a6a40', 'start', 13, to=(anus[0] + 9, anus[1]))
        label(f, 1530, 860, 'Tip of the coccyx', '尾骨尖', GREY, 'start', 13, to=cx)
        note(f, 900, 960, ['Positions are learning references on a schematic body outline, not needle sites.', 'The umbilicus is placed schematically; cun are proportional to this figure only.', 'On the chest wall the pleura lies a few layers under the skin.'],
             ['图中位置是画在示意体表轮廓上的学习参照，不是进针点。', '脐的位置为示意；寸按本图的比例折量。', '胸壁皮下隔几层就是胸膜。'])
        f.save('躯干壁的穴位')
