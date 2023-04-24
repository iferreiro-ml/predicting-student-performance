"""
This is a boilerplate pipeline 'ingestion'
generated using Kedro 0.18.6
"""

import numpy as np
import pandas as pd

def _sessions_train_test_split(df, test_size = 0.2, seed = 42):
    np.random.seed(seed)
    unique_sessions = df['session_id'].unique()
    test_sessions = list(np.random.choice(unique_sessions, size = int(test_size * len(unique_sessions)), replace = False))
    train_sessions = list(set(unique_sessions).difference(set(test_sessions)))
    return train_sessions, test_sessions

def _session_list_split(df, session_list):
    result_df = df[df['session_id'].isin(session_list)]
    return result_df

def _labels_q_list(df: pd.DataFrame) -> list:
    question_list = list(df['question'].unique())
    labels_q = []
    for q in question_list:
        labels_q.append(df[df['question'] == q])
    return labels_q

def jo_train_test_split(train: pd.DataFrame , labels_q: pd.DataFrame, split_options: dict) -> tuple[pd.DataFrame, list, pd.DataFrame, list]:

    train_sessions, test_sessions = _sessions_train_test_split(train, test_size = split_options["test_size"], seed = split_options["random_state"])

    test_data = _session_list_split(train, test_sessions)
    train_data = _session_list_split(train, train_sessions)
    test_labels = _session_list_split(labels_q, test_sessions).set_index('session_id')
    train_labels = _session_list_split(labels_q, train_sessions).set_index('session_id')

    train_labels_q = _labels_q_list(train_labels)
    test_labels_q = _labels_q_list(test_labels)

    return train_data, train_labels_q, test_data, test_labels_q