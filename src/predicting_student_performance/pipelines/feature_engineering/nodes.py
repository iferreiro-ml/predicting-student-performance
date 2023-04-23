"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.6
"""
import pandas as pd

def _level_time_by_session(df):
    grp = df['level_group'].iloc[0]
    limits = list(map(int, grp.split('-')))
    features_df = pd.pivot_table(df, index = 'session_id', columns = 'level', values = 'time_diffs', aggfunc = sum).fillna(0)
    for l in range(limits[0],limits[1]+1):
        if l not in features_df:
            features_df[l] = 0
    return features_df

def feature_engineering_by_question(train: pd.DataFrame, labels_q: pd.DataFrame, lk_question: pd.DataFrame) -> list:
    
    primary_q = []
    q_i, q_e = (labels_q['question'].min(), labels_q['question'].max()+1)

    for q in range(q_i, q_e):
        level_group = lk_question.loc[q,'level_group']
        train_level = train[train['level_group'] == level_group]
        labels = labels_q[labels_q['question'] == q].drop('question', axis = 1)
        primary_q.append(_level_time_by_session(train_level).merge(labels, on = 'session_id'))

    return primary_q