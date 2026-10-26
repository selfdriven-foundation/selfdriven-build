import adsk.core, adsk.fusion, json, math

ITEM = 'BUILT IN FUSION'
NAME = 'Back plate r8 - mark + words (built in Fusion)'
BODY = 'Back plate (copy of r7) + mark + words'
PLANE = "Back - plane on the plate's outer face (z 53)"

def find(des):
    root = des.rootComponent
    occ27 = [o for o in root.occurrences if ITEM in o.component.name][0]
    comp27 = occ27.component
    occ = [o for o in comp27.occurrences if o.component.name == NAME]
    return root, occ27, comp27, (occ[0] if occ else None)

def report(des, comp):
    b = [x for x in comp.bRepBodies if x.name == BODY][0]
    bb = b.boundingBox
    print('plate now: volume %.6f cm3, faces %d, box x %.4f..%.4f y %.4f..%.4f z %.4f..%.4f (cm, case frame)' % (
        b.volume, b.faces.count, bb.minPoint.x, bb.maxPoint.x, bb.minPoint.y, bb.maxPoint.y, bb.minPoint.z, bb.maxPoint.z))
    tl = des.timeline
    bad = []
    for i in range(tl.count):
        try:
            hs = tl.item(i).healthState
        except Exception:
            hs = -1
        if hs not in (0, 5):
            bad.append((i, tl.item(i).name, hs))
    print('timeline', tl.count, 'items; not healthy:', bad)
    return b

SKETCH = 'Back 1 - ten bolt marks that make way (sketch)'
FEATURE = 'Back 1 - the ten bolt marks filled'
OP = 'join'            # 'join' or 'cut'
DIST = '-0.6 mm'
RINGS = json.loads('[[[3.6094,-39.5],[2.4547,-37.5],[0.1453,-37.5],[-1.0094,-39.5],[0.1453,-41.5],[2.4547,-41.5]],[[38.5094,-3.5],[37.3547,-1.5],[35.0453,-1.5],[33.8906,-3.5],[35.0453,-5.5],[37.3547,-5.5]],[[5.6094,-5.5],[4.4547,-3.5],[2.1453,-3.5],[0.9906,-5.5],[2.1453,-7.5],[4.4547,-7.5]],[[36.5094,-37.5],[35.3547,-35.5],[33.0453,-35.5],[31.8906,-37.5],[33.0453,-39.5],[35.3547,-39.5]],[[-9.3906,-67.613],[-10.5453,-65.613],[-12.8547,-65.613],[-14.0094,-67.613],[-12.8547,-69.613],[-10.5453,-69.613]],[[51.5094,-67.613],[50.3547,-65.613],[48.0453,-65.613],[46.8906,-67.613],[48.0453,-69.613],[50.3547,-69.613]],[[-20.8906,-55.113],[-22.0453,-53.113],[-24.3547,-53.113],[-25.5094,-55.113],[-24.3547,-57.113],[-22.0453,-57.113]],[[15.0594,-54.113],[13.9047,-52.113],[11.5953,-52.113],[10.4406,-54.113],[11.5953,-56.113],[13.9047,-56.113]],[[27.0594,-54.113],[25.9047,-52.113],[23.5953,-52.113],[22.4406,-54.113],[23.5953,-56.113],[25.9047,-56.113]],[[63.0094,-55.113],[61.8547,-53.113],[59.5453,-53.113],[58.3906,-55.113],[59.5453,-57.113],[61.8547,-57.113]]]')     # closed outlines, case mm, as the reader behind the case sees them

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    root, occ27, comp27, occ = find(des)
    comp = occ.component
    if [s for s in comp.sketches if s.name == SKETCH]:
        print('ALREADY THERE:', SKETCH); report(des, comp); return
    if not [p for p in des.userParameters if p.name == 'engrave_depth']:
        des.userParameters.add('engrave_depth', adsk.core.ValueInput.createByString('0.6 mm'), 'mm', 'how deep mark and words are cut into the back plate')
    planes = [p for p in comp.constructionPlanes if p.name == PLANE]
    if planes:
        plane = planes[0]
    else:
        pin = comp.constructionPlanes.createInput()
        pin.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByString('53 mm'))
        plane = comp.constructionPlanes.add(pin); plane.name = PLANE
    body = report(des, comp)
    v0 = body.volume
    sk = comp.sketches.add(plane); sk.name = SKETCH
    sk.isComputeDeferred = True
    lines = sk.sketchCurves.sketchLines
    n = 0
    for ring in RINGS:
        pts = [sk.modelToSketchSpace(adsk.core.Point3D.create(x / 10.0, y / 10.0, 5.3)) for x, y in ring]
        first = lines.addByTwoPoints(pts[0], pts[1]); prev = first; n += 1
        for p in pts[2:]:
            prev = lines.addByTwoPoints(prev.endSketchPoint, p); n += 1
        lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint); n += 1
    for l in lines:
        l.isFixed = True
    sk.isComputeDeferred = False
    print('sketch', SKETCH, ': lines', n, 'outlines', len(RINGS), 'profiles', sk.profiles.count)
    if sk.profiles.count != len(RINGS):
        print('*** profiles do not match the outlines - nothing cut'); return
    col = adsk.core.ObjectCollection.create()
    for p in sk.profiles:
        col.add(p)
    ext = comp.features.extrudeFeatures
    op = adsk.fusion.FeatureOperations.JoinFeatureOperation if OP == 'join' else adsk.fusion.FeatureOperations.CutFeatureOperation
    inp = ext.createInput(col, op)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByString(DIST))
    inp.participantBodies = [body]
    f = ext.add(inp); f.name = FEATURE
    sk.isLightBulbOn = False
    body = report(des, comp)
    print('volume change %.6f cm3' % (body.volume - v0))
