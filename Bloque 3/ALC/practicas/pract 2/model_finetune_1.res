model:svc params: {'C': 1}
              precision    recall  f1-score   support

           N       0.63      0.67      0.65       219
         NEU       0.20      0.14      0.17        69
        NONE       0.18      0.15      0.16        62
           P       0.54      0.59      0.56       156

    accuracy                           0.51       506
   macro avg       0.38      0.39      0.38       506
weighted avg       0.49      0.51      0.50       506

model:svc params: {'C': 0.5}
              precision    recall  f1-score   support

           N       0.62      0.69      0.65       219
         NEU       0.16      0.10      0.12        69
        NONE       0.21      0.16      0.18        62
           P       0.54      0.58      0.56       156

    accuracy                           0.51       506
   macro avg       0.38      0.39      0.38       506
weighted avg       0.48      0.51      0.50       506

model:svc params: {'C': 0.1}
              precision    recall  f1-score   support

           N       0.62      0.77      0.69       219
         NEU       0.16      0.06      0.09        69
        NONE       0.29      0.18      0.22        62
           P       0.54      0.60      0.57       156

    accuracy                           0.55       506
   macro avg       0.40      0.40      0.39       506
weighted avg       0.49      0.55      0.51       506

model:svc params: {'C': 0.05}
              precision    recall  f1-score   support

           N       0.62      0.78      0.69       219
         NEU       0.29      0.06      0.10        69
        NONE       0.32      0.16      0.22        62
           P       0.55      0.64      0.59       156

    accuracy                           0.56       506
   macro avg       0.44      0.41      0.40       506
weighted avg       0.51      0.56      0.52       506

model:svc params: {'C': 0.01}
              precision    recall  f1-score   support

           N       0.60      0.79      0.69       219
         NEU       0.67      0.03      0.06        69
        NONE       0.30      0.10      0.15        62
           P       0.54      0.67      0.60       156

    accuracy                           0.57       506
   macro avg       0.53      0.40      0.37       506
weighted avg       0.56      0.57      0.51       506

model:svc params: {'C': 0.005}
              precision    recall  f1-score   support

           N       0.58      0.79      0.67       219
         NEU       0.67      0.03      0.06        69
        NONE       0.23      0.05      0.08        62
           P       0.52      0.65      0.58       156

    accuracy                           0.55       506
   macro avg       0.50      0.38      0.35       506
weighted avg       0.53      0.55      0.49       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.0001}
              precision    recall  f1-score   support

           N       0.61      0.73      0.66       219
         NEU       0.18      0.09      0.12        69
        NONE       0.23      0.16      0.19        62
           P       0.53      0.57      0.55       156

    accuracy                           0.52       506
   macro avg       0.39      0.39      0.38       506
weighted avg       0.48      0.52      0.50       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.0005}
              precision    recall  f1-score   support

           N       0.61      0.73      0.67       219
         NEU       0.23      0.10      0.14        69
        NONE       0.23      0.16      0.19        62
           P       0.54      0.58      0.56       156

    accuracy                           0.53       506
   macro avg       0.40      0.39      0.39       506
weighted avg       0.49      0.53      0.50       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.001}
              precision    recall  f1-score   support

           N       0.61      0.83      0.70       219
         NEU       0.21      0.10      0.14        69
        NONE       0.28      0.15      0.19        62
           P       0.62      0.56      0.59       156

    accuracy                           0.56       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.52      0.56      0.53       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.005}
              precision    recall  f1-score   support

           N       0.62      0.74      0.68       219
         NEU       0.38      0.13      0.19        69
        NONE       0.36      0.15      0.21        62
           P       0.54      0.68      0.60       156

    accuracy                           0.57       506
   macro avg       0.48      0.42      0.42       506
weighted avg       0.53      0.57      0.53       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.61      0.78      0.68       219
         NEU       0.30      0.04      0.08        69
        NONE       0.28      0.15      0.19        62
           P       0.54      0.63      0.58       156

    accuracy                           0.56       506
   macro avg       0.43      0.40      0.38       506
