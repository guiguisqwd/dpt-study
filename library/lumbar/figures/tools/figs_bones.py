"""Figures 01-03: bones, landmarks, joints and ligaments."""
from lumbarfig import *  # noqa: F401,F403

# Fixes to computed points (midline structures)
LM['sacral-promontory'] = [0.0, 0.948, -0.005]
LM['post-sacral-foramen'] = [-0.017, 0.944, -0.082]
LM['sacral-hiatus'] = [0.0, 0.868, -0.086]


def register(fig):

    @fig('01')
    def bones_overview():
        f = Fig('01', 1700, 1180, 'Lumbar spine, sacrum and pelvis: posterior and right lateral views',
                '腰椎、骶骨与骨盆：后面观与右侧面观')
        K = 2500
        p = Stage(f, 'post', 0.0, -1.0, 560, 660, K)
        low = p.P2(0, -0.862)[1]
        p.bones(('rib11', 'rib11-left', 'rib12', 'rib12-left', 'coccyx'))
        p.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'))
        clip_begin(f, 0, 0, 1000, low); p.bones(('hip-bone', 'hip-bone-left')); f.end()
        # Supracristal (Tuffier's) line across the tops of the iliac crests
        a, b = p.at('iliac-crest-top'), p.P(mirror(LM['iliac-crest-top']))
        f.path(f'M{a[0] - 30:.1f},{a[1]:.1f} L{b[0] + 30:.1f},{b[1]:.1f}', '#8c2f39', 1.8, dash='9 6', rough=False)
        f.bi(a[0] + 105, a[1] + 4, 'Supracristal line ≈ L4 spinous process', '嵴上线 ≈ 第 4 腰椎棘突', 14, '#8c2f39', 'start', '700')
        f.bi(560, 150, 'Posterior view', '后面观', 18, INK, 'middle', '700')
        for i in range(1, 6):
            q = p.at(f'l{i}-sp')
            label(f, 120, q[1] + 6, f'L{i} vertebra', f'第 {i} 腰椎', INK, 'start', 14, to=(q[0] - 4, q[1]))
        q = p.at('t12-sp'); label(f, 120, q[1] + 4, 'T12 vertebra', '第 12 胸椎', INK, 'start', 14, to=(q[0] - 4, q[1]))
        label(f, 860, 420, 'Twelfth rib', '第 12 肋', GREY, 'start', 14, to=p.P([-0.07, 1.075, -0.05]))
        label(f, 860, 300, 'Spinous process', '棘突', GREY, 'start', 14, to=p.at('l2-sp'))
        label(f, 872, 490, 'Transverse process', '横突', GREY, 'start', 14, to=p.at('l3-tp'))
        label(f, 860, 560, 'Iliac crest', '髂嵴', GREY, 'start', 14, to=p.P([-0.085, 1.0, -0.05]))
        label(f, 905, 760, 'Posterior superior iliac spine (PSIS)', '髂后上棘', GREY, 'start', 14, to=p.at('psis'))
        label(f, 905, 840, 'Posterior sacral foramina', '骶后孔', GREY, 'start', 14, to=p.P([-0.0172, 0.908, -0.09]))
        label(f, 120, 880, 'Median sacral crest', '骶正中嵴', GREY, 'start', 14, to=p.at('median-sacral-crest'))
        label(f, 120, 1000, 'Coccyx', '尾骨', GREY, 'start', 14, to=p.at('coccyx-tip', dy=0.012))
        label(f, 120, 800, 'Sacrum', '骶骨', GREY, 'start', 14, to=p.P([0.02, 0.93, -0.08]))

        l = Stage(f, 'lat', -0.035, -1.0, 1360, 660, K)
        l.spine(('t12', 'l1', 'l2', 'l3', 'l4', 'l5'))
        l.bones(('coccyx',))
        f.bi(1360, 150, 'Right lateral view (anterior to the right)', '右侧面观（前方在右）', 18, INK, 'middle', '700')
        label(f, 1520, 330, 'Vertebral body', '椎体', GREY, 'start', 14, to=l.at('l1-body-ant', dz=-0.01))
        mid = lambda a, b: [(x + y) / 2 for x, y in zip(LM[a], LM[b])]
        ivf = mid('l3-pedicle', 'l4-pedicle'); ivf[2] -= 0.004
        label(f, 1520, 520, 'Intervertebral foramen', '椎间孔', GREY, 'start', 14, to=l.P(ivf))
        label(f, 1520, 430, 'Intervertebral disc space', '椎间盘间隙', GREY, 'start', 14, to=l.P(mid('l2-body-ant', 'l3-body-ant')))
        label(f, 1040, 330, 'Spinous process', '棘突', GREY, 'start', 14, to=l.at('l1-sp'))
        label(f, 1040, 470, 'Pedicle', '椎弓根', GREY, 'start', 14, to=l.at('l3-pedicle'))
        fj = mid('l4-iap', 'l5-sap')
        label(f, 1040, 565, 'Zygapophyseal (facet) joint', '关节突关节', GREY, 'start', 14, to=l.P(fj))
        label(f, 1520, 760, 'Sacral promontory', '骶骨岬', GREY, 'start', 14, to=l.at('sacral-promontory'))
        label(f, 1520, 680, 'Lumbosacral joint (L5–S1)', '腰骶关节（L5–S1）', GREY, 'start', 14, to=l.P([0, 0.956, -0.007]))
        # Lordosis arc (anterior convexity)
        pts = [l.at(f'{lv}-body-ant', dz=0.005) for lv in ['l1', 'l2', 'l3', 'l4', 'l5']]
        d = 'M' + ' L'.join('%.1f,%.1f' % q for q in pts)
        f.raw(f'<path d="{d}" fill="none" stroke="{TEAL}" stroke-width="2.4" stroke-dasharray="3 6" stroke-linecap="round"/>')
        f.bi(1530, 595, 'Lumbar lordosis', '腰椎前凸', 15, TEAL, 'start', '700')
        f.save('腰椎骶骨与骨盆')

    register_02(fig)
    register_03(fig)


