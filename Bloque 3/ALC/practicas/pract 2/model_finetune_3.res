model:svc params: {'C': 0.1, 'max_iter': 10000}
              precision    recall  f1-score   support

           N       0.60      0.77      0.68       219
         NEU       0.22      0.06      0.09        69
        NONE       0.37      0.21      0.27        62
           P       0.61      0.68      0.64       156

    accuracy                           0.58       506
   macro avg       0.45      0.43      0.42       506
weighted avg       0.52      0.58      0.54       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.01, 'max_iter': 10000}
              precision    recall  f1-score   support

           N       0.57      0.82      0.68       219
         NEU       0.33      0.03      0.05        69
        NONE       0.42      0.18      0.25        62
           P       0.60      0.62      0.61       156

    accuracy                           0.57       506
   macro avg       0.48      0.41      0.40       506
weighted avg       0.53      0.57      0.52       506

model:lr params: {'C': 0.5, 'solver': 'lbfgs', 'max_iter': 10000}
              precision    recall  f1-score   support

           N       0.59      0.78      0.67       219
         NEU       0.33      0.06      0.10        69
        NONE       0.34      0.18      0.23        62
           P       0.59      0.65      0.62       156

    accuracy                           0.57       506
   macro avg       0.46      0.42      0.41       506
weighted avg       0.52      0.57      0.52       506

model:lr params: {'C': 0.5, 'solver': 'liblinear', 'max_iter': 10000}
              precision    recall  f1-score   support

           N       0.60      0.79      0.68       219
         NEU       0.40      0.06      0.10        69
        NONE       0.38      0.18      0.24        62
           P       0.58      0.66      0.62       156

    accuracy                           0.58       506
   macro avg       0.49      0.42      0.41       506
weighted avg       0.54      0.58      0.53       506

