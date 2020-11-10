

class Process:
    def __init__(self, p_name, p_p, b_t, a_t=0):
        self.name = p_name
        self.burst_time = b_t
        self.arrival_time = a_t
        self.priority = p_p
        self.w_time = 0
        self.response_time = 0
        self.turnaround_time = 0

    def hi(self):
        print('Hi. My name is {}'.format(self.name))

    def getBurstTime(self):
        return int(self.burst_time)

    def getArrivalTime(self):
        return int(self.arrival_time)

    def getName(self):
        return str(self.name)
    
    def __str__(self):
        return ('{}\t{:.2f}\t{:.2f}\t{:.2f}'.format(self.name, self.w_time, self.response_time, self.turnaround_time))