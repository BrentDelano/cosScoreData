# Written by Brent Delano
# 4/7/2020
# Uses the cos_score.py and binning_ms.py files to find similarities between spectra

import pyteomics
from pyteomics import mgf
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import spectrum_alignment
import cos_score
import binning_ms
import copy

sys.path.insert(1, './lib')

# reads in mgf files that have been passed in as a list of strings of file paths, or a single file path as a string
# returns four lists: 
#	spectra: lists spectra as lists of tuples [first value = m/z ratio, second value = intensity)
#	masses: a list of lists of the masses of the spectra
#	mzs: a list of lists of the m/z ratios of the spectra
#	intensities: a list of lists of the intensities of the spectra
def read_mgfs(mgfs):
	cosine_mgf = cos_score.read_mgf_cosine(mgfs)
	binning_mgf = binning_ms.read_mgf_binning(mgfs)
	spectra, masses, mzs, intensities, identifiers = cosine_mgf[0], cosine_mgf[1], binning_mgf[0], binning_mgf[1], binning_mgf[2]
	return spectra, masses, mzs, intensities, identifiers


# uses binning_ms.py and takes the m/z ratios from the spectra data in an mgf file and bins them together, returning a matrix of binned spectra
# read binning_ms.create_bins and binning_ms.create_peak_matrix for an in depth documentation of this function
def bin_spectra(mgfs, binsize):
	mgf_data = binning_ms.read_mgf_binning(mgfs)
	mzs, intensities, identifiers = mgf_data[0], mgf_data[1], mgf_data[2]
	bins = binning_ms.create_bins(mzs, binsize)
	filled_bins = binning_ms.create_peak_matrix(mzs, intensities, identifiers, bins)
	return filled_bins


# uses cos_score.py to calculate the cosine scores of all the spectra passed in, creating a .txt file with a nxn matrix of cosine scores (n = # of spectra)
# also requires the mass of all the spectra
# read cos_score.calc_cos_scores() for an in depth documentation of this function
def calc_cos_scores(mgfs, specific_spectra=0):
	mgf_data = cos_score.read_mgf_cosine(mgfs, specific_spectra)
	spectra, masses = mgf_data[0], mgf_data[1]
	cos_score.calc_cos_scores(spectra, masses)


# for testing
def main():
	mgf_data = read_mgfs(['./data/HMDB.mgf', './data/agp500.mgf', './data/agp3k.mgf'])
	spectra, masses, mzs, intensities, identifiers = mgf_data[0], mgf_data[1], mgf_data[2], mgf_data[3], mgf_data[4]

	# print(bin_spectra(mzs, intensities, identifiers, 1))
	# calc_cos_scores(spectra, masses)

if __name__ == "__main__":
	main()
