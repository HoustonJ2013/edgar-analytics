## Project Summary
This repo is for the insightdatascience [coding challenges.](https://github.com/InsightDataScience/edgar-analytics)
Given streaming log from Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system, the program output the user ip, how long they stay and how many documents they acessed. 

## Resources:
### python 2.7
### python libraries: 
+ argparse Version 1.1
+ collections
+ time 

The final version for submission is in src/sessionization.py 

## Methogology and implementation. 

### Use file object from open function to handle read and write. We can switch the I/O to streaming data for next step. 

### Use two OrderedDict from collections module to save the active users. One is ordered by first action time, and another is ordered by last action time. The space complexity depends on the definition of inactivity_period, and is close to ~18010 if we define the inactivity period as 7200s (2 hours).    

### Use datetime module to parse and effient comparison of timestamps objects. 

### Use time module to test the code speed and optimized. The final version is 400 times faster than the initial version. 

### Pesudo code:


#### For each line in the log: 
+ Parse one line of the log
+ If current time stamp is 1s increment compared to previous, search and return the expried users from the active user dictionary, delete the expired users from active user dictionaries. For efficiency I used user dictionary ordered by last action time to search for expried users. 
+ Write out info for the expired users 
+ Add current log information to active users or update the active user information
#### When finished reading, write out the info for rest of the active users 


A class EDGAR was defined to process the log and write the output. 
Here is how to instantiate the class and parse the input log. 
```
    sess = EDGAR(logfile, inactivity_period, output)
    sess.parse_log()
```

## Time complexity and space complexity: Statistics of the log data 


## Summary 
