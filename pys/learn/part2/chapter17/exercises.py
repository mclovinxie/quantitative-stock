from datetime import datetime

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.stats.anova as anova
import statsmodels.api as sm


def f1():
    X = [i for i in range(1952, 2013, 4)]
    Y = [29.3, 28.8, 28.5, 28.4, 29.4, 27.6, 27.7, 27.7] + [27.8, 27.4, 27.8, 27.1, 27.3, 27.1, 27.0, 27.5]
    plt.scatter(X, Y)
    plt.xlabel('YEAR')
    plt.ylabel('MINUTES')
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    print(model.summary())
    print(model.predict(sm.add_constant([i for i in range(2016, 2016 + 4 * 1 + 1, 4)])))


def f5():
    X = [20, 25, 30, 35, 40, 50, 60, 65, 70, 75, 80, 90]
    SX = [i ** 2 for i in X]
    Y = [1.81, 1.7, 1.65, 1.55, 1.48, 1.4, 1.3, 1.26, 1.24, 1.21, 1.2, 1.18]
    plt.scatter(X, Y)
    plt.xlabel('ACCOUNT')
    plt.ylabel('PRICE')
    
    df = pd.DataFrame({
        'X': X,
        'SX': SX,
        'Y': Y
        }, index=[i for i in range(1, 13)])
    model = sm.OLS(df['Y'], sm.add_constant(df.iloc[:, 0:2])).fit()
    print(model.summary())
    print(model.predict(sm.add_constant(pd.DataFrame({'X': [95, 100], 'SX': [9025, 10000]}).iloc[:, :])))
    print(df.iloc[:, 0:2].corr())
    
    model = sm.OLS(df['Y'], sm.add_constant(df['X'])).fit()
    print(model.summary())
    print(model.predict(sm.add_constant(pd.DataFrame({'X': [95, 100]}).iloc[:, :])))
    
    model = sm.OLS(df['Y'], sm.add_constant(df['SX'])).fit()
    print(model.summary())
    print(model.predict(sm.add_constant(pd.DataFrame({'SX': [9025, 10000]}).iloc[:, :])))


if __name__ == '__main__':
    f5()
