import threading
from time import sleep, ctime

loops = [4, 2]

def loop(nloop, nsec):
    print ("start loop " + str(nloop) + " at:" + str(ctime()))
    sleep(4)
    print ("loop " + str(nloop)  + " done at:" + str(ctime()))

def main():
    print ("starting at :" + str(ctime()))
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target = loop, args = (i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print ("all done at:" + str(ctime()))

if __name__ == "__main__":
    main()
