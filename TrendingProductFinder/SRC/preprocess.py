
import pandas as pd
import numpy as np

def compute_growth_and_baseline(df):
    """
    df: DataFrame from pytrends with datetime index and one column per keyword
    returns DataFrame with columns:
      - baseline (mean)
      - recent (mean of last N points)
      - growth_pct
    """
    result = []
    for col in df.columns:
        series = df[col].fillna(0)
        baseline = series.mean()
        recent = series.tail(max(1, int(len(series)*0.25))).mean()
  
        growth = (recent - baseline) / (baseline + 1e-9)
        result.append((col, baseline, recent, growth))
    res_df = pd.DataFrame(result, columns=['keyword','baseline','recent','growth'])

    return res_df
