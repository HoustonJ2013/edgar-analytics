## Project Summary
This repo is for the insightdatascience [coding challenges](https://github.com/InsightDataScience/edgar-analytics)
Given streaming log from Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system, the program output the user ip, how long they stay and how many documents they acessed. 

## Resources:
### python 2.7
### python libraries: 
+ argparse Version 1.1
+ collections
+ time 

The final version for submission is in src/sessionization.py 

## Methogology:

A class EDGAR was defined to process the log and write the output. 
Here is how to instantiate the class and parse the input log. 
'''
    sess = EDGAR(logfile, inactivity_period, output)
    sess.parse_log()
'''

