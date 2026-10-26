# MK-I r8 draft - CORRECTIONS OF 2026-10-07. f8 - READ-ONLY for the design: Fusion writes the item as STEP for the read-back
# (case body with the five corrections, the cover with its end moved, the reference bodies) and three of its own pictures.
import adsk.core, adsk.fusion, os

DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
STEP = 'MK1_r8fix_fusion_readback_item_final_NOT-FOR-PRINT.step'
# name, what the camera looks at (case x, y, z mm), where it stands from there (case direction), which way is up (case), width and height of the view (mm), picture size
VIEWS = [('MK1_r8fix_whole_back.png', (30.0, -1.0, 53.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), 300.0, 210.0, 2000, 1400),
         ('MK1_r8fix_top_opening.png', (4.0, 36.6, 28.0), (-0.30, 1.0, 0.55), (0.0, 0.0, 1.0), 84.0, 60.0, 1960, 1400),
         ('MK1_r8fix_side_window.png', (75.7, -12.0, 24.0), (1.0, -0.30, 0.55), (0.0, 0.0, 1.0), 98.0, 70.0, 1960, 1400)]
F = lambda x, y, z: (-x / 10.0, z / 10.0, y / 10.0)          # case (x, y, z) mm -> Fusion (X, Y, Z) cm

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    occ27 = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0]
    comp = occ27.component
    b = comp.bRepBodies.item(0)
    cov = [o for o in comp.occurrences if o.component.name.startswith('Speaker cover (PROVISIONAL')][0].component
    print('case body %.6f cm3, %d faces | cover %.3f mm3 | timeline %d steps | modified %s' % (b.volume, b.faces.count, cov.bRepBodies.item(0).volume * 1000, des.timeline.count, app.activeDocument.isModified))
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, comp)), os.path.getsize(DIR + STEP))
    vp = app.activeViewport
    orig = vp.camera
    for fn, tgt, frm, up, w, h, pw, ph in VIEWS:
        cam = vp.camera
        cam.isSmoothTransition = False
        cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
        t = F(*tgt); d = F(*frm); u = F(*up)
        n = (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) ** 0.5
        cam.target = adsk.core.Point3D.create(*t)
        cam.eye = adsk.core.Point3D.create(t[0] + d[0] / n * 120.0, t[1] + d[1] / n * 120.0, t[2] + d[2] / n * 120.0)
        cam.upVector = adsk.core.Vector3D.create(u[0] * 10, u[1] * 10, u[2] * 10)
        cam.setExtents(w / 10.0, h / 10.0)
        vp.camera = cam; vp.refresh(); adsk.doEvents()
        print(fn, vp.saveAsImageFile(DIR + 'shots/' + fn, pw, ph))
    orig.isSmoothTransition = False
    vp.camera = orig; vp.refresh()
