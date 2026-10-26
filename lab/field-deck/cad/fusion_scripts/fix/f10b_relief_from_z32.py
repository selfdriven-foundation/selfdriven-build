# MK-I r8 draft - CORRECTIONS OF 2026-10-07, improved 2026-10-08 after the independent review of the test corner.
# f10b: THE RELIEF IN THE BOTTOM WALL STARTS AT z 32.0 INSTEAD OF 35.5, and its run-out lies exactly in the 45 degree face.
# Why: the body is lowered over the stack, so the battery board's lower edge passes the wall BELOW the relief on its way in,
# and that wall leans in as it rises. At z 35.5 the unrelieved wall left the edge 0.66 mm by the drawing and 0.16 at the
# worst - less than the 1.3 / 0.6 it has once it is in its place. From z 32.0 the way in is wider than the seat everywhere.
# And the 45 degree face under the plate's seat is y = z - 123.812995 on this solid (measured), not z - 123.8.
# No new step: four fixed things in the relief's sketch are moved (the foot's guide line, the corner in the cavity at the
# foot, the 45 degree guide line, the corner on it), and the floor's two tied corners are put at their new places with them.
# (f10b: the first version, f10, left those two to the sketch solver. It never ran.)
# Tried first in the cloud (calcheck/relief_v2.py): relief 1701.145 mm3 with the notches; body after this 117.640554 cm3.
import adsk.core, adsk.fusion, math

