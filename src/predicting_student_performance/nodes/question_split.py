"""
This is a boilerplate pipeline 'ingestion'
generated using Kedro 0.18.6
"""

import pandas as pd

def question_split(labels: pd.DataFrame) -> pd.DataFrame: 
    lbls = labels.copy()
    lbls[['session_id', 'question']] = lbls['session_id'].str.split('_q', expand = True).astype({0: int, 1: int})
    return lbls