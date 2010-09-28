#!/opt/local/bin/python
#import pickle
import time
import hashlib

l = []
db = dict(l)
path = "/Users/igable/code/texwatcher/readme"
while True:
	checksum = hashlib.md5(open(path).read()).hexdigest()
	if db.get(path, None) != checksum:
		print checksum
		print "\n"
		print "file changed"
		db[path] = checksum
	time.sleep(2)

#pickle.dump(db.items(), open("db", "w"))
