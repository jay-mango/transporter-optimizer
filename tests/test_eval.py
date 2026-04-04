import win32com.client
import os
import time

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

try:
    doc.Reset()
    doc.Start()

    while doc.SolutionState in [4, 8]:
        time.sleep(0.1)

    print('Evaluating max(cuboid1.x[1]):', doc.EvaluateExpression('max(cuboid1.x[1])'))
    print('Evaluating min(cuboid1.x[1]):', doc.EvaluateExpression('min(cuboid1.x[1])'))
    print('Evaluating cuboid1.x[1]:', doc.EvaluateExpression('cuboid1.x[1]'))
    
    # Try looking for a simulation result curve
    res = doc.AnalysisResults
    # Let's just print a few properties of res to see if we can get the max over time
    print('Has Results?', res is not None)
    
except Exception as e:
    print(e)
finally:
    doc.Close()
    simX.Quit()
