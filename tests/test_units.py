import win32com.client, math, os, time

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

j = doc.SimObjects('revoluteJoint3')

j.Parameters('phiRel0').Value = -5.0 # -5 * 180 / pi = -286 degrees ? OR -5 degrees?
doc.Reset()
doc.Start()
while doc.SolutionState in [4, 8]:
    time.sleep(0.1)
print('Max Distance (if -5.0 float given):', doc.EvaluateExpression('max(cuboid1.x[1])'))

j.Parameters('phiRel0').Value = math.radians(-5.0) # -5 degrees in radians
doc.Reset()
doc.Start()
while doc.SolutionState in [4, 8]:
    time.sleep(0.1)
print('Max Distance (if math.radians given):', doc.EvaluateExpression('max(cuboid1.x[1])'))
