import sys, os
import argparse
import json


# Author: Josh Messitte (811976008)
# CSCI 6760 Project 1: Traceroute

# Main method
if __name__ == '__main__':


    # Set up argument parsing automation
    prog = 'python3 trstats.py'
    descr = 'Python Wrapper Script to Analyze Traceroute Performance'
    parser = argparse.ArgumentParser(prog = prog, description = descr)
    parser.add_argument('-o','--output',type = str, default = 'output.json', required = True, help = 'Path and Name of outpt JSON')
    parser.add_argument('-n','--num_runs',type = int, default = 10, help = 'Number of times traceroute will run')
    parser.add_argument('-d','--run_delay',type = int, default = 0, help = 'Number of seconds to wait between two condsectuive runs')
    parser.add_argument('-m','--max_hops',type = int, default = 100, help = 'Number of times traceroute will run')
    parser.add_argument('-t','--target',type = str, default = 'www.yahoo.co.jp', help = 'A target domain name or IP address')
    parser.add_argument('--test', '--test', type = str, default = None, help = 'Directory containing num_runs text files, each with traceroute output. If present, override and do not run traceroute.')

    # Parse the given arguments
    args = parser.parse_args()

    if args.test != None:
        # A directiory of text files was provided // this conditional branch executes // DON'T run traceroute
        print ('Test directory was provided')

        
    else:
        # NO test directory provided // RUN traceroute
        print('Running traceroute and measuring latency...')
        target = args.target
        traceroute_counter = 1

        # Will end up being 2-dim matrices for collecting data
        hosts_by_hop = []
        times_by_hop = []

        
        while traceroute_counter < args.num_runs:
            # Outer TR loop
            tr_cmd = 'traceroute ' + target + ' > tr_output.txt'
            tr_out = ''
            os.system(tr_cmd)

            # txt_f will open the file and pull all needed data
            txt_f = open('tr_output.txt','r')
            count = 0
            
            
            while True:
                #File for each line of a txt file
                curr = txt_f.readline()

    
                if len(curr) < 1:
                    break
                
                
                if count > 0:
                    # Past first line
                    curr_hop = int(curr[1:2])
                    curr = curr[4:]

                    total_parsets = curr.count('(')
                    
                
                    # If traceroute yields statistics, we will observe the 'ms' unit measurement
                    hosts = []
                    times = []
                    
                    # Pull first host-time matchup
                    if total_parsets > 0:

                        double_sp = curr.find('  ')
                        msloc = curr.find(' ms')
                        hosts.append(curr[0:double_sp])
                        if curr[double_sp+2:msloc] != '*':
                            times.append(float(curr[double_sp+2:msloc]))
                        curr = curr[msloc+1:]

                    total_parsets = curr.count('(')

                    if total_parsets == 0:
                        # Form: domain_(ip)__x_ms__x_ms__x_ms
                        msloc = curr.find(' ms')
                        
                        if msloc != -1 and curr[4:msloc] != '*':
                            times.append(float(curr[4:msloc]))
                        curr = curr[msloc+1:]
                        msloc = curr.find(' ms')
                        if msloc != -1 and curr[4:msloc] != '*':
                            times.append(float(curr[4:msloc]))
                        

                    elif total_parsets == 1:
                        # Two total hosts for this single hop
                        if curr.find('(') < curr.find('  '):
                            #Form: domain_(ip)__x_ms_domain_(ip)__x_ms__x_ms
                            double_sp = curr.find('  ')
                            hosts.append(curr[3:double_sp])
                            curr = curr[double_sp+2:]
                            msloc = curr.find(' ms')
                            if msloc != -1 and curr[0:msloc] != '*':
                                times.append(float(curr[0:msloc]))
                            curr = curr[msloc+1:]
                            msloc = curr.find(' ms')
                            if msloc != -1 and curr[4:msloc] != '*':
                                times.append(float(curr[4:msloc]))
                        elif curr.find('(') > curr.find('  '):
                            # Form: domain_ip__x_ms__x_ms_domain_(ip)__x_ms
                            msloc = curr.find(' ms')
                            if msloc!= -1 and curr[4:msloc] != '*':
                                times.append(float(curr[4:msloc]))
                            curr = curr[msloc+1:]
                            double_sp = curr.find('  ')
                            hosts.append(curr[3:double_sp])
                            curr = curr[double_sp+2:]
                            msloc = curr.find(' ms')
                            if msloc != -1 and curr[0:msloc] != '*':
                                times.append(float(curr[0:msloc]))

                            
                    # Form: domain_(ip)__x_ms_domain_(ip)__x_ms_domain_(ip)__x_ms
                    elif total_parsets == 3:
                        double_sp = curr.find('  ')
                        hosts.append(curr[3:double_sp])
                        curr = curr[double_sp+2:]
                        msloc = curr.find(' ms')
                        
                        if msloc != -1 and curr[0:msloc] != '*':
                            times.append(float(curr[0:msloc]))
                        curr = curr[msloc+1:]
                        double_sp = curr.find('  ')
                        hosts.append(curr[3:double_sp])
                        curr = curr[double_sp+2:]
                        msloc = curr.find(' ms')
                        if msloc != 0 and curr[0:msloc] != '*':
                            times.append(float(curr[0:msloc]))

                    # Update hosts
                    if len(hosts_by_hop) < curr_hop:
                        hosts_by_hop.append(hosts)
                    else:
                        hosts_by_hop[curr_hop-1].extend(hosts)

        
                    # Update times
                    if len(times_by_hop) < curr_hop:
                        times_by_hop.append(times)
                    else:
                        times_by_hop[curr_hop-1].extend(times)

                count += 1
                
            traceroute_counter += 1

        

        seen_hosts = []
        hc = 1
        # Remove dups from arrays
        for hop in hosts_by_hop:
            print('Hop: ',hc)
            hc += 1
            for host in hop:
                if host in seen_hosts:
                    hop.remove(host)
                else:
                    print('Host: ',host)

        hc = 0
        for hop in times_by_hop:
            print('Hop: ',hc)
            hc += 1
            for time in hop:
                print(time,' ms ')
