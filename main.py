from kubernetes import client, config
from common.monitor import Monitor
from common.filter import Filter
from fcfs.strategy import FCFS
from scheduler.scheduler import Scheduler

mnt = Monitor()
flt = Filter()
fcfs = FCFS()
sched = Scheduler(strategy=fcfs)