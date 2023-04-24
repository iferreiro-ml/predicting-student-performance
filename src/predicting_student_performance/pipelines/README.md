# Pipeline design
```mermaid
flowchart TB
    subgraph Ingestion
        id[(train)]-->reduce_memory_usage
        id2[(test)]-->reduce_memory_usage
        id30[(test_prd)]-.->reduce_memory_usage
        reduce_memory_usage --> id1[(light_train)]
        reduce_memory_usage --> id3[(light_test)]
        reduce_memory_usage -.->id31[(light_prd)]
        id4[(labels)]-->question_split
        id31[(light_prd)] -.-> time_diff_def
        id1[(light_train)]-->time_diff_def
        question_split-->id5[(labels_q)]
        time_diff_def -.-> id60[(events_prd)]
        time_diff_def --> id6[(events_train)]
    end
    subgraph Split data
        id6[(events_train)] --> split_data
        id5[(labels_q)] --> split_data
        id8((seed)) --> split_data
        id9((test_size)) --> split_data
        split_data --> id10[(train_data)]
        split_data --> id11[(labels_q_train)]
        split_data --> id12[(test_data)]
        split_data --> id13[(labels_q_test)]
    end
    subgraph Feature Engineering
        id10[(train_data)] --> feature_engineering_by_question
        id12[(test_data)] --> feature_engineering_by_question
        id60[(events_prd)] -.-> feature_engineering_by_question
        feature_engineering_by_question -.-> id70[(features_q_prd)]
        feature_engineering_by_question --> id7[(features_q_train)]
        feature_engineering_by_question --> id71[(features_q_test)]
    end
    subgraph Normalization train data
        id7[(features_q_train)] --> upsampling
        id11[(train_labels_q)] --> upsampling
        id14((ups_seed)) --> upsampling
        upsampling --> id16[(unscaled_X_train)]
        upsampling --> id17[(y_train)]
        id16[(unscaled_X_train)] --> scaling
        scaling --> id15[\scaler/]
        scaling --> id18[(X_train)]
    end
    subgraph Normalization prd data
        id70[(features_q_prd)] -.-> prd_norm
        id15[\scaler/] -.-> prd_norm
        prd_norm -.-> id32[(X)]
    end
    subgraph Model train
        id19[\clf/] --> model_train
        id18[(X_train)] --> model_train
        id17[(y_train)] --> model_train
        model_train --> id19[\clf/] 
    end
    subgraph Normalization test data
        id12[(test_data)] --> test_norm
        id13[(test_labels)] --> test_norm
        id15[\scaler/] --> test_norm
        test_norm --> id20[(X_test)]
        test_norm --> id21[(y_test)]
    end
    subgraph Predict
        id19[\clf/] --> predict
        id20[(X_test)] --> predict
        id32[(X)] -.-> predict
        predict -.-> id22[(y_pred)]
    end
    subgraph Test evaluation
        id21[(y_test)] --> evaluate
        id22[(y_pred)] --> evaluate
        evaluate --> id23[(report)]
    end
    subgraph Submission
        id22[(y_pred)] -.-> submit
    end
```
