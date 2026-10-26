# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07). f2: FIX 2 - the side window (handle side) goes
# 2.5 mm further down (its lower end from y -26.0 to y -28.5): the lower USB pair is at y -19.0, not -17.9, and may sit
# 0.5 lower still; a 16 mm plug then reaches y -27.5. One outline (the window's own cross-section: the opening and the
# 45 degree bevels of its upper and lower edge), pushed along the wall. 1.75 mm of plain wall stays between the window
# and the armour recess (its rim is at y -30.25). Tried first in the cloud (calcheck/fix_proto.py): takes 159.17 mm3.
import adsk.core, adsk.fusion

BODY = 'Body (copy of r7) + sound posts + slot'
PL = 'Fix 2 - plane just inside the side window (y -25.8)'
SK = 'Fix 2 - side window: its outline, seen from above (sketch)'
FT = 'Fix 2 - side window 2.5 mm further down (for the plugs of the lower USB pair)'
# (x, z) in the case frame, mm: the opening x 67.7..80.7, z 11..36; the lower edge's bevel (down to z 8.5 at the wall's
# outer face x 75.7) and the upper edge's bevel (up to z 38.5 there)
PTS = [(67.7, 11.0), (73.2, 11.0), (76.2, 8.0), (76.2, 11.0), (80.7, 11.0), (80.7, 36.0), (78.7, 36.0), (78.7, 41.5), (73.2, 36.0), (67.7, 36.0)]

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    VI = adsk.core.ValueInput.createByString
    if not des.userParameters.itemByName('side_window_extra'):
        print('*** the named number side_window_extra is missing - run f1 first'); return
    if [s for s in comp.sketches if s.name == SK]:
        print('ALREADY THERE:', SK); return
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    v0 = body.volume; n0 = comp.bRepBodies.count
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(comp.xZConstructionPlane, VI('-25.8 mm'))
    plane = comp.constructionPlanes.add(pin); plane.name = PL
    g = plane.geometry
    print('plane: origin (%.4f, %.4f, %.4f) cm, normal (%.2f, %.2f, %.2f)' % (g.origin.x, g.origin.y, g.origin.z, g.normal.x, g.normal.y, g.normal.z))
    if abs(g.origin.y + 2.58) > 1e-6:
        print('*** the plane is not at y -25.8 mm - stopped'); plane.deleteMe(); return
    sk = comp.sketches.add(plane); sk.name = SK
    P = lambda x, z: sk.modelToSketchSpace(adsk.core.Point3D.create(x / 10.0, -2.58, z / 10.0))
    if max(abs(P(x, z).z) for x, z in PTS) > 1e-7:
        print('*** the sketch does not lie in the plane - stopped'); sk.deleteMe(); plane.deleteMe(); return
    L = sk.sketchCurves.sketchLines
    first = prev = L.addByTwoPoints(P(*PTS[0]), P(*PTS[1]))
    for x, z in PTS[2:]:
        prev = L.addByTwoPoints(prev.endSketchPoint, P(x, z))
    L.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
    for l in L:
        l.isFixed = True
    xd, yd = sk.xDirection, sk.yDirection
    ny = xd.z * yd.x - xd.x * yd.z                     # the sketch's own normal, its y part: a plus distance goes that way
    print('sketch: %d lines, %d profile(s), x (%.0f,%.0f,%.0f) y (%.0f,%.0f,%.0f), normal y %+.0f' % (L.count, sk.profiles.count, xd.x, xd.y, xd.z, yd.x, yd.y, yd.z, ny))
    if sk.profiles.count != 1 or abs(abs(ny) - 1.0) > 1e-6:
        print('*** not one closed outline, or the sketch is not square to y - stopped (sketch left for inspection)'); return
    ext = comp.features.extrudeFeatures
    einp = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    einp.setDistanceExtent(False, VI(('-' if ny > 0 else '') + '( side_window_extra + 0.2 mm )'))     # toward -y, the bottom
    einp.participantBodies = [body]
    f = ext.add(einp); f.name = FT
    sk.isLightBulbOn = False; plane.isLightBulbOn = False
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    print('FIX 2 done: health %d %s; body volume change %.3f mm3 (trial in the cloud: -159.17); bodies in the item %d (before %d); faces %d' % (
        f.healthState, f.errorOrWarningMessage, (body.volume - v0) * 1000.0, comp.bRepBodies.count, n0, body.faces.count))
    print('body volume now %.6f cm3 (trial after fixes 1+2: 119.344099); timeline %d steps' % (body.volume, des.timeline.count))
