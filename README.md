## Project Summary
This repo is for the insightdatascience [coding challenges.](https://github.com/InsightDataScience/edgar-analytics)
Given the streaming log from Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system, the program output the information on the fly such as user ip, how long they stay and how many documents they acessed. 

## Resources:
- python 2.7
- python libraries: 
  * argparse Version 1.1
  * collections
  * time 

The final version for submission is in src/sessionization.py 

## Methogology and implementation. 

### Data Structure and Modules
- Use file object from open function to handle read and write. We can switch the I/O to streaming data for next step. 
- Use two OrderedDict from collections module to save the active users. One is ordered by first action time, and another is ordered by last action time. The space complexity depends on the definition of inactivity_period, and is close to ~18010 if we define the inactivity period as 7200s (2 hours).    
- Use datetime module to parse and effient comparison of timestamps objects. 
- Use time module to test the code speed and optimized. The final version is 400 times faster than the initial version. 

### Pesudo code:
For each line in the log: 
  + Parse one line of the log
  + If current time stamp is 1s increment compared to previous, search and return the expried users from the active user dictionary, delete the expired users from active user dictionaries. For efficiency I used user dictionary ordered by last action time to search for expried users. 
  + Write out info for the expired users 
  + Add current log information to active users or update the active user information
When finished reading, write out the info for rest of the active users 


A class EDGAR was defined to process the log and write the output. Here is how to instantiate the class and parse the input log. 
```
    sess = EDGAR(logfile, inactivity_period, output)
    sess.parse_log()
```

## Time complexity and space complexity: Statistics of the log data 
### Space complexity
The log files are red line by line on the fly from the text files, and the space complexity for ordered dictionary is relatively small. The space complexity depends on the definition of inactivity_period, and is close to ~18010 if we define the inactivity period as 7200s (2 hours).
### Time complexity
Time compolexity is O(n), where n is the number of entries in the log file. The main cost is to read, parse, and update the active user dictionary, which cost on O(1) for each entry. Some overhead is to check the expired users and write out the results. For a typical log from [SEC](https://www.sec.gov/dera/data/edgar-log-file-data-set.html), the average cost for the overhead is << 1 for each entry. 


For a large log of ~ 2gb size, the total run time 640s that is 27 micro-seconds per entry. 
The computer specs are as follow:
- Memory 12 GB 
- Processor Intel i5-2520M 
- OS: ubuntu 16.04
## Summary 
By using the ordered dictionary and datetime structure, I used an efficient algorithm to process the log and output the user activity information. This code can be easily scaled up by changing the I/O.  
