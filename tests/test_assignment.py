import win32com.client
import os

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

try:
    print("Testing string vs tuple assignment to psi0:")
    
    # 1. String assignment {0, 5, 0}
    doc.SimObjects('rightleg').Parameters('psi0').Value = "{0, 5, 0}"
    doc.Reset()
    doc.Start()
    while doc.SolutionState in [4, 8]: pass
    print("Distance after string '{0, 5, 0}' assignment:", doc.EvaluateExpression('cuboid1.x[1]'))

    # 2. Tuple assignment (0, 5, 0)
    doc.SimObjects('rightleg').Parameters('psi0').Value = (0.0, 5.0, 0.0)
    doc.Reset()
    doc.Start()
    while doc.SolutionState in [4, 8]: pass
    print("Distance after tuple (0.0, 5.0, 0.0) assignment:", doc.EvaluateExpression('cuboid1.x[1]'))

    # 3. Tuple assignment (0, 5 radians, 0)
    # 5 degrees is ~0.087 radians
    rad_val = 5.0 * 3.14159 / 180.0
    doc.SimObjects('rightleg').Parameters('psi0').Value = (0.0, rad_val, 0.0)
    doc.Reset()
    doc.Start()
    while doc.SolutionState in [4, 8]: pass
    print("Distance after tuple (0.0, 0.087, 0.0) assignment (rads):", doc.EvaluateExpression('cuboid1.x[1]'))

except Exception as e:
    print(e)
finally:
    doc.Close()
    simX.Quit()