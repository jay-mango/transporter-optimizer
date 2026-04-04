# MTE 351 Project - Bayesian Optimization

This repository contains a Bayesian Optimization pipeline designed to automatically discover the best physical configuration for our SimulationX model. It uses an AI-driven search library called **Optuna** to interface directly with the SimulationX engine and run hundreds of trials without human intervention.

## Why are we doing this?

Manually guessing angles and forces to make the robot jump further is incredibly slow and inefficient. This script automates the process by mathematically learning from past jumps.
Instead of guessing randomly, Bayesian Optimization looks at the history of previous trials (e.g. which forces and angles produced the longest distances) and predicts where the next best combination lies, balancing exploring new areas and exploiting known good configurations.

## Connecting to SimulationX via the COM API

This project uses the Windows **COM (Component Object Model) API** to let Python act as a remote control for SimulationX. By using the `pywin32` library, Python can launch SimulationX programmatically (`win32com.client.Dispatch("ESI.SimulationX47")`), load our `.isx` model, and manipulate it exactly as a human would through the GUI.

This bridge enables a few critical capabilities:

- **Direct Variable Injection**: We dynamically edit object parameters (like `doc.SimObjects("rightleg").Parameters("psi0").Value`) with new angles and forces. By formatting array variables as strings matching the UI, we safely interact with the physics engine in Degrees rather than getting caught in messy background conversions to Radians.
- **Automated Execution**: Python sends `doc.Reset()` and `doc.Start()` commands to run the simulation, then waits for the solver states to finish computing.
- **Result Extraction**: We yank the final evaluation metrics right out of the engine using `doc.EvaluateExpression("max(cuboid1.x[1])")`.

This completely eliminates manual data entry and makes our rapid testing loop possible.

## How it Works

1. **The Optuna Brain**: `main.py` asks Optuna to suggest parameters for `f_t` (force), `theta` (angle), and `beta` (angle).
2. **The Physics Engine injection**: Python uses the COM interface to inject these suggested numbers directly into our SimulationX project (`C:/flexlm/Project/Model5.isx`).
3. **The Simulation**: Python tells SimulationX to run the simulation invisibly in the background.
4. **The Score**: Python reads the maximum distance achieved (`cuboid1.x[1]`) from the SimulationX results.
5. **The Feedback Loop**: Python feeds this distance back to Optuna. Optuna learns from the result and formulates an even smarter, educated guess for the next trial.

This process loops hundreds of times to find the absolute maximum distance possible.

## Setup

1. **Create a virtual environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   # On Windows use:
   venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **IMPORTANT**: Ensure the absolute path to the SimulationX `.isx` file on line 14 of `main.py` matches the correct path on your machine before running!

## Usage

Run the main script to start the automatic optimization process:

```bash
python main.py
```

As it runs, it will print terminal outputs showing the parameters tested and the distance achieved.

The optimizer remembers past trials automatically! It stores all of its history in `results/optimization_results5.db`. If you cancel the script and run it again later, it will pick up exactly where it left off, reading past successes from the database to inform its next guesses.

## Evaluating Results

- **`visualize_results.py`**: A Matplotlib dashboard that reads from the SQLite database to generate three plots for the final report:
  - **Optimization History**: Shows the progression of our best distances over time.
  - **Parallel Coordinates**: Visualizes the high-dimensional relationships between force, angles, and distance.
  - **Parameter Importances**: Uses Scikit-learn to rank which simulation parameters had the biggest impact on jump distance.
- **`read_db.py`**: We created a helper script to query the SQLite database to reveal exactly how many trials ran and print the exact high-precision decimal values of the Top 3 best trial configurations found.
- **CSV Exports**: Every time the script finishes, it can dump its history to CSV files (e.g., `optimization_history.csv`) sorted from best distance to worst. This is great for opening in Excel.

## Project Structure

- `main.py`: Entry point containing the core Optuna study and SimulationX hook.
- `visualize_results.py`: Desktop dashboard for plotting the Optuna database using `optuna.visualization.matplotlib`.
- `read_db.py`: Helper script to extract the exact winning parameters from the database.
- `results/`: Directory containing the active Optuna SQLite databases (`optimization_results5.db`, etc.) which store all memory and historical trial data.
- `tests/`: A folder containing miscellaneous troubleshooting scripts we used to debug COM communication quirks, unit conversions, and string parsing errors.
- `requirements.txt`: Python package dependencies (including `matplotlib` and `scikit-learn` for visualizations).
