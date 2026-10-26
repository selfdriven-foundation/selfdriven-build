# v2 - changes nothing in the design (v1's r7 pictures missed: r7's body sits in a child occurrence with its own transform): Fusion's own pictures of the TOP OPENING's side edge (correction 1, x -5.6) on the r8 body,
# and the same spot on r7's body (edge at x -1.2), for the owner's look-and-decide (the cosmetic point of correction 1).
# For each picture only that body is shown; everything else is hidden for a moment and set back exactly as it was.
import adsk.core, adsk.fusion, os
DIR = '/path/to/Field Deck/7 - Next Case/mk1/shots/'
R8, R7 = 'BUILT IN FUSION', 'design r7 (power lever):1'
R7_BODY = 'Body (armoured, open back, window for the power lever)'
# (name, case x, y, z of the middle, look FROM (case axes), up (case axes), width, height mm, pixels)
VIEWS = [('slant', (-6.0, 40.0, 30.0), (-0.45, 0.75, 0.48), (0, 0, 1), 70.0, 52.0, 1600, 1200),
         ('close', (-5.0, 40.0, 30.0), (-0.45, 0.75, 0.48), (0, 0, 1), 36.0, 27.0, 1600, 1200)]


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    root = des.rootComponent
    r8 = [o for o in root.occurrences if R8 in o.component.name][0]
    r7 = [o for o in root.occurrences if R7 in o.name][0]
    print('modified before %s' % app.activeDocument.isModified)
    saved = [(o, o.isLightBulbOn) for o in root.occurrences] + [(o, o.isLightBulbOn) for o in r8.component.occurrences] + \
            [(o, o.isLightBulbOn) for o in r7.component.occurrences]
    bodies = [(b, b.isLightBulbOn) for b in r8.component.bRepBodies]
    vp = app.activeViewport
    orig = vp.camera
    try:
        for tag, item, keep in (('r8', r8, None), ('r7', r7, R7_BODY)):
            for o in root.occurrences:
                o.isLightBulbOn = (o == item)
            for o in item.component.occurrences:
                o.isLightBulbOn = (keep is not None and o.component.name.startswith(keep))
            for b, was in bodies:
                b.isLightBulbOn = (tag == 'r8')
            adsk.doEvents()
            m = item.transform2
            if keep is not None:                                   # the body is a child occurrence: its transform, then the item's
                ch = [o for o in item.component.occurrences if o.component.name.startswith(keep)][0]
                m = ch.transform2.copy(); m.transformBy(item.transform2)
            for nm, (x, y, z), d, up, w, h, pw, ph in VIEWS:
                n = sum(c * c for c in d) ** 0.5
                t = adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0); t.transformBy(m)
                e = adsk.core.Point3D.create((x + 1200 * d[0] / n) / 10.0, (y + 1200 * d[1] / n) / 10.0, (z + 1200 * d[2] / n) / 10.0); e.transformBy(m)
                k = sum(a * b for a, b in zip(up, d)) / n
                u = adsk.core.Vector3D.create(up[0] - k * d[0] / n, up[1] - k * d[1] / n, up[2] - k * d[2] / n); u.transformBy(m)
                cam = vp.camera
                cam.isSmoothTransition = False
                cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
                cam.target = t; cam.eye = e; cam.upVector = u
                cam.setExtents(w / 10.0, h / 10.0)
                vp.camera = cam; vp.refresh(); adsk.doEvents()
                fn = 'MK1_top_opening_edge_v2_%s_%s.png' % (tag, nm)
                print(fn, vp.saveAsImageFile(DIR + fn, pw, ph))
    finally:
        for o, was in saved:
            o.isLightBulbOn = was
        for b, was in bodies:
            b.isLightBulbOn = was
        orig.isSmoothTransition = False
        vp.camera = orig; vp.refresh()
        print('shown again as before: %s %s | modified %s' % (all(o.isLightBulbOn == was for o, was in saved), all(b.isLightBulbOn == was for b, was in bodies), app.activeDocument.isModified))
