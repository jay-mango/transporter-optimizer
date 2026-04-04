import optuna
import matplotlib.pyplot as plt
from optuna.visualization.matplotlib import plot_optimization_history
from optuna.visualization.matplotlib import plot_parallel_coordinate
from optuna.visualization.matplotlib import plot_param_importances

def main():
    # Connect to the SQLite database
    # Switch this to optimization_results.db or whichever you want to visualize
    db_url = "sqlite:///results/optimization_results2.db"
    study_name = "mte351_optimization5"  # The default name unless you specified otherwise
    
    print(f"Loading study from {db_url}...")
    try:
        # Load the study
        study = optuna.load_study(study_name=study_name, storage=db_url)
    except Exception as e:
        print(f"Error loading study: {e}")
        print("Note: If you didn't name your study 'mte351_optimization5', you might need to use:")
        print("study = optuna.get_all_study_summaries(storage=db_url)[0].study_name")
        
        # Fallback to the first study found in the db
        summaries = optuna.get_all_study_summaries(storage=db_url)
        if not summaries:
            print("No studies found in the database.")
            return
        study_name = summaries[0].study_name
        print(f"Falling back to study name: {study_name}")
        study = optuna.load_study(study_name=study_name, storage=db_url)

    print(f"Best trial: {study.best_trial.number}")
    print(f"Best value: {study.best_value}")

    # 1. Optimization History
    print("Generating Optimization History plot...")
    fig_history = plot_optimization_history(study)
    plt.tight_layout()
    plt.show()

    # 2. Parallel Coordinate Plot (High-dimensional parameter relationships)
    print("Generating Parallel Coordinate plot...")
    fig_parallel = plot_parallel_coordinate(study)
    plt.tight_layout()
    plt.show()

    # 3. Parameter Importances
    # Note: Requires scikit-learn installed to evaluate feature importances
    print("Generating Parameter Importances plot...")
    try:
        fig_importances = plot_param_importances(study)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not generate parameter importances (scikit-learn might be missing): {e}")

if __name__ == "__main__":
    main()
