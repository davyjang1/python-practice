from atexit import register
from re import compile
from threading import Thread
from time import ctime
from urllib.request import urlopen as uopen

REGEX = compile(b'#([\d,]+) in Books ')
AMZN = 'http://amazon.com/dp/'
ISBNs = {
	'0132269937': 'Core Python Programming',
#	'0132356139': 'Python Web Development with Django',
	'0137143419': 'Python Fundamentals'
}

def getRanking(isbn):
	page = uopen("%s%s" % (AMZN, isbn))
	data = page.read()
	page.close()
	#print data
	return REGEX.findall(data)[0]

def _showRanking(isbn):
	print('- %r ranked %s' % (ISBNs[isbn], getRanking(isbn)))

def _main():
	threads = []
	print('At', ctime(), 'on Amazon...')
	for isbn in ISBNs:
		new_thread = Thread(target = _showRanking, args =  (isbn,))
		threads.append(new_thread)
		#_showRanking(isbn)
	
	for thread in threads:
		thread.start()
	
	for thread in threads:
		thread.join()
		

@register
def _atexit():
	print('all Done at:', ctime())

if __name__ == '__main__':
	_main()
