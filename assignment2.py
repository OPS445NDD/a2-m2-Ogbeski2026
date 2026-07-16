#!/usr/bin/env python3

'''
OPS445 Assignment 2 - Summer 2026
Program: assignment2.py 
Author: "Ogbemudia Obariase"
The python code in this file is original work written by
"Ogbemudia Obariase". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script reports on system and process memory usage. 
When run with no arguments, it shows total memory used out of total 
available system memory. When given the name of a running program, 
it shows the Resident Set Size (Rss) memory used by each process
associated with that program, plus a combined total.


Date: 16th July, 2026

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human readable format")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use if not.")
    args = parser.parse_args()
    return args

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    # round (not truncate) so the space count matches expectations exactly
    num_spaces = round(length * (1 - percent))
    num_hashes = length - num_spaces
    return ('#' * num_hashes) + (' ' * num_spaces)

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    # open the meminfo file to do this!
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('MemTotal:'):
            # line looks like: 'MemTotal:       32993367 kB\n'
            return int(line.split()[1])

def get_avail_mem() -> int:
    "return total memory that is currently available"
    # open the meminfo file to do this!
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('MemAvailable:'):
            return int(line.split()[1])

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    # please use os.popen('pidof <app>') to do this!
    pids = os.popen(f'pidof {app_name}').read()
    return pids.split()

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the Resident memory used"
    # for a process, open the smaps file and return the total of each
    # Rss line.
    total_rss = 0
    with open(f'/proc/{proc_id}/smaps') as f:
        for line in f:
            if line.startswith('Rss:'):
                total_rss += int(line.split()[1])
    return total_rss 

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:  # not program name is specified.
        pass
    else:
        pass
