# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07), built in the owner's Fusion file "cyberdeck" as new
# steps at the end of the timeline. f1: the named numbers, and FIX 1 - the top opening goes 4.4 mm further toward the side
# without the handle (its edge from x -1.2 to x -5.6): HDMI 0 is at x +2.29, not +6.7, and its plug needs the room.
# One outline (the opening's own cross-section: the notch and the 45 degree bevel of its upper edge), pushed sideways.
# Tried first in the cloud (calcheck/fix_proto.py): takes 484.11 mm3. Keep a script under about 8 kB; read the state back.
import adsk.core, adsk.fusion

BODY = 'Body (copy of r7) + sound posts + slot'
PL = 'Fix 1 - plane just inside the top opening (x -1.0)'
SK = 'Fix 1 - top opening: its outline, seen from the side (sketch)'
FT = 'Fix 1 - top opening 4.4 mm further (for the plug of HDMI 0)'
# (y, z) in the case frame, mm: the notch y 31.6..41.6, z 4.5..44, and the bevel of its upper edge (from the wall's inner
# face at z 44 up and out at 45 degrees)
PTS = [(31.6, 4.5), (41.6, 4.5), (41.6, 44.0), (39.6, 44.0), (39.6, 49.5), (34.1, 44.0), (31.6, 44.0)]
PARS = [('top_opening_extra', '4.4 mm', 'FIX 1 (2026-10-07): the top opening goes this much further toward the side without the handle than in r7 (edge at x -5.6, was -1.2) - for the plug of HDMI 0. At 4.4 the edge lies in the groove beside the armour plate; keep it'),
        ('side_window_extra', '2.5 mm', 'FIX 2 (2026-10-07): the side window (handle side) goes this much further down than in r7 (lower end at y -28.5, was -26) - for the plugs of the lower USB pair. 1.75 mm of plain wall stays before the armour recess'),
        ('stand_wall_relief_depth', '1.3 mm', 'FIX 3 (2026-10-07): how deep the relief is cut into the INSIDE of the bottom wall (the wall the deck stands on), where the battery board and its two brass posts come. The wall is 2.5: 1.2 stays. Not more than 1.5'),
        ('sound_post2_x', '11 mm', 'FIX 5 (2026-10-07): screw post 2 of the speaker cover, its distance from the middle line toward the side without the handle (was 6.6; moved 4.4 with the top opening)')]

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    VI = adsk.core.ValueInput.createByString
    up = des.userParameters
    for name, expr, note in PARS:
        if not up.itemByName(name):
            up.add(name, VI(expr), 'mm', note)
        print('parameter', name, '=', up.itemByName(name).expression)
    if [s for s in comp.sketches if s.name == SK]:
        print('ALREADY THERE:', SK); return
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    v0 = body.volume; n0 = comp.bRepBodies.count
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(comp.yZConstructionPlane, VI('-1 mm'))
    plane = comp.constructionPlanes.add(pin); plane.name = PL
    g = plane.geometry
    print('plane: origin (%.4f, %.4f, %.4f) cm, normal (%.2f, %.2f, %.2f)' % (g.origin.x, g.origin.y, g.origin.z, g.normal.x, g.normal.y, g.normal.z))
    if abs(g.origin.x + 0.1) > 1e-6:
        print('*** the plane is not at x -1.0 mm - stopped'); plane.deleteMe(); return
    sk = comp.sketches.add(plane); sk.name = SK
    P = lambda y, z: sk.modelToSketchSpace(adsk.core.Point3D.create(-0.1, y / 10.0, z / 10.0))
    if max(abs(P(y, z).z) for y, z in PTS) > 1e-7:
        print('*** the sketch does not lie in the plane - stopped'); sk.deleteMe(); plane.deleteMe(); return
    L = sk.sketchCurves.sketchLines
    first = prev = L.addByTwoPoints(P(*PTS[0]), P(*PTS[1]))
    for y, z in PTS[2:]:
        prev = L.addByTwoPoints(prev.endSketchPoint, P(y, z))
    L.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
    for l in L:
        l.isFixed = True
    xd, yd = sk.xDirection, sk.yDirection
    nx = xd.y * yd.z - xd.z * yd.y                     # the sketch's own normal, its x part: a plus distance goes that way
    print('sketch: %d lines, %d profile(s), x (%.0f,%.0f,%.0f) y (%.0f,%.0f,%.0f), normal x %+.0f' % (L.count, sk.profiles.count, xd.x, xd.y, xd.z, yd.x, yd.y, yd.z, nx))
    if sk.profiles.count != 1 or abs(abs(nx) - 1.0) > 1e-6:
        print('*** not one closed outline, or the sketch is not square to x - stopped (sketch left for inspection)'); return
    ext = comp.features.extrudeFeatures
    einp = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    einp.setDistanceExtent(False, VI(('-' if nx > 0 else '') + '( top_opening_extra + 0.2 mm )'))     # toward -x, the side without the handle
    einp.participantBodies = [body]
    f = ext.add(einp); f.name = FT
    sk.isLightBulbOn = False; plane.isLightBulbOn = False
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    print('FIX 1 done: health %d %s; body volume change %.3f mm3 (trial in the cloud: -484.11); bodies in the item %d (before %d); faces %d' % (
        f.healthState, f.errorOrWarningMessage, (body.volume - v0) * 1000.0, comp.bRepBodies.count, n0, body.faces.count))
    print('body volume now %.6f cm3; timeline %d steps; document modified %s' % (body.volume, des.timeline.count, app.activeDocument.isModified))
