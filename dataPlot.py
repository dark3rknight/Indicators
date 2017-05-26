import matplotlib.pyplot as plt

def multiAxis_LabeledPlot(vals1, label1, vals2 = None, label2 = None, vals3 = None, label3 = None, vals4 = None, label4 = None):
    plt.close()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(vals1, color = 'darkred', linewidth = 0.6, label = label1)
    if vals2 != None:
        ax1.plot(vals2, color = 'blue', linewidth = 0.6, label = label2)
    if vals3 != None:
       ax1.plot(vals3, color = 'green', linewidth = 0.6, label = label3)
    if vals4 != None:
        ax4 = ax1.twinx()
        ax4.plot(vals4, color = 'salmon', linewidth = 0.6, label = label4)
    ax1.grid(True)
    ax1.legend()
    plt.legend()
    plt.show()

def multiAxisplot(vals1, vals2 = None, vals3 = None, vals4 = None):
    plt.close()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(vals1, color = 'darkred', linewidth = 0.6)
    if vals2 != None:
        ax1.plot(vals2, color = 'blue', linewidth = 0.6)
    if vals3 != None:
       ax1.plot(vals3, color = 'green', linewidth = 0.6)
    if vals4 != None:
        ax4 = ax1.twinx()
        ax4.plot(vals4, color = 'salmon', linewidth = 0.6)
    plt.show()