BODY = 'Body (copy of r7) + sound posts + slot'
SK3 = 'Fix 3 - relief in the bottom wall: its outline, seen from the side (sketch)'
C12, S12, T12 = math.cos(math.radians(12.0)), math.sin(math.radians(12.0)), math.tan(math.radians(12.0))
A_IN = -92.0 + 2.5 / C12 + T12 * 11.6
Y_I = lambda z: A_IN + T12 * z
X0, Z0_OLD, Z0, CH_OLD, CH = -27.0, 35.5, 32.0, -123.8, -123.812995
Z_CH = (A_IN - CH) / (1.0 - T12)

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    par = des.userParameters.itemByName('stand_wall_relief_depth')
    vol = lambda: [b for b in comp.bRepBodies if b.name == BODY][0].volume
    sk = [s for s in comp.sketches if s.name == SK3][0]
    M = lambda sp: sk.sketchToModelSpace(sp.geometry)
    S = lambda y, z: sk.modelToSketchSpace(adsk.core.Point3D.create(X0 / 10.0, y / 10.0, z / 10.0))
    if abs(par.value - 0.13) > 1e-9:
        print('*** the relief depth is not 1.3 mm - set it back first'); return
    lines = [l for l in sk.sketchCurves.sketchLines]
    guides = [l for l in lines if l.isConstruction]; solid = [l for l in lines if not l.isConstruction]
    yz = lambda sp: (M(sp).y * 10, M(sp).z * 10)
    near = lambda a, b: abs(a[0] - b[0]) < 1e-4 and abs(a[1] - b[1]) < 1e-4
    seat = [l for l in guides if near(yz(l.startSketchPoint), (44.0 + CH_OLD, 44.0))]
    w0 = (Y_I(Z0_OLD), Z0_OLD)
    square = [l for l in guides if near(yz(l.startSketchPoint), (w0[0] + C12, w0[1] - S12))]
    p1 = [l.startSketchPoint for l in solid if near(yz(l.startSketchPoint), (w0[0] + 0.5, Z0_OLD))]
    zc_old = (A_IN - CH_OLD) / (1.0 - T12)
    p4 = [l.endSketchPoint for l in solid if near(yz(l.endSketchPoint), (zc_old + 0.5 + CH_OLD, zc_old + 0.5))]
    print('found: 45 degree guide %d, foot guide %d, corner p1 %d, corner p4 %d (each must be at least 1); body before %.6f cm3 (must be 118.067923)' % (len(seat), len(square), len(p1), len(p4), vol()))
    if not (seat and square and p1 and p4):
        cur = [yz(l.startSketchPoint) + yz(l.endSketchPoint) for l in lines]
        print('*** the sketch is not in the state this script expects (already moved?) - nothing done. Lines now:', [tuple(round(v, 4) for v in c) for c in cur]); return
    seat, square, p1, p4 = seat[0], square[0], p1[0], p4[0]
    w1 = (Y_I(Z0), Z0)
    jobs = [(seat.startSketchPoint, (44.0 + CH, 44.0)), (seat.endSketchPoint, (49.0 + CH, 49.0)),
            (square.startSketchPoint, (w1[0] + C12, w1[1] - S12)), (square.endSketchPoint, (w1[0] - 3.0 * C12, w1[1] + 3.0 * S12)),
            (p1, (w1[0] + 0.5, Z0)), (p4, (Z_CH + 0.5 + CH, Z_CH + 0.5))]
    # the floor's two corners are TIED (not fixed): p2 lies on the foot's guide line, p3 on the 45 degree guide line. They are
    # put at their new places as well, so that nothing is left for the sketch solver to find when the sketch computes again.
    zf_old = (A_IN - 1.3 / C12 - CH_OLD) / (1.0 - T12); zf = (A_IN - 1.3 / C12 - CH) / (1.0 - T12)
    p2 = [l.endSketchPoint for l in solid if near(yz(l.endSketchPoint), (w0[0] - 1.3 * C12, Z0_OLD + 1.3 * S12))]
    p3 = [l.endSketchPoint for l in solid if near(yz(l.endSketchPoint), (zf_old + CH_OLD, zf_old))]
    print('tied corners found: p2 %d, p3 %d (each must be at least 1)' % (len(p2), len(p3)))
    if not (p2 and p3):
        print('*** the floor is not where this script expects it - nothing done'); return
    tied = [(p2[0], (w1[0] - 1.3 * C12, Z0 + 1.3 * S12)), (p3[0], (zf + CH, zf))]
    sk.isComputeDeferred = True
    for l in (seat, square):
        l.isFixed = False
    for sp, _ in jobs:
        sp.isFixed = False
    moved = []
    for sp, (y, z) in jobs + tied:
        t = S(y, z); c = sp.geometry
        T = adsk.core.Matrix3D.create(); T.translation = adsk.core.Vector3D.create(t.x - c.x, t.y - c.y, 0)
        col = adsk.core.ObjectCollection.create(); col.add(sp)
        moved.append(sk.move(col, T))
    print('points moved (6 fixed, then the 2 tied ones):', moved)
    for sp, _ in jobs:
        sp.isFixed = True
    for l in (seat, square):
        l.isFixed = True
    sk.isComputeDeferred = False
    adsk.doEvents()
    lines = [l for l in sk.sketchCurves.sketchLines if not l.isConstruction]
    want = {'p1 (in the cavity, at the foot)': (w1[0] + 0.5, Z0), 'p2 (floor, at the foot)': (w1[0] - 1.3 * C12, Z0 + 1.3 * S12),
            'p3 (floor meets the 45 degree face)': ((A_IN - 1.3 / C12 - CH) / (1.0 - T12) + CH, (A_IN - 1.3 / C12 - CH) / (1.0 - T12)), 'p4 (on the 45 degree face)': (Z_CH + 0.5 + CH, Z_CH + 0.5)}
    have = [yz(l.startSketchPoint) for l in lines]
    worst = 0.0
    for nm, w in want.items():
        d = min(math.hypot(h[0] - w[0], h[1] - w[1]) for h in have); worst = max(worst, d)
        print('   %-38s wanted (%.4f, %.4f): nearest corner of the outline is %.6f mm away' % (nm, w[0], w[1], d))
    feats = [f for f in comp.features.extrudeFeatures if f.name.startswith('Fix 3')]
    print('sketch fully tied down: %s; profiles %d; corners off by %.6f mm at most; health of the Fix 3 cuts %s' % (sk.isFullyConstrained, sk.profiles.count, worst, [f.healthState for f in feats]))
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    print('body now %.6f cm3 (trial in the cloud: 117.640554); bodies %d; faces %d; steps not healthy: %s' % (
        body.volume, comp.bRepBodies.count, body.faces.count, [des.timeline.item(i).name for i in range(des.timeline.count) if not des.timeline.item(i).isGroup and des.timeline.item(i).healthState != 0]))
