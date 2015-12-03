# source: https://kaggle2.blob.core.windows.net/forum-message-attachments/88846/2811/crimeSF_NN_logodds.html?sv=2012-02-12&se=2015-12-03T21%3A30%3A37Z&sr=b&sp=r&sig=5BjDpVtU4WLtPKkqjyD%2Brp83e9%2FCy0blRwsmPFqsx7o%3D
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pylab as plt
from sklearn import preprocessing
from matplotlib.colors import LogNorm

iterate_color = ['red', 'orange', 'yellow', 'blue', 'cyan', 'magenta', 'green', 'darkgreen', 'purple', 'pink']
key_daysofweek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def main():
    trainDF=pd.read_csv("train.csv")
    xy_scaler=preprocessing.StandardScaler()
    xy_scaler.fit(trainDF[["X","Y"]])
    trainDF[["X","Y"]]=xy_scaler.transform(trainDF[["X","Y"]])
    trainDF=trainDF[abs(trainDF["Y"])<100]
    trainDF.index=range(len(trainDF))

    # byRaw(trainDF)
    # byPdDistrict(trainDF)
    # byCategoryThenPdDistrict(trainDF)
    # byDayOfWeek(trainDF)
    byCategoryThenDayOfWeek(trainDF)

def byRaw(trainDF):
    plt.plot(trainDF["X"],trainDF["Y"],'.')
    plt.show()

def byPdDistrict(trainDF):
    groups = trainDF.groupby('PdDistrict')
    for name, group in groups:
        plt.plot(group.X, group.Y, '.')
    plt.show()

def byCategoryThenPdDistrict(trainDF):
    plt.figure(figsize=(20, 20))
    groupsC = trainDF.groupby('Category')
    ii = 0
    # category_to_plot = ['ASSAULT', 'EMBEZZLEMENT', 'EXTORTION']
    category_to_plot = map(lambda x: x[0], groupsC)[0:15]
    for nameC, groupC in groupsC:
        if nameC in category_to_plot:
            plt.subplot((len(category_to_plot)+4)/5, 5, ii)
            color = 0
            groupsPd = groupC.groupby('PdDistrict')
            for namePd, groupPd in groupsPd:
                plt.plot(groupPd.X, groupPd.Y, '.', color=iterate_color[color])
                # plt.plot(groupPd.X, groupPd.Y, '.', color=iterate_color[color], markersize=20)
                color = (color+1) % len(iterate_color)
            plt.title(nameC, fontsize=30)
            plt.ylim([-0.15, 0.15])
            ii+=1
    plt.show()

def byDayOfWeek(trainDF):
    plt.figure(figsize=(20, 20))
    groups = trainDF.groupby('DayOfWeek')
    ii = 1;
    key_daysofweek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for name, group in sorted(groups, key=lambda x: key_daysofweek.index(x[0])):
        plt.subplot(2, 4, ii)
        histo, xedges, yedges = np.histogram2d(np.array(group.X),np.array(group.Y), bins=(100, 100))
        myextent  =[xedges[0],xedges[-1],yedges[0],yedges[-1]]
        plt.imshow(histo.T,origin='low',extent=myextent,interpolation='nearest',aspect='auto',norm=LogNorm())
        plt.title(name, fontsize=30)
        ii+=1
    plt.suptitle('All Crime Categories on Each Day of Week', fontsize=40)
    plt.show()

def byCategoryThenDayOfWeek(trainDF):
    plt.figure(figsize=(20, 20))
    groupsC = trainDF.groupby('Category')
    ii = 1
    # category_to_plot = ['ASSAULT', 'EMBEZZLEMENT', 'EXTORTION']
    category_to_plot = map(lambda x: x[0], groupsC)[0:15]
    for nameC, groupC in groupsC:
        if nameC in category_to_plot:
            ax = plt.subplot((len(category_to_plot)+4)/5, 5, ii)
            counts = groupC.DayOfWeek.value_counts().to_dict()
            counts_values = map(lambda x: counts[x], sorted(counts.keys(), key=lambda x: key_daysofweek.index(x)))
            ax.bar(map(lambda x:key_daysofweek.index(x), key_daysofweek), counts_values)
            ax.set_xticks(map(lambda x:key_daysofweek.index(x), key_daysofweek))
            ax.set_xticklabels(map(lambda x: x[0], key_daysofweek))
            plt.title(nameC, fontsize=30)
            ii+=1
    plt.show()

    
if __name__ == "__main__":
  # execute only if run as a script
  main()
