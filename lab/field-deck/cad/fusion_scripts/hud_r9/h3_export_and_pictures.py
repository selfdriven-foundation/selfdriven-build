# h3 - after h1 and h2, changes nothing in the design: the r8 item as STEP for the read-back, and Fusion's own pictures of the
# new HUD - the window square on (the body alone), and the pod's back square on with the new cap on it. For the pictures every
# other occurrence in the r8 item is hidden for a moment and then set back exactly as it was (only what is shown changes;
# nothing in the design). It never saves.
import adsk.core, adsk.fusion, os, math
DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
ITEM = 'BUILT IN FUSION'
BODY_PREFIX = 'Body (copy of r7)'
CAP_COMP = 'HUD cap r9 - for the real OLED (built in Fusion)'
STEP = 'MK1_r9_hud_fusion_readback_item_NOT-FOR-PRINT.step'
C48, S48 = math.cos(math.radians(48.0)), math.sin(math.radians(48.0))
FDIR, FIN = (0.0, C48, S48), (0.0, -S48, C48)        # along the facet (up the screen), into the pod (case axes)


def facet_pt(x, a, d):
    return (x, 71.5 + C48 * a - S48 * d, S48 * a + C48 * d)


# (file, case point in the middle, the direction the camera looks FROM (case axes), the picture's up (case axes), width,
# height in mm, pixels, show the new cap)
VIEWS = [('MK1_r9_hud_window_fusion.png', facet_pt(76.5, 17.0, 0.0), tuple(-c for c in FIN), FDIR, 52.0, 58.0, 1400, 1562, False),
         ('MK1_r9_hud_back_with_cap_fusion.png', facet_pt(76.5, 14.0, 36.0), FIN, FDIR, 52.0, 62.0, 1400, 1669, True)]


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    item_occ = [o for o in des.rootComponent.occurrences if ITEM in o.component.name][0]
    item = item_occ.component
    caps = [o for o in item.occurrences if o.component.name == CAP_COMP]
    if len(caps) != 1:
        print('STOPPED: h2 has not run (no %r)' % CAP_COMP); return
    b = [x for x in item.bRepBodies if x.name.startswith(BODY_PREFIX)][0]
    print('body %r %.6f cm3, %d faces | new cap %.4f mm3 | modified %s' % (b.name, b.volume, b.faces.count, caps[0].component.bRepBodies.item(0).volume * 1000,
                                                                          app.activeDocument.isModified))
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, item)), os.path.getsize(DIR + STEP))
    vp = app.activeViewport
    orig = vp.camera
    shown = [(o, o.isLightBulbOn) for o in item.occurrences]
    try:
        mid = item_occ.transform2
        for fn, (x, y, z), d, up, w, h, pw, ph, cap in VIEWS:
            for o, was in shown:
                o.isLightBulbOn = bool(cap and o.component.name == CAP_COMP)
            adsk.doEvents()
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
        print('shown again as before: %s | modified %s' % (all(o.isLightBulbOn == was for o, was in shown), app.activeDocument.isModified))
