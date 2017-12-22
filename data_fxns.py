from collections import Counter, OrderedDict
from drug_objects import drug, review, drug_dataset 
import pandas as pd
import pylab as pl
import numpy as np
from matplotlib.mlab import griddata
from numpy import linspace, meshgrid
import itertools, pickle

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import gridspec
from matplotlib.mlab import griddata

from sklearn.metrics import confusion_matrix


# bin scores together (e.g. 10 bins to 5 bins)
def binning_fxn(_bin_conv, _dataset):
    _bins_l = []
    for _bin in _bin_conv:
        if _bin_conv[_bin] not in _bins_l:
            _bins_l.append(_bin_conv[_bin])

    bins_d = OrderedDict()
    for ik, _bin in enumerate(_bins_l):
        bins_d[_bin] = ik+1

    binned_targets = []
    for target in _dataset.target:
        binned_targets.append(bins_d[_bin_conv[target]])

    _labels = binned_targets
    _target_names = _bins_l
    return _labels, _target_names


# merge drugs with the same generic to be analyzed together
def merge_generics(lst):
    c = Counter
    generics = {}
    listed = []
    for drug in lst:
        if drug.generic in generics:
            generics[drug.generic].append(drug)
        else:
            generics[drug.generic] = [drug] 

    merg = []
    merged_datasets = []
    for drug in generics:
        all_together = generics[drug][0]
        for ik in range(1,len(generics[drug])):
            all_together.reviews = all_together.reviews +generics[drug][ik].reviews
        merg.append(all_together)

    for drug in merg:
        try:
            drug.build_df()
        except:
            continue
        merged_datasets.append(drug_dataset(drug.df))
        print(drug.generic, len(drug.df), len(drug_dataset(drug.df).data))    
    return merg, merged_datasets


# build drug dataset (either for a single drug, a single generic, or all drugs combined)
def build_drug_dataset(set_type, pickle_file, ind = 0):
    _lst = pickle.load(open(pickle_file, 'rb'))
    if set_type == 'single':
        one_drug = _lst[ind]
        one_drug.build_df()
        dataset = drug_dataset(one_drug.df)
    else:
        merged_drugs, merged_datasets = merge_generics(_lst)
        if set_type == 'generic':
            one_drug = merged_drugs[ind]
            dataset = merged_datasets[ind]
        if set_type == 'all':
            _all_together = merged_drugs[0]
            for generic_drug in merged_drugs[1:]:
                _all_together.reviews = _all_together.reviews +generic_drug.reviews
            _all_together.build_df() 
            one_drug = _all_together
            dataset = drug_dataset(one_drug.df)
    return one_drug, dataset
                       

# returns counts of 1-5 predicted scores for each true score bucket 
def filter_count_scores(pick, _y_pred, _y_true, N_CLUSTERS):
    filtered_pred = []
    filtered_true = []
    for ik, score in enumerate(_y_pred):
        if score == pick:
            filtered_pred.append(_y_pred[ik])
            filtered_true.append(_y_true[ik])
            
    c = Counter(filtered_true)
    counts_ls = []
    for ik in np.arange(1,N_CLUSTERS+1):
        if ik in c.keys():
            counts_ls.append(c[ik])
        else:
            counts_ls.append(0)
    return counts_ls


# plot confusion matrix
# adapted from: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(fig, ax, cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues, y_label='True label', x_label='Predicted label' ):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    title_sz = 22
    axis_sz = 20
    tick_sz = 16
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    im1 = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.set_title(title , fontsize=axis_sz)
    tick_marks = np.arange(len(classes))
    ax.set_xticks(tick_marks, classes)#, rotation=45)
    ax.set_yticks(tick_marks, classes)
    
    xtickNames = ax.get_xticklabels()
    ytickNames = ax.get_yticklabels()
    
    plt.setp(ytickNames, rotation=0, fontsize=tick_sz)
    plt.setp(xtickNames, rotation=0, fontsize=tick_sz)
    plt.colorbar(im1,fraction=0.046, pad=0.04)
    
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    ax.set_ylabel(y_label, fontsize=axis_sz)
    ax.set_xlabel(x_label, fontsize=axis_sz)
    
    
def double_confusionPlot(data1, data2, _title, _x_label, _y_label, _target_names):
    figSize = (14, 7)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=figSize, facecolor='w')
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    title_text = _title
    st = fig.suptitle(title_text, fontsize=20)
    st.set_y(0.95)

    cnf_matrix = confusion_matrix(data1, data2)
    np.set_printoptions(precision=2)

    ax1 = plt.subplot(gs[0])
    plot_confusion_matrix(fig, ax1, cnf_matrix, classes=_target_names,
                              title='Confusion matrix, without normalization', x_label = _x_label, y_label = _y_label)

    ax2 = plt.subplot(gs[1])
    plot_confusion_matrix(fig, ax2, cnf_matrix, classes=_target_names, normalize=True,
                              title='Normalized confusion matrix', x_label = _x_label, y_label = _y_label)