# MK-I r8 draft - CORRECTIONS OF 2026-10-07, repaired 2026-10-08. f9: the two notches over the brass posts get SLOPED tops.
# The notches of f4 had flat tops (z 47.6, 10 x 2 mm): level faces with only the bed under them, 47 mm up - the slicer
# ("support on build plate only, threshold 30") would have stood a tower under each (support_survey.py: 19.8 mm2 each).
# Now: one triangle per post, drawn ON THE RELIEF'S FLOOR, ridge at z 49.0 over the post's middle, sides at 45 degrees,
# pushed 6 mm square to the wall toward the cavity. Roof faces 46.2 degrees from level: no support, no bridge.
# The floor's plane is set off from the wall's inner face by the named number stand_wall_relief_depth, so the notches
# follow the relief when that number is changed. f4's four steps (plane, sketch, two cuts) are REMOVED.
# Tried first in the cloud (calcheck/relief_v2.py): each notch takes 13.963 mm3; body after this 118.067923 cm3.
import adsk.core, adsk.fusion, math

BODY = 'Body (copy of r7) + sound posts + slot'
OLD = ['Fix 3 - notch over the first brass post (x -20.1)', 'Fix 3 - notch over the second brass post (x +37.9)']
OLD_SK = 'Fix 3 - notch over a brass post: its outline, seen from the side (sketch)'
OLD_PL = 'Fix 3 - plane beside the first brass post (x -25.1)'
SK3 = 'Fix 3 - relief in the bottom wall: its outline, seen from the side (sketch)'
PL3 = "Fix 3 - plane at the relief's end (x -27)"
PA = "Fix 3 - plane on the bottom wall's inner face"
PB = "Fix 3 - plane on the relief's floor (inner face, moved out by the relief's depth)"
SK = "Fix 3 - notch over each brass post: a triangle on the relief's floor (sketch)"
FT = 'Fix 3 - notches with sloped tops over the two brass posts (they print without support)'
C12, S12, T12 = math.cos(math.radians(12.0)), math.sin(math.radians(12.0)), math.tan(math.radians(12.0))
Y_I = lambda z: -92.0 + 2.5 / C12 + T12 * (z + 11.6)
Z_RIDGE, Z_BASE, POSTS = 49.0, 44.0, (-20.1, 37.9)

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    VI = adsk.core.ValueInput.createByString
    P3 = adsk.core.Point3D.create
    vol = lambda: [b for b in comp.bRepBodies if b.name == BODY][0].volume
    par = des.userParameters.itemByName('stand_wall_relief_depth')
    if [s for s in comp.sketches if s.name == SK]:
        print('ALREADY THERE:', SK); return
    if abs(par.value - 0.13) > 1e-9:
        print('*** the relief depth is not 1.3 mm - set it back first'); return
    print('body before: %.6f cm3 (with the flat notches: 118.045783)' % vol())
    ext = comp.features.extrudeFeatures
    gone = 0
    for nm in OLD:
        f = [q for q in ext if q.name == nm]
        if f:
            f[0].deleteMe(); gone += 1
    for s in [q for q in comp.sketches if q.name == OLD_SK]:
        s.deleteMe(); gone += 1
    for p in [q for q in comp.constructionPlanes if q.name == OLD_PL]:
        p.deleteMe(); gone += 1
    print('removed %d of the 4 steps of the flat notches; body now %.6f cm3 (relief alone: 118.095850)' % (gone, vol()))
    sk3 = [s for s in comp.sketches if s.name == SK3][0]
    pl3 = [p for p in comp.constructionPlanes if p.name == PL3][0]
    wall = None
    for l in sk3.sketchCurves.sketchLines:
        if l.isConstruction:
            a = sk3.sketchToModelSpace(l.startSketchPoint.geometry); b = sk3.sketchToModelSpace(l.endSketchPoint.geometry)
            if abs(a.z * 10 - 33.0) < 1e-6 and abs(b.z * 10 - 49.0) < 1e-6:
                wall = l
    if not wall:
        print('*** the guide line on the wall\'s inner face was not found - stopped'); return
    pin = comp.constructionPlanes.createInput()
    pin.setByAngle(wall, VI('90 deg'), pl3)
    pa = comp.constructionPlanes.add(pin); pa.name = PA
    ga = pa.geometry
    dot = ga.normal.y * C12 - ga.normal.z * S12                 # + : its normal points toward the cavity
    on_face = abs((ga.origin.y * 10 - Y_I(ga.origin.z * 10)))    # 0 : its origin lies on the inner face
    print('plane A: origin (%.3f, %.3f, %.3f) mm, normal (%.4f, %.4f, %.4f); toward the cavity %+.4f; off the inner face %.6f mm' % (
        ga.origin.x * 10, ga.origin.y * 10, ga.origin.z * 10, ga.normal.x, ga.normal.y, ga.normal.z, dot, on_face))
    if abs(abs(dot) - 1.0) > 1e-6 or on_face > 1e-5:
        print('*** plane A is not the wall\'s inner face - stopped (plane left for inspection)'); return
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(pa, VI(('-' if dot > 0 else '') + 'stand_wall_relief_depth'))
    pb = comp.constructionPlanes.add(pin); pb.name = PB
    gb = pb.geometry
    moved = ((gb.origin.y - ga.origin.y) * C12 - (gb.origin.z - ga.origin.z) * S12) * 10     # along "toward the cavity": must be -1.3
    print('plane B: origin (%.3f, %.3f, %.3f) mm; moved %.4f mm toward the cavity (must be -1.3000)' % (gb.origin.x * 10, gb.origin.y * 10, gb.origin.z * 10, moved))
    if abs(moved + 1.3) > 1e-6:
        print('*** plane B is not the relief\'s floor - stopped (planes left for inspection)'); return
    sk = comp.sketches.add(pb); sk.name = SK
    L = sk.sketchCurves.sketchLines
    half = (Z_RIDGE - Z_BASE) / C12
    yb, yr = Y_I(Z_BASE) - 1.3 / C12, Y_I(Z_RIDGE) - 1.3 / C12
    worst = 0.0
    for px in POSTS:
        pts = [sk.modelToSketchSpace(P3(x / 10.0, y / 10.0, z / 10.0)) for x, y, z in ((px - half, yb, Z_BASE), (px + half, yb, Z_BASE), (px, yr, Z_RIDGE))]
        worst = max([worst] + [abs(p.z) for p in pts])
        l1 = L.addByTwoPoints(pts[0], pts[1]); l2 = L.addByTwoPoints(l1.endSketchPoint, pts[2]); l3 = L.addByTwoPoints(l2.endSketchPoint, l1.startSketchPoint)
        for l in (l1, l2, l3):
            l.isFixed = True; l.startSketchPoint.isFixed = True; l.endSketchPoint.isFixed = True
    xd, yd = sk.xDirection, sk.yDirection
    n = (xd.y * yd.z - xd.z * yd.y, xd.z * yd.x - xd.x * yd.z, xd.x * yd.y - xd.y * yd.x)
    toward = n[1] * C12 - n[2] * S12
    print('sketch: %d lines, %d profiles (must be 2), fully tied down %s; corners off the plane by %.7f cm at most; its normal toward the cavity %+.4f' % (
        L.count, sk.profiles.count, sk.isFullyConstrained, worst, toward))
    if sk.profiles.count != 2 or worst > 1e-6 or abs(abs(toward) - 1.0) > 1e-6:
        print('*** the triangles are not what was meant - stopped before cutting (sketch left for inspection)'); return
    col = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        col.add(sk.profiles.item(i))
    v1 = vol()
    einp = ext.createInput(col, adsk.fusion.FeatureOperations.CutFeatureOperation)
    einp.setDistanceExtent(False, VI(('' if toward > 0 else '-') + '6 mm'))
    einp.participantBodies = [[b for b in comp.bRepBodies if b.name == BODY][0]]
    f = ext.add(einp); f.name = FT
    sk.isLightBulbOn = False; pa.isLightBulbOn = False; pb.isLightBulbOn = False
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    print('notches cut: health %d %s; body volume change %.3f mm3 (trial in the cloud: -27.926); body now %.6f cm3 (trial: 118.067923); bodies %d; faces %d' % (
        f.healthState, f.errorOrWarningMessage, (body.volume - v1) * 1000.0, body.volume, comp.bRepBodies.count, body.faces.count))
    print('timeline %d steps; steps not healthy: %s' % (des.timeline.count, [des.timeline.item(i).name for i in range(des.timeline.count) if not des.timeline.item(i).isGroup and des.timeline.item(i).healthState != 0]))
