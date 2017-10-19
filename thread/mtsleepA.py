import _thread
from time import sleep, ctime

def loop0():
    print ("start loop 0 at:" + str(ctime()))
    sleep(4)
    print ("loop 0 done at:" + str(ctime()))

def loop1():
    print ("start loop 1 at:" + str(ctime()))
    sleep(4)
    print ("loop 1 done at:" + str(ctime()))

def main():
    print ("starting at :" + str(ctime()))
    _thread.start_new_thread(loop0, ())
    _thread.start_new_thread(loop1, ())
    # if not sleep, the main thread will exit, the two sons will be killed too.
    sleep(6)
    print ("all done at:" + str(ctime()))

if __name__ == "__main__":
    main()
