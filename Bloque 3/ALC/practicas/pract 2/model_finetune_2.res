model:svc params: {'C': 1}
              precision    recall  f1-score   support

           N       0.60      0.73      0.66       219
         NEU       0.33      0.13      0.19        69
        NONE       0.30      0.13      0.18        62
           P       0.55      0.66      0.60       156

    accuracy                           0.55       506
   macro avg       0.45      0.41      0.41       506
weighted avg       0.51      0.55      0.52       506

model:svc params: {'C': 0.5}
              precision    recall  f1-score   support

           N       0.60      0.74      0.66       219
         NEU       0.36      0.13      0.19        69
        NONE       0.31      0.13      0.18        62
           P       0.56      0.66      0.60       156

    accuracy                           0.56       506
   macro avg       0.46      0.41      0.41       506
weighted avg       0.52      0.56      0.52       506

model:svc params: {'C': 0.1}
              precision    recall  f1-score   support

           N       0.61      0.76      0.67       219
         NEU       0.40      0.12      0.18        69
        NONE       0.35      0.15      0.20        62
           P       0.55      0.66      0.60       156

    accuracy                           0.57       506
   macro avg       0.48      0.42      0.41       506
weighted avg       0.53      0.57      0.53       506

model:svc params: {'C': 0.05}
              precision    recall  f1-score   support

           N       0.61      0.77      0.68       219
         NEU       0.38      0.09      0.14        69
        NONE       0.33      0.13      0.19        62
           P       0.55      0.67      0.60       156

    accuracy                           0.57       506
   macro avg       0.47      0.41      0.40       506
weighted avg       0.53      0.57      0.52       506

model:svc params: {'C': 0.01}
              precision    recall  f1-score   support

           N       0.60      0.81      0.69       219
         NEU       0.50      0.03      0.05        69
        NONE       0.40      0.10      0.16        62
           P       0.55      0.67      0.61       156

    accuracy                           0.57       506
   macro avg       0.51      0.40      0.38       506
weighted avg       0.55      0.57      0.51       506

model:svc params: {'C': 0.005}
              precision    recall  f1-score   support

           N       0.58      0.79      0.67       219
         NEU       1.00      0.01      0.03        69
        NONE       0.33      0.06      0.11        62
           P       0.54      0.67      0.59       156

    accuracy                           0.56       506
   macro avg       0.61      0.39      0.35       506
weighted avg       0.59      0.56      0.49       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.0001}
              precision    recall  f1-score   support

           N       0.60      0.69      0.64       219
         NEU       0.31      0.14      0.20        69
        NONE       0.23      0.10      0.14        62
           P       0.52      0.65      0.58       156

    accuracy                           0.53       506
   macro avg       0.42      0.40      0.39       506
weighted avg       0.49      0.53      0.50       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.0005}
              precision    recall  f1-score   support

           N       0.59      0.81      0.68       219
         NEU       0.50      0.10      0.17        69
        NONE       0.32      0.11      0.17        62
           P       0.57      0.62      0.59       156

    accuracy                           0.57       506
   macro avg       0.49      0.41      0.40       506
weighted avg       0.54      0.57      0.52       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.001}
              precision    recall  f1-score   support

           N       0.61      0.80      0.69       219
         NEU       0.38      0.13      0.19        69
        NONE       0.30      0.11      0.16        62
           P       0.56      0.62      0.59       156

    accuracy                           0.57       506
   macro avg       0.46      0.41      0.41       506
weighted avg       0.52      0.57      0.53       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.005}
              precision    recall  f1-score   support

           N       0.58      0.82      0.68       219
         NEU       0.50      0.06      0.10        69
        NONE       0.30      0.10      0.15        62
           P       0.56      0.61      0.58       156

    accuracy                           0.56       506
   macro avg       0.49      0.40      0.38       506
weighted avg       0.53      0.56      0.51       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.60      0.77      0.67       219
         NEU       0.50      0.06      0.10        69
        NONE       0.32      0.13      0.18        62
           P       0.53      0.65      0.58       156

    accuracy                           0.56       506
   macro avg       0.49      0.40      0.39       506
weighted avg       0.53      0.56      0.51       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.58      0.79      0.67       219
         NEU       0.00      0.00      0.00        69
        NONE       0.31      0.08      0.13        62
           P       0.52      0.65      0.58       156

    accuracy                           0.55       506
   macro avg       0.35      0.38      0.34       506
weighted avg       0.45      0.55      0.48       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.1}
              precision    recall  f1-score   support

           N       0.56      0.79      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.25      0.05      0.08        62
           P       0.52      0.63      0.57       156

    accuracy                           0.54       506
   macro avg       0.33      0.37      0.33       506
weighted avg       0.44      0.54      0.47       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.0001}
              precision    recall  f1-score   support

           N       0.60      0.78      0.68       219
         NEU       0.41      0.10      0.16        69
        NONE       0.24      0.23      0.23        62
           P       0.59      0.56      0.58       156

    accuracy                           0.55       506
   macro avg       0.46      0.42      0.41       506
