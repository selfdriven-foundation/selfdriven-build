# MK-I r8 draft - f7c (2026-10-07): the two REFERENCE things that belong to the provisional speaker cover follow it.
#  - the reference speaker (maker's size, not measured) moves 2.2 mm, to the middle of the shorter cover: one Move step
#    in its own component;
#  - the cover's two screws: the old pair is a copy shared with the earlier draft item, so it is switched OFF here (not
#    changed) and a new pair of plain reference screws is put in: screw 1 where it was, screw 2 on post 2's new place.
import adsk.core, adsk.fusion

NAME = 'Speaker cover screws 2x M3x8 (reference; screw 2 at the new place of post 2)'
P3 = adsk.core.Point3D.create
SCREWS = [(-98.0, 40.3), (-11.0, 66.1)]           # post 1, post 2 (case mm)
Z_SEAT, HEAD_H, HEAD_D, LEN = 16.0, 2.2, 5.6, 8.0   # the heads lie on the cover's lugs (z 16)

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    VI = adsk.core.ValueInput.createByString
    # ---- the reference speaker
    spk = [o for o in comp.occurrences if o.component.name.startswith('Speaker (reference')][0].component
    b = spk.bRepBodies.item(0); bb = b.boundingBox
    print('reference speaker before: x %.2f..%.2f' % (bb.minPoint.x * 10, bb.maxPoint.x * 10))
    if abs(bb.minPoint.x * 10 + 86.6) < 1e-6:
        col = adsk.core.ObjectCollection.create(); col.add(b)
        mi = spk.features.moveFeatures.createInput2(col)
        mi.defineAsTranslateXYZ(VI('-2.2 mm'), VI('0 mm'), VI('0 mm'), False)
        mv = spk.features.moveFeatures.add(mi)
        mv.name = 'Speaker to the middle of the shorter cover (2.2 mm toward the side without the handle)'
        bb = spk.bRepBodies.item(0).boundingBox
        print('reference speaker after: x %.2f..%.2f (wanted -88.80..-18.80), y %.2f..%.2f, z %.2f..%.2f; health %d' % (
            bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10, mv.healthState))
    else:
        print('   not at its old place - left alone')
    # ---- the screws
    if [o for o in comp.occurrences if o.component.name == NAME]:
        print('new screws ALREADY THERE'); return
    old = [o for o in comp.occurrences if o.component.name.startswith('Speaker cover screws 2x M3x8') ]
    look = old[0].component.bRepBodies.item(0).appearance if old else None
    tbm = adsk.fusion.TemporaryBRepManager.get()
    made = []
    for x, y in SCREWS:
        head = tbm.createCylinderOrCone(P3(x / 10.0, y / 10.0, Z_SEAT / 10.0), HEAD_D / 20.0, P3(x / 10.0, y / 10.0, (Z_SEAT + HEAD_H) / 10.0), HEAD_D / 20.0)
        shank = tbm.createCylinderOrCone(P3(x / 10.0, y / 10.0, (Z_SEAT - LEN) / 10.0), 0.15, P3(x / 10.0, y / 10.0, Z_SEAT / 10.0), 0.15)
        tbm.booleanOperation(head, shank, adsk.fusion.BooleanTypes.UnionBooleanType)
        made.append(head)
    occ = comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    c2 = occ.component; c2.name = NAME
    bf = c2.features.baseFeatures.add()
    bf.startEdit()
    for t in made:
        c2.bRepBodies.add(t, bf)
    bf.finishEdit()
    bf.name = 'Two reference screws (not parts)'
    for k, q in enumerate(c2.bRepBodies):
        q.name = 'Screw %d (M3x8)' % (k + 1)
        if look:
            try:
                q.appearance = look
            except:
                pass
        bb = q.boundingBox
        print('   %s: x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f, %.2f mm3' % (q.name, bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10, q.volume * 1000))
    for o in old:
        o.isLightBulbOn = False; print('   switched off:', o.name)
    print('timeline %d steps; not healthy steps: %s' % (des.timeline.count, [des.timeline.item(i).name for i in range(des.timeline.count) if not des.timeline.item(i).isGroup and des.timeline.item(i).healthState != 0]))
