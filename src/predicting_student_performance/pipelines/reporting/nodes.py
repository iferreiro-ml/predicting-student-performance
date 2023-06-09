"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.6
"""
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, confusion_matrix, roc_auc_score
import plotly.graph_objects as go

def overall_performance(y_test: np.ndarray, y_pred: np.ndarray) -> tuple[dict, go.Figure]:
    y_pred_all = np.concatenate(y_pred)
    y_test_all = np.concatenate(y_test)
    
    metrics = {"f1": f1_score(y_test_all, y_pred_all),
               "roc_auc": roc_auc_score(y_test_all, y_pred_all),
               "predicted_1s": np.sum(y_pred_all)/ y_pred_all.size,
               "real_1s": np.sum(y_test_all)/ y_test_all.size}
    
    fig = go.Figure(data=[go.Table(
            header=dict(values=list(metrics.keys()),
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        font=dict(color='black', family="Lato", size=14),
                        align='left'),
            cells=dict(values=list(metrics.values()),
                    line_color='darkslategray',
                    fill_color='lightcyan',
                    font=dict(color='black', family="Lato", size=14),
                    align='left'))
                    ])

    fig.update_layout(width=800, height=500)
    
    return metrics, fig


def question_performance(y_test: np.ndarray, y_pred: np.ndarray) -> tuple[pd.DataFrame, go.Figure]:
    
    metrics = pd.DataFrame(
        {       "question": [q for q in range(1,len(y_test)+1)],
                "f1": [f1_score(y_test[q], y_pred[q]) for q in range (0, len(y_test))],
               "roc_auc": [roc_auc_score(y_test[q], y_pred[q]) for q in range (0, len(y_test))],
               "predicted_1s": [np.sum(y_pred[q])/ y_pred[q].size for q in range (0, len(y_test))],
               "real_1s": [np.sum(y_test[q])/ y_test[q].size for q in range (0, len(y_test))]
            }
        )
    
    fig = go.Figure(data=[go.Table(
            header=dict(values=list(metrics.columns),
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        font=dict(color='black', family="Lato", size=14),
                        align='left'),
            cells=dict(values=list(metrics.to_numpy().round(4).T),
                    line_color='darkslategray',
                    fill_color='lightcyan',
                    font=dict(color='black', family="Lato", size=14),
                    align='left'))
                    ])

    fig.update_layout(width=800, height=500)
    
    return metrics, fig


def track_params(split_options: dict, upsampling_seed: float) -> dict:
    return {"test_size": split_options['test_size'], "split_seed": split_options['random_state'], "upsampling_seed": upsampling_seed}

# def model_performance_metrics():
#     for q in range(eval_df['question'].min(), eval_df['question'].max()+1):
#         eval_df_q = eval_df[eval_df['question'] == q]
#         y_test = eval_df_q['correct'].to_numpy()
#         y_pred = eval_df_q['predicted'].to_numpy(dtype=int)
#         display('Question '+str(q))
#         display('Percentage of predicted correct answers: ' + str(np.sum(y_pred)/ y_pred.size))
#         display('Percentage of real correct answers: ' + str(np.sum(y_test)/ y_test.size))
#         display('F1 Score: ' + str(f1_score(y_test, y_pred)))
#         display('ROC AUC Score: ' + str(roc_auc_score(y_test, y_pred)))
#         display('Confusion matrix: ')
#         display(confusion_matrix(y_test, y_pred))