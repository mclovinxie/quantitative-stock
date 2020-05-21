from datetime import datetime

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.stats.anova as anova
from statsmodels.formula.api import ols


def f1():
    data = {
        'D1': [16, 14, 10, 9, 15, 14, 8, 6, 13, 9],
        'D2': [20, 15, 16, 12, 11, 10, 6, 7, 9, 11],
        'D3': [10, 11, 13, 11, 9, 8, 13, 11, 6, 7],
        'D4': [8, 11, 6, 7, 7, 9, 12, 15, 10, 13],
        'D5': [7, 6, 8, 8, 13, 6, 10, 7, 5, 9]
        }
    data = {
        'District': ['D1'] * 10 + ['D2'] * 10 + ['D3'] * 10 + ['D4'] * 10 + ['D5'] * 10,
        'Count': data['D1'] + data['D2'] + data['D3'] + data['D4'] + data['D5']
        }
    df = pd.DataFrame(data, index=[i for i in range(50)])
    model = ols('Count ~ C(District)', data=df).fit()
    table1 = anova.anova_lm(model)
    print(table1)


def f2():
    data = {
        'A': [0.0312, 0.0245, -0.0156, 0.0113, 0.0055],
        'B': [-0.0224, 0.0056, 0.0133, -0.0105, 0.0141],
        'C': [0.0153, 0.0241, -0.0188, -0.0031, -0.0065],
        'D': [0.0105, 0.0186, -0.0081, 0.0234, 0.0033],
        }
    data = {
        'Proposal': ['A'] * 5 + ['B'] * 5 + ['C'] * 5 + ['D'] * 5,
        'Variance': data['A'] + data['B'] + data['C'] + data['D']
        }
    df = pd.DataFrame(data, index=[i for i in range(20)])
    model = ols('Variance ~ C(Proposal)', data=df).fit()
    table1 = anova.anova_lm(model)
    print(table1)


def f3():
    data = {
        'A': [48, 38, 45, 47, 40],
        'B': [26, 35, 30, 29, 31],
        'C': [38, 40, 49, 51, 51]
        }
    ttest = stats.ttest_rel(data['B'], data['C'])
    print(ttest)
    if ttest.pvalue > 0.05:
        print('eq')
    else:
        print('not eq')
    
    data = {
        'Factory': ['A'] * 5 + ['B'] * 5 + ['C'] * 5,
        'Lifespan': data['A'] + data['B'] + data['C']
        }
    df = pd.DataFrame(data, index=[i for i in range(15)])
    model = ols('Lifespan ~ C(Factory)', data=df).fit()
    table1 = anova.anova_lm(model)
    print(table1)


if __name__ == '__main__':
    f3()
