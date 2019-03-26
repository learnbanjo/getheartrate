#
#Calculating Average Heart Beat Rate from ECG data
#Project Reference: http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/
#

import wfdb as wd
import matplotlib.pyplot as plt
import numpy as np
import glob, os



for filename in glob.glob("*.hea"):

    # Step 1: Getting Data
    # Data Source: https://www.physionet.org/physiobank/database/aami-ec13/

    #ecgfilename = 'aami3c'
    ecgfilename = os.path.splitext(filename)[0]
    signals, fields = wd.rdsamp(ecgfilename)

    samplingFrequency = fields['fs']
    signalLen = len(signals)

    plt.clf()
    plt.title("Heart Rate Signal " + ecgfilename)
    plt.plot(signals)
    plt.pause(1)

    plt.title("Heart Rate Signal " + ecgfilename + " Zoomed-In 8X")
    for x in range(1, 28, 1):
        plt.xlim(int(signalLen * x / 64), int(signalLen * (64-x) / 64))
        plt.pause(0.001)

    #step 2: calculate moving average

    #moving average, source:  https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy

    def moving_average(a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    windowTime = 0.75
    windowSize = int(windowTime * samplingFrequency)
    averageFactor = 1.2

    secPerMin = 60
    maxHeartRate = 220
    resolutionFactor = 10

    minPauseTime = int(secPerMin/maxHeartRate/resolutionFactor*samplingFrequency)
    signalAverage = np.mean(signals)

    movingAverageWindow = moving_average(signals, windowSize)

    movingAverage1 = np.full(int(windowSize/2), signalAverage)
    movingAverage2 = np.append(movingAverage1, movingAverageWindow)
    movingAverage3 = np.append(movingAverage2, np.full(int(windowSize/2), signalAverage))
    movingAverage3 = movingAverage3 * averageFactor

    plt.pause(1)
    plt.title("Heart Rate Signal " + ecgfilename + " /w Moving Average") #The title of our plot
    plt.plot(movingAverage3, color='green')
    plt.pause(2)

    #step 3: calculate picks for area that's higher than moving average

    windowValues = []
    peakPoints = []
    for i, signalValue in enumerate(signals):
        if signalValue > movingAverage3[i]:
            if len(windowValues) == 0:
                windowStartingPosition = i
            windowValues = np.append(windowValues, signalValue)
        else:
            if len(windowValues) > 0:
                # window must be wide enough so it's not a noise
                if len(windowValues) > minPauseTime:
                    peak = np.argmax(windowValues)
#                    peakPoints = np.append(peakPoints, int(windowStartingPosition+peak))
                    peakPoints.append(int(windowStartingPosition+peak))
                windowValues = []

    numOfPeakPoints = len(peakPoints)
    peakPointValues = [signals[int(x)] for x in peakPoints]
    heartRate = int(numOfPeakPoints/((peakPoints[-1] - peakPoints[0])/samplingFrequency)*secPerMin)
    
    plt.title("Heart Rate Signal " + ecgfilename + "/w Peak" )
    plt.scatter(peakPoints[0], peakPointValues[0], color='red', label='average: %.1f BPM' % heartRate)
    for i in range(int(numOfPeakPoints*2/16), int(numOfPeakPoints*10/16)):
        plt.scatter(peakPoints[i], peakPointValues[i], color='red')
        plt.pause(0.0001)

    #step 4 calculate and show show BPM

    plt.title("Heart Rate Signal " + ecgfilename + " Average BPM")
    plt.legend(loc=9, framealpha=0.6)
    plt.pause(3)
