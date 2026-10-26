# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07). f3: FIX 3 - a relief INSIDE the bottom wall (the
# slanted wall the deck stands on), where the battery board's lower end and its two brass posts come: by Raspberry Pi's
# drawing they TOUCH that wall. The owner saw the picture and said "looks ok" (2026-10-07). Nothing changes outside.
# The outline (seen from the side) is tied to ONE named number, stand_wall_relief_depth: its floor runs parallel to the
# wall's inner face at that depth; its lower end starts at z 35.5; at the top it runs out along the 45 degree face under
# the back plate's seat, carried on down - no ledge, so nothing starts in mid-air when the body prints mouth down.
# Tried first in the cloud (calcheck/bottom_relief.py, fix_proto.py): this step takes 1245.85 mm3 at a depth of 1.3.
import adsk.core, adsk.fusion, math

BODY = 'Body (copy of r7) + sound posts + slot'
PL = "Fix 3 - plane at the relief's end (x -27)"
SK = 'Fix 3 - relief in the bottom wall: its outline, seen from the side (sketch)'
FT = 'Fix 3 - relief inside the bottom wall (room for the battery board)'
X0, LENGTH = -27.0, '91.5 mm'                      # from x -27.0 to x +64.5: the board is x -23.7 .. +61.3
T12, C12, S12 = math.tan(math.radians(12.0)), math.cos(math.radians(12.0)), math.sin(math.radians(12.0))
Y_I = lambda z: -92.0 + 2.5 / C12 + T12 * (z + 11.6)        # the bottom wall's inner face (y at height z), case mm
CH = -123.8                                                # the 45 degree face under the plate's seat: y = z + CH
Z_CH = (CH - (-92.0 + 2.5 / C12 + T12 * 11.6)) / (T12 - 1.0)   # where that face leaves the wall: z 46.76
Z0 = 35.5                                                  # where the relief starts

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    VI = adsk.core.ValueInput.createByString
    par = des.userParameters.itemByName('stand_wall_relief_depth')
    if not par:
        print('*** the named number stand_wall_relief_depth is missing - run f1 first'); return
    if [s for s in comp.sketches if s.name == SK]:
        print('ALREADY THERE:', SK); return
    deep = par.value * 10.0
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    v0 = body.volume; n0 = comp.bRepBodies.count
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(comp.yZConstructionPlane, VI('%g mm' % X0))
    plane = comp.constructionPlanes.add(pin); plane.name = PL
    if abs(plane.geometry.origin.x - X0 / 10.0) > 1e-6:
        print('*** the plane is not at x %g - stopped' % X0); plane.deleteMe(); return
    sk = comp.sketches.add(plane); sk.name = SK
    P = lambda y, z: sk.modelToSketchSpace(adsk.core.Point3D.create(X0 / 10.0, y / 10.0, z / 10.0))
    M = lambda sp: sk.sketchToModelSpace(sp.geometry)
    z_run = (CH - (-92.0 + 2.5 / C12 + T12 * 11.6) + deep / C12) / (T12 - 1.0)   # where the floor meets the 45 degree face
    w0 = (Y_I(Z0), Z0)
    p1 = (w0[0] + 0.5, Z0)                                  # 0.5 inside the cavity, so the cut is clean
    p2 = (w0[0] - deep * C12, Z0 + deep * S12)              # the lower end, square to the wall
    p3 = (z_run + CH, z_run)
    p4 = (Z_CH + 0.5 + CH, Z_CH + 0.5)                      # a little up the 45 degree face
    L = sk.sketchCurves.sketchLines
    def guide(a, b):
        l = L.addByTwoPoints(P(*a), P(*b)); l.isConstruction = True; l.isFixed = True; return l
    wall = guide((Y_I(33.0), 33.0), (Y_I(49.0), 49.0))      # the wall's inner face
    seat = guide((44.0 + CH, 44.0), (49.0 + CH, 49.0))      # the 45 degree face under the seat, carried on down
    square = guide((w0[0] + 1.0 * C12, Z0 - 1.0 * S12), (w0[0] - 3.0 * C12, Z0 + 3.0 * S12))   # square to the wall, at z 35.5
    l1 = L.addByTwoPoints(P(*p1), P(*p2))
    l2 = L.addByTwoPoints(l1.endSketchPoint, P(*p3))        # the floor
    l3 = L.addByTwoPoints(l2.endSketchPoint, P(*p4))        # the run-out
    L.addByTwoPoints(l3.endSketchPoint, l1.startSketchPoint)
    l1.startSketchPoint.isFixed = True; l3.endSketchPoint.isFixed = True
    gc = sk.geometricConstraints
    gc.addCoincident(l1.endSketchPoint, square)
    gc.addCoincident(l2.endSketchPoint, seat)
    gc.addParallel(l2, wall)
    dim = sk.sketchDimensions.addOffsetDimension(wall, l2, P(-82.5, 40.0))
    dim.parameter.expression = 'stand_wall_relief_depth'
    err = 0.0
    for sp, want in ((l1.startSketchPoint, p1), (l1.endSketchPoint, p2), (l2.endSketchPoint, p3), (l3.endSketchPoint, p4)):
        m = M(sp); err = max(err, abs(m.y * 10 - want[0]), abs(m.z * 10 - want[1]), abs(m.x * 10 - X0))
    xd, yd = sk.xDirection, sk.yDirection
    nx = xd.y * yd.z - xd.z * yd.y
    print('sketch: %d lines, %d profile(s); fully tied down: %s; depth %s = %.4f mm; corners off their places by %.6f mm at most; normal x %+.0f' % (
        L.count, sk.profiles.count, sk.isFullyConstrained, dim.parameter.expression, dim.parameter.value * 10, err, nx))
    print('corners (y, z): p1 %.4f %.4f  p2 %.4f %.4f  p3 %.4f %.4f  p4 %.4f %.4f' % (p1 + p2 + p3 + p4))
    if sk.profiles.count != 1 or err > 1e-4 or abs(abs(nx) - 1.0) > 1e-6:
        print('*** the outline is not what was meant - stopped before cutting (sketch left for inspection)'); return
    ext = comp.features.extrudeFeatures
    einp = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    einp.setDistanceExtent(False, VI(('' if nx > 0 else '-') + LENGTH))          # toward +x, the handle side
    einp.participantBodies = [body]
    f = ext.add(einp); f.name = FT
    sk.isLightBulbOn = False; plane.isLightBulbOn = False
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    print('FIX 3 (relief) done: health %d %s; body volume change %.3f mm3 (trial in the cloud: -1245.849); bodies %d (before %d); faces %d' % (
        f.healthState, f.errorOrWarningMessage, (body.volume - v0) * 1000.0, comp.bRepBodies.count, n0, body.faces.count))
    print('body volume now %.6f cm3; timeline %d steps' % (body.volume, des.timeline.count))