def register_02(fig):

    @fig('02')
    def typical_vertebra():
        f = Fig('02', 1700, 1060, 'A typical lumbar vertebra (L4): superior view and the L4–L5 motion segment from the right',
                '典型腰椎（第 4 腰椎）：上面观与右侧观的 L4–L5 运动节段')
        s = Stage(f, 'sup', 0.0, 0.025, 470, 560, 6400)
        s.shape('skeleton-vertebra-l4', BONE_E, SHADE, 2.0)
        s.shape('skeleton-vertebra-l4', BONE_E, BONE, 1.6, layer='sup-1')
        s.shape('skeleton-vertebra-l4', BONE_E, '#fffaf0', 1.6, layer='sup-2')
        f.bi(470, 150, 'L4 seen from above (anterior up)', '第 4 腰椎上面观（前方在上）', 18, INK, 'middle', '700')
        sp = lambda x, z: s.P([x, 1.02, z])
        label(f, 760, 250, 'Vertebral body', '椎体', GREY, 'start', 14, to=sp(0.0, -0.002))
        label(f, 760, 900, 'Spinous process', '棘突', GREY, 'start', 14, to=sp(0.0, -0.062))
        label(f, 60, 580, 'Transverse process', '横突', GREY, 'start', 14, to=sp(0.040, -0.033))
        label(f, 60, 250, 'Pedicle', '椎弓根', GREY, 'start', 14, to=sp(0.016, -0.019))
        label(f, 760, 640, 'Lamina', '椎板', GREY, 'start', 14, to=sp(-0.011, -0.045))
        label(f, 60, 520, 'Superior articular process', '上关节突', GREY, 'start', 14, to=sp(0.021, -0.036))
        label(f, 60, 760, 'Mammillary process', '乳突', GREY, 'start', 14, to=sp(0.024, -0.045))
        label(f, 60, 640, 'Accessory process', '副突', GREY, 'start', 14, to=sp(0.028, -0.032))
        label(f, 760, 420, 'Vertebral canal (vertebral foramen)', '椎管（椎孔）', GREY, 'start', 14, to=sp(0.0, -0.030))
        note(f, 60, 960, ['Lumbar superior facets face posteromedially: they limit axial rotation and resist translation.'],
             ['腰椎上关节面朝向后内侧：限制轴向旋转并抵抗平移。'])

        l = Stage(f, 'lat', -0.02, -1.0, 1320, 560, 5200)
        for lv in ('l4', 'l5'): l.shape(VERT[lv], BONE_E, BONE, 1.8)
        l.shape(VERT['l5'], BONE_E, '#fffaf0', 1.6, layer='lat-2')
        f.bi(1320, 150, 'L4–L5 from the right (anterior to the right)', 'L4–L5 右侧观（前方在右）', 18, INK, 'middle', '700')
        pars = l.P([-0.0165, 1.015, -0.0365])
        f.raw(f'<ellipse cx="{pars[0]:.1f}" cy="{pars[1]:.1f}" rx="22" ry="34" fill="#b94334" fill-opacity=".18" stroke="#b94334" stroke-width="2.2" stroke-dasharray="5 4"/>')
        label(f, 1000, 330, 'Pars interarticularis', '椎弓峡部', '#b94334', 'start', 14, to=(pars[0] - 18, pars[1] - 20))
        mid = lambda a, b: [(x + y) / 2 for x, y in zip(LM[a], LM[b])]
        label(f, 1000, 820, 'Facet joint (L4 inferior + L5 superior articular process)', '关节突关节（L4 下关节突 + L5 上关节突）', GREY, 'start', 14,
              to=l.P(mid('l4-iap', 'l5-sap')))
        ivf = mid('l4-pedicle', 'l5-pedicle'); ivf[2] -= 0.003
        label(f, 1500, 330, 'Intervertebral foramen', '椎间孔', GREY, 'start', 14, to=l.P(ivf))
        label(f, 1525, 600, 'Disc space (L4–L5)', '椎间盘间隙（L4–L5）', GREY, 'start', 14, to=l.P(mid('l4-body-ant', 'l5-body-ant')))
        label(f, 1000, 220, 'Superior articular process', '上关节突', GREY, 'start', 14, to=l.at('l4-sap'))
        label(f, 1000, 760, 'Spinous process', '棘突', GREY, 'start', 14, to=l.at('l5-sp'))
        label(f, 1500, 700, 'Pedicle', '椎弓根', GREY, 'start', 14, to=l.at('l5-pedicle'))
        f.save('典型腰椎与运动节段')


