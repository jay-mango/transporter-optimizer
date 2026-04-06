import optuna
import win32com.client
import math
import os
import pandas as pd
import time

# Dispatch opens SimulationX in the background
print("Connecting to SimulationX...")
simX = win32com.client.Dispatch("ESI.SimulationX47")

# Optional: Set to True if you want to watch it run (slower), False for hidden (faster)
simX.Visible = True

# IMPORTANT: Provide the ABSOLUTE path to your .isx file
file_path = os.path.abspath("C:/flexlm/Project/Model5.isx")
doc = simX.Documents.Open(file_path)
print("Model loaded successfully.")

def objective(trial):
    # Let Optuna suggest values (Adjust these ranges based on our previous math!)
    f_t_guess = trial.suggest_float('f_t', 100, 100)
    theta_guess_deg = trial.suggest_float('theta_deg', 5, 5)
    beta_guess_deg = trial.suggest_float('beta_deg', -2.45646, -2.456455)

    if (theta_guess_deg + beta_guess_deg) <= 0:
            raise optuna.TrialPruned()

    # No conversion needed! SimulationX parameters read from the COM API default to matching the 
    # display unit from the UI. If the GUI is set to Degrees, .Value expects Degrees!

    try:
        # --- 3. INJECT YOUR VARIABLES INTO SIMULATIONX ---
        
        # 1. theta: Inject DEGREES directly. (Previously math.radians caused it to tilt 60x less than claimed!)
        doc.SimObjects("revoluteJoint3").Parameters("phiRel0").Value = theta_guess_deg
        
        # 2. beta: Fetch current string, parse into floats, manipulate index 0, push tuple back.
        # This completely PREVENTS string parsing bugs and geometry explosions!
        psi0_str = doc.SimObjects("rightleg").Parameters("psi0").Value
        rightleg_psi0 = [float(x) for x in psi0_str.strip("{}").split(",")]
        # 0-indexed Python array. [1] represents the middle value (the Y-Axis rotation)
        rightleg_psi0[1] = beta_guess_deg  
        psi0_new_str = f"{{{rightleg_psi0[0]},{rightleg_psi0[1]},{rightleg_psi0[2]}}}"
        doc.SimObjects("rightleg").Parameters("psi0").Value = psi0_new_str
        
        # 3. ft.y: The COM registry exposes the object as "Ft" with parameter "F"
        doc.SimObjects("Ft").Parameters("F").Value = f_t_guess

        # --- 4. RUN THE SIMULATION ---
        doc.Reset()
        doc.Start()

        # FORCE python to wait! COM sometimes doesn't block.
        # Wait while the simulation is calculating (State 4 = Initializing, State 8 = Calculating)
        # It usually returns to State 16 (Finished) or State 0 (Idle)
        start_time = time.time()
        while doc.SolutionState in [4, 8]:
            if time.time() - start_time > 60.0:
                print(f"[!] Warning: Trial {trial.number:03d} timed out after 60 seconds. Stopping simulation step.")
                doc.Stop()
                return 0.0  # Return a bad score to let Optuna know this failed
            time.sleep(0.1)

        # --- 5. EXTRACT YOUR TARGET RESULT ---
        # 1. Distance (Maximize)
        max_distance = doc.EvaluateExpression("max(cuboid1.x[1])")
        
        # 2. Final Time (Minimize)
        total_time = doc.EvaluateExpression("time")
        
        # We will set time as a user attribute so it goes into the database cleanly
        trial.set_user_attr("total_time", total_time)
        
        try:
            best_val = trial.study.best_value
            best_num = trial.study.best_trial.number
            
            # Update the displayed best if the current trial is breaking the record!
            if max_distance > best_val:
                best_val = max_distance
                best_num = trial.number
                
            best_str = f" | Best So Far: {best_val:.4f} m (Trial {best_num:03d})"
        except ValueError:
            # Handles the very first successful trial where optuna doesn't have a 'best' yet
            best_str = f" | Best So Far: {max_distance:.4f} m (Trial {trial.number:03d})"
        
        print(f"Trial {trial.number:03d} | f_t = {f_t_guess:5.2f} N | theta = {theta_guess_deg:6.2f}° | beta = {beta_guess_deg:5.2f}° ---> Distance: {max_distance:.4f} m | Time: {total_time:.2f}s{best_str}")

    except KeyboardInterrupt:
        # If the user hits Ctrl+C, raise it immediately so the script exits cleanly
        print(f"\n[!] Manual interruption detected at Trial {trial.number}. Halting simulation.")
        raise
        
    except Exception as e:
        import traceback
        print(f"Trial {trial.number} failed: {e}")
        # If the simulation crashes (e.g., impossible geometry), return a terrible score
        return 0.0 

    return max_distance

if __name__ == "__main__":
    # Suppress Optuna's messy default INFO logs so our custom prints are clean
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    
    print("Starting Optuna Study...")
    
    # We want to MAXIMIZE the distance
    study = optuna.create_study(
        study_name='mte351_optimization5',
        storage='sqlite:///results/optimization_results4.db',
        load_if_exists=True,
        direction='maximize'
    )
    
    try:
        study.optimize(objective, n_trials=1)  
    except KeyboardInterrupt:
        print("\n\nOptuna Optimization Stopped by User!")

    # --- 6. SAVE TO CSV ---
    print("\nSaving partial iteration history...")
    df = study.trials_dataframe()
    if not df.empty:
        # Let's save a clean sorted CSV so the best distances are at the top!
        df_sorted = df.sort_values(by="value", ascending=False)
        df_sorted.to_csv("results/optimization_history4.csv", index=False)
        print("Saved iteration history to results/optimization_history5.csv (Sorted by Best Score)")
    else:
        print("No successful trials completed. No CSV saved.")

    # --- 7. PRINT THE WINNER ---
    if len(study.trials) > 0 and study.best_trial is not None:
        print("\n" + "="*30)
        print("OPTIMIZATION COMPLETE")
        print("="*30)
        print(f"Longest Distance: {study.best_trial.value:.2f} meters")
        print("Winning Parameters:")
        for key, value in study.best_trial.params.items():
            print(f"  {key}: {value:.3f}")
    
    # Clean up and close SimulationX
    try:
        doc.Close()
        simX.Quit()
    except Exception:
        pass