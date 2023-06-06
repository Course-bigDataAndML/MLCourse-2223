#!/usr/bin/env python
# coding: utf-8

from pyspark.ml.feature import VectorAssembler
import numpy as np
import matplotlib.pyplot as plt 

# create a plot of the invariant mass distribution
def plotSignalvsBg(df, variable):

    ## hist is a tuple containing bins and counts foreach bin
    hist_signal, hist_bkg = compute_hist(data=df, feature=variable, target='label', n_bins=50, x_lim=[0,3])

    f, ax = plt.subplots()
    ax.hist(hist_signal[0][:-1], bins=hist_signal[0], weights=hist_signal[1], alpha=0.5, label='signal')
    ax.hist(hist_bkg[0][:-1], bins=hist_bkg[0], weights=hist_bkg[1], alpha=0.5, label='background')
    ax.set_xlabel(variable)
    ax.set_ylabel('counts')
    ax.set_title("Distribution of "+variable)
    ax.legend()
    plt.show()
    f.savefig("SignalvsBackground.pdf", bbox_inches='tight')
    return

def plotSignalvsBgWithPrediction(df, pred_full, variable):
    
    ## hist is a tuple containing bins and counts foreach bin
    hist_signal, hist_bkg = compute_hist(data=df, feature=variable, target='label', n_bins=50, x_lim=[0,3])

    hist_signal_pred, hist_bkg_pred = compute_hist(data=pred_full,
                                               feature=variable, target='prediction',
                                               n_bins=50, x_lim=[0,3])

    hist_signal_pred, hist_bkg_pred = compute_hist(data=pred_full,
                                               feature=variable, target='prediction',
                                               n_bins=50, x_lim=[0,3])
    
    f, ax = plt.subplots()
    ax.hist(hist_signal[0][:-1], bins=hist_signal[0], weights=hist_signal[1],
        alpha=0.5, label='signal')
    ax.hist(hist_bkg[0][:-1], bins=hist_bkg[0], weights=hist_bkg[1],
        alpha=0.5, label='background')

    ax.hist(hist_signal_pred[0][:-1], bins=hist_signal_pred[0], weights=hist_signal_pred[1],
        label='predicted signal', histtype='step',
        linestyle='--', color='green', linewidth=2)
    ax.hist(hist_bkg_pred[0][:-1], bins=hist_bkg_pred[0], weights=hist_bkg_pred[1],
        label='predicted background', histtype='step',
        linestyle='--', color='red', linewidth=2)

    ax.set_xlabel(variable)
    ax.set_ylabel('counts')
    ax.legend()
    ax.set_title("Distribution of "+variable)
    plt.show()
    f.savefig("SignalvsBackgroundPred.pdf", bbox_inches='tight')
    
    return

# for Keras
def plotSignalvsBgWithPrediction2(x_test, y_test, y_pred, variable):
    
    def isSignal(x, y):
        if (y>=0.5):
            return x
        else: 
            return -1.
    
    def isBackground(x, y):
        if (y<0.5):
            return x
        else: 
            return -1.
    
    isSignalNP = np.vectorize(isSignal)
    isBackgroundNP = np.vectorize(isBackground)

    x_signal = isSignalNP(x_test, y_test)
    x_background = isBackgroundNP(x_test, y_test)
    x_signal_pred = isSignalNP(x_test, y_pred[:,0])
    x_background_pred = isBackgroundNP(x_test, y_pred[:,0])

    f, ax = plt.subplots()
    plt.hist(x_signal, bins = 100, range=[0, 3.5], alpha=0.5, label='signal') 
    plt.hist(x_background, bins = 100, range=[0, 3.5], alpha=0.5, label='background') 
    plt.hist(x_signal_pred, bins = 100, range=[0, 3.5], label='predicted signal', histtype='step',
        linestyle='--', color='green', linewidth=2) 
    plt.hist(x_background_pred, bins = 100, range=[0, 3.5], label='predicted background', histtype='step',
        linestyle='--', color='red', linewidth=2) 
    
    plt.title("histogram") 
    ax.set_xlabel(variable)
    ax.set_ylabel('counts')
    ax.legend()
    ax.set_title("Distribution of "+variable)
    plt.show()
    f.savefig("SignalvsBackgroundPred.pdf", bbox_inches='tight')

    return

#for signal vs background plot
def compute_hist(data, feature, target='label', n_bins=100, x_lim=[0,3]):
        
    from pyspark.sql.functions import col
    
    ## Fix the range
    data = data.where((col(feature)<=x_lim[1]) &
                      (col(feature)>=x_lim[0]))
    
    sgn = data.where(col(target)==1.0) 
    bkg = data.where(col(target)==0.0)

    ## Compute the histograms
    bins_sgn, counts_sgn = sgn.select(feature).rdd.flatMap(lambda x: x).histogram(n_bins)
    bins_bkg, counts_bkg = bkg.select(feature).rdd.flatMap(lambda x: x).histogram(n_bins)
    
    return (bins_sgn, counts_sgn), (bins_bkg, counts_bkg)

