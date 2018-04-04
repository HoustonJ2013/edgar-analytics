import argparse
from datetime import datetime
from collections import OrderedDict
from time import time

class EDGAR:

    def __init__(self, logfile="", duration_file="", outputfile=""):
        self.logfile = logfile
        self.duration = self._read_duration(duration_file)
        self.active_users = OrderedDict()  # key: user ip  value : (min_time, max_time, num_access)
                                           # Keep order of max_time
        self.active_users2 = OrderedDict()  # key: user ip  value : (min_time, max_time, num_access)
                                            # Keep order of min_time
        self.f_output = open(outputfile, "w+")
        ## helper attributes
        self.log_header = {}  # Map of header name to index in a row
        self.maxdict_size = 0 # max size of the active_users dictionary
        self.num_check = 0

    def _parse_line(self, linestr):
        '''
        parse the log file string
        :param linestr: one string for one line in log file
        :return: parsed ip, dattime obj, cik, accession, extension
        '''
        _parsed = linestr.split(",")
        ip = _parsed[self.log_header["ip"]]
        date = _parsed[self.log_header["date"]]
        time = _parsed[self.log_header["time"]]
        datetime_str = "".join([date, time])
        cdatetime = datetime.strptime(datetime_str, "%Y-%m-%d%H:%M:%S")
        cik = _parsed[self.log_header["cik"]]
        accession = _parsed[self.log_header["accession"]]
        extention = _parsed[self.log_header["extention"]]
        return ip, cdatetime, cik, accession, extention

    def _read_duration(self, file):
        with open(file) as f:
            duration = f.readline().split()[0]
        return int(duration)

    def _write_to_output(self, output_dict):
        output_list = []
        for ip, val in output_dict.iteritems():
            mintime, maxtime, num_access = val
            mintime_str = mintime.strftime(format="%Y-%m-%d %H:%M:%S")
            maxtime_str = maxtime.strftime(format="%Y-%m-%d %H:%M:%S")
            duration = (maxtime - mintime).total_seconds() + 1
            output_list.append((ip, mintime_str, maxtime_str, duration, num_access))
        output_list.sort(key=lambda x: x[1])
        for item in output_list:
            self.f_output.write("%s,%s,%s,%i,%i \n"%(item))

    def check_expire(self, cdatetime):
        '''
        For each datetime update check which  user activity expired, remove it from dict and return
        :param cdatetime:
        :return: expired user and the info
        '''
        expire_dict = OrderedDict()
        for ip, val in self.active_users.iteritems():
            mintime, maxtime, num_access = val
            self.num_check += 1
            if (cdatetime - maxtime).total_seconds() > self.duration:
                del self.active_users[ip]
                del self.active_users2[ip]
                expire_dict[ip] = val
            else:
                break

        return expire_dict

    def parse_log(self, header=1):
        '''
        :param header: 0 use predefined header for EDGAR 1: read headers from log file
        :return:
        '''
        if header == 0:
            self.log_header = {'accession': 5,
                             'browser\n': 14,
                             'cik': 4,
                             'code': 7,
                             'crawler': 13,
                             'date': 1,
                             'extention': 6,
                             'find': 12,
                             'idx': 9,
                             'ip': 0,
                             'noagent': 11,
                             'norefer': 10,
                             'size': 8,
                             'time': 2,
                             'zone': 3}
        else:
            with open(self.logfile) as f:
                headers = f.readline().split(",")
                for i, header in enumerate(headers):
                    self.log_header[header] = i

                for line in f:
                    ip, cdatetime, cik, accession, extention = self._parse_line(line)
                    ## Check expired user and write to output
                    output_dict = self.check_expire(cdatetime)
                    if len(output_dict) > 0: self._write_to_output(output_dict)
                    ## update ip
                    if len(self.active_users) > self.maxdict_size: self.maxdict_size \
                                                                = len(self.active_users)
                    if ip in self.active_users:
                        mintime, maxtime, num_access = self.active_users[ip]
                        del self.active_users[ip]
                        self.active_users[ip] = mintime, cdatetime, num_access + 1
                        self.active_users2[ip] = mintime, cdatetime, num_access + 1
                    else:
                        self.active_users[ip] = cdatetime, cdatetime, 1
                        self.active_users2[ip] = cdatetime, cdatetime, 1
                ## At the end of log files write rest of active users into the output
                if len(self.active_users2) > 0: self._write_to_output(self.active_users2)
                self.f_output.close() ## Close the output file
        pass

def run_time(funcs):
    start = time()
    for func in funcs:
        func()
    end = time()
    return end - start

def main(args):
    logfile = args.log
    inactivity_period = args.inactivity_period
    output = args.output
    sess = EDGAR(logfile, inactivity_period, output)
    sess.parse_log()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', '--log', type=str, default='./input/log.csv')
    parser.add_argument('-inact', '--inactivity_period', type=str, default='./input/inactivity_period.txt')
    parser.add_argument('-out', '--output', type=str, default='./output/sessionization.txt')
    args = parser.parse_args()
    main(args)