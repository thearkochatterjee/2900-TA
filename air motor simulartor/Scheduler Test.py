import sched, time

s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    print("Frame print_time",time.time(),a)

def print_some_times():
    print_time(time.time())
    s.enter(10,1,print_time)
    s.enter(5,2,print_time,argument=('positional',))
    s.enter(5,1,print_time,kwargs={'a':'keyword'})
    s.run()
    print(time.time())

print_some_times()