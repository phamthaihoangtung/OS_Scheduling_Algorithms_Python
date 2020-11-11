from tqdm import tnrange, tqdm_notebook, tqdm
from time import sleep
from Process import Process
import math
from pandas import DataFrame

class RoundRobin:
    def __init__(self, p_list, quantumn_time):
        self.processes_list = p_list
        self.num_processes = len(p_list)
        self.average_wait_time = 0
        self.quantumn_time = quantumn_time
        self.log_file = 'RoundRobin'

    def display(self):
        print("Process\tWaiting\tRespons\tTurnaround")
        for process in self.processes_list:
            print(process)
        print()

    def log(self):
        ### log all data to csv file
        list_process_name = [self.processes_list[i].name for i in range(self.num_processes)]
        list_wait_time = [self.processes_list[i].w_time for i in range(self.num_processes)]
        list_response_time = [self.processes_list[i].response_time for i in range(self.num_processes)]
        list_turnaround_time = [self.processes_list[i].turnaround_time for i in range(self.num_processes)]

        df = DataFrame({'Process': list_process_name, 
                        'Waiting time': list_wait_time, 
                        'Response time': list_response_time,
                        'Turnaround time': list_turnaround_time})
        
        df.to_csv('./output/'+self.log_file+'_Log.csv', index=False)

    def sortProcesses(self):
        pass

    def calculate(self):
        ### calculate response time - time from job arrives to first access
        response_time = 0
        self.processes_list[0].response_time = response_time

        for i in range(1, self.num_processes):
            response_time += min(self.quantumn_time,
                                 self.processes_list[i-1].burst_time)
            self.processes_list[i].response_time = response_time

        response_time_list = [self.processes_list[i].response_time for i in range(self.num_processes)]
        self.average_response_time = sum(response_time_list)/self.num_processes

        ### calculate turn around time - time from job arrives to job completes
        turnaround_time = 0
        running_list = [self.processes_list[i].burst_time for i in range(self.num_processes)]
        running_index_list = [i for i in range(self.num_processes)]
        index = 0

        while(len(running_index_list) != 0):
            ### get running process, its running time and update turnaround time, new remaining time 
            running_process = running_list[index]
            running_time = min(self.quantumn_time, running_process)
            turnaround_time += running_time
            running_list[index] -= running_time
            
            ### the process has no remaining time, update process attributes, pop it 
            if running_list[index] == 0:
                self.processes_list[running_index_list[index]].turnaround_time = turnaround_time
                self.processes_list[running_index_list[index]].w_time = turnaround_time - self.processes_list[index].burst_time
                running_list.pop(index)
                running_index_list.pop(index)
                ### backward index
                index -= 1

            if index >= len(running_list)-1:
                index = 0
            else:
                index += 1

        ### get all turnaround time and waititng time
        list_turnaround_time = [self.processes_list[i].turnaround_time for i in range(self.num_processes)]
        list_wait_time = [self.processes_list[i].w_time for i in range(self.num_processes)]

        ### calculate average time
        self.average_wait_time = sum(list_wait_time)/self.num_processes
        self.average_turnaround_time = sum(list_turnaround_time)/self.num_processes

        print("Average waiting time: %.4f" % (self.average_wait_time))
        print("Average response time: %.4f" % (self.average_response_time))
        print("Average turnaround time: %.4f" % (self.average_turnaround_time))
        print()

    def run(self):
        self.sortProcesses()
        self.calculate()
        self.display()
        self.log()
