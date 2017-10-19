import threading
from time import sleep, ctime

loops = [4, 2]

class loop_thread(threading.Thread):
    
    def __init__(self, nloop, nsec):
        super().__init__()
        self.nloop = nloop
        self.nsec = nsec

    def run(self):
        print ("start loop " + str(self.nloop) + " at:" + str(ctime()))
        sleep(self.nsec)
        print ("loop " + str(self.nloop)  + " done at:" + str(ctime()))

def main():
    print ("starting at :" + str(ctime()))
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = loop_thread(i, loops[i])
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print ("all done at:" + str(ctime()))

if __name__ == "__main__":
    main()
