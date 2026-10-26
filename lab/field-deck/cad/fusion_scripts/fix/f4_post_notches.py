# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07). f4: FIX 3, second part - over each of the battery
# board's two brass posts the relief keeps its full depth up to z 47.6 (a notch 10 mm wide, flat top = a 10 mm bridge when
# the body prints mouth down). The posts stand at x -20.1 and x +37.9 (58 mm apart), their tops at z 43.6 .. 45.9.
# The notch's outline is tied to the same named number as the relief (stand_wall_relief_depth).
# Tried first in the cloud (calcheck/bottom_relief.py): each notch takes 25.033 mm3 more.
# It also ties down the end points of the three guide lines in the relief's sketch (f3 left them loose; no change in shape).
import adsk.core, adsk.fusion, math

BODY = 'Body (copy of r7) + sound posts + slot'
SK3 = 'Fix 3 - relief in the bottom wall: its outline, seen from the side (sketch)'
PL = 'Fix 3 - plane beside the first brass post (x -25.1)'
SK = 'Fix 3 - notch over a brass post: its outline, seen from the side (sketch)'
FT1 = 'Fix 3 - notch over the first brass post (x -20.1)'
FT2 = 'Fix 3 - notch over the second brass post (x +37.9)'
X0, WIDTH, PITCH = -25.1, '10 mm', '58 mm'
T12, C12 = math.tan(math.radians(12.0)), math.cos(math.radians(12.0))
Y_I = lambda z: -92.0 + 2.5 / C12 + T12 * (z + 11.6)        # the bottom wall's inner face (y at height z), case mm
CH = -123.8                                                # the 45 degree face under the plate's seat: y = z + CH
ZA, ZB = 44.9, 47.6                                        # the notch: from z 44.9 (inside the relief) to its flat top

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    VI = adsk.core.ValueInput.createByString
    par = des.userParameters.itemByName('stand_wall_relief_depth')
    sk3 = [s for s in comp.sketches if s.name == SK3]
    if not par or not sk3:
        print('*** the relief (f3) is not there - stopped'); return
    n = 0
    for l in sk3[0].sketchCurves.sketchLines:
        if l.isConstruction:
            for p in (l.startSketchPoint, l.endSketchPoint):
                if not p.isFixed:
                    p.isFixed = True; n += 1
    print("relief's sketch: %d guide end points tied down; fully tied down now: %s" % (n, sk3[0].isFullyConstrained))
    if [s for s in comp.sketches if s.name == SK]:
        print('ALREADY THERE:', SK); return
    deep = par.value * 10.0
    Y_F = lambda z: Y_I(z) - deep / C12                     # the relief's floor
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    v0 = body.volume; n0 = comp.bRepBodies.count
    print('body volume before the notches %.6f cm3 (trial: 118.098246)' % v0)
    pin = comp.constructionPlanes.createInput()
    pin.setByOffset(comp.yZConstructionPlane, VI('%g mm' % X0))
    plane = comp.constructionPlanes.add(pin); plane.name = PL
    if abs(plane.geometry.origin.x - X0 / 10.0) > 1e-6:
        print('*** the plane is not at x %g - stopped' % X0); plane.deleteMe(); return
    sk = comp.sketches.add(plane); sk.name = SK
    P = lambda y, z: sk.modelToSketchSpace(adsk.core.Point3D.create(X0 / 10.0, y / 10.0, z / 10.0))
    a, b = (Y_F(ZA), ZA), (Y_F(ZB), ZB)                     # on the relief's floor
    c, d = (ZB + CH + 0.5, ZB), (Y_I(ZA) + 0.5, ZA)         # inside the cavity, 0.5 clear of the faces
    L = sk.sketchCurves.sketchLines
    def guide(p, q):
        l = L.addByTwoPoints(P(*p), P(*q)); l.isConstruction = True; l.isFixed = True
        l.startSketchPoint.isFixed = True; l.endSketchPoint.isFixed = True; return l
    wall = guide((Y_I(43.0), 43.0), (Y_I(49.0), 49.0))      # the wall's inner face
    top = guide((-80.0, ZB), (-75.0, ZB))                   # the notch's flat top, z 47.6
    low = guide((-80.5, ZA), (-76.0, ZA))                   # its lower end, z 44.9
    n1 = L.addByTwoPoints(P(*a), P(*b))                     # the floor
    n2 = L.addByTwoPoints(n1.endSketchPoint, P(*c))         # the flat top
    n3 = L.addByTwoPoints(n2.endSketchPoint, P(*d))
    L.addByTwoPoints(n3.endSketchPoint, n1.startSketchPoint)
    n2.endSketchPoint.isFixed = True; n3.endSketchPoint.isFixed = True
    gc = sk.geometricConstraints
    gc.addCoincident(n1.startSketchPoint, low)
    gc.addCoincident(n1.endSketchPoint, top)
    gc.addParallel(n1, wall)
    dim = sk.sketchDimensions.addOffsetDimension(wall, n1, P(-80.5, 46.5))
    dim.parameter.expression = 'stand_wall_relief_depth'
    err = 0.0
    for sp, want in ((n1.startSketchPoint, a), (n1.endSketchPoint, b), (n2.endSketchPoint, c), (n3.endSketchPoint, d)):
        m = sk.sketchToModelSpace(sp.geometry); err = max(err, abs(m.y * 10 - want[0]), abs(m.z * 10 - want[1]), abs(m.x * 10 - X0))
    xd, yd = sk.xDirection, sk.yDirection
    nx = xd.y * yd.z - xd.z * yd.y
    print('sketch: %d lines, %d profile(s); fully tied down: %s; depth %s = %.4f mm; corners off their places by %.6f mm at most; normal x %+.0f' % (
        L.count, sk.profiles.count, sk.isFullyConstrained, dim.parameter.expression, dim.parameter.value * 10, err, nx))
    print('corners (y, z): a %.4f %.4f  b %.4f %.4f  c %.4f %.4f  d %.4f %.4f' % (a + b + c + d))
    if sk.profiles.count != 1 or err > 1e-4 or abs(abs(nx) - 1.0) > 1e-6:
        print('*** the outline is not what was meant - stopped before cutting (sketch left for inspection)'); return
    sign = '' if nx > 0 else '-'
    ext = comp.features.extrudeFeatures
    for name, start in ((FT1, None), (FT2, PITCH)):
        v1 = [q for q in comp.bRepBodies if q.name == BODY][0].volume
        einp = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
        if start:
            einp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI(sign + start))    # the second post, 58 mm on
        einp.setDistanceExtent(False, VI(sign + WIDTH))                                       # toward +x
        einp.participantBodies = [[q for q in comp.bRepBodies if q.name == BODY][0]]
        f = ext.add(einp); f.name = name
        v2 = [q for q in comp.bRepBodies if q.name == BODY][0].volume
        print('%s: health %d %s; body volume change %.3f mm3 (trial: -25.033)' % (name, f.healthState, f.errorOrWarningMessage, (v2 - v1) * 1000.0))
    sk.isLightBulbOn = False; plane.isLightBulbOn = False
    body = [q for q in comp.bRepBodies if q.name == BODY][0]
    print('FIX 3 complete: body volume now %.6f cm3 (trial after fixes 1, 2, 3: 118.048179); bodies %d (before %d); faces %d; timeline %d steps' % (
        body.volume, comp.bRepBodies.count, n0, body.faces.count, des.timeline.count))
