from threading import Thread
from queue import Queue
from math import floor
import time


# cause some trouble here, either absent or not vote

def start_priest(Id, msg_queues, priest_ids, decs):
	ballots = {}
	passed_decs = []

	lastTried = 0
	prevVotes = {} # like prevVotes[id] = [] or lastest dec

	# need reinit begin
	state = "idle"
	quorum = []
	voters = []
	decree = None
	outcome = None
	# need reinit end


	nextBal = None
	prevBal = None
	prevDec = None
	
	if Id == 0:
		state = "trying"

	while(1):

		for other in priest_ids:
			item = msg_queues[other][Id].get()
			if item:
			    msg_type = item['type']
				if "NextBallot" == msg_type:
					if None == nextBal or item['ballot_num'] >= nextBal:
						nextBal = item['ballot_num']
						#TODO record the owner of nextBal

				elif "LastVote" == msg_type:
					#print ("Recieve LastVote from " + str(other) + " " + str(item))
					if item['NextBal'] == lastTried and "trying" == status:
						if (item['prevBal'] and item['prevDec']):
							# later compare, just compare between the last ones 
							prevVotes.setdefault(other, []).append({"bal": item['prevBal'],
												"dec": item["prevDec"]})
				elif "BeginBallot" == msg_type:
					if item["ballot_num"] == nextBal and (not prevBal or nextBal > prevBal):
						prevBal = nextBal
						prevDec = item['decree']

				elif "Voted" == msg_type:
					if item['prevBal'] == lastTried and "polling" == status:
						voters.append(other)

				elif "Success" == msg_type:
					if not outcome:
						outcome = item['outcome']		
					if outcome not in passed_decs:
						passed_decs.append(outcome)
					if set(decs).issubset(set(passed_decs)):
						return

			if status == "trying":
				msg = {}
				msg['type'] = "NextBallot"
				msg['ballot_num'] = lastTried + 1
				msg_queues[Id][other].put(msg)

				if len(prevVotes.keys()) > 0:
					cnt = floor(len(prevVotes.keys()) / 2) + 1
					for present in prevVotes.keys():
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
					if not decree:
						decree = decs[0]
					
					ballots[lastTried] = {"dec" : decree, "qrm": quorum, 'vate':[]}

			if None == prevBal or nextBal > prevBal:
				msg = {}
				msg['type'] = "LastVote"
				msg['nextBal'] = nextBal
				msg['prevBal'] = prevBal
				msg['prevDec'] = prevDec
				msg_queues[Id][other].put(msg)

			if "polling" == status:
				msg = {}
				msg['type'] = "BeginBallot"
				msg["ballot_num"] = lastTried
				msg["decree"] = decree
				if other in quorum:
					msg_queues[Id][other].put(msg)

			if prevBal:
				msg = {}
				msg['type'] = "Voted"
				msg['prevBal'] = prevBal
				msg_queues[Id][other].put(msg)


			if "polling" == status and set(quorum).issubset(set(voters)) and not outcome:
				outcome = decree

			if outcome:
				msg = {}
				msg['type'] = "Success"
				msg['outcome'] = outcome
				msg_queues[Id][other].put(msg)
				state = "idle"
				quorum = []
				voters = []
				decree = None
				outcome = None

		time.sleep(3)

def main():
	threads = []
	priest_ids = []
	priest_num = 5
	msg_queues = {}
	decs = {0 : "No.0 dec", 1 : "No.1 dec", 2 : "No.2 dec", 3 : "No.3 dec"}
	#TODO owner

	for i in range(priest_num):
		for j in range(i, priest_num):
			# msg_queues[i][j] means i is writer and j is reader
			msg_queues.setdefault(i, {})[j] = Queue(32)
			if i != j:
				msg_queues.setdefault(j, {})[i] = Queue(32)


	for i in range(priest_num):
		priest_ids.append(i)
		t = Thread(target = start_priest, args = (i, msg_queues, priest_ids, decs))
		threads.append(t)
	
	for i in range(priest_num):
		threads[i].start()
	
	for i in range(priest_num):
		threads[i].join()

if __name__ == "__main__":
    main()
