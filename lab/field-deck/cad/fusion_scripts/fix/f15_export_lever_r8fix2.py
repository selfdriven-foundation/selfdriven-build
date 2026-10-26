# MK-I r8 draft - READ-ONLY for the design: Fusion writes the power lever (f12 + f12e + f14: the wider tip side) as STEP for
# the read-back in the cloud (mk1_lever_r8fix2_check.py). Changes nothing; does not save.
import adsk.core, adsk.fusion, os

DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
STEP = 'MK1_r8fix2_power_lever_fusion_readback_NOT-FOR-PRINT.step'
COMP = 'Power lever r8 - tip set to the true switch place (built in Fusion)'

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    item = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    comp = [o for o in item.occurrences if o.component.name == COMP][0].component
    par = des.userParameters.itemByName('button_lever_gap')
    bodies = [(b.name, round(b.volume * 1000, 4), b.faces.count) for b in comp.bRepBodies]
    bb = comp.bRepBodies.item(0).boundingBox
    print('bodies %s | lowest y %.3f | %s = %s | modified %s' % (bodies, bb.minPoint.y * 10, par.name, par.expression, app.activeDocument.isModified))
    if len(bodies) != 1 or abs(par.value - 0.1) > 1e-9:
        print('*** not exported: one body and a gap of 1 mm expected'); return
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, comp)), os.path.getsize(DIR + STEP))
