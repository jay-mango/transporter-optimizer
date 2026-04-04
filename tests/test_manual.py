import win32com.client, math, os, time

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

j = doc.SimObjects('revoluteJoint3')
j.Parameters('phiRel0').Value = -0.26314059 # Injecting exactly what the GUI screenshot showed in the field

r = doc.SimObjects('rightleg')
p = [float(x) for x in r.Parameters('psi0').Value.strip('{}').split(',')]
p[1] = 0.86570481
r.Parameters('psi0').Value = tuple(p)

f = doc.SimObjects('Ft')
f.Parameters('F').Value = 68.905239

doc.Reset()
doc.Start()
while doc.SolutionState in [4, 8]:
    time.sleep(0.1)

print('Max Distance (FULLY MANUAL UI DEGREES):', doc.EvaluateExpression('max(cuboid1.x[1])'))
