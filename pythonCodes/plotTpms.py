#!/usr/bin/python

# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import csv
import os

import matplotlib.animation as animation
path = '/Users/jav/'
plt.ion()  # tell matplotlib you want interactive mode to plot data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
date = []
time = []
temp = []


def DownloadCSV():
    os.system('scp -i ' + path + 'system_key root@192.168.3.250:/sdcard/tpms* ' + path + 'mss/myCodes/csv/')

def animate(i,time, temp):
  with open(path+'mss/myCodes/csv/tpms1.csv', 'r') as csvfile:
   plots = csv.reader(csvfile, delimiter=',')
   for row in plots:
       if row[0]!= '':
        #print(row)
        string = row[0]
        txt = string.split()
      # date.append(txt[0])
        time.append(row[0])
        temp.append(row[1])
        time = time[-20:]
        temp = temp[-20:]
        ax.clear()
        ax.plot(time, temp)
        plot()


def plot():
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

def main():
    print("###################################################")
    #DownloadCSV()
    #extract_values()

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(time, temp), interval=1000)
    plt.show()
    plt.pause(60)



if __name__ == '__main__':
    main()