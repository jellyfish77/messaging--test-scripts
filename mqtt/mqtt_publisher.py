#########################################################
#
# Run with: python3 test-publisher.py m n
#    where:#         
#         l qos (0, 1, or 2)
#         m is delay between messages (s)
#         n is number of messages
#         o is client_id
#         p host
#         q port
#         topic
#
# Examples:
#   python3 test-publisher.py --broker 172.17.0.4 --port 1883 --client pub-01 --qos 1 --nummsgs 10000 --topic test/topic2
#   python3 test-publisher.py --broker 172.17.0.5 --port 1883 --clientid pub-01 --qos 1 --nummsgs 1 --topic test --message "{\"field\":\"blah\"}"
#
# Help:
#   python3 test-publisher.py -h
#    
#########################################################

import sys
import paho.mqtt.client as mqtt  #import the subscribing_client
import time
import logging,sys
import argparse

#broker="iot.eclipse.org"
#broker="broker.hivemq.com"
keepalive=1200

# parse args
parser=argparse.ArgumentParser()
parser.add_argument('--broker', help='MQTT Broker URL or IP')
parser.add_argument('--port', help='MQTT Broker Port')
parser.add_argument('--clientid', help='')
parser.add_argument('--qos', help='')
parser.add_argument('--nummsgs', help='')
parser.add_argument('--cleansession', help='')
parser.add_argument('--topic', help='')
parser.add_argument('--message', help='Custom message to send to topic')
args=parser.parse_args()

logging.basicConfig(level=logging.DEBUG)
#use DEBUG,INFO,WARNING

def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)+"subscribing_client_id  "+str(client)
    print(m)

def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "+str(rc)+"subscribing_client_id  "+str(client)
    print(m)
   
def on_publish(client, userdata, mid):
    m="Broker ack received, result code: "+str(userdata)+"subscribing_client_id  "+str(mid)
    print(m)
    global pub_ack
    pub_ack=True
    pass

def pub(client,topic,msg,qos,p_msg):
    logging.info(p_msg + " publishing " + msg + " to topic="+topic +" with qos="+str(qos))
    ret=client.publish(topic, msg, qos)
    print('publish result: ' + str(ret))


print(sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4] + " " + sys.argv[5] + " " + sys.argv[6] + " " + sys.argv[7])

publishing_client = mqtt.Client(args.clientid)    #create new instance 

# attache callback functions
publishing_client.on_connect=on_connect               
publishing_client.on_publish=on_publish      
publishing_client.on_disconnect=on_disconnect       

print("Connecting publishing_client")
publishing_client.connect(args.broker, int(args.port), keepalive)      #connect to broker
# run a thread in background to handle the network connection and sending/receiving data
publishing_client.loop_start()  

print("Publishing +"+str(int(args.nummsgs)) +" messages...")

for x in range(1, int(args.nummsgs)+1):
  pub_ack=False  
  
  if not args.message:
    message="Message "+str(x)
  else:
    message=args.message
  
  pub(publishing_client, args.topic, message, int(args.qos), args.clientid)
  while pub_ack != True:
    time.sleep(.1)  

publishing_client.disconnect() # disconnect from broker
publishing_client.loop_stop()  
print("Done")