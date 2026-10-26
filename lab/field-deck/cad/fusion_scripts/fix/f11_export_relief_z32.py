# MK-I r8 draft - CORRECTIONS OF 2026-10-07 / 08. f11 - READ-ONLY for the design: Fusion writes the item as STEP for the
# read-back, after f10 (the relief in the bottom wall from z 32.0). Nothing in the design is changed by this script.
import adsk.core, adsk.fusion, os

DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
STEP = 'MK1_r8fix_fusion_readback_item_relief-z32_NOT-FOR-PRINT.step'
BODY = 'Body (copy of r7) + sound posts + slot'

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    b = [x for x in comp.bRepBodies if x.name == BODY][0]
    cov = [o for o in comp.occurrences if o.component.name.startswith('Speaker cover (PROVISIONAL')][0].component
    bad = [des.timeline.item(i).name for i in range(des.timeline.count) if not des.timeline.item(i).isGroup and des.timeline.item(i).healthState != 0]
    print('case body %.6f cm3, %d faces | cover %.3f mm3 | timeline %d steps, not healthy: %s | modified %s | offline %s' % (
        b.volume, b.faces.count, cov.bRepBodies.item(0).volume * 1000, des.timeline.count, bad, app.activeDocument.isModified, app.isOffLine))
    for n in ('top_opening_extra', 'side_window_extra', 'stand_wall_relief_depth', 'sound_post2_x'):
        p = des.userParameters.itemByName(n)
        print('   %-26s %s' % (n, p.expression))
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, comp)), os.path.getsize(DIR + STEP))
