from datetime import datetime

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('../../../../rsc/learn/part 2/013/history.csv', sep=';')
data['date'] = data['date'].map(lambda e: datetime.strptime(e, '%d/%m/%Y'))


def f1():
    pass


def f2():
    em_data = data['Emerging Markets'].map(lambda e: float(e[:len(e) - 1]) / 100)
    pos_em = em_data[em_data>0]
    neg_em = em_data[em_data<0]
    print(len(em_data))
    print(len(pos_em))
    print(len(neg_em))
    print(len(pos_em) / len(em_data))
    
    lt_2010 = data[data.date < '2010']['Emerging Markets'].map(lambda e: float(e[:len(e) - 1]) / 100)
    pos_em_2010 = lt_2010[lt_2010>0]
    print(len(lt_2010))
    print(len(pos_em_2010))
    p = len(pos_em_2010) / len(lt_2010)
    print(p)
    print(1 - stats.binom.cdf(6, 12, p))


def f3():
    nd_1 = np.random.normal(size=100)
    nd_1.sort()
    nd_2 = np.random.normal(scale=0.5, size=100)
    nd_2.sort()
    nd_3 = np.random.normal(scale=2.0, size=100)
    nd_3.sort()
    nd_4 = np.random.normal(loc=2.0, scale=1.0, size=100)
    nd_4.sort()
    
    fig, ax = plt.subplots(1, 1)
    ax.plot(nd_1, stats.norm.pdf(nd_1), '-*', label='A', color='k')
    ax.plot(nd_2, stats.norm.pdf(nd_2, 0.0, 0.5), '-+', label='B', color='y')
    ax.plot(nd_3, stats.norm.pdf(nd_3, 0.0, 2.0), '--', label='C', color='r')
    ax.plot(nd_4, stats.norm.pdf(nd_4, 2.0, 1.0), '--*', label='D', color='g')
    ax.legend(loc='best')
    
    '''
    plt.plot(nd_1, stats.norm.pdf(nd_1, 0.0, 1.0), label='A')
    plt.plot(nd_2, stats.norm.pdf(nd_2, 0.0, 0.5), label='B')
    plt.plot(nd_3, stats.norm.pdf(nd_3, 0.0, 2.0), label='C')
    plt.plot(nd_4, stats.norm.pdf(nd_4, 2.0, 1.0), label='D')
    plt.legend()
    '''


def f5():
    def fx(x):
        if x <= 0:
            return 0
        return np.e**(-x / 2) / 2
    
    def gen():
        xs, ys = [], []
        i, d, sm = -1, 1, 0.0
        while i <= 50:
            pd = fx(i)
            if sm + pd >= 1.0:
                break
            sm += pd
            xs.append(i)
            ys.append(pd)
            i += d
        if sm < 1.0:
            xs.append(i + d)
            ys.append(1.0 - sm)
        return xs, ys
    
    X, Y = gen()
    plt.plot(X, Y, label='LN')


def f6():
    def fx(x):
        if x <= 0:
            return 0
        return ((np.e**((np.log([x])[0]) ** 2 / 2)) / (x * (np.pi * 2) ** 0.5))
    
    def gen():
        xs, ys = [], []
        i, d, sm = -1, 1, 0.0
        while i <= 50:
            pd = fx(i)
            if sm + pd >= 1.0:
                break
            sm += pd
            xs.append(i)
            ys.append(pd)
            i += d
        if sm < 1.0:
            xs.append(i + d)
            ys.append(1.0 - sm)
        return xs, ys
    
    X, Y = gen()
    plt.plot(X, Y, label='LN')


if __name__ == '__main__':
    f6()
