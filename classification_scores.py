
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from pyriemann.classification import MDM
from pyriemann.estimation import ERPCovariances
from braininvaders2012.dataset import BrainInvaders2012
from tqdm import tqdm
import numpy as np
import mne
import joblib
"""
=============================
Classification of the trials
=============================

This example shows how to extract the epochs from the dataset of a given
subject and then classify them using Machine Learning techniques using
Riemannian Geometry. 

"""
# Authors: Pedro Rodrigues <pedro.rodrigues01@gmail.com>
#
# License: BSD (3-clause)

import warnings
warnings.filterwarnings("ignore")

# define the dataset instance
dataset = BrainInvaders2012(Training=True)

scr = {}
# get the data from subject of interest
for subject in dataset.subject_list:

	data = dataset._get_single_subject_data(subject)
	raw = data['session_1']['run_training']

	# filter data and resample
	fmin = 1
	fmax = 24
	raw.filter(fmin, fmax, verbose=False)

	# detect the events and cut the signal into epochs
	events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
	event_id = {'NonTarget': 1, 'Target': 2}
	epochs = mne.Epochs(raw, events, event_id, tmin=0.0, tmax=1.0, baseline=None, verbose=False, preload=True)
	epochs.pick_types(eeg=True)

	# get trials and labels
	X = epochs.get_data()
	y = events[:, -1]
	y = LabelEncoder().fit_transform(y)

	# cross validation
	skf = StratifiedKFold(n_splits=5)
	clf = make_pipeline(ERPCovariances(estimator='lwf', classes=[1]), MDM())
	scr[subject] = cross_val_score(clf, X, y, cv=skf, scoring='roc_auc').mean()

	# print results of classification
	print('subject', subject)
	print('mean AUC :', scr[subject])

	#####

filename = './classification_scores.pkl'
joblib.dump(scr, filename)	

with open('classification_scores.txt', 'w') as the_file:
    for subject in scr.keys():
        the_file.write('subject ' + str(subject).zfill(2) + ' :' + ' {:.2f}'.format(scr[subject]) + '\n')


