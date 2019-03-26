README.txt
X433-3 Project 'Calculate Heart Rate from ECG Data'

Instructor Alexander I. Iliev, Ph.D.
Author: Shih-Chieh (Jerry) Hsu

Project Overview:
    This app
        - reads ECG data
        - identify heart beats
        - calculate heart rates BPM(Beats Per Minute)

    The app using the follow algorithm to identify heart beats
        - calculate moving average of the input data with window size
        - identify positions (time/sample-location) of peak values in each section
          where samples are above the corresponding moving averages
        - the number of the samples in the section needs to be more than a threshold to be considered
        - find the time between the first and last peak value and calculate BPM from that information

Platform/Systems:
  - MacOS High Sierra on Macbook Pro 2012
  - Python 3.6 running in PyCharm

Package:
    - ECG Data Reader Package: https://wfdb.readthedocs.io/en/latest/
    - ECG Data Source: https://www.physionet.org/physiobank/database/aami-ec13/
    - Numpy
    - Matplotlib

Run the program:
    - place all project files in the same folder
    - install following packages if not already done
        wfdb
        numpy
        matplotlib
    - just run ecg_heartbeat.py, everything runs in one go
    - included are 10 ECG data used by FDA to validate heart beat devices

