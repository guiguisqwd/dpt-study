"""Figures 04-07: muscles of mastication, suprahyoid muscles and muscles of facial expression, with origins and insertions.
O/I label texts are the short figure labels; content.json diagram labels repeat them (figure-labels.json)."""
from tmjfig import *  # noqa: F401,F403


def register(fig):

    @fig('04')
    def masseter_temporalis():
        f = Fig('04', 1900, 1300, 'Temporalis and masseter (right lateral view)', '颞肌与咬肌（右侧面观）')
        # temporalis
        f.bi(360, 150, name_of('temporalis')['en'], name_of('temporalis')['zh'], 19, COLOR['temporalis'], 'middle', '700')
        clip_begin(f, 40, 185, 640, 670)
        st = Stage(f, 'lat', 0.0, -1.605, 360, 520, 5200); L = st.L
        skull_lat(st, zyg=False, arch=False)
        st.muscle('temporalis', op=0.8)
        o = edge(st, 'Temporalis muscle', 'top', 0.45, 9)
        tip = L(0.045, 1.566)
        fibres(f, o, [tip], COLOR['temporalis'], 9, 0.55, 1.1)
        st.bone('Zygomatic bone', op=0.82, outer=True); st.bone('Temporal bone.r|arch', op=0.82, outer=True)
        f.end()
        oi(f, o, [L(0.041, 1.561), tip, L(0.049, 1.556)], LETTER['temporalis'], LETTER['temporalis'], line=False)
        label(f, 60, 890, 'Posterior fibres run almost horizontally', '后部纤维近水平', COLOR['temporalis'], 'start', 14, to=L(-0.035, 1.612))
        label(f, 420, 890, 'Anterior fibres run vertically', '前部纤维垂直', COLOR['temporalis'], 'start', 14, to=L(0.045, 1.60))
        label(f, 700, 420, 'Temporal fossa', '颞窝', INK, 'start', 14, to=L(0.02, 1.625))
        label(f, 700, 520, 'Zygomatic arch (tendon passes deep to it)', '颧弓（肌腱从其深面经过）', INK, 'start', 14, to=L(0.03, 1.5775))
        label(f, 700, 620, 'Coronoid process', '冠突', INK, 'start', 14, to=L(0.046, 1.5625))
        # masseter
        f.bi(1460, 150, name_of('masseter')['en'], name_of('masseter')['zh'], 19, COLOR['masseter'], 'middle', '700')
        clip_begin(f, 1080, 185, 760, 670)
        st = Stage(f, 'lat', 0.032, -1.548, 1460, 520, 8000); L = st.L
        skull_lat(st)
        st.muscle('masseter-deep', op=0.8); st.muscle('masseter-superficial', op=0.85)
        os_, od = edge(st, 'Superficial part of masseter', 'top', 0.12, 5), edge(st, 'Deep part of masseter', 'top', 0.12, 4)
        ins = edge(st, 'Superficial part of masseter', 'bottom', 0.14, 5)
        fibres(f, os_, ins, COLOR['masseter'], 7, 0.5, 1.1)
        f.end()
        oi(f, od[:1] + os_, ins, LETTER['masseter'], LETTER['masseter'])
        label(f, 1090, 890, 'Deep part (behind, fibres vertical)', '深部（靠后，纤维垂直）', COLOR['masseter'], 'start', 14, to=L(0.022, 1.560))
        label(f, 1470, 890, 'Superficial part (fibres run down and back)', '浅部（纤维向后下方）', COLOR['masseter'], 'start', 14, to=L(0.040, 1.545))
        key_oi(f, 60, 985)
        legend_oi(f, 40, 1050, [('temporalis', 'temporal fossa below the inferior temporal line, and temporal fascia', '颞下线以下的颞窝和颞筋膜',
                                 'coronoid process and anterior border of the ramus', '冠突和下颌支前缘')])
        legend_oi(f, 1080, 1050, [('masseter', 'zygomatic bone and zygomatic arch', '颧骨和颧弓',
                                   'lateral surface of the ramus, the angle and the coronoid process', '下颌支外侧面、下颌角和冠突')])
        f.save('颞肌与咬肌起点与止点')

    @fig('05')
    def pterygoids():
        f = Fig('05', 1900, 1330, 'Lateral and medial pterygoid', '翼外肌与翼内肌')
        f.bi(480, 150, 'Right lateral view, ramus and zygomatic arch shown as outlines', '右侧面观，下颌支和颧弓只画轮廓', 17, INK, 'middle', '700')
        clip_begin(f, 40, 190, 900, 670)
        st = Stage(f, 'lat', 0.028, -1.553, 480, 540, 9000); L = st.L
        skull_lat(st, mandible=False, zyg=False, arch=False)
        st.muscle('medial-pterygoid', op=0.8)
        st.muscle('lateral-pterygoid-inferior', op=0.85); st.muscle('lateral-pterygoid-superior', op=0.85)
        st.shape('Mandible|right', BONE_E, 'none', 1.6, dash='7 5', outer=True)
        st.shape('Zygomatic bone', BONE_E, 'none', 1.3, dash='3 4', outer=True); st.shape('Temporal bone.r|arch', BONE_E, 'none', 1.3, dash='3 4', outer=True)
        o_inf = edge(st, 'Inferior head of lateral pterygoid muscle', 'front', 0.15, 4)
        o_sup = edge(st, 'Superior head of lateral pterygoid muscle', 'front', 0.15, 3)
        i_lp = edge(st, 'Inferior head of lateral pterygoid muscle', 'back', 0.1, 3)
        i_mp = edge(st, 'Medial pterygoid muscle', 'bottom', 0.14, 4)
        o_mp = edge(st, 'Medial pterygoid muscle', 'top', 0.14, 3)
        f.end()
        oi(f, o_sup + o_inf, i_lp, LETTER['lateral-pterygoid'], LETTER['lateral-pterygoid'])
        oi(f, o_mp, i_mp, LETTER['medial-pterygoid'], LETTER['medial-pterygoid'])
        label(f, 60, 250, 'Superior head', '上头', COLOR['lateral-pterygoid'], 'start', 14, to=centroid(edge(st, 'Superior head of lateral pterygoid muscle', 'top', 0.5, 4)))
        label(f, 60, 330, 'Head of the mandible and joint', '下颌头与关节', INK, 'start', 14, to=L(0.006, 1.576))
        label(f, 640, 250, 'Lateral pterygoid plate', '翼突外侧板', INK, 'start', 14, to=L(0.047, 1.560))
        label(f, 640, 330, 'Inferior head', '下头', COLOR['lateral-pterygoid'], 'start', 14, to=centroid(edge(st, 'Inferior head of lateral pterygoid muscle', 'bottom', 0.5, 4)))
        label(f, 60, 890, 'Medial pterygoid (deep to the ramus)', '翼内肌（在下颌支深面）', COLOR['medial-pterygoid'], 'start', 14, to=lerp(centroid(i_mp), centroid(o_mp), 0.4))
        label(f, 520, 890, 'Ramus of the mandible (outline)', '下颌支（轮廓）', INK, 'start', 14, to=L(0.012, 1.545))
        # medial view
        f.bi(1420, 150, 'Medial view of the right half', '右半内侧面观', 17, INK, 'middle', '700')
        clip_begin(f, 990, 190, 870, 670)
        st = Stage(f, 'med', -0.030, -1.553, 1420, 540, 9000); L = st.L
        st.bone('Sphenoid bone', fill=SHADE, outer=True); st.bone('Maxilla', outer=True)
        for n in OUTLINES['med']:
            if n.endswith('.r') and n.startswith(('Lower', 'Upper')): st.shape(n, BONE_E, '#fffdf8', 1.0, rough=False, outer=True)
        st.bone('Mandible', outer=True)
        st.muscle('lateral-pterygoid', op=0.55)
        st.muscle('medial-pterygoid', op=0.85)
        o2, i2 = edge(st, 'Medial pterygoid muscle', 'top', 0.14, 4), edge(st, 'Medial pterygoid muscle', 'bottom', 0.16, 5)
        fibres(f, o2, i2, COLOR['medial-pterygoid'], 6, 0.5, 1.1)
        f.end()
        oi(f, o2, i2, LETTER['medial-pterygoid'], LETTER['medial-pterygoid'])
        label(f, 1000, 890, 'Pterygoid process of the sphenoid', '蝶骨翼突', INK, 'start', 14, to=o2[0])
        label(f, 1330, 890, 'Medial surface of the ramus and angle', '下颌支和下颌角内侧面', INK, 'start', 14, to=i2[-1])
        label(f, 1640, 330, 'Lateral pterygoid (behind)', '翼外肌（在后方）', COLOR['lateral-pterygoid'], 'start', 14, to=L(0.012, 1.571))
        key_oi(f, 60, 985)
        legend_oi(f, 40, 1050, [('lateral-pterygoid', 'greater wing of the sphenoid (superior head); lateral surface of the lateral pterygoid plate (inferior head)',
                                 '蝶骨大翼（上头）；翼突外侧板外侧面（下头）', 'pterygoid fovea on the neck of the mandible; joint capsule and disc', '下颌颈的翼肌凹；关节囊和关节盘')])
        legend_oi(f, 40, 1168, [('medial-pterygoid', 'medial surface of the lateral pterygoid plate; tuberosity of the maxilla', '翼突外侧板内侧面；上颌结节',
                                 'medial surface of the ramus and angle of the mandible', '下颌支和下颌角内侧面')])
        f.save('翼外肌与翼内肌起点与止点')

    @fig('06')
    def suprahyoid():
        f = Fig('06', 1900, 1560, 'Suprahyoid muscles: digastric, stylohyoid, mylohyoid and geniohyoid', '舌骨上肌：二腹肌、茎突舌骨肌、下颌舌骨肌与颏舌骨肌')
        f.bi(640, 150, 'Right lateral view', '右侧面观', 17, INK, 'middle', '700')
        clip_begin(f, 250, 260, 790, 650)
        st = Stage(f, 'lat', 0.025, -1.535, 650, 590, 7400); L = st.L
        skull_lat(st, calvaria=False, hyoid=True)
        st.muscle('mylohyoid', op=0.7)
        st.muscle('stylohyoid', op=0.85)
        st.muscle('digastric', op=0.9)
        st.shape('Geniohyoid muscle', COLOR['geniohyoid'], 'none', 1.8, dash='5 4', outer=True)
        f.end()
        o_dp = edge(st, 'Posterior belly of digastric muscle', 'top', 0.08, 2); i_d = edge(st, 'Intermediate tendon of digastric muscle', 'bottom', 0.6, 2)
        o_da = edge(st, 'Anterior belly of digastric muscle', 'front', 0.08, 2)
        area(f, o_dp, ORIGIN_C); area(f, o_da, ORIGIN_C); area(f, i_d, INSERT_C)
        tag(f, o_dp[0][0] - 24, o_dp[0][1] - 4, LETTER['digastric'], ORIGIN_C); tag(f, o_da[-1][0] + 26, o_da[-1][1] + 8, LETTER['digastric'], ORIGIN_C)
        tag(f, i_d[0][0] - 6, i_d[0][1] + 30, LETTER['digastric'], INSERT_C)
        o_st = edge(st, 'Stylohyoid muscle', 'top', 0.08, 2); i_st = edge(st, 'Stylohyoid muscle', 'bottom', 0.08, 2)
        area(f, o_st, ORIGIN_C); area(f, i_st, INSERT_C)
        tag(f, o_st[0][0] + 28, o_st[0][1] - 10, LETTER['stylohyoid'], ORIGIN_C); tag(f, i_st[0][0] - 34, i_st[0][1] + 6, LETTER['stylohyoid'], INSERT_C)
        label(f, 40, 300, 'Mastoid process', '乳突', INK, 'start', 14, to=L(-0.021, 1.558))
        label(f, 40, 380, 'Styloid process', '茎突', INK, 'start', 14, to=L(-0.003, 1.557))
        label(f, 40, 560, 'Posterior belly of digastric', '二腹肌后腹', COLOR['digastric'], 'start', 14, to=centroid(edge(st, 'Posterior belly of digastric muscle', 'top', 0.6, 4)))
        label(f, 40, 640, 'Stylohyoid', '茎突舌骨肌', COLOR['stylohyoid'], 'start', 14, to=centroid(edge(st, 'Stylohyoid muscle', 'bottom', 0.5, 4)))
        label(f, 40, 800, 'Intermediate tendon and sling', '中间腱与纤维环', COLOR['digastric'], 'start', 14, to=centroid(i_d))
        label(f, 250, 950, 'Hyoid bone', '舌骨', INK, 'start', 14, to=L(0.020, 1.5005))
        label(f, 420, 950, 'Anterior belly of digastric', '二腹肌前腹', COLOR['digastric'], 'start', 14, to=centroid(edge(st, 'Anterior belly of digastric muscle', 'bottom', 0.8, 4)))
        label(f, 700, 950, 'Mylohyoid', '下颌舌骨肌', COLOR['mylohyoid'], 'start', 14, to=centroid(edge(st, 'Mylohyoid muscle', 'top', 0.5, 4)))
        label(f, 560, 215, 'Geniohyoid (deep to mylohyoid, dashed)', '颏舌骨肌（在下颌舌骨肌深面，虚线）', COLOR['geniohyoid'], 'start', 14,
              to=centroid(edge(st, 'Geniohyoid muscle', 'top', 0.6, 4)))
        # inferior view
        f.bi(1480, 150, 'View from below, anterior at the top', '下面观，上方为前', 17, INK, 'middle', '700')
        clip_begin(f, 1080, 265, 790, 650)
        st = Stage(f, 'inf', 0.0, -0.040, 1480, 590, 6800); L = st.L
        st.bone('Mandible', outer=True); st.bone('Hyoid bone', outer=True)
        for sd in 'rl':
            st.muscle('mylohyoid', op=0.8, side=sd)
        st.shape('Geniohyoid muscle', COLOR['geniohyoid'], 'none', 1.8, dash='5 4', outer=True, side='l')
        for sd in 'rl': st.muscle('digastric-anterior', op=0.9, side=sd)
        st.muscle('stylohyoid', op=0.85); st.muscle('digastric-posterior', op=0.9); st.shape('Intermediate tendon of digastric muscle', COLOR['digastric'], tint(COLOR['digastric']), 1.5, outer=True)
        f.end()
        f.path('M%.1f,%.1f L%.1f,%.1f' % (*L(0, 0.073), *L(0, 0.040)), '#fff', 2.2, dash='2 5', rough=False)
        o_my = edge(st, 'Mylohyoid muscle', 'front', 0.1, 5, side='l'); i_my = [L(0.001, 0.068), L(0.001, 0.045)]
        hy = [L(0.004, 0.036), L(0.014, 0.034)]
        area(f, o_my, ORIGIN_C); area(f, i_my + hy, INSERT_C)
        tag(f, o_my[2][0] + 28, o_my[2][1], LETTER['mylohyoid'], ORIGIN_C); tag(f, hy[1][0] + 4, hy[1][1] + 28, LETTER['mylohyoid'], INSERT_C)
        g_o, g_i = L(0.003, 0.074), L(0.004, 0.039)
        area(f, [g_o], ORIGIN_C); tag(f, g_o[0] + 4, g_o[1] - 26, LETTER['geniohyoid'], ORIGIN_C); tag(f, g_i[0] - 30, g_i[1] + 30, LETTER['geniohyoid'], INSERT_C)
        label(f, 1090, 215, 'Body of the mandible', '下颌体', INK, 'start', 14, to=L(-0.03, 0.062))
        label(f, 1090, 950, 'Posterior belly of digastric', '二腹肌后腹', COLOR['digastric'], 'start', 14, to=L(-0.034, 0.012))
        label(f, 1340, 950, 'Hyoid bone', '舌骨', INK, 'start', 14, to=L(-0.012, 0.022))
        label(f, 1350, 215, 'Mylohyoid line', '下颌舌骨线', INK, 'start', 14, to=o_my[1])
        label(f, 1590, 215, 'Mylohyoid raphe', '下颌舌骨肌缝', INK, 'start', 14, to=L(0, 0.056))
        label(f, 1480, 950, 'Anterior belly of digastric', '二腹肌前腹', COLOR['digastric'], 'start', 14, to=L(0.011, 0.055))
        label(f, 1740, 950, 'Mylohyoid', '下颌舌骨肌', COLOR['mylohyoid'], 'start', 14, to=L(0.022, 0.05))
        key_oi(f, 60, 1040)
        legend_oi(f, 40, 1100, [('digastric', 'digastric fossa of the mandible (anterior belly); mastoid notch of the temporal bone (posterior belly)', '下颌骨二腹肌窝（前腹）；颞骨乳突切迹（后腹）',
                                 'intermediate tendon, held to the hyoid bone by a fibrous sling', '中间腱，由纤维环系于舌骨'),
                                ('stylohyoid', 'styloid process of the temporal bone', '颞骨茎突', 'body of the hyoid bone near the greater horn', '舌骨体与大角交界处')])
        legend_oi(f, 1000, 1100, [('mylohyoid', 'mylohyoid line of the mandible', '下颌骨的下颌舌骨线', 'mylohyoid raphe and body of the hyoid bone', '下颌舌骨肌缝和舌骨体'),
                                  ('geniohyoid', 'inferior mental spine of the mandible', '下颌骨下颏棘', 'body of the hyoid bone', '舌骨体')])
        note(f, 40, 1360, ['Infrahyoid muscles are not drawn. They hold the hyoid bone steady from below so that the suprahyoid muscles can open the jaw.'],
             ['图中未画舌骨下肌。它们从下方固定舌骨，使舌骨上肌能够张口。'])
        f.save('舌骨上肌起点与止点')

    @fig('07')
    def facial():
        f = Fig('07', 2000, 1760, 'Muscles of facial expression', '表情肌')
        f.bi(620, 150, 'Anterior view', '前面观', 17, INK, 'middle', '700')
        clip_begin(f, 270, 200, 700, 800)
        st = Stage(f, 'ant', 0.0, -1.592, 620, 610, 4800); L = st.L
        st.shape('skin', SKIN, SKIN_F, 1.5, rough=False); skull_ant(st, op=0.9)
        for mid in ['platysma', 'buccinator', 'frontalis', 'zygomaticus-major', 'orbicularis-oculi', 'orbicularis-oris']:
            for sd in 'rl': st.muscle(mid if mid != 'frontalis' else 'occipitofrontalis', op=0.8, side=sd, parts=MESH[mid])
        f.end()
        column(f, 30, 260, 125, [('Frontal belly of occipitofrontalis', '枕额肌额腹', L(-0.03, 1.65)), ('Orbicularis oculi, orbital part', '眼轮匝肌眶部', L(-0.052, 1.60)),
                                 ('Orbicularis oculi, palpebral part', '眼轮匝肌睑部', L(-0.035, 1.594)), ('Zygomaticus major', '颧大肌', L(-0.045, 1.566)),
                                 ('Buccinator', '颊肌', L(-0.034, 1.538)), ('Platysma', '颈阔肌', L(-0.03, 1.522))], 'start', 14)
        label(f, 985, 700, 'Modiolus', '蜗轴', INK, 'start', 14, to=L(0.027, 1.540))
        label(f, 985, 800, 'Orbicularis oris', '口轮匝肌', COLOR['orbicularis-oris'], 'start', 14, to=L(0.012, 1.548))
        # O/I areas on the left half of the picture (right side of the face)
        area(f, [L(-0.045, 1.615), L(-0.02, 1.612), L(-0.005, 1.607)], ORIGIN_C); tag(f, *L(-0.028, 1.622), LETTER['occipitofrontalis'], ORIGIN_C)
        area(f, [L(-0.045, 1.660), L(-0.02, 1.664)], INSERT_C); tag(f, *L(-0.03, 1.669), LETTER['occipitofrontalis'], INSERT_C)
        area(f, [L(-0.014, 1.598), L(-0.014, 1.588)], ORIGIN_C); tag(f, *L(-0.007, 1.593), LETTER['orbicularis-oculi'], ORIGIN_C, 13)
        area(f, [L(-0.057, 1.585)], ORIGIN_C); tag(f, *L(-0.050, 1.591), LETTER['zygomaticus-major'], ORIGIN_C)
        area(f, [L(-0.027, 1.540)], INSERT_C); tag(f, *L(-0.02, 1.531), LETTER['zygomaticus-major'], INSERT_C)
        # lateral
        f.bi(1580, 150, 'Right lateral view', '右侧面观', 17, INK, 'middle', '700')
        clip_begin(f, 1180, 260, 790, 740)
        st = Stage(f, 'lat', -0.005, -1.592, 1580, 640, 3900); L = st.L
        skin_lat(st); skull_lat(st, op=0.9)
        st.shape('Epicranial aponeurosis', '#8a8170', '#e7e1d2', 1.3, op=0.8, outer=True)
        for mid in ['platysma', 'buccinator', 'occipitofrontalis', 'zygomaticus-major', 'orbicularis-oculi', 'orbicularis-oris']: st.muscle(mid, op=0.8)
        ear_lat(st, op=0.7)
        f.end()
        o_oc = edge(st, 'Occipitalis muscle', 'bottom', 0.12, 4)
        area(f, o_oc, ORIGIN_C); tag(f, o_oc[1][0], o_oc[1][1] + 26, LETTER['occipitofrontalis'], ORIGIN_C)
        o_bu = edge(st, 'Bucinator', 'back', 0.2, 3); area(f, o_bu, ORIGIN_C); tag(f, o_bu[0][0] - 26, o_bu[0][1], LETTER['buccinator'], ORIGIN_C)
        i_bu = L(0.079, 1.541); area(f, [i_bu], INSERT_C); tag(f, i_bu[0] - 4, i_bu[1] + 26, LETTER['buccinator'], INSERT_C)
        i_pl = edge(st, 'Platysma', 'top', 0.06, 3); area(f, i_pl, INSERT_C); tag(f, i_pl[1][0], i_pl[1][1] - 24, LETTER['platysma'], INSERT_C)
        label(f, 1190, 215, 'Epicranial aponeurosis', '帽状腱膜', INK, 'start', 14, to=L(-0.03, 1.684))
        label(f, 1420, 215, 'Occipital belly of occipitofrontalis', '枕额肌枕腹', COLOR['occipitofrontalis'], 'start', 14, to=centroid(edge(st, 'Occipitalis muscle', 'top', 0.6, 4)))
        label(f, 1790, 215, 'Frontal belly', '额腹', COLOR['occipitofrontalis'], 'start', 14, to=L(0.075, 1.655))
        label(f, 1190, 1030, 'Platysma', '颈阔肌', COLOR['platysma'], 'start', 14, to=L(0.025, 1.515))
        label(f, 1440, 1030, 'Buccinator', '颊肌', COLOR['buccinator'], 'start', 14, to=L(0.062, 1.538))
        label(f, 1700, 1030, 'Orbicularis oris', '口轮匝肌', COLOR['orbicularis-oris'], 'start', 14, to=L(0.09, 1.535))
        key_oi(f, 60, 1095)
        legend_oi(f, 40, 1150, [('occipitofrontalis', 'skin of the eyebrow (frontal belly); superior nuchal line (occipital belly)', '眉部皮肤（额腹）；上项线（枕腹）',
                                 'epicranial aponeurosis', '帽状腱膜'),
                                ('orbicularis-oculi', 'medial orbital margin and medial palpebral ligament', '眶内侧缘和睑内侧韧带', 'skin around the orbit and the eyelids', '眶周皮肤和眼睑'),
                                ('zygomaticus-major', 'lateral surface of the zygomatic bone', '颧骨外侧面', 'angle of the mouth (modiolus)', '口角（蜗轴）')])
        legend_oi(f, 1040, 1150, [('orbicularis-oris', 'modiolus and the surrounding muscles', '蜗轴和周围的肌', 'skin and mucous membrane of the lips', '唇的皮肤和黏膜'),
                                  ('buccinator', 'alveolar processes opposite the molar teeth and the pterygomandibular raphe', '磨牙对应处的牙槽突和翼突下颌缝',
                                   'modiolus, continuing into orbicularis oris', '口角的蜗轴，延续为口轮匝肌'),
                                  ('platysma', 'skin and fascia over the upper chest and shoulder', '胸上部和肩部表面的皮肤和筋膜', 'lower border of the mandible and skin of the lower face', '下颌骨下缘和面下部皮肤')])
        note(f, 40, 1530, ['Most of these muscles attach to skin, so origin and insertion areas are marked only where a bony or tendinous attachment can be shown.',
                           'The lower attachment of platysma on the chest lies below the picture.'],
             ['这些肌大多附着于皮肤，所以只在能画出骨性或腱性附着的地方标出起止点区。', '颈阔肌在胸部的下方附着点在画面之外。'])
        f.save('表情肌起点与止点')
