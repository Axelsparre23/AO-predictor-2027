import numpy as np

def classification_metrics(probabilities, outcomes):
    p = np.clip(np.asarray(probabilities, dtype=float), 1e-9, 1 - 1e-9)
    y = np.asarray(outcomes, dtype=float)
    if len(p) == 0 or len(p) != len(y):
        raise ValueError("Inputs must have equal, non-zero length.")
    if not np.isin(y, [0.0, 1.0]).all():
        raise ValueError("Outcomes must be binary.")
    return {"accuracy": float(np.mean((p >= 0.5) == y)), "brier_score": float(np.mean((p - y) ** 2)), "log_loss": float(-np.mean(y * np.log(p) + (1-y) * np.log(1-p))), "n": int(len(y))}
