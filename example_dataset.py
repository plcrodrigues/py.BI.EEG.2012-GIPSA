
from scipy.io import loadmat
import numpy as np
import mne

from braininvaders2012.dataset import BrainInvaders2012
from sklearn.externals import joblib

dataset = BrainInvaders2012(Training=True, Online=False)

# get the data from subject of interest
for subject in dataset.subject_list:

	sessions = dataset._get_single_subject_data(subject)

	for session in sessions.keys():

		for run in sessions[session].keys():

			raw = sessions[session][run]

			# filter data and resample from 512 Hz to 128 Hz
			fmin = 1
			fmax = 24
			raw.filter(fmin, fmax, verbose=False)
			raw.resample(sfreq=128, verbose=False)

			# detect the events and cut the signal into epochs
			events = mne.find_events(raw=raw, shortest_event=1, verbose=False)
			event_id = {'NonTarget': 1, 'Target': 2}
			epochs = mne.Epochs(raw, events, event_id, tmin=0.0, tmax=0.6, baseline=None, verbose=False, preload=True)
			epochs.pick_types(eeg=True)

			# get epochs and their labels
			X = epochs.get_data()
			y = events[:, -1]

			# saving epochs into a pickle file
			path_folder = '/research/vibs/Pedro/datasets/BrainInvaders2012/'		
			path_file = path_folder + 'subject_' + str(subject).zfill(2) + '_' + session + '.pkl'
			data = {}
			data['epochs'] = X
			data['labels'] = y
			data['chnames'] = epochs.ch_names

			print(path_file)
			joblib.dump(data, path_file)