SAG = OUTLINES['sag']
LIG = {'all': '#4b7f8c', 'pll': '#6b5fa5', 'lf': '#c9a227', 'isl': '#8a9a5b', 'ssl': '#a0522d', 'disc': '#9fb7c8', 'nucleus': '#d8e7f0',
       'ilio': '#a0522d', 'itl': '#6b8e23'}


def sag_pt(st, zy, dz=0.0, dy=0.0): return st.P([0.0, zy[1] + dy, zy[0] + dz])


def register_03(fig):

    @fig('03')
    def disc_ligaments():
        f = Fig('03', 1700, 1180, 'Intervertebral disc and the ligaments of the lumbar spine',
                '腰椎的椎间盘与韧带')
        st = Stage(f, 'lat', -0.022, -1.02, 520, 640, 4600)
        levels = ['l2', 'l3', 'l4', 'l5']
        f.bi(520, 150, 'Midline (sagittal) section, L2–L5, seen from the right (anterior to the right)',
             '正中矢状切面 L2–L5，右侧观（前方在右）', 17, INK, 'middle', '700')
        # discs first
        for up, lo in zip(levels, levels[1:]):
            a, b = SAG[up]['body'], SAG[lo]['body']
            q = [sag_pt(st, a[1]), sag_pt(st, b[0]), sag_pt(st, b[3]), sag_pt(st, a[2])]
            f.path('M' + ' L'.join('%.1f,%.1f' % p for p in q) + 'Z', '#5d7d92', 1.6, LIG['disc'])
            c = [(q[0][0] + q[1][0] + q[2][0] * 1.3 + q[3][0] * 1.3) / 4.6, (q[0][1] + q[1][1] + q[2][1] + q[3][1]) / 4]
            h = abs(q[1][1] - q[0][1]) * 0.32 + 4
            f.raw(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{abs(q[0][0] - q[3][0]) * 0.22:.1f}" ry="{h:.1f}" fill="{LIG["nucleus"]}" stroke="#5d7d92" stroke-width="1.4"/>')
        for lv in levels:
            for part in ['body', 'arch']:
                q = [sag_pt(st, zy) for zy in SAG[lv][part]]
                f.path('M' + ' L'.join('%.1f,%.1f' % p for p in q) + 'Z', BONE_E, 1.8, BONE)
            c = [sum(sag_pt(st, zy)[i] for zy in SAG[lv]['body']) / 4 for i in (0, 1)]
            f.text(c[0], c[1] + 6, lv.upper(), 18, '#8a7a5a', 'middle', '700')
        # S1 top (schematic)
        l5 = SAG['l5']['body']
        # S1 body (schematic, dashed): its upper surface faces forwards and upwards (sacral slope)
        s1 = [sag_pt(st, l5[1], dz=-0.001, dy=-0.010), sag_pt(st, l5[1], dz=-0.012, dy=-0.038), sag_pt(st, l5[2], dz=-0.014, dy=-0.030), sag_pt(st, l5[2], dz=-0.002, dy=-0.006)]
        q = [sag_pt(st, l5[1]), s1[0], s1[3], sag_pt(st, l5[2])]
        f.path('M' + ' L'.join('%.1f,%.1f' % p for p in q) + 'Z', '#5d7d92', 1.6, LIG['disc'])
        f.path('M' + ' L'.join('%.1f,%.1f' % p for p in s1) + 'Z', BONE_E, 1.8, BONE, dash='6 4')
        f.text((s1[0][0] + s1[2][0]) / 2, (s1[0][1] + s1[1][1]) / 2 + 6, 'S1', 18, '#8a7a5a', 'middle', '700')
        # ligaments
        def band(pts, col, w, dash=None):
            d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
            f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity=".85"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        ant = [sag_pt(st, SAG[lv]['body'][i], dz=0.0022) for lv in levels for i in (0, 1)] + [s1[0]]
        band(ant, LIG['all'], 9)
        post = [sag_pt(st, SAG[lv]['body'][i], dz=-0.0016) for lv in levels for i in (3, 2)] + [s1[3]]
        band(post, LIG['pll'], 5)
        for up, lo in zip(levels, levels[1:]):
            a, b = SAG[up]['arch'], SAG[lo]['arch']
            band([sag_pt(st, a[1], dz=0.001), sag_pt(st, b[0], dz=0.001)], LIG['lf'], 9)
            q = [sag_pt(st, a[1]), sag_pt(st, b[0]), sag_pt(st, b[3]), sag_pt(st, a[2])]
            f.path('M' + ' L'.join('%.1f,%.1f' % p for p in q) + 'Z', LIG['isl'], 1.2, '#d6dfc0', op=0.9)
        ssl = [sag_pt(st, SAG[lv]['arch'][i], dz=-0.0018) for lv in levels[:3] for i in (3, 2)]
        band(ssl, LIG['ssl'], 6)
        band([ssl[-1], sag_pt(st, SAG['l5']['arch'][3], dz=-0.0018), sag_pt(st, SAG['l5']['arch'][2], dz=-0.0018)], LIG['ssl'], 4, dash='4 6')
        mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        A = lambda lv, i, part='body': sag_pt(st, SAG[lv][part][i])
        label(f, 900, 300, 'Anterior longitudinal ligament', '前纵韧带', LIG['all'], 'start', 14, to=mid(ant[0], ant[1]))
        label(f, 900, 400, 'Nucleus pulposus', '髓核', '#3f6d86', 'start', 14, to=mid(A('l3', 1), A('l4', 3)))
        label(f, 900, 500, 'Annulus fibrosus', '纤维环', '#3f6d86', 'start', 14, to=mid(mid(A('l3', 1), A('l4', 0)), mid(A('l3', 1), A('l4', 3))))
        label(f, 900, 600, 'Vertebral body (endplates above and below the disc)', '椎体（椎间盘上下为终板）', GREY, 'start', 14, to=mid(mid(A('l4', 0), A('l4', 1)), mid(A('l4', 0), A('l4', 2))))
        label(f, 900, 760, 'Lumbosacral junction (L5–S1)', '腰骶连接（L5–S1）', GREY, 'start', 14, to=mid(A('l5', 1), s1[0]))
        label(f, 60, 250, 'Supraspinous ligament', '棘上韧带', LIG['ssl'], 'start', 14, to=mid(ssl[0], ssl[1]))
        label(f, 60, 360, 'Interspinous ligament', '棘间韧带', LIG['isl'], 'start', 14, to=mid(A('l2', 2, 'arch'), A('l3', 3, 'arch')))
        label(f, 60, 470, 'Ligamentum flavum', '黄韧带', '#9a7b12', 'start', 14, to=mid(A('l3', 1, 'arch'), A('l4', 0, 'arch')))
        label(f, 60, 580, 'Spinous process', '棘突', GREY, 'start', 14, to=mid(A('l4', 2, 'arch'), A('l4', 3, 'arch')))
        label(f, 400, 250, 'Vertebral canal', '椎管', GREY, 'start', 14, to=mid(A('l4', 3), A('l4', 0, 'arch')))
        label(f, 60, 930, 'Posterior longitudinal ligament', '后纵韧带', LIG['pll'], 'start', 14, to=post[7])
        note(f, 60, 995, ['Sources differ on where the supraspinous ligament ends.', 'Some give about L3–L4; others, the sacrum (dashed).'], ['各资料对棘上韧带的下端说法不一。', '有的写约在 L3–L4，有的写延伸至骶骨（虚线）。'])

        # Panel B: disc from above
        cx, cy = 1390, 330
        f.bi(cx, 150, 'Disc seen from above', '椎间盘上面观', 17, INK, 'middle', '700')
        for k in range(6):
            f.raw(f'<ellipse cx="{cx}" cy="{cy}" rx="{190 - k * 16}" ry="{120 - k * 10}" fill="{LIG["disc"] if k == 0 else "none"}" stroke="#5d7d92" stroke-width="{1.8 if k == 0 else 1.1}"/>')
        f.raw(f'<ellipse cx="{cx}" cy="{cy + 14}" rx="78" ry="46" fill="{LIG["nucleus"]}" stroke="#5d7d92" stroke-width="1.6"/>')
        label(f, 1690, 520, 'Annulus fibrosus (concentric lamellae)', '纤维环（同心板层）', '#3f6d86', 'end', 14, to=(cx + 150, cy - 40))
        label(f, 1250, 230, 'Nucleus pulposus', '髓核', '#3f6d86', 'end', 14, to=(cx - 20, cy + 14))
        f.bi(cx, cy - 140, 'Anterior', '前', 13, GREY, 'middle', '600')
        f.bi(cx, cy + 150, 'Posterior (towards the canal)', '后（朝向椎管）', 13, GREY, 'middle', '600')

        # Panel C: iliolumbar and intertransverse ligaments, posterior view
        p = Stage(f, 'post', 0.0, -0.995, 1390, 880, 2500)
        f.bi(1390, 640, 'Iliolumbar and intertransverse ligaments (posterior view)', '髂腰韧带与横突间韧带（后面观）', 15, INK, 'middle', '700')
        top = p.P2(0, -1.05)[1]
        clip_begin(f, 1080, top, 620, 1100 - top)
        p.spine(('l3', 'l4', 'l5'), w=1.3)
        p.bones(('hip-bone', 'hip-bone-left'))
        f.end()
        for side in (lambda q: q, mirror):
            a = p.P(side(LM['l5-tp'])); b = p.P(side([-0.075, 1.0, -0.045]))
            band([a, b], LIG['ilio'], 8)
            c1 = p.P(side(LM['l4-tp'])); c2 = p.P(side(LM['l5-tp']))
            band([c1, c2], LIG['itl'], 5)
        label(f, 1110, 1124, 'Iliolumbar ligament (L5 transverse process → iliac crest)', '髂腰韧带（L5 横突 → 髂嵴）', LIG['ilio'], 'start', 13,
              to=p.P([-0.065, 1.0, -0.04]))
        label(f, 1110, 712, 'Intertransverse ligament', '横突间韧带', LIG['itl'], 'start', 13,
              to=p.P([(LM['l4-tp'][0] + LM['l5-tp'][0]) / 2, (LM['l4-tp'][1] + LM['l5-tp'][1]) / 2, -0.03]))
        f.save('椎间盘关节突关节与韧带')
