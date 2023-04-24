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

def feature_engineering_by_question(train: pd.DataFrame, lk_question: pd.DataFrame) -> list:
    
    features_q = []
    level_groups = train['level_group'].drop_duplicates().to_list()
    questions = lk_question[lk_question['level_group'].isin(level_groups)].index.to_list()

    for q in questions:
        level_group = lk_question.loc[q,'level_group']
        train_level = train[train['level_group'] == level_group]
        features_q.append(_level_time_by_session(train_level))

    return features_q