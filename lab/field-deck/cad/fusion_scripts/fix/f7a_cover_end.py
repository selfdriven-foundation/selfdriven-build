# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07). f7a: the PROVISIONAL speaker cover follows post 2.
# Its end toward the top opening moves 4.4 mm (x -1.5 -> -5.9), with the end wall, the screw well and screw hole 2
# (now at post 2's new place, x -11.0); the grille moves 2.2 mm so that it stays over the middle of the speaker.
# The cover's sketches have no dimensions (fixed lines): the lines are moved, nothing is redrawn, no step is added.
# In the cloud the same cover (mk1_sound_r8.cover() with X_NOTCH -5.6, P2 -11.0) has 11190.095 mm3 (before: 11687.295).
# REVERT = True moves everything back.
import adsk.core, adsk.fusion

REVERT = False
JOBS = [('Cover 1 ', -4.4, lambda x, y: x > -12.0, 12),          # the end wall, the inside's end, the screw well
        ('Cover 9', -4.4, lambda x, y: x > -12.0, 1),            # screw hole 2
        ('Cover 11', -2.2, lambda x, y: True, 44)]               # the 11 slots of the grille (4 corners each)

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    cov = [o for o in comp.occurrences if o.component.name.startswith('Speaker cover (PROVISIONAL')][0].component
    body = cov.bRepBodies.item(0); v0 = body.volume
    bb = body.boundingBox
    print('cover before: %.3f mm3, x %.2f..%.2f mm' % (v0 * 1000, bb.minPoint.x * 10, bb.maxPoint.x * 10))
    if (not REVERT and abs(bb.maxPoint.x * 10 + 1.5) > 1e-6) or (REVERT and abs(bb.maxPoint.x * 10 + 5.9) > 1e-6):
        print('*** the cover is not in the state this script expects - nothing done'); return
    for key, dx, pick, want in JOBS:
        sk = [s for s in cov.sketches if s.name.startswith(key)][0]
        xd = sk.xDirection
        if abs(xd.x - 1.0) > 1e-9:
            print('*** sketch', sk.name, 'is turned against the case - nothing done here'); continue
        if REVERT:
            dx = -dx; shift = -dx
            pick0 = pick; pick = lambda x, y, p=pick0, s=shift: p(x - s, y)      # the points are where the move put them
        curves = [c for c in sk.sketchCurves]
        fixed = [c for c in curves if c.isFixed]
        sk.isComputeDeferred = True
        for c in fixed:
            c.isFixed = False
        col = adsk.core.ObjectCollection.create()
        circles = [c for c in sk.sketchCurves.sketchCircles]
        if circles:
            for c in circles:
                m = sk.sketchToModelSpace(c.centerSketchPoint.geometry)
                if pick(m.x * 10, m.y * 10):
                    col.add(c)
        else:
            for p in sk.sketchPoints:
                if p == sk.originPoint:
                    continue
                m = sk.sketchToModelSpace(p.geometry)
                if pick(m.x * 10, m.y * 10):
                    col.add(p)
        n = col.count
        if n != want:
            print('*** %s: %d things to move, expected %d - left as it was' % (sk.name, n, want))
        else:
            T = adsk.core.Matrix3D.create(); T.translation = adsk.core.Vector3D.create(dx / 10.0, 0, 0)
            ok = sk.move(col, T)
            print('%s: moved %d by %+.1f mm: %s' % (sk.name, n, dx, ok))
        for c in fixed:
            c.isFixed = True
        sk.isComputeDeferred = False
    adsk.doEvents()
    body = cov.bRepBodies.item(0); bb = body.boundingBox
    print('cover after: %.3f mm3 (cloud: 11190.095 moved, 11687.295 as it was), x %.2f..%.2f, y %.2f..%.2f, z %.2f..%.2f; bodies %d' % (
        body.volume * 1000, bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10, cov.bRepBodies.count))
    for f in cov.features.extrudeFeatures:
        if f.healthState != 0:
            print('   NOT HEALTHY:', f.name, f.healthState, f.errorOrWarningMessage)
    print('cover steps not healthy: %d of %d' % (len([f for f in cov.features.extrudeFeatures if f.healthState != 0]), cov.features.extrudeFeatures.count))
    main = comp.bRepBodies.item(0)
    print('case body untouched: %.6f cm3 (must be 118.045783)' % main.volume)