weighted avg       0.50      0.56      0.51       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.56      0.79      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.36      0.08      0.13        62
           P       0.52      0.62      0.57       156

    accuracy                           0.54       506
   macro avg       0.36      0.37      0.34       506
weighted avg       0.45      0.54      0.48       506

model:sgd params: {'loss': 'log_loss', 'alpha': 0.1}
              precision    recall  f1-score   support

           N       0.56      0.78      0.65       219
         NEU       0.00      0.00      0.00        69
        NONE       0.27      0.05      0.08        62
           P       0.52      0.63      0.57       156

    accuracy                           0.54       506
   macro avg       0.34      0.36      0.33       506
weighted avg       0.44      0.54      0.47       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.0001}
              precision    recall  f1-score   support

           N       0.60      0.66      0.63       219
         NEU       0.14      0.07      0.10        69
        NONE       0.26      0.18      0.21        62
           P       0.52      0.62      0.56       156

    accuracy                           0.51       506
   macro avg       0.38      0.38      0.38       506
weighted avg       0.47      0.51      0.49       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.0005}
              precision    recall  f1-score   support

           N       0.65      0.56      0.60       219
         NEU       0.15      0.12      0.13        69
        NONE       0.29      0.19      0.23        62
           P       0.46      0.67      0.54       156

    accuracy                           0.49       506
   macro avg       0.39      0.38      0.38       506
weighted avg       0.48      0.49      0.47       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.001}
              precision    recall  f1-score   support

           N       0.62      0.72      0.66       219
         NEU       0.20      0.14      0.17        69
        NONE       0.27      0.19      0.22        62
           P       0.57      0.56      0.57       156

    accuracy                           0.53       506
   macro avg       0.41      0.40      0.40       506
weighted avg       0.50      0.53      0.51       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.005}
              precision    recall  f1-score   support

           N       0.64      0.74      0.68       219
         NEU       0.19      0.07      0.11        69
        NONE       0.28      0.21      0.24        62
           P       0.54      0.62      0.58       156

    accuracy                           0.55       506
   macro avg       0.41      0.41      0.40       506
weighted avg       0.50      0.55      0.52       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.62      0.74      0.68       219
         NEU       0.23      0.04      0.07        69
        NONE       0.31      0.16      0.21        62
           P       0.54      0.69      0.61       156

    accuracy                           0.56       506
   macro avg       0.43      0.41      0.39       506
weighted avg       0.51      0.56      0.52       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.58      0.79      0.67       219
         NEU       0.40      0.03      0.05        69
        NONE       0.36      0.08      0.13        62
           P       0.52      0.63      0.57       156

    accuracy                           0.55       506
   macro avg       0.46      0.38      0.36       506
weighted avg       0.51      0.55      0.49       506

model:sgd params: {'loss': 'hinge', 'alpha': 0.1}
              precision    recall  f1-score   support

           N       0.57      0.79      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.33      0.05      0.08        62
           P       0.51      0.62      0.56       156

    accuracy                           0.54       506
   macro avg       0.35      0.37      0.33       506
weighted avg       0.44      0.54      0.47       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.0001}
              precision    recall  f1-score   support

           N       0.61      0.67      0.64       219
         NEU       0.15      0.14      0.15        69
        NONE       0.20      0.19      0.20        62
           P       0.55      0.50      0.52       156

    accuracy                           0.49       506
   macro avg       0.38      0.38      0.38       506
weighted avg       0.48      0.49      0.48       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.0005}
              precision    recall  f1-score   support

           N       0.62      0.61      0.61       219
         NEU       0.14      0.09      0.11        69
        NONE       0.23      0.16      0.19        62
           P       0.49      0.63      0.55       156

    accuracy                           0.49       506
   macro avg       0.37      0.37      0.37       506
weighted avg       0.47      0.49      0.47       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.001}
              precision    recall  f1-score   support

           N       0.60      0.56      0.58       219
         NEU       0.22      0.14      0.17        69
        NONE       0.16      0.23      0.19        62
           P       0.50      0.54      0.52       156

    accuracy                           0.46       506
   macro avg       0.37      0.37      0.37       506