weighted avg       0.53      0.55      0.52       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.0005}
              precision    recall  f1-score   support

           N       0.60      0.70      0.65       219
         NEU       0.36      0.13      0.19        69
        NONE       0.29      0.16      0.21        62
           P       0.52      0.64      0.57       156

    accuracy                           0.54       506
   macro avg       0.44      0.41      0.40       506
weighted avg       0.51      0.54      0.51       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.001}
              precision    recall  f1-score   support

           N       0.59      0.72      0.65       219
         NEU       0.30      0.16      0.21        69
        NONE       0.28      0.08      0.12        62
           P       0.52      0.62      0.57       156

    accuracy                           0.53       506
   macro avg       0.42      0.39      0.39       506
weighted avg       0.49      0.53      0.50       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.005}
              precision    recall  f1-score   support

           N       0.61      0.74      0.67       219
         NEU       0.33      0.10      0.16        69
        NONE       0.36      0.16      0.22        62
           P       0.55      0.67      0.60       156

    accuracy                           0.56       506
   macro avg       0.46      0.42      0.41       506
weighted avg       0.52      0.56      0.52       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.60      0.78      0.68       219
         NEU       0.35      0.10      0.16        69
        NONE       0.26      0.11      0.16        62
           P       0.56      0.63      0.59       156

    accuracy                           0.56       506
   macro avg       0.44      0.41      0.40       506
weighted avg       0.51      0.56      0.52       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.59      0.79      0.68       219
         NEU       0.33      0.01      0.03        69
        NONE       0.33      0.10      0.15        62
           P       0.54      0.66      0.59       156

    accuracy                           0.56       506
   macro avg       0.45      0.39      0.36       506
weighted avg       0.51      0.56      0.50       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.1}
              precision    recall  f1-score   support

           N       0.58      0.78      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.27      0.05      0.08        62
           P       0.51      0.66      0.58       156

    accuracy                           0.55       506
   macro avg       0.34      0.37      0.33       506
weighted avg       0.44      0.55      0.47       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.0001}
              precision    recall  f1-score   support

           N       0.60      0.74      0.66       219
         NEU       0.29      0.12      0.16        69
        NONE       0.30      0.13      0.18        62
           P       0.55      0.65      0.60       156

    accuracy                           0.55       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.51      0.55      0.51       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.0005}
              precision    recall  f1-score   support

           N       0.60      0.79      0.68       219
         NEU       0.28      0.20      0.24        69
        NONE       0.26      0.08      0.12        62
           P       0.58      0.56      0.57       156

    accuracy                           0.55       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.51      0.55      0.52       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.001}
              precision    recall  f1-score   support

           N       0.60      0.78      0.67       219
         NEU       0.33      0.17      0.23        69
        NONE       0.34      0.16      0.22        62
           P       0.55      0.55      0.55       156

    accuracy                           0.55       506
   macro avg       0.46      0.42      0.42       506
weighted avg       0.52      0.55      0.52       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.005}
              precision    recall  f1-score   support

           N       0.62      0.73      0.67       219
         NEU       0.41      0.16      0.23        69
        NONE       0.35      0.19      0.25        62
           P       0.53      0.64      0.58       156

    accuracy                           0.56       506
   macro avg       0.48      0.43      0.43       506
weighted avg       0.53      0.56      0.53       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.59      0.74      0.66       219
         NEU       0.32      0.10      0.15        69
        NONE       0.27      0.23      0.25        62
           P       0.53      0.54      0.54       156

    accuracy                           0.53       506
   macro avg       0.43      0.40      0.40       506
weighted avg       0.50      0.53      0.50       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.59      0.73      0.65       219
         NEU       0.40      0.09      0.14        69
        NONE       0.31      0.16      0.21        62
           P       0.53      0.64      0.58       156

    accuracy                           0.54       506
   macro avg       0.46      0.40      0.40       506
weighted avg       0.51      0.54      0.51       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.1}
              precision    recall  f1-score   support

           N       0.61      0.79      0.69       219
         NEU       0.36      0.12      0.18        69
        NONE       0.30      0.21      0.25        62
           P       0.59      0.60      0.59       156

    accuracy                           0.57       506
   macro avg       0.47      0.43      0.43       506
weighted avg       0.53      0.57      0.53       506

