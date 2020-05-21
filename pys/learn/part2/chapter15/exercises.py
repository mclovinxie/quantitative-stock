from datetime import datetime

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('../../../../rsc/learn/part 2/013/history.csv', sep=';')


def f1():
    A = [6.683, 6.678, 6.767, 6.692, 6.672, 6.678]
    B = [6.661, 6.664, 6.668, 6.666, 6.665]
    print(stats.t.interval(0.9, len(A) - 1, np.mean(A), stats.sem(A)))
    print(stats.t.interval(0.9, len(B) - 1, np.mean(B), stats.sem(B)))


def f2():
    X = [5.9, 7.3, 6.6, 5.8, 5.7, 5.3, 5.9, 7, 6.5]
    print(stats.t.interval(0.95, len(X) - 1, np.mean(X), stats.sem(X)))


def f7():
    A = [0.225, 0.262, 0.217, 0.24, 0.23, 0.229, 0.235, 0.217]
    B = [0.209, 0.205, 0.196, 0.21, 0.202, 0.207, 0.224, 0.223]
    ttest = stats.ttest_ind(A, B)
    print(ttest)
    if ttest.pvalue > 0.05:
        print('eq')
    else:
        print('not eq')


def f8():
    A = [168, 180, 181, 172, 165, 160, 166, 165, 177, 174]
    B = [169, 170, 176, 173, 166, 167, 166, 173, 171, 170]
    ttest = stats.ttest_ind(A, B)
    print(ttest)
    if ttest.pvalue > 0.05:
        print('eq')
    else:
        print('not eq')


def f10():
    em_data = data['Emerging Markets'].map(lambda e: float(e[:len(e) - 1]) / 100)
    gm_data = data['Global Macro'].map(lambda e: float(e[:len(e) - 1]) / 100)
    ttest = stats.ttest_ind(em_data, gm_data)
    print(ttest)
    if ttest.pvalue > 0.05:
        print('eq')
    else:
        print('not eq')


def f11():
    em_data = data['Emerging Markets'].map(lambda e: float(e[:len(e) - 1]) / 100)
    gm_data = data['Global Macro'].map(lambda e: float(e[:len(e) - 1]) / 100)
    ttest = stats.ttest_rel(em_data, gm_data)
    print(ttest)
    if ttest.pvalue > 0.05:
        print('eq')
    else:
        print('not eq')


if __name__ == '__main__':
    f11()
