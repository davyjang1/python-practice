#!/usr/bin/python3

from threading import Thread
from queue import Queue
from math import floor
import time
import copy


# cause some trouble here, either absent or not vote

def start_priest(Id, msg_queues, priest_ids, decs):
	ballots = {}
	passed_decs = []

	lastTried = Id
	prevVotes = {} # like prevVotes[id] = [] or lastest dec
	re_prevVotes = []

	# need reinit begin
	status = "idle"
	quorum = []
	voters = []
	decree = None
	outcome = None
	owner = {}
	# need reinit end


	nextBal = None
	prevBal = None
	prevDec = None

	# assume that priest_ids[0,1] are the leaders
	if Id == priest_ids[0] or Id == priest_ids[1]:
	#if Id == priest_ids[1]:
		status = "trying"

	# to mock prevBal and prevDec
	if Id == priest_ids[3]:
		#time.sleep(3)
		prevBal = 0
		prevDec = 2


	if "trying" == status:
		lastTried += 1
		for other in priest_ids:
			msg = {}
			msg['type'] = "NextBallot"
			msg['ballot_num'] = lastTried
			print ("p " + str(Id) + " send " + str(msg) + " to " + str(other))
			msg_queues[Id][other].put(msg)	

	while(1):
		for other in priest_ids:
			#print (str(Id) + " try to get from " + str(other) + " queue's size:" + str(msg_queues[other][Id].qsize()))
			if msg_queues[other][Id].empty():
				item = None
			else:
				item = msg_queues[other][Id].get(block=False)
			if item:
				msg_type = item['type']
				if "NextBallot" == msg_type:
					print ("p " + str(Id) + " recieve " + str(item) + " from " + str(other))
					if None == nextBal or item['ballot_num'] >= nextBal:
						nextBal = item['ballot_num']
						owner[nextBal] = other
					if None == prevBal or nextBal > prevBal:
						msg = {}
						msg['type'] = "LastVote"
						msg['nextBal'] = nextBal
						msg['prevBal'] = prevBal
						msg['prevDec'] = prevDec
						print ("p " + str(Id) + " send " + str(msg) + " to " + str(other))
						msg_queues[Id][other].put(msg)

				elif "LastVote" == msg_type:
					print ("p " + str(Id) + " recieve " + str(item) + " from " + str(other))
					re_prevVotes.append(other)
					if item['nextBal'] == lastTried and "trying" == status:
						if (None != item['prevBal'] and None != item['prevDec']):
							# later compare, just compare between the last ones 
							prevVotes.setdefault(other, []).append({"bal": item['prevBal'],
												"dec": item["prevDec"]})

					cnt = floor(len(priest_ids) / 2) + 1
					print ("cnt:" + str(cnt))
					if len(re_prevVotes) >= cnt and "trying" == status:
						for present in re_prevVotes:
							if 0 == cnt:
								break
							quorum.append(present)
							cnt -= 1
						status = "polling"
						voters = []
						maxBal = -1

						for key in prevVotes.keys():
							if prevVotes[key][-1]["bal"] > maxBal:
								maxBal = prevVotes[key][-1]["bal"]
								decree = prevVotes[key][-1]["dec"]
						if not (decree and decree not in passed_decs):
							decree = decs[0]
						
						ballots[lastTried] = {"dec" : decree, "qrm": quorum, 'vate':[]}


						for quo in quorum:
							msg = {}
							msg['type'] = "BeginBallot"
							msg["ballot_num"] = lastTried
							msg["decree"] = decree
							print ("p " + str(Id) + " send " + str(msg) + " to " + str(quo))
							msg_queues[Id][quo].put(msg)

				elif "BeginBallot" == msg_type:
					print ("p " + str(Id) + " recieve " + str(item) + " from " + str(other))
					if item["ballot_num"] == nextBal and (None == prevBal or nextBal > prevBal):
						prevBal = nextBal
						prevDec = item['decree']
						#TODO store in stable strorage
						msg = {}
						msg['type'] = "Voted"
						msg['prevBal'] = prevBal
						print ("p " + str(Id) + " send " + str(msg) + " to " + str(other))
						msg_queues[Id][other].put(msg)

				elif "Voted" == msg_type:
					print ("p " + str(Id) + " recieve " + str(item) + " from " + str(other))
					if item['prevBal'] == lastTried and "polling" == status:
						voters.append(other)
					if "polling" == status and set(quorum).issubset(set(voters)) and None == outcome:
						outcome = decree
					if None != outcome:
						for in_other in priest_ids:
							msg = {}
							msg['type'] = "Success"
							msg['outcome'] = outcome
							print ("p " + str(Id) + " send " + str(msg) + " to " + str(in_other))
							msg_queues[Id][in_other].put(msg)
						status = "trying"
						quorum = []
						voters = []
						decree = None
						outcome = None
						owner = {}
						re_prevVotes = []
						lastTried += 1
						for other in priest_ids:
							msg = {}
							msg['type'] = "NextBallot"
							msg['ballot_num'] = lastTried
							print("p " + str(Id) + " send " + str(msg) + " to " + str(other))
							msg_queues[Id][other].put(msg)



				elif "Success" == msg_type:
					print ("p " + str(Id) + " recieve " + str(item) + " from " + str(other))
					if None == outcome:
						outcome = item['outcome']
						print("p " + str(Id) + ":The outcome is " + str(outcome))
					if outcome not in passed_decs:
						passed_decs.append(outcome)
						decs.remove(outcome)
						
					if not len(decs):
						return

		time.sleep(1)

def main():
	threads = []
	priest_ids = []
	priest_num = 5
	msg_queues = {}
	decs = {0 : "No.0 dec"}
	#TODO owner

	for i in range(priest_num):
		for j in range(i, priest_num):
			# msg_queues[i][j] means i is writer and j is reader
			msg_queues.setdefault(i, {})[j] = Queue(32)
			if i != j:
				msg_queues.setdefault(j, {})[i] = Queue(32)


	for i in range(priest_num):
		priest_ids.append(i)
		dec_ids = list(decs.keys())
		t = Thread(target = start_priest, args = (i, msg_queues, priest_ids, copy.copy(dec_ids)))
		threads.append(t)
	
	for i in range(priest_num):
		threads[i].start()
	
	for i in range(priest_num):
		threads[i].join()

if __name__ == "__main__":
    main()
