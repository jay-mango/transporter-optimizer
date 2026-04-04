import win32com.client
import os

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

try:
    doc.Reset()
    doc.Start()
    while doc.SolutionState in [4, 8]:
        pass

    results = doc.AnalysisResults
    # Let's try to get the curve for cuboid1.x[1]
    res_obj = None
    try:
        # SimulationX 4.0+ usually has AnalysisResults.GetResult("cuboid1.x[1]") or similar
        print("AnalysisResults properties:", dir(results))
    except Exception as e:
        print("Dir failed:", e)

    # Let's try EvaluateExpression over a string that calculates time-max
    try:
        # Some SimulationX expressions support finding the maximum over history if specified correctly
        print("MaxVal:", doc.EvaluateExpression("max(cuboid1.x[1])"))
    except:
        pass

except Exception as e:
    print(e)
finally:
    doc.Close()
    simX.Quit()
