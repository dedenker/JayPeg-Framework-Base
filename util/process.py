# een process beheer systeem
# dit moet uit eindelijk uitgroeien tot een multiprocess API
# Alleen om forken, joinen en kill makkelijker te maken.
# een goeie samenwerken met MSGBUS voor PID, voor kill commando's
# dit moet gebeuren in MAIN zodat er een mooie diagram bij gehouden kan worden.
# dan plus CPU en Networking gebruik!!
# er kan ook DISK IO en Memory bij?

# meerdere voorbeelden die handig zijn

#Queue kan gehele module/class doorgeven
#Pipe kan informatie doorgeven
#Event kan boolean doorgeven

# kan er dan in redis een tree gebouwed worden?
"""
main = (jaypeg,1)
1 = (bios,2),(audio,3),(vision,4)
2 = 5,6
3 = 7,8,9
4 = 10,11,12
5 = 13,14
"""
# hoe dan met triggers? extra bios of bios.trigger? dit vereist een 3D table en REDIS doet alleen 2D goed...


import multiprocessing as mp
import psutil
#import msgbus ?
import signal
import redis,os,time
from datetime import datetime

r_server = redis.Redis("localhost")

#Test opstelling
#
#Job creator
#
#Job monitor
#
#Job deployment (krijgt PID terug)
#
#Job Killer
#

# misschien is sysv_ipc mini berichten hier een idee!!


# Logger toevoegen voor detail.

Deze uitbouwen dat als init plaats vind er een pid & ppid komen om zo process registratie krijgen!

def pid_info():
    # dit geeft een lijst van process ID en EXE naam
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            print(pinfo)


#def net_info(pid) # if no PID is total

#def cpu_info(pid) # if no PID it is per CPU core

#def disk_info

#def mem_info

def fork(name = None,target,args): #args = list?
    #p = mp.current_process() # geeft main PID
    """
    try:
      parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
      return None
    children = parent.children(recursive=True)
    for process in children:
      append list with current children
    """
    fork = mp.Process(name=name,target=target, args=(args,))
    # print 'Starting:', fork.name, fork.pid
    #pid = p.pid
    fork.start()
    #fork.join() # als geen join blijft er hangen...!time-out test!
    #for process in children:
    #  append list with current children = compare lists and the new is known
    return fork.pid

def kill(pids):
    if len(pids) >= 1:
        for pid in pids:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for process in children:
                if not (process.pid == current_process):
                    print "Process: ",current_process,  " killed process: ", process.pid
                    process.send_signal(signal.SIGTERM)
    else:
        parent = psutil.Process(pids)
        children = parent.children(recursive=True)
        for process in children:
            if not (process.pid == current_process):
                print "Process: ",current_process,  " killed process: ", process.pid
                process.send_signal(signal.SIGTERM)


def worker(t):
    print "working"
    print "worker PID " , os.getpid()
    time.sleep(t)
    print "klaar"
    return

def overwork(t):
    t = t * 2
    print "Over working"
    print "over worker PID " , os.getpid()
    time.sleep(t)
    print "klaar...?"
    return
    

def timeout(t, now):
    #t1 = datetime.now()
    t = t + 1
    while True:
        t2 = datetime.now()
        delta = t2 - now
        if delta.seconds >= t:
            print "te ver!"
            return True
            #break
        #return False



def test():
    pid = os.getpid()
    t = 5
    print "main: ", pid
    proc1 = fork("work",worker,t)
    print "fork1: ", proc1
    proc2 = fork("overwork",overwork,t)
    print "fork2: ", proc2
    if timeout(t,datetime.now()):
        for proc in proclist:
            if proc is is_alive():
                pass
            else:
                print "stop!"
                kill(proc)
    print "einde"

test()

def get_threads_cpu_percent(p, interval=0.1):
   total_percent = p.get_cpu_percent(interval)
   total_time = sum(p.cpu_times())
   return [total_percent * ((t.system_time + t.user_time)/total_time) for t in p.get_threads()]

# Example usage for process with process id 8008:
#proc = psutil.Process(8008)
#print(get_threads_cpu_percent(proc))

#def get_pid():
    # dit zou met forking moeten gaan...

# dan moet er een verwerking komen die dit bijhoudt...

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
      parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
      return
    children = parent.children(recursive=True)
    for process in children:
      process.send_signal(sig)


# ++++
# zou dan een combi zijn om bij te houden welke componenten welke modules forken...
"""
import psutil
>>> psutil.net_connections()

import psutil
>>> psutil.net_io_counters()
snetio(bytes_sent=14508483, bytes_recv=62749361, packets_sent=84311, packets_recv=94888, errin=0, errout=0, dropin=0, dropout=0)
>>>
>>> psutil.net_io_counters(pernic=True)



import multiprocessing
import time

def wait_for_event(e):
    #Wait for the event to be set before doing anything
    print 'wait_for_event: starting'
    e.wait()
    print 'wait_for_event: e.is_set()->', e.is_set()

def wait_for_event_timeout(e, t):
    #Wait t seconds and then timeout
    print 'wait_for_event_timeout: starting'
    e.wait(t)
    print 'wait_for_event_timeout: e.is_set()->', e.is_set()


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='block', 
                                 target=wait_for_event,
                                 args=(e,))
    w1.start()

    w2 = multiprocessing.Process(name='non-block', 
                                 target=wait_for_event_timeout, 
                                 args=(e, 2))
    w2.start()

    print 'main: waiting before calling Event.set()'
    time.sleep(3)
    e.set()
    print 'main: event is set'
"""
