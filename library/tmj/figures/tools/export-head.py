"""Export the head meshes, nerve and vessel curves and label points the tmj figures need from Z-Anatomy Startup.blend.

    <python with bpy> -I export-head.py -- <Startup.blend> <out.npz>
Coordinates are written in model axes (x, z_blender, -y_blender), metres. Then run project-outlines.py on the .npz."""
import bpy, sys, json, re
import numpy as np
blend, outp = sys.argv[sys.argv.index('--')+1:][:2]
bpy.ops.wm.open_mainfile(filepath=blend, use_scripts=False)
D = bpy.data.objects
PAIRED_BONES = ['Temporal bone','Zygomatic bone','Maxilla','Parietal bone','Nasal bone','Lacrimal bone','Palatine bone','Inferior nasal concha']
UNPAIRED = ['Mandible','Sphenoid bone','Frontal bone','Occipital bone','Ethmoid bone','Vomer','Hyoid bone','Atlas (C1)','Axis (C2)']
MUS = ['Superficial part of masseter','Deep part of masseter','Temporalis muscle','Medial pterygoid muscle','Superior head of lateral pterygoid muscle','Inferior head of lateral pterygoid muscle','Frontalis muscle','Occipitalis muscle','Epicranial aponeurosis','Anterior belly of digastric muscle','Posterior belly of digastric muscle','Intermediate tendon of digastric muscle','Mylohyoid muscle','Geniohyoid muscle','Stylohyoid muscle','Orbicularis oris muscle','Orbital part of orbicularis oculi','Palpebral part of orbicularis oculi','Zygomaticus major muscle','Zygomaticus minor muscle','Bucinator','Platysma','Sternocleidomastoid muscle','Risorius muscle','Depressor anguli oris','Depressor labii inferioris','Mentalis muscle','Levator labii superioris','Nasalis muscle','Procerus muscle','Corrugator supercilii',
       'Articular disc of temporomandibular joint','Articular capsule of temporomandibular joint','Lateral temporomandibular ligament','Sphenomandibular ligament','Stylomandibular ligament','Parotid gland','Stylohyoid ligament','Sternohyoid muscle','Omohyoid muscle','Thyrohyoid muscle','Eyebrow']
want = set(UNPAIRED)
for n in PAIRED_BONES + MUS: want |= {n + '.r', n + '.l'}
for o in D:
    if o.type == 'MESH' and re.search(r'(tooth|incisor|canine|premolar|molar)', o.name, re.I) and not re.search(r'\.[a-z]?[ijst]$|\.o|\.e', o.name): want.add(o.name)
    if o.type == 'MESH' and o.parent and o.parent.name in ('Auricular region.g',): want.add(o.name)
    if o.type == 'MESH' and re.search(r'(nasal cartilage|alar cartilage|Eyeball$|Cornea|Thyroid cartilage$|Cricoid cartilage$|Tongue$)', o.name, re.I): want.add(o.name)
dg = bpy.context.evaluated_depsgraph_get()
def conv(v): return np.c_[v[:,0], v[:,2], -v[:,1]]   # blender (x, y, z-up) -> model (x, y-up, z-anterior)
meshes = {}
for n in sorted(want):
    o = D.get(n)
    if not o or o.type != 'MESH': print('MISSING', n); continue
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    me.calc_loop_triangles()
    v = np.array([ev.matrix_world @ x.co for x in me.vertices], dtype=float)
    f = np.array([t.vertices[:] for t in me.loop_triangles], dtype=int)
    if len(f) == 0: print('NOFACES', n); continue
    meshes[n] = (conv(v), f)
    ev.to_mesh_clear()
curves = {}
CUR = r'^(Trigeminal nerve|Ophthalmic nerve|Maxillary nerve|Anterior division of mandibular|Posterior division of mandibular|Buccal nerve|Lingual nerve|Inferior alveolar nerve|Mental nerve|Nerve to mylohyoid|Chorda tympani|Facial nerve|Hypoglossal nerve|Superficial temporal artery|Maxillary artery|Facial artery|Transverse facial artery|External carotid artery|Middle meningeal artery|Retromandibular vein|Superficial temporal veins|Frontal nerve|Supra-orbital|Infra-orbital nerve|Auriculotemporal|Great auricular|Zygomatic nerve|Lacrimal nerve|Nasociliary|Supratrochlear nerve|Infratrochlear)'
allc = [o.name for o in D if o.type == 'CURVE']
for o in D:
    if o.type != 'CURVE': continue
    anc = []; p = o.parent
    while p: anc.append(p.name); p = p.parent
    if re.search(CUR, o.name) or any(re.search(r'^(Trigeminal nerve|Facial nerve|Ophthalmic nerve|Maxillary nerve)', a) for a in anc):
        sp = []
        for s in o.data.splines:
            pts = [o.matrix_world @ (bp.co) for bp in s.bezier_points] if s.type == 'BEZIER' else [o.matrix_world @ p.co.xyz for p in s.points]
            if len(pts) > 1: sp.append(conv(np.array(pts, dtype=float)).round(5).tolist())
        curves[o.name] = {'splines': sp, 'bevel': o.data.bevel_depth, 'parents': anc[:2]}
labels = {}
for o in D:
    if o.type == 'MESH' and o.name.endswith(('.j', '.i')) and len(o.data.vertices) == 2 and o.parent and o.parent.parent:
        gp = o.parent.parent.name
        if gp in want or gp in ('Trigeminal nerve (V).r', 'Mandibular nerve.g') or re.search(r'(mandib|temporal|sphenoid|zygom|maxill|hyoid|pteryg|masseter|facial|trigem|parotid)', gp, re.I):
            vs = conv(np.array([o.matrix_world @ v.co for v in o.data.vertices], dtype=float))
            lab = conv(np.array([o.parent.matrix_world.translation], dtype=float))[0]
            if np.linalg.norm(lab) > 0.1: labels[o.name[:-2] + '|' + gp] = lab.round(5).tolist()
np.savez_compressed(outp, names=np.array(list(meshes), dtype=object), **{f'v{i}': m[0] for i, m in enumerate(meshes.values())}, **{f'f{i}': m[1] for i, m in enumerate(meshes.values())})
json.dump({'curves': curves, 'labels': labels}, open(outp + '.json', 'w'))
print('meshes', len(meshes), 'curves', len(curves), 'labels', len(labels))
print(sorted(curves))
