import win32com.client
import os

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

try:
    print("Initial rightleg psi0:", doc.SimObjects("rightleg").Parameters("psi0").Value)
    
    # Try setting with tuple
    doc.SimObjects("rightleg").Parameters("psi0").Value = (0.0, 5.0, 0.0)
    print("After setting with tuple:", doc.SimObjects("rightleg").Parameters("psi0").Value)
    
    # Try setting with string, since that's what was read
    doc.SimObjects("rightleg").Parameters("psi0").Value = "{0.0, 6.0, 0.0}"
    print("After setting with string:", doc.SimObjects("rightleg").Parameters("psi0").Value)

except Exception as e:
    print(e)
finally:
    doc.Close()
    simX.Quit()
