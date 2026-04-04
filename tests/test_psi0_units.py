import win32com.client
import os

simX = win32com.client.Dispatch('ESI.SimulationX47')
doc = simX.Documents.Open(os.path.abspath(r'C:\flexlm\Project\Model5.isx'))

try:
    print("Initial rightleg psi0:", doc.SimObjects("rightleg").Parameters("psi0").Value)
    
    # Try setting string 90 degrees
    doc.SimObjects("rightleg").Parameters("psi0").Value = "{0,90,0}"
    print("Set to string {0,90,0}, read back:", doc.SimObjects("rightleg").Parameters("psi0").Value)

    # Now let's try tuple (0, 90, 0)
    doc.SimObjects("rightleg").Parameters("psi0").Value = (0.0, 90.0, 0.0)
    print("Set to tuple (0,90,0), read back:", doc.SimObjects("rightleg").Parameters("psi0").Value)
    
except Exception as e:
    print(e)
finally:
    doc.Close()
    simX.Quit()
