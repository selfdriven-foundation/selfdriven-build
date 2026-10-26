# v2 - after v1, changes nothing in the design: the r8 item as STEP for the read-back, and Fusion's own pictures of the new
# body - the handle side square on (the deck standing), the side window's lintel and the top opening's lintel seen from inside,
# from below. For the pictures every occurrence in the r8 item (front, plate, handle, electronics ...) is hidden for a moment
# and then set back exactly as it was (only what is shown changes; nothing in the design). It never saves.
import adsk.core, adsk.fusion, os
DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
ITEM = 'BUILT IN FUSION'
BODY_PREFIX = 'Body (copy of r7)'
SK1 = 'Vents - three slots in the handle-side wall (sketch at z 38.0)'
STEP = 'MK1_r8_vents_fusion_readback_item_NOT-FOR-PRINT.step'
# (file, case x, y, z of the middle, the direction the camera looks FROM (case axes), the picture's up (case axes, made square
# to the line of sight), width, height in mm, pixels)
VIEWS = [('MK1_r8_vents_handle_side.png', (75.0, -23.0, 26.5), (1, 0, 0), (0, 1, 0), 72.0, 130.0, 1108, 2000),
         ('MK1_r8_vents_side_window_lintel_from_inside.png', (74.45, 0.0, 38.6), (-0.6, 0, -0.8), (0, 0, 1), 80.0, 36.0, 2000, 900),
         ('MK1_r8_vents_top_opening_lintel_from_inside.png', (20.0, 34.0, 46.6), (0, -0.5, -0.866), (0, 0, 1), 70.0, 32.0, 2000, 914)]


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    item_occ = [o for o in des.rootComponent.occurrences if ITEM in o.component.name][0]
    item = item_occ.component
    if not [s for s in item.sketches if s.name == SK1]:
        print('STOPPED: v1 has not run (no sketch %r)' % SK1); return
    b = [x for x in item.bRepBodies if x.name.startswith(BODY_PREFIX)][0]
    print('body %r %.6f cm3, %d faces | modified %s' % (b.name, b.volume, b.faces.count, app.activeDocument.isModified))
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, item)), os.path.getsize(DIR + STEP))
    vp = app.activeViewport
    orig = vp.camera
    shown = [(o, o.isLightBulbOn) for o in item.occurrences]
    try:
        for o, was in shown:
            o.isLightBulbOn = False
        adsk.doEvents()
        mid = item_occ.transform2
        for fn, (x, y, z), d, up, w, h, pw, ph in VIEWS:
            n = sum(c * c for c in d) ** 0.5
            dn = [c / n for c in d]
            t = adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0); t.transformBy(mid)
            e = adsk.core.Point3D.create((x + 1200.0 * dn[0]) / 10.0, (y + 1200.0 * dn[1]) / 10.0, (z + 1200.0 * dn[2]) / 10.0); e.transformBy(mid)
            k = sum(a * c for a, c in zip(up, dn))
            u = adsk.core.Vector3D.create(up[0] - k * dn[0], up[1] - k * dn[1], up[2] - k * dn[2]); u.transformBy(mid)
            cam = vp.camera
            cam.isSmoothTransition = False
            cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
            cam.target = t; cam.eye = e; cam.upVector = u
            cam.setExtents(w / 10.0, h / 10.0)
            vp.camera = cam; vp.refresh(); adsk.doEvents()
            print(fn, vp.saveAsImageFile(DIR + 'shots/' + fn, pw, ph))
    finally:
        for o, was in shown:
            o.isLightBulbOn = was
        orig.isSmoothTransition = False
        vp.camera = orig; vp.refresh()
        print('shown again as before: %s' % all(o.isLightBulbOn == was for o, was in shown))
