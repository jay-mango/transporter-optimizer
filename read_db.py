import sqlite3
import pandas as pd

# Ensure pandas prints all decimal places for full precision
pd.set_option('display.precision', 16)
pd.set_option('display.float_format', lambda x: f'{x:.16g}')

conn = sqlite3.connect('results/optimization_results5.db')
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:", tables['name'].tolist())

try:
    print("\n--- Trial Counts ---")
    trials_query = pd.read_sql('SELECT COUNT(*) as count FROM trials', conn)
    print(f"Total trials in database: {trials_query.iloc[0,0]}")
    
    print("\n--- Top 3 Trials ---")
    top_trials = pd.read_sql('SELECT trial_id, value FROM trial_values ORDER BY value DESC LIMIT 3', conn)
    print(top_trials)
    
    trial_ids = tuple(top_trials['trial_id'].tolist())
    if len(trial_ids) == 1:
        # SQLite needs (1,) format for IN clause with 1 element
        in_clause = f"({trial_ids[0]})"
    else:
        in_clause = str(trial_ids)
        
    print("\n--- Parameters for Top 3 Trials ---")
    params = pd.read_sql(f'SELECT trial_id, param_name, param_value FROM trial_params WHERE trial_id IN {in_clause}', conn)
    print(params)
    
except Exception as e:
    print("\nError querying optuna tables:", e)
