import pandas as pd

data = pd.read_csv('../../../../rsc/learn/part 2/013/history.csv', sep=';')

def f1():
    em_data = data['Emerging Markets'].map(lambda e: float(e[:len(e) - 1]) / 100)
    print(em_data.mean())
    print(em_data.median())
    print(em_data.mode())
    print([em_data.quantile(i) for i in [0.1, 0.9]])


def f2():
    ed_data = data['Event Driven'].map(lambda e: float(e[:len(e) - 1]) / 100)
    print(ed_data.max() - ed_data.min())
    print(ed_data.mad())
    print(ed_data.var())
    print(ed_data.std())


def f3():
    rv_data = data['Relative Value'].map(lambda e: float(e[:len(e) - 1]) / 100)
    fia_data = data['Fixed Income Arbitrage'].map(lambda e: float(e[:len(e) - 1]) / 100)
    import matplotlib.pyplot as plt
    '''
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    ax1.plot(rv_data, color='k')
    ax1.set_ylabel('RV profit')
    ax1.set_title('RV')
    ax2.plot(fia_data, color='g')
    ax2.set_ylabel('Fixed Income Arbitrage profit')
    ax2.set_title('FIA')
    '''
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.plot(rv_data, '--*', label='RV', color='k')
    ax.plot(fia_data, '-+', label='FIA', color='g')
    ax.legend(loc='best')
    
    print(rv_data.describe())
    print(fia_data.describe())


def f4():
    print(data.describe())


if __name__ == '__main__':
    f3()