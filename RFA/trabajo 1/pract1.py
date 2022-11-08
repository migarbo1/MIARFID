import math
import pickle
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.linear_model import LogisticRegression, SGDClassifier, Perceptron, RidgeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import sys
import numpy as np

def load_data():
    if len(sys.argv)<3:
        print('Usage: %s [<model>] <trdata> <dvdata>' % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) == 3:
        model = None
        tr = np.load(sys.argv[1])['tr']
        dv = np.load(sys.argv[2])['dv']

    if len(sys.argv) == 4:
        file = open(sys.argv[1], mode='rb') 
        model = pickle.Unpickler(file).load()
        tr = np.load(sys.argv[2])['tr']
        dv = np.load(sys.argv[3])['dv']

    return tr, dv, model

def split_datalabels(tr):
    _,L=tr.shape
    D=L-1
    x_tr=tr[:,1:D]
    y_tr=tr[:,-1] 
    return x_tr, y_tr

def lda_transform(x_tr, x_dv, y_tr, y_dv):
    X = np.concatenate((x_tr, x_dv))
    Y = np.concatenate((y_tr, y_dv))
    lin_dep_ana = LDA(n_components=1)
    lin_dep_ana = lin_dep_ana.fit(X,Y)
    X = lin_dep_ana.transform(X)
    x_tr = X[0:x_tr.shape[0],:]
    x_dv = X[x_tr.shape[0]:,:]
    return x_tr, x_dv

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

def accuracy(y_real, y_pred):
    err = (y_real != y_pred).sum()/y_real.shape[0]
    r=1.96*math.sqrt(err*(1-err)/y_real.shape[0])
    print("Dev CER: %.2f%% [%.2f, %.2f]" % (err*100,(err-r)*100,(err+r)*100))
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

def gen_model_concat(x_tr,x_dv,y_tr, y_dv):
    x_tr, x_dv = lda_transform(x_tr, x_dv, y_tr, y_dv)
    X = np.concatenate((x_tr, x_dv))
    Y = np.concatenate((y_tr, y_dv))
    model = create_model('ridge')
    model = model.fit(X, Y)
    y_pred = model.predict(x_dv)
    _,_ = accuracy(y_dv, y_pred)
    save_model(model, 'model_pm_trdv.sav')

if __name__ == '__main__':
    tr, dv, model = load_data()
    x_tr, y_tr = split_datalabels(tr)
    x_dv, y_dv = split_datalabels(dv)

    x_tr, x_dv = lda_transform(x_tr, x_dv, y_tr, y_dv)

    gen_save = False
    if model == None:
        gen_save = True
        model = create_model('ridge')
        model = model.fit(x_tr, y_tr)
    y_pred = model.predict(x_dv)

    err, ic = accuracy(y_dv, y_pred)
    probs = model.predict_proba(x_dv)[:,1]
    _auc = auc(y_dv, probs)
    print(_auc*100)

    if gen_save: 
        save_model(model, 'model_pm_tr.sav')
        gen_model_concat(x_tr,x_dv,y_tr, y_dv)

    plot_roc(y_dv, probs, 'result')