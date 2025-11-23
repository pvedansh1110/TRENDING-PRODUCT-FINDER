
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def compute_trend_score(df_features, weights=None):
    """
    df_features: DataFrame with columns ['keyword','baseline','recent','growth']
    weights: dict of weights e.g. {'growth':0.6, 'baseline':0.3, 'recent':0.1}
    """
    if weights is None:
        weights = {'growth':0.6, 'baseline':0.3, 'recent':0.1}
    feat = df_features.copy()
    scaler = MinMaxScaler()
  
    feat[['baseline_s','recent_s','growth_s']] = scaler.fit_transform(
        feat[['baseline','recent','growth']].fillna(0).values
    )
    feat['trend_score'] = (
        weights['growth'] * feat['growth_s'] +
        weights['baseline'] * feat['baseline_s'] +
        weights['recent'] * feat['recent_s']
    )
    return feat.sort_values('trend_score', ascending=False)
