# MK-I r8 draft - READ-ONLY for the design: Fusion writes the power lever (f12 + f12e) as STEP for the read-back in the cloud.
import adsk.core, adsk.fusion, os

DIR = '/path/to/Field Deck/7 - Next Case/mk1/'
STEP = 'MK1_r8fix_power_lever_fusion_readback_NOT-FOR-PRINT.step'
COMP = 'Power lever r8 - tip set to the true switch place (built in Fusion)'

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    item = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    comp = [o for o in item.occurrences if o.component.name == COMP][0].component
    par = des.userParameters.itemByName('button_lever_gap')
    b = comp.bRepBodies.item(0)
    print('lever %s: %.4f mm3, %d faces | %s = %s | modified %s' % (b.name, b.volume * 1000, b.faces.count, par.name, par.expression, app.activeDocument.isModified))
    em = des.exportManager
    print('export', STEP, em.execute(em.createSTEPExportOptions(DIR + STEP, comp)), os.path.getsize(DIR + STEP))
