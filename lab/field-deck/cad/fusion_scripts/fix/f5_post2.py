# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07). f5: FIX 5 - screw post 2 of the speaker cover moves
# 4.4 mm toward the side without the handle, with the top opening's edge (from x -6.6 to x -11.0), so that the cover that
# goes on it later ends short of HDMI 0's plug. Not a new step: the post's place in the sketch "Sound 1" is now the named
# number sound_post2_x (it was the plain number 6.60 mm). Tried first in the cloud: the body's volume changes by -2.39 mm3
# (the post stands on a different piece of the armour's pattern).
import adsk.core, adsk.fusion

BODY = 'Body (copy of r7) + sound posts + slot'
SK = 'Sound 1 - posts and their screw holes (sketch)'

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    par = des.userParameters.itemByName('sound_post2_x')
    sk = [s for s in comp.sketches if s.name == SK][0]
    dims = [d for d in sk.sketchDimensions if abs(d.parameter.value - 0.66) < 1e-9 or d.parameter.expression == 'sound_post2_x']
    print('dimensions that place post 2 across:', [(d.parameter.name, d.parameter.expression) for d in dims])
    if not par or len(dims) != 1:
        print('*** not exactly one such dimension, or the named number is missing - stopped'); return
    d = dims[0]
    if d.parameter.expression == 'sound_post2_x':
        print('ALREADY DONE')
    else:
        v0 = [b for b in comp.bRepBodies if b.name == BODY][0].volume
        d.parameter.expression = 'sound_post2_x'
        adsk.doEvents()
        v1 = [b for b in comp.bRepBodies if b.name == BODY][0].volume
        print('post 2: %s is now %s = %.2f mm; body volume change %.3f mm3 (trial in the cloud: -2.39)' % (d.parameter.name, d.parameter.expression, d.parameter.value * 10, (v1 - v0) * 1000.0))
    for c in sk.sketchCurves.sketchCircles:
        m = sk.sketchToModelSpace(c.centerSketchPoint.geometry)
        print('   circle %.2f mm round at (%.3f, %.3f) mm' % (c.radius * 20, m.x * 10, m.y * 10))
    body = [b for b in comp.bRepBodies if b.name == BODY][0]
    pc = lambda x, y, z: body.pointContainment(adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0))
    print('in the body (0 = inside, 2 = outside): post 2 new place, in its wall (-11.0+2.4, 66.1, 10): %d; in its screw hole (-11.0, 66.1, 10): %d; old place, far side (-4.0, 66.1, 10): %d' % (
        pc(-8.6, 66.1, 10.0), pc(-11.0, 66.1, 10.0), pc(-4.0, 66.1, 10.0)))
    bad = [(t.name, t.healthState) for t in [des.timeline.item(i).entity for i in range(des.timeline.count)] if hasattr(t, 'healthState') and t.healthState != 0]
    print('body volume now %.6f cm3 (trial: 118.045785); bodies %d; faces %d; timeline %d steps; steps that are not healthy: %s' % (
        body.volume, comp.bRepBodies.count, body.faces.count, des.timeline.count, bad))
