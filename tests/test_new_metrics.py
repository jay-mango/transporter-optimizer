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

    print("--- Test: Evaluating Final Angle ---")
    try:
        final_angle_rad = doc.EvaluateExpression('revoluteJoint3.phiRel(time)')[0]
        print(f"Final Angle (radians): {final_angle_rad}")
        print(f"Final Angle (degrees): {final_angle_rad * 180.0 / 3.14159}")
    except Exception as e:
        print("Error evaluating phiRel over time:", e)
        
    try:
        # Sometimes you can just evaluate the current value if the simulation ended
        final_angle_current = doc.EvaluateExpression('revoluteJoint3.phiRel')
        print(f"Final Angle directly: {final_angle_current}")
    except Exception as e:
        print("Error evaluating phiRel directly:", e)

    print("\n--- Test: Evaluating Simulation Time ---")
    try:
        sim_time = doc.EvaluateExpression('time')
        print(f"Simulation Time: {sim_time}")
    except Exception as e:
        print("Error evaluating time:", e)

except Exception as e:
    print("Main Error:", e)
finally:
    doc.Close()
    simX.Quit()
