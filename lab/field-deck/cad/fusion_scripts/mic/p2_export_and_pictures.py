# p2 - after p1, changes nothing in the design: the new front (mic pocket) as STEP for the read-back, and Fusion's own pictures - the chin from the
# front (the three marks and the pinhole) and the pocket from behind (square on, and at a slant). For the pictures from behind
# everything else in the r8 item (the other occurrences and the item's own body) is hidden for a moment and then set back exactly
# as it was (only what is shown changes; nothing in the design).
import adsk.core, adsk.fusion, os
DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
COMP_NAME = 'Front r8 - mic pocket (built in Fusion)'
STEP = 'MK1_r8_front_micpocket_fusion_readback_NOT-FOR-PRINT.step'
# (file, case x, y, z of the middle, the direction the camera looks FROM (case axes), width, height in mm, pixels, from the front?)
VIEWS = [('MK1_r8_micpocket_chin_from_front.png', (0.0, -76.0, -11.6), (0, 0, -1), 130.0, 34.0, 2600, 680, True),
         ('MK1_r8_micpocket_close_from_front.png', (0.0, -75.0, -11.6), (0, 0, -1), 24.0, 16.0, 1500, 1000, True),
         ('MK1_r8_micpocket_from_behind.png', (0.0, -75.0, 0.0), (0, 0, 1), 30.0, 20.0, 1500, 1000, False),
         ('MK1_r8_micpocket_slant_from_behind.png', (0.0, -75.0, -5.0), (-0.40, -0.50, 0.77), 34.0, 24.0, 1700, 1200, False)]


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    item_occ = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0]
    item = item_occ.component
    mine = [o for o in item.occurrences if o.component.name == COMP_NAME]
    if len(mine) != 1:
        print('STOPPED: %d components named %s' % (len(mine), COMP_NAME)); return
    comp = mine[0].component
    b = comp.bRepBodies.item(0)
    p = des.userParameters.itemByName('mic_bore_dia')
    print('mic_bore_dia %s | %r %.6f cm3, %d faces | modified %s' % (p.expression, b.name, b.volume, b.faces.count, app.activeDocument.isModified))
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, comp)), os.path.getsize(DIR + STEP))
    vp = app.activeViewport
    orig = vp.camera
    shown = [(o, o.isLightBulbOn) for o in item.occurrences]
    own = [(bb, bb.isLightBulbOn) for bb in item.bRepBodies]
    try:
        for fn, (x, y, z), d, w, h, pw, ph, front in VIEWS:
            for o, was in shown:
                o.isLightBulbOn = was if front else (o.component.name == COMP_NAME)
            for bb, was in own:
                bb.isLightBulbOn = was if front else False
            adsk.doEvents()
            mid = item_occ.transform2
            n = sum(c * c for c in d) ** 0.5
            t = adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0); t.transformBy(mid)
            e = adsk.core.Point3D.create((x + 1200.0 * d[0] / n) / 10.0, (y + 1200.0 * d[1] / n) / 10.0, (z + 1200.0 * d[2] / n) / 10.0); e.transformBy(mid)
            k = d[1] / n                                       # case +y, made square to the line of sight
            u = adsk.core.Vector3D.create(-k * d[0] / n, 1.0 - k * d[1] / n, -k * d[2] / n); u.transformBy(mid)
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
        for bb, was in own:
            bb.isLightBulbOn = was
        orig.isSmoothTransition = False
        vp.camera = orig; vp.refresh()
        print('shown again as before: occurrences %s, the item body %s' % (all(o.isLightBulbOn == was for o, was in shown), all(bb.isLightBulbOn == was for bb, was in own)))