model:lr params: {'C': 1, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.61      0.77      0.68       219
         NEU       0.42      0.12      0.18        69
        NONE       0.25      0.11      0.16        62
           P       0.55      0.65      0.59       156

    accuracy                           0.56       506
   macro avg       0.46      0.41      0.40       506
weighted avg       0.52      0.56      0.52       506

model:lr params: {'C': 0.5, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.61      0.78      0.68       219
         NEU       0.38      0.09      0.14        69
        NONE       0.24      0.10      0.14        62
           P       0.55      0.65      0.60       156

    accuracy                           0.56       506
   macro avg       0.44      0.40      0.39       506
weighted avg       0.51      0.56      0.52       506

model:lr params: {'C': 0.1, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.58      0.79      0.67       219
         NEU       0.60      0.04      0.08        69
        NONE       0.29      0.10      0.14        62
           P       0.55      0.64      0.59       156

    accuracy                           0.56       506
   macro avg       0.50      0.39      0.37       506
weighted avg       0.54      0.56      0.50       506

model:lr params: {'C': 0.05, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.58      0.80      0.67       219
         NEU       1.00      0.03      0.06        69
        NONE       0.35      0.10      0.15        62
           P       0.55      0.65      0.60       156

    accuracy                           0.56       506
   macro avg       0.62      0.39      0.37       506
weighted avg       0.60      0.56      0.50       506

model:lr params: {'C': 0.01, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.55      0.80      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.22      0.03      0.06        62
           P       0.53      0.60      0.56       156

    accuracy                           0.54       506
   macro avg       0.33      0.36      0.32       506
weighted avg       0.43      0.54      0.46       506

model:lr params: {'C': 0.005, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.55      0.81      0.65       219
         NEU       0.00      0.00      0.00        69
        NONE       0.14      0.02      0.03        62
           P       0.54      0.61      0.57       156

    accuracy                           0.54       506
   macro avg       0.31      0.36      0.31       506
weighted avg       0.42      0.54      0.46       506

model:lr params: {'C': 1, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.61      0.78      0.68       219
         NEU       0.38      0.09      0.14        69
        NONE       0.26      0.10      0.14        62
           P       0.55      0.65      0.60       156

    accuracy                           0.56       506
   macro avg       0.45      0.40      0.39       506
weighted avg       0.52      0.56      0.52       506

model:lr params: {'C': 0.5, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.60      0.79      0.68       219
         NEU       0.42      0.07      0.12        69
        NONE       0.27      0.10      0.14        62
           P       0.55      0.65      0.60       156

    accuracy                           0.57       506
   macro avg       0.46      0.40      0.39       506
weighted avg       0.52      0.57      0.51       506

model:lr params: {'C': 0.1, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.60      0.80      0.68       219
         NEU       0.50      0.03      0.05        69
        NONE       0.29      0.08      0.13        62
           P       0.54      0.67      0.60       156

    accuracy                           0.57       506
   macro avg       0.48      0.39      0.37       506
weighted avg       0.53      0.57      0.50       506

model:lr params: {'C': 0.05, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.59      0.79      0.68       219
         NEU       1.00      0.03      0.06        69
        NONE       0.29      0.08      0.13        62
           P       0.54      0.66      0.59       156

    accuracy                           0.56       506
   macro avg       0.61      0.39      0.36       506
weighted avg       0.59      0.56      0.50       506

model:lr params: {'C': 0.01, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.56      0.81      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.25      0.03      0.06        62
           P       0.53      0.62      0.57       156

    accuracy                           0.54       506
   macro avg       0.33      0.36      0.32       506
weighted avg       0.44      0.54      0.47       506

model:lr params: {'C': 0.005, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.55      0.80      0.65       219
         NEU       0.00      0.00      0.00        69
        NONE       0.25      0.02      0.03        62
           P       0.52      0.61      0.56       156

    accuracy                           0.54       506
   macro avg       0.33      0.36      0.31       506
weighted avg       0.43      0.54      0.46       506

model:perceptron params: {}
              precision    recall  f1-score   support

           N       0.58      0.80      0.67       219
         NEU       0.36      0.13      0.19        69
        NONE       0.36      0.15      0.21        62
           P       0.58      0.57      0.57       156

    accuracy                           0.56       506
   macro avg       0.47      0.41      0.41       506
weighted avg       0.52      0.56      0.52       506

model:ridge params: {'alpha': 1}
              precision    recall  f1-score   support

           N       0.61      0.74      0.67       219
         NEU       0.30      0.10      0.15        69
        NONE       0.30      0.13      0.18        62
           P       0.56      0.67      0.61       156

    accuracy                           0.56       506
   macro avg       0.44      0.41      0.40       506
weighted avg       0.51      0.56      0.52       506

model:ridge params: {'alpha': 0.25}
              precision    recall  f1-score   support

           N       0.60      0.73      0.66       219
         NEU       0.29      0.10      0.15        69
        NONE       0.29      0.13      0.18        62
           P       0.56      0.68      0.61       156

    accuracy                           0.56       506
   macro avg       0.44      0.41      0.40       506
weighted avg       0.51      0.56      0.52       506

model:ridge params: {'alpha': 0.125}
              precision    recall  f1-score   support

           N       0.60      0.73      0.66       219
         NEU       0.29      0.10      0.15        69
        NONE       0.29      0.13      0.18        62
           P       0.56      0.68      0.61       156

    accuracy                           0.55       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.51      0.55      0.52       506

model:ridge params: {'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.60      0.73      0.66       219
         NEU       0.29      0.10      0.15        69
        NONE       0.29      0.13      0.18        62
           P       0.56      0.68      0.61       156

    accuracy                           0.55       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.51      0.55      0.52       506

model:ridge params: {'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.60      0.73      0.66       219
         NEU       0.29      0.10      0.15        69
        NONE       0.29      0.13      0.18        62
           P       0.56      0.68      0.61       156

    accuracy                           0.55       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.51      0.55      0.52       506

