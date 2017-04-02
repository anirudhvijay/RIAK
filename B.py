#!/usr/bin/python

import _thread
import time
import riak

# Define a function for the thread
def write(myBucket):
	cnt = 0
	while 1:
		msg=input("Enter message")
		tosendMsg = {
		'cnt':cnt,
	  	'from': "B",
	  	'body': msg,
	  	'to': "A"
		}
		newVal = myBucket.new(str(tosendMsg['cnt'])+"B", data=tosendMsg)
		newVal.store()
		cnt+=1

def read(myBucket):
	cnt = 0
	while 1:
		fetchedVal = myBucket.get(str(cnt)+"A")
		if fetchedVal.data and str(fetchedVal.data['to'])=="B":
			print ("%s: %s" %(fetchedVal.data['from'],fetchedVal.data['body']))
		cnt+=1


myClient = riak.RiakClient(pb_port=8087, protocol='pbc')
myBucket = myClient.bucket('test')
# Create two threads as follows
try:
   _thread.start_new_thread( write, (myBucket,) )
   _thread.start_new_thread( read, (myBucket,) )
except:
   print ("Error: unable to start thread")

while 1:
   pass