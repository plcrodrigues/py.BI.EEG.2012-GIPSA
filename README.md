# Brain Invaders 2012 Dataset

Repository with basic scripts for using the Brain Invaders 2012a dataset developed at GIPSA-lab. The dataset files and their documentation are all available at 

https://zenodo.org/record/2649069

The code of this repository was developed in **Python 3** using MNE-Python [1, 2] as tool for the EEG processing.

The package can be downloaded from `PyPi`:

```
pip install braininvaders2012
```

For contributors, it will be necessary to clone the repository on your local machine using git. To make things work, you might need to install some packages. They are all listed in the `requirements.txt` file and can be easily installed by doing

```
pip install -r requirements.txt
```

in your command line. 

Then, to ensure that your code finds the right scripts whenever you do `import braininvaders2012`, you should also do

```
python setup.py develop
```

Note that you might want to create a *virtual environment* before doing all these installations (e.g. using Anaconda).

# References

[1] Gramfort et al. "MNE software for processing MEG and EEG data" [DOI](https://doi.org/10.1016/j.neuroimage.2013.10.027)

[2] Gramfort et al. "MEG and EEG data analysis with MNE-Python" [DOI](https://doi.org/10.3389/fnins.2013.00267)

# How to cite?

If you like our work, please cite the following paper:

G. F. P. Van Veen, A. Barachant, A. Andreev, G. Cattan, P. L. Coelho Rodrigues, and M. Congedo, ‘Building Brain Invaders: EEG data of an experimental validation’, GIPSA-lab, Research Report 1, mai 2019. [Online]. Available: https://hal.archives-ouvertes.fr/hal-02126068
