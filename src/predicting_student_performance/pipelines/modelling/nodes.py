"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.18.6
"""

import pandas as pd
from sklearn.utils import resample

def upsample_minority_class(features_q: list, labels_q: list, seed = 42) -> tuple[list, list]:
    
    upsampled_features_q = []
    upsampled_labels_q = []

    for q in range(0,len(labels_q)):
        features = features_q[q]
        labels = labels_q[q]

        # upsample
        labels_incorrect = labels[labels['correct']==0]
        labels_correct = labels[labels['correct']==1]
        features_incorrect = features.loc[labels['correct']==0,:]
        features_correct = features.loc[labels['correct']==1,:]
        
        if len(labels_incorrect.index) > len(labels_correct.index):
            labels_correct, features_correct = resample(labels_correct, features_correct, replace=True,
                                      n_samples=len(labels_incorrect.index), random_state=seed)
        elif len(labels_incorrect.index) < len(labels_correct.index):
            labels_incorrect, features_incorrect = resample(labels_incorrect, features_incorrect, replace=True,
                                        n_samples=len(labels_correct.index), random_state=seed)
        
        assert len(labels_incorrect.index) == len(features_correct.index), 'Upsampling failed'
        
        upsamples_features = pd.concat([features_correct, features_incorrect])
        upsampled_labels = pd.concat([labels_correct, labels_incorrect])

        upsampled_features_q.append(upsamples_features)
        upsampled_labels_q.append(upsampled_labels)
        
    return upsampled_features_q, upsampled_labels_q
