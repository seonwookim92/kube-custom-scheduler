from kubernetes import client, config
from common.monitor import Monitor
from common.filter import Filter
from fcfs.strategy import FCFS
from scheduler.scheduler import Scheduler

from time import sleep

mnt = Monitor()
flt = Filter()
fcfs = FCFS()
sched = Scheduler(strategy=fcfs)

while True:
    pod, node = sched.decision()
    if pod is not None:
        sched.scheduling(pod, node)
    sleep(10)