weighted avg       0.47      0.46      0.46       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.005}
              precision    recall  f1-score   support

           N       0.59      0.56      0.57       219
         NEU       0.21      0.12      0.15        69
        NONE       0.18      0.26      0.21        62
           P       0.52      0.58      0.55       156

    accuracy                           0.47       506
   macro avg       0.37      0.38      0.37       506
weighted avg       0.47      0.47      0.46       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.59      0.74      0.66       219
         NEU       0.13      0.03      0.05        69
        NONE       0.28      0.21      0.24        62
           P       0.54      0.58      0.56       156

    accuracy                           0.53       506
   macro avg       0.39      0.39      0.38       506
weighted avg       0.47      0.53      0.49       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.56      0.62      0.58       219
         NEU       0.18      0.26      0.22        69
        NONE       0.17      0.26      0.20        62
           P       0.60      0.27      0.37       156

    accuracy                           0.42       506
   macro avg       0.38      0.35      0.34       506
weighted avg       0.47      0.42      0.42       506

model:sgd params: {'loss': 'perceptron', 'alpha': 0.1}
              precision    recall  f1-score   support

           N       0.60      0.71      0.65       219
         NEU       0.20      0.20      0.20        69
        NONE       0.26      0.21      0.23        62
           P       0.59      0.48      0.53       156

    accuracy                           0.51       506
   macro avg       0.41      0.40      0.40       506
weighted avg       0.50      0.51      0.50       506

