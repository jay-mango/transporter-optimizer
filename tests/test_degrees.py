import win32com.client, math, os, time

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

j = doc.SimObjects('revoluteJoint3')
j.Parameters('phiRel0').Value = -5.0
print("If I set -5.0, COM reads it back as:", j.Parameters('phiRel0').Value)
