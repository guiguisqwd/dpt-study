"""Figures 01-02: thoracic cage, a typical rib and its joints."""
from trunkfig import *  # noqa: F401,F403


def register(fig):

    @fig('01')
    def cage():
        f = Fig('01', 1800, 1150, 'Thoracic cage: anterior and right lateral views', '胸廓：前面观与右侧面观')
        K = 2050
        a = Stage(f, 'ant', 0.0, -1.25, 560, 600, K)
        a.cage(); cartilages(a)
        a.bones(('manubrium', 'sternum-body', 'xiphoid'))
        title(f, 560, 128, 'Anterior view', '前面观')
        L, R = 60, 905
        label(f, L, 200, 'Jugular notch', '颈静脉切迹', INK, 'start', 14, to=a.at('jugular-notch'))
        label(f, L, 268, 'Manubrium', '胸骨柄', INK, 'start', 14, to=a.P([0.008, 1.38, 0.05]))
        label(f, R, 300, 'Sternal angle (second costal cartilage)', '胸骨角（平第 2 肋软骨）', '#8c2f39', 'start', 14, to=a.P([0.012, 1.3589, 0.09]))
        label(f, L, 420, 'Body of sternum', '胸骨体', INK, 'start', 14, to=a.P([0.006, 1.30, 0.1]))
        label(f, L, 620, 'Xiphoid process', '剑突', INK, 'start', 14, to=a.P([0.0, 1.232, 0.1]))
        label(f, R, 190, 'First rib', '第 1 肋', GREY, 'start', 14, to=a.P([0.06, 1.413, 0.0]))
        c = cartilage_line(4)[5]; label(f, R, 430, 'Costal cartilage', '肋软骨', CART_E, 'start', 14, to=a.P([-c[0], c[1], c[2]]))
        c = cartilage_line(9)[4]; label(f, R, 760, 'Costal margin (cartilages 7–10)', '肋弓（第 7–10 肋软骨）', CART_E, 'start', 14, to=a.P([-c[0], c[1], c[2]]))
        e = LM['rib7-end']; label(f, R, 600, 'Costochondral joint', '肋软骨结合', GREY, 'start', 14, to=a.P([-e[0], e[1], e[2]]))
        s = STERNAL[5]; label(f, L, 520, 'Sternocostal joint', '胸肋关节', GREY, 'start', 14, to=a.P(list(s)))
        e = LM['rib11-end']; label(f, R, 900, 'Floating ribs (11 and 12)', '浮肋（第 11、12 肋）', GREY, 'start', 14, to=a.P([-e[0], e[1], e[2]]))
        label(f, L, 760, 'True ribs 1–7', '真肋：第 1–7 肋', GREY, 'start', 14)
        label(f, L, 820, 'False ribs 8–12', '假肋：第 8–12 肋', GREY, 'start', 14)
        for n in range(1, 11):  # rib numbers on the right ribs
            q = a.at(f'rib{n}-lat'); f.text(q[0] - 16, q[1] + 5, str(n), 13, '#7a6a55', 'middle', '700')
        b = Stage(f, 'lat', 0.0, -1.25, 1380, 600, K)
        b.cage(sides=('',)); cartilages(b, sides=(1,))
        b.bones(('manubrium', 'sternum-body', 'xiphoid'))
        title(f, 1380, 128, 'Right lateral view', '右侧面观')
        label(f, 1650, 330, 'Sternal angle', '胸骨角', '#8c2f39', 'start', 14, to=b.at('sternal-angle'))
        label(f, 1085, 235, 'T4–T5 level', '约平第 4–5 胸椎', '#8c2f39', 'start', 14, to=b.P([0, 1.3589, -0.042]))
        p1, p2 = b.at('sternal-angle'), b.P([0, 1.3589, -0.042])
        f.path(f'M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}', '#8c2f39', 1.6, dash='8 6', rough=False)
        label(f, 1085, 940, 'Thoracic vertebrae T1–T12', '第 1–12 胸椎', GREY, 'start', 14, to=b.at('t10-sp', dz=0.002))
        label(f, 1650, 700, 'Xiphoid process', '剑突', INK, 'start', 14, to=b.at('xiphoid-tip'))
        note(f, 60, 1010, ['The model has no costal cartilages; the pale blue bars are drawn in schematically.'], ['模型没有肋软骨；浅蓝色的条是示意补画的。'])
        f.save('胸廓前面观与侧面观')

    @fig('02')
    def rib_joints():
        f = Fig('02', 1700, 1000, 'A typical rib and its joints: seventh ribs with the T7 vertebra, seen from above', '典型肋及其关节：第 7 肋与第 7 胸椎（上面观）')
        K = 2900
        s = Stage(f, 'sup', 0.0, 0.0, 850, 540, K)
        s.shape('skeleton-body-of-sternum', BONE_E, BONE, 1.5)
        for sgn in (1, -1):
            pts = [s.P([p[0] * sgn, p[1], p[2]]) for p in bez(LM['rib7-end'], [-0.07, 1.2, 0.1], [-0.02, 1.25, 0.094])]
            d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
            f.raw(f'<path d="{d}" fill="none" stroke="{CART_E}" stroke-width="18" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{CART}" stroke-width="15" stroke-linecap="round"/>')
        s.bones(('rib7', 'rib7-left')); s.shape('skeleton-vertebra-t7', BONE_E, BONE, 1.5)
        f.bi(850, 150, 'Anterior', '前', 15, GREY, 'middle', '700'); f.bi(850, 880, 'Posterior', '后', 15, GREY, 'middle', '700')
        f.bi(1290, 150, 'Right side', '右侧', 15, GREY, 'middle', '700'); f.bi(410, 150, 'Left side', '左侧', 15, GREY, 'middle', '700')
        R, L = 1330, 60
        label(f, R, 800, 'Head of the rib', '肋头', INK, 'start', 14, to=s.at('rib7-head'))
        label(f, R, 870, 'Tubercle of the rib', '肋结节', INK, 'start', 14, to=s.P([-0.047, 1.29, -0.09]))
        label(f, R, 700, 'Angle of the rib', '肋角', INK, 'start', 14, to=s.at('rib7-angle'))
        label(f, R, 500, 'Body of the rib', '肋体', GREY, 'start', 14, to=s.at('rib7-lat'))
        label(f, R, 330, 'Costochondral joint', '肋软骨结合', GREY, 'start', 14, to=s.at('rib7-end'))
        label(f, R, 250, 'Costal cartilage', '肋软骨', CART_E, 'start', 14, to=s.P([-0.066, 1.2, 0.096]))
        label(f, L, 250, 'Sternocostal joint', '胸肋关节', GREY, 'start', 14, to=s.P([0.022, 1.25, 0.094]))
        label(f, L, 330, 'Body of sternum', '胸骨体', INK, 'start', 14, to=s.P([0.004, 1.25, 0.085]))
        hd = LM['rib7-head']; label(f, L, 720, 'Costovertebral joint', '肋头关节（肋椎关节）', '#8c2f39', 'start', 14, to=s.P([-hd[0] - 0.004, hd[1], hd[2] + 0.004]))
        label(f, L, 800, 'Costotransverse joint', '肋横突关节', '#8c2f39', 'start', 14, to=s.P([0.043, 1.29, -0.086]))
        label(f, L, 560, 'Vertebral body of T7', '第 7 胸椎椎体', GREY, 'start', 14, to=s.P([0.01, 1.29, -0.035]))
        label(f, L, 640, 'Transverse process', '横突', GREY, 'start', 14, to=s.P([0.034, 1.29, -0.08]))
        label(f, L, 880, 'Spinous process', '棘突', GREY, 'start', 14, to=s.at('t7-sp'))
        for sgn in (1, -1):  # joint markers
            for p in ([hd[0] * sgn, hd[1], hd[2] + 0.002], [-0.043 * sgn, 1.29, -0.086]):
                q = s.P(p); f.raw(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="13" fill="#8c2f39" fill-opacity=".18" stroke="#8c2f39" stroke-width="2" stroke-dasharray="5 4"/>')
        note(f, 560, 930, ['Red dashed circles mark the two posterior joints of each rib; the costal cartilage is drawn schematically.'], ['红色虚线圈标出每根肋后方的两个关节；肋软骨为示意补画。'])
        f.save('典型肋及其关节')
