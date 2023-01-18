import pandas as pd
import numpy as np

from neuroHarmonize import harmonizationLearn


def corr_matrix_harmonization(corr, cov, smooth_terms: list = [], v: bool = 0):
    """
    Harmonization with ComBat over correlation matrix and their covariables.
    ComBat used: https://github.com/rpomponio/neuroHarmonize

    :param corr: Correlation matrix this can be 2D (rows, columns) or 3D (subjects, rows, columns)
    :param cov: pandas.DataFrame with the covariables. All covariates must be encoded numerically
     (you must handle categorical covariates in a pre-processing step, see pandas.get_dummies).
     The DataFrame must also contain a single column called "SITE" with labels that identify
     sites (the labels in "SITE" need not be numeric)
    :param smooth_terms: specifying nonlinear co variate effects, it's a list with the terms.
    For example, you may want to specify age as a nonlinear term in the harmonization model,
     if age exhibits nonlinear relationships with brain volumes or any variable smooth_terms=['AGE'].
    :param v: bool, version to use in the correlation matrix harmonization.
    {0: takes the full matrix, 1: takes only the triangular and the other values are set to 0}
    :return: Harmonized Correlation Matrix, the same dimension as the input
    """
    subj_corr = np.empty((0, 0), float)
    m_flat_row = np.zeros((0, corr.shape[1]*corr.shape[1]))
    for i in range(len(corr)):
        if v:
            # Only select a triangular matrix and the other values is 0
            #matriz_triu = np.triu(corr, k=0)
            matriz_tril = np.tril(corr[i], k=0)
            matriz_diag = np.diag(np.diag(corr[i]))
            matriz_dim = corr[i].shape[0]
            m_flat_column = matriz_tril.flatten()
            m_flat_row = np.vstack((m_flat_row, m_flat_column.reshape(1, -1)))
        else:
            # Full matrix
            matriz_column = corr[i].flatten()
            matriz_dim = corr[i].shape[0]
            matriz_row = matriz_column.reshape(1, -1)
            m_flat_row = np.vstack((m_flat_row, matriz_row))
    if corr.shape[1] <= 10:
        # ComBat don't use Empirical Bayes when the harmonization is made with a small number of features
        if smooth_terms:
            my_model, my_data_adj = harmonizationLearn(m_flat_row, cov, smooth_terms, eb=False)
        else:
            my_model, my_data_adj = harmonizationLearn(m_flat_row, cov, eb=False)
    else:
        # ComBat uses Empirical Bayes to fit a prior distribution for the site effects for each site
        if smooth_terms:
            my_model, my_data_adj = harmonizationLearn(m_flat_row, cov, smooth_terms)
        else:
            my_model, my_data_adj = harmonizationLearn(m_flat_row, cov)
    if v:
        matriz_orig = m_flat_row.reshape(matriz_dim, matriz_dim)
        matriz_orig = matriz_orig + matriz_orig.T - matriz_diag
    else:
        matriz_orig = my_data_adj.reshape(corr.shape[0], corr.shape[1], corr.shape[2])

    return my_model, matriz_orig
