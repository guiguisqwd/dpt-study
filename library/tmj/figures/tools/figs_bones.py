"""Figures 01-03: skull and mandible landmarks, and the temporomandibular joint."""
from tmjfig import *  # noqa: F401,F403


def register(fig):

    @fig('01')
    def skull_lateral():
        f = Fig('01', 1760, 1300, 'Skull, right lateral view: bones and landmarks around the jaw joint', '颅骨右侧面观：颞下颌关节周围的骨与骨性标志')
        st = Stage(f, 'lat', -0.008, -1.595, 760, 700, 5000)
        skull_lat(st, hyoid=True)
        m = st.L(-0.009, 1.5725); f.raw(f'<ellipse cx="{m[0]:.1f}" cy="{m[1]:.1f}" rx="13" ry="11" fill="#5b5448" opacity=".75"/>')
        L = st.L
        column(f, 40, 150, 62, [
            ('Parietal bone', '顶骨', L(-0.05, 1.67)), ('Temporal fossa', '颞窝', L(0.016, 1.612)), ('Temporal bone', '颞骨', L(-0.025, 1.598)),
            ('Occipital bone', '枕骨', L(-0.085, 1.60))], 'start')
        column(f, 40, 700, 62, [
            ('External acoustic meatus', '外耳道', m), ('Mandibular fossa', '下颌窝', L(0.003, 1.5805)), ('Mastoid process', '乳突', L(-0.021, 1.558)),
            ('Styloid process', '茎突', L(-0.003, 1.557)), ('Condylar process', '髁突', L(0.007, 1.572)), ('Ramus of the mandible', '下颌支', L(0.014, 1.538)),
            ('Angle of the mandible', '下颌角', L(0.0105, 1.5235)), ('Hyoid bone', '舌骨', L(0.018, 1.5005))], 'start')
        column(f, 1330, 170, 62, [
            ('Frontal bone', '额骨', L(0.065, 1.665)), ('Sphenoid bone (greater wing)', '蝶骨（大翼）', L(0.036, 1.606)), ('Nasal bone', '鼻骨', L(0.0855, 1.598)),
            ('Zygomatic bone', '颧骨', L(0.057, 1.586)), ('Zygomatic arch', '颧弓', L(0.027, 1.5785)), ('Articular tubercle', '关节结节', L(0.0135, 1.5765)),
            ('Maxilla', '上颌骨', L(0.074, 1.566)), ('Coronoid process (behind the zygomatic bone)', '冠突（被颧骨挡住）', L(0.044, 1.567)),
            ('Lateral pterygoid plate (through the notch)', '翼突外侧板（透过下颌切迹可见）', L(0.030, 1.562)),
            ('Infratemporal fossa (deep to the ramus)', '颞下窝（下颌支深面）', L(0.0185, 1.5545)), ('Mandible', '下颌骨', L(0.055, 1.5195)),
            ('Mental foramen', '颏孔', L(0.066, 1.5185))], 'start')
        mf = L(0.066, 1.5185); f.raw(f'<ellipse cx="{mf[0]:.1f}" cy="{mf[1]:.1f}" rx="5" ry="4" fill="#5b5448"/>')
        note(f, 40, 1215, ['Bones are projected from the 3D model; the external acoustic meatus and the mental foramen are added by hand.'],
             ['骨骼由 3D 模型投影得到；外耳道和颏孔为手工添加。'])
        f.save('颅骨侧面观骨与骨性标志')

    @fig('02')
    def mandible():
        f = Fig('02', 1920, 1120, 'Mandible: lateral surface and medial surface of the right half', '下颌骨：右半的外侧面与内侧面')
        K = 7600
        # lateral
        st = Stage(f, 'lat', 0.043, -1.545, 480, 560, K); L = st.L
        for n in OUTLINES['lat']:
            if n.endswith('.r') and n.startswith('Lower'): st.shape(n, BONE_E, '#fffdf8', 1.0, rough=False, outer=True)
        st.bone('Mandible|right', outer=True)
        f.bi(480, 150, 'Lateral surface', '外侧面', 19, INK, 'middle', '700')
        mf = L(0.066, 1.5185); f.raw(f'<ellipse cx="{mf[0]:.1f}" cy="{mf[1]:.1f}" rx="7" ry="5.5" fill="#5b5448"/>')
        f.path(curve([L(0.046, 1.552), L(0.049, 1.536), L(0.060, 1.5215), L(0.072, 1.517)]), '#8a8170', 1.4, dash='5 4', rough=False)
        column(f, 40, 215, 58, [('Head of the mandible (condyle)', '下颌头（髁突头）', L(0.006, 1.5775)), ('Neck of the mandible', '下颌颈', L(0.010, 1.566)),
                               ('Condylar process (head and neck)', '髁突（头和颈）', L(0.007, 1.572))], 'start')
        column(f, 40, 520, 60, [('Ramus', '下颌支', L(0.025, 1.545)), ('Angle of the mandible', '下颌角', L(0.0105, 1.524))], 'start')
        label(f, 400, 215, 'Mandibular notch', '下颌切迹', anchor='start', to=L(0.031, 1.5585))
        label(f, 600, 215, 'Coronoid process', '冠突', anchor='start', to=L(0.045, 1.566))
        label(f, 300, 960, 'Body of the mandible', '下颌体', anchor='start', to=L(0.05, 1.5165))
        label(f, 560, 960, 'Mental foramen', '颏孔', anchor='start', to=mf)
        label(f, 700, 330, 'Oblique line', '斜线', anchor='start', to=L(0.049, 1.536))
        # medial
        st = Stage(f, 'med', -0.043, -1.545, 1300, 560, K); L = st.L
        for n in OUTLINES['med']:
            if n.endswith('.r') and n.startswith('Lower'): st.shape(n, BONE_E, '#fffdf8', 1.0, rough=False, outer=True)
        st.bone('Mandible', outer=True)
        f.bi(1300, 150, 'Medial surface', '内侧面', 19, INK, 'middle', '700')
        fo = L(0.027, 1.5475); f.raw(f'<ellipse cx="{fo[0]:.1f}" cy="{fo[1]:.1f}" rx="9" ry="12" fill="#5b5448" transform="rotate(-25 {fo[0]:.1f} {fo[1]:.1f})"/>')
        f.path(curve([L(0.030, 1.5445), L(0.036, 1.537), L(0.046, 1.5295)]), '#8a8170', 1.6, dash='4 4', rough=False)  # mylohyoid groove
        ml = [L(0.047, 1.538), L(0.058, 1.524), L(0.068, 1.516), L(0.0745, 1.5125)]
        f.path(curve(ml), '#7a5f3a', 2.6, rough=False)
        pf = L(0.011, 1.5695); f.raw(f'<ellipse cx="{pf[0]:.1f}" cy="{pf[1]:.1f}" rx="10" ry="7" fill="{SHADE}" stroke="#8a8170" stroke-width="1.4" stroke-dasharray="3 3"/>')
        df = L(0.0785, 1.505); f.raw(f'<ellipse cx="{df[0]:.1f}" cy="{df[1]:.1f}" rx="13" ry="7" fill="{SHADE}" stroke="#8a8170" stroke-width="1.4" stroke-dasharray="3 3"/>')
        ms = L(0.0785, 1.5155); f.raw(f'<path d="M{ms[0] - 4:.1f},{ms[1] - 7:.1f} l8,4 l-8,4 l8,4 l-8,4" fill="none" stroke="#5b5448" stroke-width="2"/>')
        column(f, 1640, 215, 62, [('Head of the mandible', '下颌头', L(0.006, 1.5775)), ('Pterygoid fovea', '翼肌凹', pf), ('Mandibular notch', '下颌切迹', L(0.031, 1.5585)),
                                 ('Mandibular foramen and lingula', '下颌孔与下颌小舌', fo), ('Mylohyoid groove', '下颌舌骨沟', L(0.036, 1.537)),
                                 ('Angle of the mandible', '下颌角', L(0.014, 1.527))], 'start')
        label(f, 1060, 215, 'Coronoid process', '冠突', anchor='start', to=L(0.045, 1.566))
        label(f, 900, 330, 'Mylohyoid line', '下颌舌骨线', anchor='start', to=ml[1])
        label(f, 900, 440, 'Sublingual fossa', '舌下腺凹', anchor='start', to=L(0.0715, 1.517))
        label(f, 900, 960, 'Mental spines', '颏棘', anchor='start', to=ms)
        label(f, 1080, 960, 'Digastric fossa', '二腹肌窝', anchor='start', to=df)
        label(f, 1280, 960, 'Submandibular fossa', '下颌下腺凹', anchor='start', to=L(0.052, 1.521))
        note(f, 40, 1030, ['Outlines are projected from the 3D model. Foramina, lines and fossae are drawn by hand at their usual positions.'],
             ['轮廓由 3D 模型投影得到。孔、线和凹为手工画在通常位置。'])
        f.save('下颌骨外侧面与内侧面')

    @fig('03')
    def tmj():
        f = Fig('03', 1900, 1180, 'Temporomandibular joint: sagittal section (mouth closed) and ligaments', '颞下颌关节：矢状切面（闭口位）与韧带')
        f.bi(470, 150, 'Sagittal section, anterior to the right', '矢状切面，右侧为前方', 18, INK, 'middle', '700')
        p = tmj_sag(f, 420, 520, 1.75)
        column(f, 40, 195, 46, [('Mandibular fossa', '下颌窝', p['fossa']), ('Upper joint compartment (gliding)', '关节上腔（滑动）', p['upper'])], 'start')
        column(f, 30, 650, 62, [('Postglenoid tubercle', '关节后结节', p['postglenoid']), ('External acoustic meatus', '外耳道', p['meatus']),
                               ('Retrodiscal tissue', '盘后组织', p['retro']), ('Head of the mandible', '下颌头', p['head']), ('Neck of the mandible', '下颌颈', p['neck'])], 'start')
        column(f, 620, 215, 60, [('Articular tubercle', '关节结节', p['tubercle'])], 'start')
        label(f, 330, 215, 'Articular disc: posterior band', '关节盘：后带', anchor='start', to=p['post-band'])
        label(f, 880, 470, 'Articular disc: anterior band', '关节盘：前带', anchor='start', to=p['ant-band'])
        label(f, 880, 550, 'Intermediate zone', '中间带', anchor='start', to=p['disc'])
        label(f, 880, 630, 'Lower joint compartment (hinge)', '关节下腔（铰链）', anchor='start', to=p['lower'])
        label(f, 880, 300, 'Lateral pterygoid, superior head', '翼外肌上头', COLOR['lateral-pterygoid'], 'start', to=p['lp-sup'])
        label(f, 880, 760, 'Lateral pterygoid, inferior head', '翼外肌下头', COLOR['lateral-pterygoid'], 'start', to=p['lp-inf'])
        f.raw('<rect x="60" y="920" width="26" height="12" fill="#8fb4c9"/>'); f.bi(96, 932, 'Fibrocartilage on the joint surfaces', '关节面的纤维软骨', 13, INK, 'start', '600')
        # ligaments, lateral view from the model
        f.bi(1520, 150, 'Ligaments, right lateral view', '韧带，右侧面观', 18, INK, 'middle', '700')
        clip_begin(f, 1200, 190, 640, 760)
        st = Stage(f, 'lat', 0.012, -1.556, 1520, 560, 10500); L = st.L
        skull_lat(st, calvaria=False)
        st.shape('Sphenomandibular ligament', '#7a5aa6', '#d9cdea', 1.6, op=0.55, dash='5 4', outer=True)
        st.shape('Stylomandibular ligament', '#2f7f8f', '#c5e0e5', 1.6, op=0.9, outer=True)
        st.shape('Articular capsule of temporomandibular joint', '#8a6d3b', '#eadfc8', 1.6, op=0.85, outer=True)
        st.shape('Lateral temporomandibular ligament', '#b94334', '#efc4bd', 1.8, op=0.9, outer=True)
        f.end()
        column(f, 1210, 985, 0, [('Capsule', '关节囊', L(0.0065, 1.5745))], 'start')
        label(f, 1370, 985, 'Lateral ligament', '外侧韧带', '#b94334', 'start', to=L(0.006, 1.566))
        label(f, 1560, 985, 'Stylomandibular ligament', '茎突下颌韧带', '#2f7f8f', 'start', to=L(0.0035, 1.543))
        label(f, 1210, 1060, 'Sphenomandibular ligament (medial to the ramus, dashed)', '蝶下颌韧带（在下颌支内侧，虚线）', '#7a5aa6', 'start', to=L(0.016, 1.553))
        f.save('颞下颌关节矢状切面与韧带')
