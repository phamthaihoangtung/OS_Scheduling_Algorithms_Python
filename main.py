#!/usr/bin/python3
from Process import Process
from FCFS import FCFS
from SJF import SJF
from Priority import Priority
from RoundRobin import RoundRobin
import pandas as pd
import sys 
import random

INPUT_PATH = './input/process.csv'
OUTPUT_PATH = './output'

list_processes = []

if len(sys.argv) == 1:
    df = pd.read_csv(INPUT_PATH)
    records = df.to_dict('records')
    for record in records:
        process = Process(record['process'], record['priority'], record['burst'])
        list_processes.append(process)
else: 
    if sys.argv[1] == 'random':
        ### generate random processes
        df = pd.DataFrame(columns=['process', 'priority', 'burst'])
        df.to_csv(INPUT_PATH, index=False)

        num_process = random.randint(1, 10)
        priority_list = [i for i in range(1, num_process+1)]
        
        for i in range(1, num_process+1):
            name_process = 'p'+str(i)
            priority = random.choice(priority_list)
            burst_time = random.randint(1, 10)

            process = Process(name_process, priority, burst_time)
            list_processes.append(process)

            df = pd.DataFrame.from_records([{'process': name_process, 
                                             'priority': priority, 
                                             'burst': burst_time}])

            df.to_csv(INPUT_PATH, mode='a', header=False, index=False)

            priority_list.remove(priority)


def menu():
    while(True):
        print("\nWhat algorithm you want to launch?")
        print('1. FCFS')
        print('2. SJF')
        print('3. Priority')
        print('4. RoundRobin')
        z = input('(1-4): ')
        print()
        if z == '1':
            fcfs = FCFS(list_processes)
            fcfs.run()
        elif z == '2':
            sjf = SJF(list_processes)
            sjf.run()
        elif z == '3':
            pr = Priority(list_processes)
            pr.run()
        elif z == '4':
            quantumn_time = float(input('Quantumn time: '))
            rr = RoundRobin(list_processes, quantumn_time)
            rr.run()
        else:
            print("Wrong input")
            pass


if __name__ == "__main__":
    menu()
