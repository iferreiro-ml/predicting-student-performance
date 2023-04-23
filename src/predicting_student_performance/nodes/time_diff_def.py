import pandas as pd

def time_diff_def(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.sort_values(by=['session_id', 'elapsed_time'], inplace=True)
    df['time_diffs'] = df['elapsed_time'].diff(1)
    df.loc[df['time_diffs'].isna(), 'time_diffs'] = 0
    df.loc[df['time_diffs']<0, 'time_diffs'] = 0
    return df