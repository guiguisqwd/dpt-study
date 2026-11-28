"""Figures 08-10: intercostal nerve course, trunk wall nerves with dermatomes, pudendal nerve."""
from trunkfig import *  # noqa: F401,F403


def register(fig):

    @fig('08')
    def intercostal_nerve():
        f = Fig('08', 1800, 1080, 'Course of an intercostal nerve: section at the seventh rib, seen from above', '肋间神经的走行：第 7 肋平面的断面（上面观）')
        K = 2500
        s = Stage(f, 'sup', 0.0, -0.005, 640, 570, K)
        P = lambda x, z: s.P([x, 1.25, z])
        skin = [P(0.172 * math.cos(t), 0.0 + 0.128 * math.sin(t) - 0.002) for t in [2 * math.pi * k / 40 for k in range(40)]]
        f.path(blob(skin), '#b7ab95', 2, '#f7efe2', rough=False)
        s.shape('skeleton-body-of-sternum', BONE_E, BONE, 1.5)
        for sgn in (1, -1):
            pts = [s.P([p[0] * sgn, p[1], p[2]]) for p in bez(LM['rib7-end'], [-0.07, 1.2, 0.1], [-0.02, 1.25, 0.094])]
            d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
            f.raw(f'<path d="{d}" fill="none" stroke="{CART_E}" stroke-width="16" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{CART}" stroke-width="13" stroke-linecap="round"/>')
        s.bones(('rib7', 'rib7-left')); s.shape('skeleton-vertebra-t7', BONE_E, BONE, 1.5)
        cord = P(0, -0.0707); f.raw(f'<ellipse cx="{cord[0]:.1f}" cy="{cord[1]:.1f}" rx="13" ry="11" fill="#f0e2a8" stroke="#8a6a10" stroke-width="2"/>')
        main = [P(-0.005, -0.0707), P(-0.02, -0.073), P(-0.034, -0.08), P(-0.075, -0.086), P(-0.112, -0.055), P(-0.131, 0.008), P(-0.118, 0.05), P(-0.097, 0.075), P(-0.062, 0.089), P(-0.03, 0.084)]
        nerve(f, main, 5, smooth=True)
        nerve(f, [P(-0.02, -0.073), P(-0.028, -0.095), P(-0.03, -0.118)], 3.5, smooth=True)          # posterior ramus
        nerve(f, [P(-0.131, 0.008), P(-0.15, 0.014), P(-0.168, 0.02)], 3.5, smooth=True)               # lateral cutaneous
        nerve(f, [P(-0.03, 0.084), P(-0.034, 0.104), P(-0.03, 0.124)], 3.5, smooth=True)               # anterior cutaneous
        g = P(-0.024, -0.05); f.circle(g[0], g[1], 9, NERVE, '#8a6a10', 1.5)
        nerve(f, [P(-0.024, -0.05), P(-0.024, -0.072)], 2.5)
        for n, (x, z) in enumerate([(-0.02, -0.062), (-0.052, -0.07), (-0.1, -0.058), (-0.118, 0.012), (-0.047, 0.074)], 1): f.step(*P(x, z), n)
        f.bi(640, 150, 'Anterior', '前', 15, GREY, 'middle', '700'); f.bi(640, 960, 'Posterior', '后', 15, GREY, 'middle', '700')
        L = 40
        label(f, L, 880, 'Spinal cord', '脊髓', '#8a6a10', 'start', 14, to=(cord[0] - 10, cord[1]))
        label(f, L, 800, 'Sympathetic ganglion and rami communicantes', '交感神经节与交通支', '#8a6a10', 'start', 14, to=(g[0] - 2, g[1] - 4))
        label(f, 900, 960, 'Posterior ramus (to the back muscles and skin)', '后支（到背部肌和皮肤）', '#8a6a10', 'start', 14, to=P(-0.03, -0.112))
        label(f, 1085, 520, 'Lateral cutaneous branch', '外侧皮支', '#8a6a10', 'start', 14, to=P(-0.16, 0.017))
        label(f, 840, 205, 'Anterior cutaneous branch', '前皮支', '#8a6a10', 'start', 14, to=P(-0.033, 0.112))
        label(f, L, 300, 'Sternum', '胸骨', INK, 'start', 14, to=P(0.012, 0.09))
        label(f, L, 420, 'Seventh rib', '第 7 肋', INK, 'start', 14, to=P(0.14, 0.0))
        label(f, L, 660, 'T7 vertebra', '第 7 胸椎', INK, 'start', 14, to=P(0.012, -0.04))
        label(f, L, 220, 'Skin', '皮肤', GREY, 'start', 14, to=P(0.11, 0.097))
        step_cards(f, 1260, 150, [
            ('Leaves the intervertebral foramen; the anterior ramus turns laterally and is joined to the sympathetic trunk.', '出椎间孔；前支转向外侧，并与交感干相连。'),
            ('Near the spine it lies between the internal intercostal membrane and the parietal pleura.', '在脊柱附近，位于肋间内膜与壁层胸膜之间。'),
            ('From about the angle of the rib it runs in the costal groove, between the internal and innermost intercostals, below the vein and artery.', '大约从肋角起走在肋沟内，位于肋间内肌与肋间最内肌之间，在静脉和动脉下方。'),
            ('Near the midaxillary line the lateral cutaneous branch pierces the muscles to the skin.', '在腋中线附近，外侧皮支穿出肌层到皮肤。'),
            ('Beside the sternum it turns forward and ends as the anterior cutaneous branch.', '在胸骨旁转向前方，终末为前皮支。')], 500)
        note(f, 1260, 800, ['The nerve is drawn on the inner side of the rib; in life it lies under the', 'lower border of the rib, hidden from above.'], ['神经画在肋骨内侧；实际位于肋骨下缘的深面，', '从上方看被肋骨遮住。'])
        f.save('肋间神经的走行')

    @fig('09')
    def trunk_nerves():
        f = Fig('09', 1800, 1200, 'Nerves of the trunk wall (T7–L1) and dermatome landmarks (anterior view)', '躯干壁的神经（T7–L1）与皮节标志（前面观）')
        K = 1450
        s = Stage(f, 'ant', 0.0, -1.12, 760, 620, K)
        s.skin()
        torso(s, ribs=range(2, 13), op=0.55)
        s.muscle('rectus-abdominis', op=0.35); s.muscle('inguinal-ligament', col='#6b5f4c'); s.muscle('inguinal-ligament-left', col='#6b5f4c')
        P = lambda x, y: s.P([x, y, 0])
        ends = {7: 1.165, 8: 1.125, 9: 1.08, 10: 1.02, 11: 0.975}
        for n, ye in ends.items():
            a, b = LM[f'rib{n}-lat'], LM[f'rib{n}-end']
            pts = [P(a[0] + 0.006, a[1] - 0.012), P(b[0], b[1] - 0.012), P(-0.082, min(ye + 0.012, b[1] - 0.016)), P(-0.03, ye)]
            nerve(f, pts, 3.2, smooth=True); f.circle(*P(-0.03, ye), 4, NERVE, '#8a6a10', 1)
            f.text(P(a[0], a[1])[0] - 30, P(a[0], a[1] - 0.012)[1] + 5, f'T{n}', 13, '#8a6a10', 'middle', '700')
        for pts, t in (([(-0.108, 1.045), (-0.1, 0.99), (-0.075, 0.94), (-0.03, 0.925)], 'T12'), ([(-0.13, 1.0), (-0.11, 0.955), (-0.06, 0.905), (-0.018, 0.888)], ''), ([(-0.128, 0.985), (-0.112, 0.94), (-0.065, 0.89), (-0.03, 0.862)], '')):
            nerve(f, [P(*p) for p in pts], 3.2, smooth=True, dash=None if t else None); f.circle(*P(*pts[-1]), 4, NERVE, '#8a6a10', 1)
        f.text(P(-0.108, 1.045)[0] - 34, P(-0.108, 1.045)[1] + 5, 'T12', 13, '#8a6a10', 'middle', '700')
        L = 40
        label(f, L, 420, 'Intercostal nerves (in the costal groove)', '肋间神经（走在肋沟内）', '#8a6a10', 'start', 14, to=P(-0.125, 1.2))
        label(f, L, 560, 'Thoraco-abdominal nerves T7–T11', '胸腹神经 T7–T11', '#8a6a10', 'start', 14, to=P(-0.09, 1.1))
        label(f, L, 640, 'They pass behind the costal margin', '在肋弓后方离开肋间隙', GREY, 'start', 14, to=P(-0.112, 1.135))
        label(f, L, 740, 'Subcostal nerve T12', '肋下神经 T12', '#8a6a10', 'start', 14, to=P(-0.1, 0.99))
        label(f, L, 830, 'Iliohypogastric nerve L1', '髂腹下神经 L1', '#8a6a10', 'start', 14, to=P(-0.11, 0.955))
        label(f, L, 920, 'Ilioinguinal nerve L1', '髂腹股沟神经 L1', '#8a6a10', 'start', 14, to=P(-0.09, 0.914))
        label(f, L, 1010, 'Anterior cutaneous branches (through the rectus sheath)', '前皮支（穿过腹直肌鞘）', '#8a6a10', 'start', 14, to=P(-0.03, 1.02))
        label(f, L, 300, 'Rectus abdominis (faint)', '腹直肌（淡色）', COLOR['rectus-abdominis'], 'start', 14, to=P(-0.05, 1.21))
        # dermatome bands on the patient's left
        cid = f.id('skinclip'); f.raw(f'<clipPath id="{cid}"><path d="{s.d(OUTLINES["ant"]["skin"])}"/></clipPath><g clip-path="url(#{cid})">')
        bands = [('T4', 1.287, '#7a5aa6'), ('T6', 1.232, '#2b6c7c'), ('T10', 1.02, '#b94334'), ('T12', 0.93, '#4f8a4a'), ('L1', 0.893, '#365e91')]
        for t, y, col in bands:
            slope = 0.05 if y > 1.1 else 0.045
            pts = [P(0.0, y + 0.014), P(0.17, y + 0.014 + slope), P(0.17, y - 0.014 + slope), P(0.0, y - 0.014)]
            poly(f, pts, col, col, 1.2, op=0.42)
        f.end()
        R = 1130
        for (t, y, col), (en, zh), ly in zip(bands, [('T4: nipple', 'T4：乳头平面'), ('T6: xiphoid process', 'T6：剑突平面'), ('T10: umbilicus', 'T10：脐平面'), ('T12: just above the inguinal ligament', 'T12：腹股沟韧带稍上方'), ('L1: groin', 'L1：腹股沟')], (300, 400, 700, 820, 920)):
            label(f, R, ly, en, zh, col, 'start', 15, to=P(0.11, y + 0.033))
        um = P(0, 1.02); f.circle(um[0], um[1], 6, '#6b5f4c', '#fff', 1.5)
        nip = P(0.095, 1.3); f.circle(nip[0], nip[1], 5, '#a0705c', '#fff', 1.5)
        f.bi(430, 150, 'Right side: nerves', '右侧：神经', 16, INK, 'middle', '700'); f.bi(1040, 150, 'Left side: dermatome landmarks', '左侧：皮节标志', 16, INK, 'middle', '700')
        note(f, 1130, 1030, ['Nerve paths and band positions are schematic. Each band marks one landmark level;', 'neighbouring dermatomes overlap. The umbilicus and nipple are placed schematically.'],
             ['神经走行和色带位置为示意。每条色带只标一个标志平面；', '相邻皮节互相重叠。脐和乳头的位置为示意。'])
        f.save('躯干壁的神经与皮节标志')

    @fig('10')
    def pudendal():
        f = Fig('10', 1800, 1150, 'Pudendal nerve (S2–S4): out of the pelvis and back in round the ischial spine (posterior view)', '阴部神经（S2–S4）：出骨盆后绕坐骨棘返回（后面观）')
        K = 3500
        s = Stage(f, 'post', 0.0, -0.9, 620, 600, K)
        s.bones(('hip-bone', 'hip-bone-left', 'sacrum', 'coccyx'))
        P = lambda x, y: s.P([x, y, -0.05])
        for sgn in (1, -1):
            # sacrotuberous then sacrospinous ligament (schematic)
            f.path(smooth_band([P(0.03 * sgn, 0.915), P(0.016 * sgn, 0.868)], [P(0.05 * sgn, 0.805), P(0.038 * sgn, 0.8)]), '#6b7f86', 1.4, '#cfdde0', op=0.85)
            f.path(smooth_band([P(0.022 * sgn, 0.884), P(0.012 * sgn, 0.852)], [P(0.046 * sgn, 0.87), P(0.044 * sgn, 0.861)]), '#5b4a7a', 1.4, '#d9d0e6', op=0.92)
        f.path(smooth_band([P(-0.026, 0.945), P(-0.03, 0.912)], [P(-0.125, 0.905), P(-0.125, 0.89)]), '#9a8f80', 1.4, '#e7dfd2', op=0.8)  # piriformis
        for y in (0.932, 0.915, 0.9): nerve(f, [P(-0.02, y), P(-0.045, 0.892)], 2.6)
        nerve(f, [P(-0.045, 0.892), P(-0.053, 0.876), P(-0.05, 0.862), P(-0.04, 0.848), P(-0.036, 0.83), P(-0.031, 0.812)], 5, smooth=True)
        nerve(f, [P(-0.037, 0.836), P(-0.022, 0.83), P(-0.008, 0.826)], 3.2, smooth=True)
        nerve(f, [P(-0.033, 0.82), P(-0.02, 0.808), P(-0.01, 0.8)], 3.2, smooth=True)
        nerve(f, [P(-0.031, 0.812), P(-0.022, 0.795), P(-0.012, 0.786)], 3.2, smooth=True, dash='7 5')
        an = P(0, 0.822); f.raw(f'<ellipse cx="{an[0]:.1f}" cy="{an[1]:.1f}" rx="13" ry="16" fill="#e9d3b8" stroke="#8a6a40" stroke-width="2"/>')
        for n, (x, y) in enumerate([(-0.014, 0.918), (-0.066, 0.894), (-0.064, 0.868), (-0.052, 0.848), (-0.05, 0.826), (-0.044, 0.796)], 1): f.step(*P(x, y), n)
        L, R = 40, 960
        label(f, L, 300, 'Sacrum', '骶骨', INK, 'start', 14, to=P(0.012, 0.93))
        label(f, L, 470, 'Greater sciatic foramen', '坐骨大孔', GREY, 'start', 14, to=P(0.05, 0.895))
        label(f, L, 560, 'Sacrospinous ligament', '骶棘韧带', '#5b4a7a', 'start', 14, to=P(0.032, 0.868))
        label(f, L, 650, 'Ischial spine', '坐骨棘', INK, 'start', 14, to=P(0.046, 0.866))
        label(f, L, 740, 'Lesser sciatic foramen', '坐骨小孔', GREY, 'start', 14, to=P(0.046, 0.845))
        label(f, L, 830, 'Sacrotuberous ligament', '骶结节韧带', '#4f666d', 'start', 14, to=P(0.036, 0.84))
        label(f, L, 930, 'Ischial tuberosity', '坐骨结节', INK, 'start', 14, to=P(0.046, 0.8))
        label(f, L, 1010, 'Coccyx', '尾骨', INK, 'start', 14, to=P(0.002, 0.845))
        label(f, R, 300, 'Piriformis (the nerve leaves below it)', '梨状肌（神经从它下方穿出）', '#7a6f60', 'start', 14, to=P(-0.1, 0.9))
        label(f, R, 800, 'Inferior rectal nerve', '肛（直肠下）神经', '#8a6a10', 'start', 14, to=P(-0.02, 0.83))
        label(f, R, 880, 'Perineal nerve', '会阴神经', '#8a6a10', 'start', 14, to=P(-0.02, 0.808))
        label(f, R, 960, 'Dorsal nerve of the penis or clitoris (dashed, runs forward)', '阴茎（阴蒂）背神经（虚线，向前走）', '#8a6a10', 'start', 14, to=P(-0.02, 0.793))
        label(f, R, 1040, 'Anus', '肛门', '#8a6a40', 'start', 14, to=(an[0] + 8, an[1] + 10))
        step_cards(f, 1290, 150, [
            ('The anterior rami of S2, S3 and S4 join inside the pelvis.', 'S2、S3、S4 的前支在盆腔内汇合。'),
            ('The nerve leaves through the greater sciatic foramen, below piriformis.', '经坐骨大孔、在梨状肌下方出骨盆。'),
            ('It hooks round the sacrospinous ligament at the ischial spine.', '在坐骨棘处绕过骶棘韧带。'),
            ('It re-enters through the lesser sciatic foramen.', '经坐骨小孔返回。'),
            ('It runs in the pudendal (Alcock) canal on the lateral wall of the ischioanal fossa.', '走在坐骨肛门窝外侧壁的阴部管（Alcock 管）内。'),
            ('It divides into the inferior rectal nerve, the perineal nerve and the dorsal nerve of the penis or clitoris.', '分为肛（直肠下）神经、会阴神经和阴茎（阴蒂）背神经。')], 470)
        f.save('阴部神经的走行')
