# MK-I r8 draft - CORRECTIONS FOR THE STACK'S REAL PLACE (2026-10-07). f6: REFERENCE BODIES, not parts of the case -
# the boards, posts, sockets and the power switch WHERE THEY REALLY ARE (Raspberry Pi's drawing of the display + the
# owner's photo IMG_1856; calcheck/mk1_stack_true.py, stack "by the drawing": top not leaning, battery board's back at
# z 38.9). The old reference bodies stand where the September caliper sheet had them (2.6 .. 4.4 mm off): they are
# switched OFF (not removed). r7's lever and its screw are switched off too: the lever is remade to a reading.
# Sizes of sockets are the usual ones for these parts, not measured. All numbers: case frame, mm.
import adsk.core, adsk.fusion

NAME = 'Stack where it REALLY is (reference - Raspberry Pi drawing + photo, 2026-10-07)'
P3, V3 = adsk.core.Point3D.create, adsk.core.Vector3D.create
# name, (x0, x1, y0, y1, z0, z1), whose look to copy
BOXES = [('Battery board X1201 (85 x 106.6 x 1.6)', (-23.70, 61.30, -78.76, 27.84, 37.3, 38.9), 'Electronics'),
         ('Raspberry Pi 5 board (85 x 56 x 1.4), its parts face the screen', (-23.71, 61.29, -28.0, 28.0, 30.9, 32.3), 'Electronics'),
         ('Network socket (16 wide)', (43.3, 64.3, 9.8, 25.8, 17.4, 30.9), 'Top sockets'),
         ('USB pair, upper (blue)', (46.8, 64.3, -7.7, 5.5, 15.3, 30.9), 'Top sockets'),
         ('USB pair, lower (black)', (46.8, 64.3, -25.6, -12.4, 15.3, 30.9), 'Top sockets'),
         ("Pi's own power socket USB-C (stays shut)", (-16.98, -8.04, 21.7, 29.0, 27.7, 30.9), 'Top sockets'),
         ('HDMI 0', (-0.96, 5.54, 22.3, 29.8, 27.9, 30.9), 'Top sockets'),
         ('HDMI 1', (12.54, 19.04, 22.3, 29.8, 27.9, 30.9), 'Top sockets'),
         ('Charge socket USB-C (on the battery board)', (23.62, 32.56, 21.5, 28.84, 34.1, 37.3), 'Top sockets'),
         ('Power switch (on the battery board)', (-23.70, -16.50, -71.56, -64.36, 30.3, 37.3), 'UPS power switch (')]
# name, (x, y, z) of one end, of the other end, radius, whose look to copy
CYLS = [('Brass post 1 (6 tall)', (-20.10, -75.26, 38.9), (-20.10, -75.26, 44.9), 2.6, 'UPS brass posts'),
        ('Brass post 2 (6 tall)', (37.90, -75.26, 38.9), (37.90, -75.26, 44.9), 2.6, 'UPS brass posts'),
        ("Power switch's plunger (3.5 round): the button to press", (-27.60, -67.96, 33.6), (-23.70, -67.96, 33.6), 1.75, 'UPS power switch plunger')]
OFF = ['Electronics (reference, estimated)', 'UPS brass posts 2x (reference, estimated)', 'Top sockets (reference)',
       'UPS power switch (reference, estimated)', 'UPS power switch plunger (reference, estimated)',
       'Power lever (printed, goes in last from outside)', 'Power lever screw 1x M3x8']

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    if [o for o in comp.occurrences if o.component.name == NAME]:
        print('ALREADY THERE'); return
    look = {}
    for o in comp.occurrences:
        if o.component.bRepBodies.count:
            look[o.component.name] = o.component.bRepBodies.item(0).appearance
    tbm = adsk.fusion.TemporaryBRepManager.get()
    made = []
    for name, (x0, x1, y0, y1, z0, z1), like in BOXES:
        obb = adsk.core.OrientedBoundingBox3D.create(P3((x0 + x1) / 20.0, (y0 + y1) / 20.0, (z0 + z1) / 20.0), V3(1, 0, 0), V3(0, 1, 0),
                                                     (x1 - x0) / 10.0, (y1 - y0) / 10.0, (z1 - z0) / 10.0)
        made.append((name, tbm.createBox(obb), like))
    for name, a, b, r, like in CYLS:
        made.append((name, tbm.createCylinderOrCone(P3(a[0] / 10.0, a[1] / 10.0, a[2] / 10.0), r / 10.0, P3(b[0] / 10.0, b[1] / 10.0, b[2] / 10.0), r / 10.0), like))
    occ = comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    c2 = occ.component; c2.name = NAME
    bf = c2.features.baseFeatures.add()
    bf.startEdit()
    for name, tmp, like in made:
        c2.bRepBodies.add(tmp, bf)
    bf.finishEdit()
    bf.name = 'Reference bodies at the real places (boxes and bars, not parts)'
    for (name, tmp, like), b in zip(made, c2.bRepBodies):
        b.name = name
        for k, ap in look.items():
            if k.startswith(like) and ap:
                try:
                    b.appearance = ap
                except:
                    pass
        bb = b.boundingBox
        print('   %-62s x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f' % (name[:62], bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10))
    n = 0
    for o in comp.occurrences:
        if any(o.component.name.startswith(k) for k in OFF) and o.isLightBulbOn:
            o.isLightBulbOn = False; n += 1; print('   switched off:', o.name)
    print('reference component made: %d bodies; %d old ones switched off; timeline %d steps' % (c2.bRepBodies.count, n, des.timeline.count))
