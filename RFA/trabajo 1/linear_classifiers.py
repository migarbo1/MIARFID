import pickle
import numpy as np
import sys
import math
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, SGDClassifier, Perceptron, RidgeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

models = {
    'SGD': [ #best in librispeech: pca: 15, LDA: true, stand: false, penalty: l1
        {'penalty': 'l2', 'max_iter':20000,'n_jobs':4},
        {'penalty': 'l1', 'max_iter':20000,'n_jobs':4},
        # {'loss':'log', 'max_iter':20000,'n_jobs':4}, equivalent to l2
    ],
    'perceptron':[
        {'penalty':'l2', 'max_iter':20000,'n_jobs':4}
        # {'penalty':'l1', 'max_iter':20000,'n_jobs':4}, l2 works better
    ],
    'logRes':[
        # {'penalty':'l1','solver': 'saga' , 'max_iter':20000,'n_jobs':4},
        {'penalty':'elasticnet', 'l1_ratio': 0.25, 'solver': 'saga' , 'max_iter':20000,'n_jobs':4},
        {'penalty':'elasticnet', 'l1_ratio': 0.75, 'solver': 'saga' , 'max_iter':20000,'n_jobs':4}
        # {'penalty':'elasticnet', 'l1_ratio': 0.5, 'solver': 'saga' , 'max_iter':20000,'n_jobs':4},
        # {'penalty':'l2','solver': 'saga' , 'max_iter':20000,'n_jobs':4},
        # {'penalty':'l2', 'max_iter':20000,'n_jobs':4},
    ],
    'ridge':[
        {'solver':'svd', 'max_iter':5000},
        {'solver':'sag', 'max_iter':5000}
        # {'solver':'cholesky', 'max_iter':5000},
    ]
}

def load_data():
    if len(sys.argv)!=3:
        print('Usage: %s <trdata> <dvdata>' % sys.argv[0])
        sys.exit(1)

    tr = np.load(sys.argv[1])['tr']
    
    dv = np.load(sys.argv[2])['dv']
    return tr, dv

def split_datalabels(tr):
    _,L=tr.shape
    D=L-1   
    x_tr=tr[:,1:D]
    y_tr=tr[:,-1] 
    return x_tr, y_tr

def accuracy(y_real, y_pred):
    err = (y_real != y_pred).sum()/y_real.shape[0]
    r=1.96*math.sqrt(err*(1-err)/y_real.shape[0])
    # print("Dev CER: %.2f%% [%.2f, %.2f]" % (err*100,(err-r)*100,(err+r)*100))
    return err, r

def auc(y_real, probs):
    auc = metrics.roc_auc_score(y_real,probs)
    # print("Dev AUC: %.1f%%" % (auc*100))
    return auc

def save_model(model, name):
    pickle.dump(model, open(name, 'wb'))

def plot_roc(y_real, probs, img_name):
    fpr, tpr, _ = metrics.roc_curve(y_real,probs,pos_label=1);  

    plt.plot(fpr,tpr)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig('outputs/'+img_name)
    plt.show()

def standarize(x_train):
    return StandardScaler().fit_transform(x_train)

def create_model(model_name = 'logRes', kargs = {}):
    if model_name == 'SGD':
        model = SGDClassifier(**kargs)
    if model_name == 'perceptron':
        model = Perceptron(**kargs)
    if model_name == 'logRes':
        model = LogisticRegression(**kargs)
    if model_name == 'ridge':
        model = RidgeClassifier(**kargs)

    return CalibratedClassifierCV(model, cv=5, method='isotonic')

if __name__ == '__main__':
    tr, dv = load_data()

    for key in models:
        for args in models[key]:
            for pca in [20,15]:
                for stand in [True, False]:
                    for lda in [True, False]:
                        x_tr, y_tr = split_datalabels(tr)
                        x_dv, y_dv = split_datalabels(dv)

                        if stand:
                            x_tr = standarize(x_tr)
                            x_dv = standarize(x_dv)

                        
                        X = np.concatenate((x_tr, x_dv))
                        X = PCA(n_components=pca).fit_transform(X)
                        x_tr = X[0:x_tr.shape[0],:]
                        x_dv = X[x_tr.shape[0]:,:]

                        if lda:
                            X = np.concatenate((x_tr, x_dv))
                            Y = np.concatenate((y_tr, y_dv))
                            lin_dep_ana = LDA(n_components=1)
                            lin_dep_ana = lin_dep_ana.fit(X,Y)
                            X = lin_dep_ana.transform(X)
                            x_tr = X[0:x_tr.shape[0],:]
                            x_dv = X[x_tr.shape[0]:,:]


                        model = create_model(key, args)
                        model = model.fit(x_tr, y_tr)
                        y_pred = model.predict(x_dv)

                        err, ic = accuracy(y_dv, y_pred)
                        probs = model.predict_proba(x_dv)[:,1]
                        _auc = auc(y_dv, probs)
                        result = { 'model': key, 'args': args, 'PCA': pca, 'use_LDA': lda, 'standarized_data': stand, 'CER': err, 'ic': ic, 'auc': _auc }
                        print('{},'.format(result))

    # plot_roc(y_dv, probs, 'SGD(PCA-10)')
