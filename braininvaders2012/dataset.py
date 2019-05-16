#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import mne
import numpy as np
from braininvaders2012 import download as dl
import os
import glob
import zipfile
import yaml
from scipy.io import loadmat

BI2012a_URL = 'https://zenodo.org/record/2649069/files/'

class BrainInvaders2012():
    '''
    We describe the experimental procedures for a dataset that we have made publicly available at 
    https://doi.org/10.5281/zenodo.2649006 in mat and csv formats. This dataset contains 
    electroencephalographic (EEG) recordings of 25 subjects testing the Brain Invaders 
    (Congedo, 2011), a visual P300 Brain-Computer Interface inspired by the famous vintage video 
    game Space Invaders (Taito, Tokyo, Japan). The visual P300 is an event-related potential 
    elicited by a visual stimulation, peaking 240-600 ms after stimulus onset. EEG data were recorded
    by 16 electrodes in an experiment that took place in the GIPSA-lab, Grenoble, France, in 2012 
    (Van Veen, 2013 and Congedo, 2013). A full description of the experiment is available 
    https://hal.archives-ouvertes.fr/hal-02126068. Python code for manipulating the data is 
    available at https://github.com/plcrodrigues/py.BI.EEG.2012-GIPSA.The ID of this dataset is
    BI.EEG.2012-GIPSA.

    **Full description of the experiment and dataset**
    https://hal.archives-ouvertes.fr/hal-02126068

    **Link to the data**
    https://doi.org/10.5281/zenodo.2649006
 
    **Authors**
    Principal Investigator: B.Sc. Gijsbrecht Franciscus Petrus van Veen
    Technical Supervisors: Ph.D. Alexandre Barachant, Eng. Anton Andreev, Eng. Grégoire Cattan, Eng. Pedro. L. C. Rodrigues
    Scientific Supervisor: Ph.D. Marco Congedo

    **ID of the dataset**
    BI.EEG.2012-GIPSA
    '''

    def __init__(self, Training=True, Online=False):

        self.training = Training
        self.online = Online
        self.subject_list = list(range(1, 25 + 1))

    def _get_single_subject_data(self, subject):
        """return data for a single subject"""

        file_path_list = self.data_path(subject)
        sessions = {}
        for file_path in file_path_list:

            session_name = 'session_1'
            condition = file_path.split('_')[-1].split('.')[0].split(os.sep)[-1]
            run_name = 'run_' + condition

            chnames = ['F7',
                       'F3',
                       'Fz',
                       'F4',
                       'F8',
                       'T7',
                       'C3',
                       'Cz',
                       'C4',
                       'T8',
                       'P7',
                       'P3',
                       'Pz',
                       'P4',
                       'P8',
                       'O1',
                       'O2',
                       'STI 014']
            chtypes = ['eeg'] * 17 + ['stim']               

            X = loadmat(file_path)[condition].T
            S = X[1:18,:]
            stim = (X[18,:] + X[19,:])[None,:]
            X = np.concatenate([S, stim])

            info = mne.create_info(ch_names=chnames, sfreq=128,
                                   ch_types=chtypes, montage='standard_1020',
                                   verbose=False)
            raw = mne.io.RawArray(data=X, info=info, verbose=False)

            # get rid of the Fz channel (it is the ground)
            raw.info['bads'] = ['Fz']
            raw.pick_types(eeg=True, stim=True)

            sessions[session_name] = {}
            sessions[session_name][run_name] = raw

        return sessions

    def data_path(self, subject, path=None, force_update=False,
                  update_path=None, verbose=None):

        if subject not in self.subject_list:
            raise(ValueError("Invalid subject number"))

        # check if has the .zip
        url = BI2012a_URL + 'subject_' + str(subject).zfill(2) + '.zip'
        path_zip = dl.data_path(url, 'BRAININVADERS2012')
        path_folder = path_zip.strip('subject_' + str(subject).zfill(2) + '.zip')

        # check if has to unzip
        if not(os.path.isdir(path_folder + 'subject{:d}/'.format(subject))):
            print('unzip', path_zip)
            zip_ref = zipfile.ZipFile(path_zip, "r")
            zip_ref.extractall(path_folder)

        subject_paths = []

        # filter the data regarding the experimental conditions
        if self.training:
            subject_paths.append(path_folder + 'subject_' + str(subject).zfill(2) + '/training.mat')
        if self.online:
            subject_paths.append(path_folder + 'subject_' + str(subject).zfill(2) + '/online.mat')

        return subject_paths
