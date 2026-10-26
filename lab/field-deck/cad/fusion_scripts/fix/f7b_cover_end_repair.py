# MK-I r8 draft - f7b: REPAIR of f7a (2026-10-07). f7a moved the cover's end, but the four lines of the screw well stayed
# where they were: their eight end points were fixed one by one (the other lines' corners were not), and a fixed point
# does not move. Result: cover 10227.394 mm3 instead of 11190.095, and the step "Cover 10" lost its body.
# This moves those eight points the same 4.4 mm and gives "Cover 10" its body back if it still has none.
import adsk.core, adsk.fusion

WANT_PTS = [(-11.7, 70.0), (-11.7, 61.0), (-11.7, 61.0), (-2.7, 61.0), (-10.5, 70.0), (-10.5, 62.2), (-10.5, 62.2), (-2.7, 62.2)]

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    cov = [o for o in comp.occurrences if o.component.name.startswith('Speaker cover (PROVISIONAL')][0].component
    sk = [s for s in cov.sketches if s.name.startswith('Cover 1 ')][0]
    print('cover before the repair: %.3f mm3' % (cov.bRepBodies.item(0).volume * 1000))
    pts = [p for p in sk.sketchPoints if p != sk.originPoint and p.isFixed]
    have = sorted((round(sk.sketchToModelSpace(p.geometry).x * 10, 2), round(sk.sketchToModelSpace(p.geometry).y * 10, 2)) for p in pts)
    if have != sorted(WANT_PTS):
        print('*** the eight fixed points are not where this repair expects them - nothing done:', have); return
    lines = [l for l in sk.sketchCurves.sketchLines if l.startSketchPoint in pts or l.endSketchPoint in pts]
    print('lines to move: %d (must be 4); points: %d' % (len(lines), len(pts)))
    if len(lines) != 4:
        print('*** nothing done'); return
    sk.isComputeDeferred = True
    for l in lines:
        l.isFixed = False
    col = adsk.core.ObjectCollection.create()
    for p in pts:
        p.isFixed = False
        col.add(p)
    T = adsk.core.Matrix3D.create(); T.translation = adsk.core.Vector3D.create(-0.44, 0, 0)
    ok = sk.move(col, T)
    for p in pts:
        p.isFixed = True
    for l in lines:
        l.isFixed = True
    sk.isComputeDeferred = False
    adsk.doEvents()
    print('moved: %s; the sketch now has %d profiles (must be 4):' % (ok, sk.profiles.count))
    for i in range(sk.profiles.count):
        ap = sk.profiles.item(i).areaProperties()
        print('   %.2f mm2 at (%.2f, %.2f)' % (ap.area * 100, ap.centroid.x * 10, ap.centroid.y * 10))
    f10 = [f for f in cov.features.extrudeFeatures if f.name.startswith('Cover 10')][0]
    print('Cover 10 health now: %d %s' % (f10.healthState, f10.errorOrWarningMessage))
    if f10.healthState != 0:
        f10.timelineObject.rollTo(True)
        f10.participantBodies = [cov.bRepBodies.item(0)]
        des.timeline.moveToEnd()
        adsk.doEvents()
        f10 = [f for f in cov.features.extrudeFeatures if f.name.startswith('Cover 10')][0]
        print('Cover 10 was given the cover again: health %d %s' % (f10.healthState, f10.errorOrWarningMessage))
    body = cov.bRepBodies.item(0); bb = body.boundingBox
    print('cover after the repair: %.3f mm3 (cloud: 11190.095), x %.2f..%.2f; bodies in its component %d; steps not healthy: %s' % (
        body.volume * 1000, bb.minPoint.x * 10, bb.maxPoint.x * 10, cov.bRepBodies.count, [f.name for f in cov.features.extrudeFeatures if f.healthState != 0]))
    print('whole timeline: %d steps, marker at %d; not healthy anywhere: %s' % (des.timeline.count, des.timeline.markerPosition, [des.timeline.item(i).name for i in range(des.timeline.count) if des.timeline.item(i).healthState != 0]))
    print('case body: %.6f cm3 (must be 118.045783)' % comp.bRepBodies.item(0).volume)
