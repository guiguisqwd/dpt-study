"""Figure 08: cross-section through the lower back (thoracolumbar fascia and the muscle compartments)."""
from lumbarfig import *  # noqa: F401,F403

TLF = '#3d5a80'


def register(fig):

    @fig('08')
    def cross_section():
        f = Fig('08', 1700, 1080, 'Cross-section of the lower back at a mid-lumbar level: the thoracolumbar fascia and the muscle compartments',
                '腰椎中段水平的下背部横断面：胸腰筋膜与肌肉分隔')
        st = Stage(f, 'sup', 0.0, 0.03, 700, 560, 4200)
        lft = lambda x, z: st.P([x, 1, z])    # the person's left = image left
        rgt = lambda x, z: st.P([-x, 1, z])   # the person's right = image right
        for s in (lft, rgt):
            # skin of the back
            sk = [s(0.09, -0.005), s(0.091, -0.045), s(0.075, -0.08), s(0.04, -0.094), s(0.0, -0.097)]
            f.path('M' + ' L'.join('%.1f,%.1f' % p for p in sk), '#b7ab95', 1.6, rough=False)
            # abdominal wall muscles heading anterolaterally from the lateral raphe (cut short)
            for k, (col, d) in enumerate([('#8a7a5a', 0.0), ('#9a8a6a', 0.005), ('#aa9a7a', 0.010)]):
                a, b, c = s(0.075 + d * 0.3, -0.042), s(0.082 + d, -0.02), s(0.080 + d, 0.008)
                f.path(f'M{a[0]:.1f},{a[1]:.1f} Q{b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}', col, 5 - k, rough=False)
            f.path(blob(ell(st, (1 if s is lft else -1) * 0.031, -0.004, 0.016, 0.019)), COLOR['psoas-major'], 1.6, tint(COLOR['psoas-major']))
            sg = 1 if s is lft else -1
            f.path(blob(ell(st, sg * 0.058, -0.027, 0.017, 0.009)), COLOR['quadratus-lumborum'], 1.6, tint(COLOR['quadratus-lumborum']))
            f.path(blob(ell(st, sg * 0.013, -0.061, 0.011, 0.017)), COLOR['multifidus'], 1.6, tint(COLOR['multifidus']))
            f.path(blob(ell(st, sg * 0.033, -0.060, 0.012, 0.016)), COLOR['longissimus-thoracis'], 1.6, tint(COLOR['longissimus-thoracis']))
            f.path(blob(ell(st, sg * 0.054, -0.056, 0.011, 0.013)), COLOR['iliocostalis-lumborum'], 1.6, tint(COLOR['iliocostalis-lumborum']))
        st.shape('skeleton-vertebra-l4', BONE_E, SHADE, 1.8)
        st.shape('skeleton-vertebra-l4', BONE_E, BONE, 1.4, layer='sup-1')
        for s in (lft, rgt):
            # posterior layer: spinous process → over multifidus and erector spinae → lateral raphe
            post = [s(0.0, -0.066), s(0.02, -0.08), s(0.045, -0.078), s(0.065, -0.068), s(0.075, -0.042)]
            f.path('M' + ' L'.join('%.1f,%.1f' % p for p in post), TLF, 3.2, rough=False)
            # middle layer: transverse process tip → lateral raphe (between erector spinae and quadratus lumborum)
            mid = [s(0.044, -0.034), s(0.06, -0.038), s(0.075, -0.042)]
            f.path('M' + ' L'.join('%.1f,%.1f' % p for p in mid), TLF, 2.6, rough=False)
            # anterior layer: front of the transverse process → over quadratus lumborum → lateral raphe
            ant = [s(0.042, -0.026), s(0.058, -0.016), s(0.072, -0.024), s(0.075, -0.042)]
            f.path('M' + ' L'.join('%.1f,%.1f' % p for p in ant), TLF, 2.0, dash='6 4', rough=False)
            f.circle(*s(0.075, -0.042), 5, TLF, '#fff', 1.5)
        f.bi(700, 132, 'Seen from above (anterior up); the person\'s right side is on the right', '上面观（前方在上）；身体右侧在图右侧', 15, INK, 'middle', '700')
        label(f, 700, 215, 'Vertebral body', '椎体', GREY, 'middle', 14, to=st.P([0, 1, 0.012]))
        # right column: muscles and bony parts of the person's right side
        label(f, 1180, 300, 'Psoas major', '腰大肌', COLOR['psoas-major'], 'start', 14, to=rgt(0.031, -0.004))
        label(f, 1180, 400, 'Quadratus lumborum', '腰方肌', COLOR['quadratus-lumborum'], 'start', 14, to=rgt(0.058, -0.027))
        label(f, 1180, 500, 'Transverse process', '横突', GREY, 'start', 14, to=rgt(0.043, -0.032))
        label(f, 1180, 600, 'Iliocostalis lumborum', '腰髂肋肌', COLOR['iliocostalis-lumborum'], 'start', 14, to=rgt(0.054, -0.056))
        label(f, 1180, 700, 'Longissimus thoracis', '胸最长肌', COLOR['longissimus-thoracis'], 'start', 14, to=rgt(0.033, -0.060))
        label(f, 1180, 800, 'Multifidus', '多裂肌', COLOR['multifidus'], 'start', 14, to=rgt(0.013, -0.061))
        label(f, 1180, 900, 'Spinous process', '棘突', GREY, 'start', 14, to=st.P([0, 1, -0.064]))
        # left column: the thoracolumbar fascia on the person's left side
        f.bi(40, 300, 'Thoracolumbar fascia', '胸腰筋膜', 16, TLF, 'start', '700')
        label(f, 40, 380, 'Anterior layer', '前层', TLF, 'start', 14, to=lft(0.058, -0.016))
        label(f, 40, 470, 'Abdominal wall muscles (cut)', '腹壁肌（切断）', '#8a7a5a', 'start', 14, to=lft(0.083, -0.012))
        label(f, 40, 580, 'Middle layer', '中层', TLF, 'start', 14, to=lft(0.06, -0.038))
        label(f, 40, 680, 'Lateral raphe', '外侧缝', TLF, 'start', 14, to=lft(0.075, -0.042))
        label(f, 40, 800, 'Posterior layer', '后层', TLF, 'start', 14, to=lft(0.045, -0.078))
        note(f, 40, 975, ['Posterior layer: spinous processes to the lateral raphe, over the erector spinae and multifidus. Middle layer: transverse process tips to the lateral raphe.',
                          'Anterior layer: over the front of quadratus lumborum. Transversus abdominis and internal oblique attach at the lateral raphe.'],
             ['后层：从棘突越过竖脊肌和多裂肌到外侧缝。中层：从横突尖到外侧缝。', '前层：覆盖腰方肌前面。腹横肌和腹内斜肌附着在外侧缝。'])
        f.save('下背部横断面与胸腰筋膜')