def plotCorrelation(train, feature): #correlation matrix

    from pyspark.ml.stat import Correlation

    matrix = Correlation.corr(train.select('features'), 'features')
    matrix_np = matrix.collect()[0]["pearson({})".format('features')].values

    import seaborn as sns

    matrix_np = matrix_np.reshape(len(feature),len(feature))

    fig, ax = plt.subplots(figsize=(12,8))
    ax = sns.heatmap(matrix_np, cmap="YlGnBu")
    ax.xaxis.set_ticklabels(feature, rotation=270)
    ax.yaxis.set_ticklabels(feature, rotation=0)
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    plt.show()
    fig.savefig("CorrMatrix.pdf", bbox_inches='tight')
    return

def prepareData(df, split):
    train, test = df.randomSplit([1.-split,split])

    #print('Events for training {}'.format(train.count()))
    #print('Events for validation {}'.format(test.count()))
    
    feature = train.columns
    feature.remove('label')

    #VectorAssembler is a transformer that combines a given list of columns into a single vector column
    assembler = VectorAssembler(inputCols=feature, outputCol='features')
    train = assembler.transform(train)
    test = assembler.transform(test)

    X_train = train.select('features')
    Y_train = train.select('label')
    X_test = test.select('features')
    Y_test = test.select('label')
   
    #newTrain.printSchema()
    
    # need to convert DF to Pandas to use keras
    X_train_2P = X_train.toPandas()
    X_test_2P = X_test.toPandas()
    Y_train_2P = Y_train.toPandas()
    Y_test_2P = Y_test.toPandas()
    
    #X_train_2P.info()

    X = np.array(X_train_2P['features'].tolist())
    y = np.array(Y_train_2P['label'].tolist())

    X_test = np.array(X_test_2P['features'].tolist())
    y_test = np.array(Y_test_2P['label'].tolist())
    
    return X, y, X_test, y_test


# Plot variable (loss, acc) vs. epoch
def plotVsEpoch(history, variable):

    #get_ipython().run_line_magic('matplotlib', 'notebook')
    
    plt.figure()
    plt.plot(history.history[variable], label='train')
    plt.plot(history.history['val_'+variable], label='validation')
    plt.ylabel(variable)
    plt.xlabel('epoch')
    plt.legend(loc='upper right')
    plt.show()
    
    return

# Draw roc curve for Keras
def drawROC2(y_true, y_pred):

    from sklearn.metrics import auc, roc_curve
    fpr, tpr, threshold = roc_curve(y_score=y_pred, y_true=y_true)
    auc = auc(fpr, tpr)

    f = plt.figure()
    plt.plot([0,1], [0,1], '--', color='orange')
    plt.plot(fpr, tpr, label='auc = {:.3f}'.format(auc))
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='lower right')
    plt.grid()    
    plt.show()
    f.savefig("AUC.pdf", bbox_inches='tight')
    
    return

# Draw roc curve
def drawROC(result):

    result_pd = result.select(['label', 'prediction', 'probability']).toPandas()

    result_pd['probability'] = result_pd['probability'].map(lambda x: list(x))
    result_pd['encoded_label'] = result_pd['label'].map(lambda x: np.eye(2)[int(x)])

    y_pred = np.array(result_pd['probability'].tolist())
    y_true = np.array(result_pd['encoded_label'].tolist())    
    
    drawROC2(y_true[:,0], y_pred[:,0])
    
    return

# Draw feature importance (only GBT models)
def drawFeatures(feature, model):
    fig, ax = plt.subplots(figsize=(8,10))
    ax.barh(range(28), model.featureImportances.toArray())
    ax.set_yticks(range(28))
    ax.set_yticklabels(feature)
    ax.set_xlabel('Importances')
    ax.set_title('Feature importance')
    plt.tight_layout()
    plt.show()
    
    return

def printMetrics(evaluator, prediction):

    auc = evaluator.evaluate(prediction, {evaluator.metricName: 'areaUnderROC'})
    print('AUC: %0.3f' % auc)
    # compute TN, TP, FN, and FP
    prediction.groupBy('label', 'prediction').count().show()

    # Calculate the elements of the confusion matrix
    TN = prediction.filter('prediction = 0 AND label = prediction').count()
    TP = prediction.filter('prediction = 1 AND label = prediction').count()
    FN = prediction.filter('prediction = 0 AND label <> prediction').count()
    FP = prediction.filter('prediction = 1 AND label <> prediction').count()

    # calculate accuracy, precision, recall, and F1-score
    accuracy = (TN + TP) / (TN + TP + FN + FP)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    F =  2 * (precision*recall) / (precision + recall)
    print('n precision: %0.3f' % precision)
    print('n recall: %0.3f' % recall)
    print('n accuracy: %0.3f' % accuracy)
    print('n F1 score: %0.3f' % F)
    
    return