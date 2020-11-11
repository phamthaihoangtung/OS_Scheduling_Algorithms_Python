from tqdm import tnrange, tqdm_notebook, tqdm
from time import sleep
from Process import Process
from pandas import DataFrame


class FCFS:
    def __init__(self, p_list):
        self.processes_list = p_list
        self.num_processes = len(p_list)
        self.average_wait_time = 0
        self.average_turnaround_time = 0
        self.log_file = 'FCFS'

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
        ### first state
        list_wait_time = [0]
        self.processes_list[0].w_time = 0
        wait_time = 0

        self.processes_list[0].response_time = 0

        list_turnaround_time = [self.processes_list[0].burst_time]
        self.processes_list[0].turnaround_time = self.processes_list[0].burst_time
        turnaround_time = self.processes_list[0].burst_time

        ### loop from 2nd process and update wait time, turn around time
        for i in range(1, self.num_processes):
            wait_time += self.processes_list[i-1].burst_time
            self.processes_list[i].w_time = wait_time

            self.processes_list[i].response_time = wait_time

            turnaround_time += self.processes_list[i].burst_time
            self.processes_list[i].turnaround_time = turnaround_time
        
        ### get all turnaround time and waititng time
        list_turnaround_time = [self.processes_list[i].turnaround_time for i in range(self.num_processes)]
        list_wait_time = [self.processes_list[i].w_time for i in range(self.num_processes)]

        ### calculate average time
        self.average_wait_time = sum(list_wait_time)/self.num_processes
        self.average_response_time = self.average_wait_time
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
        for process in self.processes_list:
            for i in tqdm(range(process.burst_time), desc=process.name):
                sleep(1)