model:lr params: {'C': 1, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.62      0.74      0.67       219
         NEU       0.14      0.07      0.10        69
        NONE       0.24      0.18      0.21        62
           P       0.55      0.59      0.57       156

    accuracy                           0.53       506
   macro avg       0.39      0.39      0.39       506
weighted avg       0.49      0.53      0.51       506

model:lr params: {'C': 0.5, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.62      0.75      0.68       219
         NEU       0.19      0.09      0.12        69
        NONE       0.28      0.18      0.22        62
           P       0.55      0.60      0.58       156

    accuracy                           0.55       506
   macro avg       0.41      0.41      0.40       506
weighted avg       0.50      0.55      0.52       506

model:lr params: {'C': 0.1, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.61      0.79      0.68       219
         NEU       0.50      0.04      0.08        69
        NONE       0.27      0.15      0.19        62
           P       0.56      0.66      0.61       156

    accuracy                           0.57       506
   macro avg       0.49      0.41      0.39       506
weighted avg       0.54      0.57      0.52       506

model:lr params: {'C': 0.05, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.59      0.79      0.68       219
         NEU       1.00      0.03      0.06        69
        NONE       0.23      0.10      0.14        62
           P       0.54      0.64      0.59       156

    accuracy                           0.56       506
   macro avg       0.59      0.39      0.36       506
weighted avg       0.59      0.56      0.50       506

model:lr params: {'C': 0.01, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.55      0.80      0.65       219
         NEU       0.00      0.00      0.00        69
        NONE       0.33      0.03      0.06        62
           P       0.53      0.63      0.58       156

    accuracy                           0.54       506
   macro avg       0.35      0.36      0.32       506
weighted avg       0.44      0.54      0.47       506

model:lr params: {'C': 0.005, 'solver': 'lbfgs'}
              precision    recall  f1-score   support

           N       0.54      0.81      0.65       219
         NEU       0.00      0.00      0.00        69
        NONE       0.00      0.00      0.00        62
           P       0.54      0.62      0.57       156

    accuracy                           0.54       506
   macro avg       0.27      0.36      0.31       506
weighted avg       0.40      0.54      0.46       506

model:lr params: {'C': 1, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.62      0.76      0.68       219
         NEU       0.18      0.07      0.10        69
        NONE       0.24      0.13      0.17        62
           P       0.54      0.60      0.57       156

    accuracy                           0.54       506
   macro avg       0.39      0.39      0.38       506
weighted avg       0.49      0.54      0.51       506

model:lr params: {'C': 0.5, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.62      0.76      0.68       219
         NEU       0.25      0.07      0.11        69
        NONE       0.29      0.16      0.21        62
           P       0.55      0.63      0.59       156

    accuracy                           0.56       506
   macro avg       0.43      0.41      0.40       506
weighted avg       0.51      0.56      0.52       506

model:lr params: {'C': 0.1, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.61      0.80      0.69       219
         NEU       0.50      0.03      0.05        69
        NONE       0.30      0.11      0.16        62
           P       0.54      0.67      0.60       156

    accuracy                           0.57       506
   macro avg       0.49      0.40      0.38       506
weighted avg       0.54      0.57      0.51       506

model:lr params: {'C': 0.05, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.59      0.79      0.68       219
         NEU       1.00      0.03      0.06        69
        NONE       0.26      0.08      0.12        62
           P       0.53      0.65      0.58       156

    accuracy                           0.56       506
   macro avg       0.59      0.39      0.36       506
weighted avg       0.59      0.56      0.49       506

model:lr params: {'C': 0.01, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.56      0.79      0.66       219
         NEU       0.00      0.00      0.00        69
        NONE       0.25      0.03      0.06        62
           P       0.52      0.63      0.57       156

    accuracy                           0.54       506
   macro avg       0.33      0.36      0.32       506
weighted avg       0.43      0.54      0.47       506

model:lr params: {'C': 0.005, 'solver': 'liblinear'}
              precision    recall  f1-score   support

           N       0.54      0.81      0.65       219
         NEU       0.00      0.00      0.00        69
        NONE       0.00      0.00      0.00        62
           P       0.52      0.60      0.56       156

    accuracy                           0.54       506
   macro avg       0.27      0.35      0.30       506
weighted avg       0.40      0.54      0.45       506

model:perceptron params: {}
              precision    recall  f1-score   support

           N       0.59      0.70      0.64       219
         NEU       0.19      0.13      0.16        69
        NONE       0.26      0.19      0.22        62
           P       0.56      0.56      0.56       156

    accuracy                           0.52       506
   macro avg       0.40      0.40      0.39       506
weighted avg       0.49      0.52      0.50       506

model:ridge params: {'alpha': 1}
              precision    recall  f1-score   support

           N       0.61      0.70      0.65       219
         NEU       0.17      0.12      0.14        69
        NONE       0.17      0.11      0.14        62
           P       0.54      0.59      0.57       156

    accuracy                           0.51       506
   macro avg       0.38      0.38      0.37       506
weighted avg       0.48      0.51      0.49       506

model:ridge params: {'alpha': 0.25}
              precision    recall  f1-score   support

           N       0.59      0.63      0.61       219
         NEU       0.20      0.17      0.18        69
        NONE       0.18      0.15      0.16        62
           P       0.54      0.56      0.55       156

    accuracy                           0.49       506
   macro avg       0.38      0.38      0.38       506
weighted avg       0.47      0.49      0.48       506

model:ridge params: {'alpha': 0.125}
              precision    recall  f1-score   support

           N       0.58      0.60      0.59       219
         NEU       0.18      0.16      0.17        69
        NONE       0.17      0.15      0.16        62
           P       0.52      0.54      0.53       156

    accuracy                           0.47       506
   macro avg       0.36      0.36      0.36       506
weighted avg       0.46      0.47      0.46       506

model:ridge params: {'alpha': 0.05}
              precision    recall  f1-score   support

           N       0.56      0.58      0.57       219
         NEU       0.17      0.17      0.17        69
        NONE       0.16      0.15      0.15        62
           P       0.51      0.51      0.51       156

    accuracy                           0.45       506
   macro avg       0.35      0.35      0.35       506
weighted avg       0.45      0.45      0.45       506

model:ridge params: {'alpha': 0.01}
              precision    recall  f1-score   support

           N       0.56      0.56      0.56       219
         NEU       0.17      0.17      0.17        69
        NONE       0.25      0.24      0.25        62
           P       0.50      0.51      0.51       156

    accuracy                           0.45       506
   macro avg       0.37      0.37      0.37       506
weighted avg       0.45      0.45      0.45       506

